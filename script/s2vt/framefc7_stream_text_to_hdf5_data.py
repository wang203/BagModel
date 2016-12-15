#!/usr/bin/env python
# fc7 for every frame in text to hdf

import csv
import numpy as np
import os
import random
random.seed(3)
import sys

from hdf5_npstreamsequence_generator import SequenceGenerator, HDF5SequenceWriter

# UNK_IDENTIFIER is the word used to identify unknown words
UNK_IDENTIFIER = '<en_unk>'

# start every sentence in a new array, pad if <max
MAX_WORDS = 80
FEAT_DIM= 4096

"""Filenames has file with vgg fc7 frame feats for vidids
   and sentences with video ids"""
class fc7FrameSequenceGenerator(SequenceGenerator):
  def __init__(self, filenames, batch_num_streams=32,
               max_words=MAX_WORDS, align=True, pad=True,
               truncate=True):
    self.max_words = max_words
    self.array_type_inputs = {} # stream inputs that are arrays
    self.array_type_inputs['frame_fc7'] = FEAT_DIM # stream inputs that are arrays
    self.lines = []
    num_empty_lines = 0
    self.vid_framefeats = {} # listofdict [{}]
    for framefeatfile, sentfile in filenames:
      print 'Reading frame features from file: %s' % framefeatfile
      with open(framefeatfile, 'rb') as featfd:
        # each line has the fc7 for 1 frame in video
        pool_csv = csv.reader(featfd)
        pool_csv = list(pool_csv)
        for line in pool_csv:
          #id_framenum = line[0]
          video_id = line[1].strip('\'').strip('[^ \']')
          
          if video_id not in self.vid_framefeats:
            self.vid_framefeats[video_id]=[]
          self.vid_framefeats[video_id].append(','.join(line[6:]))
          #print video_id+".."+str(len(self.vid_framefeats[video_id][0]))+'..'+str(len(self.vid_framefeats[video_id]))
      # reset max_words based on maximum frames in the video
      print 'Reading sentences in: %s' % sentfile
      with open(sentfile, 'r') as sentfd:
        for line in sentfd:
          #line = line.strip(',')
          id_sent = line.split(',')
          # if len(id_sent)<2:
          #   num_empty_lines += 1
          #   continue
          self.lines.append((id_sent[0], id_sent[1]))
      if num_empty_lines > 0:
        print 'Warning: ignoring %d empty lines.' % num_empty_lines
    self.line_index = 0
    self.num_resets = 0
    self.num_truncates = 0
    self.num_pads = 0
    self.num_outs = 0
    self.frame_list = []

    SequenceGenerator.__init__(self)
    self.batch_num_streams = batch_num_streams  # needed in hdf5 to seq
    # make the number of image/sentence pairs a multiple of the buffer size
    # so each timestep of each batch is useful and we can align the images
    if align:
      num_pairs = len(self.lines)
      remainder = num_pairs % BUFFER_SIZE
      if remainder > 0:
        num_needed = BUFFER_SIZE - remainder
        for i in range(num_needed):
          choice = random.randint(0, num_pairs - 1)
          self.lines.append(self.lines[choice])
      assert len(self.lines) % BUFFER_SIZE == 0

    self.pad = pad
    self.truncate = truncate
    self.negative_one_padded_streams = frozenset(('target_sentence'))

  def streams_exhausted(self):
    return self.num_resets > 0

  def dump_video_file(self, vidid_order_file, frame_seq_label_file):
    print 'Dumping vidid order to file: %s' % vidid_order_file
    with open(vidid_order_file,'wb') as vidid_file:
      for vidid, line in self.lines:
        word_count = len(line.split())
        frame_count = len(self.vid_framefeats[vidid])
        total_count = word_count +frame_count
        vidid_file.write('%s\t%d\t%d\t%d\n' % (vidid, word_count, frame_count, total_count))
    print 'Done.' 

  def next_line(self):
    num_lines = float(len(self.lines))
    if self.line_index == 1 or self.line_index == num_lines or self.line_index % 10000 == 0:
      print 'Processed %d/%d (%f%%) lines' % (self.line_index, num_lines,
                                              100 * self.line_index / num_lines)
    self.line_index += 1
    if self.line_index == num_lines:
      self.line_index = 0
      self.num_resets += 1

  def get_pad_value(self, stream_name):
    return -1 if stream_name in self.negative_one_padded_streams else 0

  def float_line_to_stream(self, line):
    return map(float, line.split(','))

#   def line_to_stream(self, sentence):
#     stream = []
#     for word in sentence.split():
#       word = word.strip()
#       if word in self.vocabulary:
#         stream.append(self.vocabulary[word])
#       else:  # unknown word; append UNK
#         stream.append(self.vocabulary[UNK_IDENTIFIER])
#     # increment the stream -- 0 will be the EOS character
#     stream = [s + 1 for s in stream]
#     return stream

  # we have pooled fc7 features already in the file
  def get_streams(self):
    vidid, line = self.lines[self.line_index]
    print vidid+" "+line
    assert vidid in self.vid_framefeats
    feats_vgg_fc7 = self.vid_framefeats[vidid] # list of fc7 feats for all frames
    num_frames = len(feats_vgg_fc7)
    stream = line #self.line_to_stream(line)
    num_words = len(stream)
    pad = self.max_words - (num_words + 1 + num_frames) if self.pad else 0
    truncated = False
    if pad < 0:
      # print '{0} #frames: {1} #words: {2}'.format(vidid, num_frames, num_words)
      # truncate frames
      if (num_words + 1) > self.max_words:
        stream = stream[:20] # truncate words to 20
      num_frames = self.max_words - (len(stream)+1)
      truncated = True
      pad = 0
      # print 'Truncated_{0}: #frames: {1} #words: {2}'.format(vidid, num_frames, len(stream))
      self.num_truncates += truncated

    if pad > 0: self.num_pads += 1
    self.num_outs += 1
    out = {}
    stream = list(stream[0])
    assert len(stream)==1
    out['cont_sentence'] = [0] + [1] * (num_frames +len(stream)) + [0] * pad
    out['input_sentence'] = [0] * num_frames + [0] + stream + [0] * pad
    out['target_sentence'] = [-1] * num_frames + stream + [0] + [-1] * pad
    # For encoder-decoder model
    out['cont_img'] = [0] + [1] * (num_frames - 1) + [0] * (len(stream) + 1 + pad)
    out['cont_sen'] = [0] * (num_frames + 1) + [1] * len(stream) + [0] * pad
    out['encoder_to_decoder'] = [0] * (num_frames - 1) + [1] + [0] * (len(stream) + 1 + pad)
    out['stage_indicator'] = [0] * num_frames + [1] * (len(stream) + 1 + pad)
    out['inv_stage_indicator'] = [1] * num_frames + [0] * (len(stream) + 1 + pad)
    # fc7 features
    out['frame_fc7'] = []
    for frame_feat in feats_vgg_fc7[:num_frames]:
      feat_fc7 = self.float_line_to_stream(frame_feat)
      out['frame_fc7'].append(np.array(feat_fc7).reshape(1, len(feat_fc7)))
    # pad last frame for the length of the sentence
    num_img_pads = len(out['input_sentence']) - num_frames
    zero_padding = np.zeros(len(feat_fc7)).reshape(1, len(feat_fc7))
    for padframe in range(num_img_pads):
      out['frame_fc7'].append(zero_padding)
    print 'len fc7 = '+str(len(out['frame_fc7']))+' len sentence = '+str(len(out['input_sentence']))
    assert len(out['frame_fc7'])==len(out['input_sentence'])
    print '------------------------> next line'
    self.next_line()
    return out


# BUFFER_SIZE = 1 # TEXT streams
BUFFER_SIZE = 32 # TEXT streams
BATCH_STREAM_LENGTH = 1000
SETTING = '../../data/datafile'
OUTPUT_DIR = '{0}/hdf5/buffer_{1}_s2vt_{2}'.format(SETTING, BUFFER_SIZE, MAX_WORDS)
OUTPUT_DIR_PATTERN = '%s/%%s_batches' % OUTPUT_DIR
FRAMEFEAT_FILE_PATTERN = '../../data/datafile/toppidlist2007-csv'
SENTS_FILE_PATTERN = '../../data/datafile/toppidbingt2007'
OUT_CORPUS_PATH = '../../data/datafile/stats/{0}'

def preprocess_dataset(split_name, data_split_name, batch_stream_length,
                      aligned=False):
 #  filenames = [(FRAMEFEAT_FILE_PATTERN.format(data_split_name),
 #               SENTS_FILE_PATTERN.format(data_split_name))]
  filenames = [(FRAMEFEAT_FILE_PATTERN,
               SENTS_FILE_PATTERN)]
  output_path = OUTPUT_DIR_PATTERN % split_name
  aligned = True
  fsg = fc7FrameSequenceGenerator(filenames, BUFFER_SIZE,
         max_words=MAX_WORDS, align=aligned, pad=aligned,
         truncate=aligned)
  fsg.batch_stream_length = batch_stream_length
  writer = HDF5SequenceWriter(fsg, output_dir=output_path)
  writer.write_to_exhaustion()
  writer.write_filelists()
  out_path = OUT_CORPUS_PATH.format(data_split_name)
  vid_id_order_outpath = '%s/yt_s2vtvgg_%s_vidid_order_%d_%d.txt' % \
  (out_path, data_split_name, BUFFER_SIZE, MAX_WORDS)
  frame_sequence_outpath = '%s/yt_s2vtvgg_%s_sequence_%d_%d_recurrent.txt' % \
  (out_path, data_split_name, BUFFER_SIZE, MAX_WORDS)
  fsg.dump_video_file(vid_id_order_outpath, frame_sequence_outpath)

def process_splits():
  DATASETS = [ # split_name, data_split_name, aligned
      ('train', 'train', False),
#      ('valid', 'val', False)
  ]
  for split_name, data_split_name, aligned in DATASETS:
    preprocess_dataset(split_name, data_split_name, BATCH_STREAM_LENGTH,aligned)

if __name__ == "__main__":
  process_splits()
