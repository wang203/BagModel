# http://www.it610.com/article/5104858.htm

import numpy as np
import matplotlib.pyplot as plt
import scipy
import sys
import caffe
import os
import leveldb
import gc

caffe_root = '/l/vision/wang203/caffe/'
year = sys.argv[1]
category = sys.argv[2]
imagedir = '/l/vision/wang203/bagmodel/data/images/test/'+year+'/'+category+'/'
# imagedir = '/l/vision/wang203/bagmodel/data/images/trycode/'
resultdir = '/l/vision/wang203/bagmodel/results/'





caffe.set_mode_gpu()
caffe.set_device(int(sys.argv[3]))
# net = caffe.Net('/l/vision/wang203/bagmodel/model/deploy.prototxt', '/l/vision/wang203/bagmodel/model/snow-auto_iter_100000.caffemodel', caffe.TEST)

net = caffe.Net('/l/vision/wang203/bagmodel/model/placesCNN_upgraded/place205deploy.prototxt', '/l/vision/wang203/bagmodel/model/placesCNN_upgraded/placemodelfile/placeft_iter_100000.caffemodel', caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
# transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_mean('data', np.load('/l/vision/wang203/bagmodel/model/placesCNN_upgraded/places205CNN_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
 
# set net to batch size of 50
batch = 100
net.blobs['data'].reshape(batch,3,227,227)

files = os.listdir(imagedir)
classnumMax = 0
fileNameNum = np.arange(0,batch,1).reshape(batch,-1) # (batch,1) array for filenames in a batch

os.system('rm '+resultdir+'filename'+year+category)
fname = open(resultdir+'filename'+year+category, 'a')
os.system('rm '+resultdir+'predi'+year+category)
fpredi = file(resultdir+'predi'+year+category,'a')
os.system('rm '+resultdir+'feature'+year+category)
ffeature = file(resultdir+'feature'+year+category,'a')
os.system('rm '+resultdir+'prob'+year+category)
fprob = file(resultdir+'prob'+year+category,'a')
i = 1
j = 0
for f in files:
  # print f
  if(os.path.isfile(imagedir+f)):
    # print i
    if(i == batch):
      i = 0
      j = j+1
      
      out = net.forward()
      fc7Data = net.blobs['fc7'].data
      probData = (net.blobs['prob'].data)
      predict = np.argmax(probData,axis=1).reshape(batch,-1)

      # for k in range(0,batch):
      #   classnum = predict[k][0]
      #   feature = fc7Data[k].reshape(1,-1)
        # tempData = feature.tobytes()
        # print feature.shape
        # print fc7Data.shape
      np.savetxt(ffeature,fc7Data)
      np.savetxt(fpredi,predict)
      np.savetxt(fprob,np.array([probData[k][predict[k][0]] for k in xrange(batch)]).T)
    # fileNameNum[i] = float(f[0:12])
    fname.write(f+'\n')
    net.blobs['data'].data[i,:,:,:] = transformer.preprocess('data', caffe.io.load_image(imagedir + f))
    i = i+1

print i
out = net.forward()
fc7Data = net.blobs['fc7'].data
probData = (net.blobs['prob'].data)
predict = np.argmax(probData,axis=1).reshape(batch,-1)

print predict
# for k in range(0,i):
#   classnum = predict[k][0]
#   feature = fc7Data[k].reshape(1,-1)
  # tempData = feature.tobytes()
  # print feature.shape
  # print fc7Data.shape
np.savetxt(ffeature,fc7Data)
np.savetxt(fpredi,predict)
np.savetxt(fprob, np.array([probData[k][predict[k][0]] for k in xrange(batch)]).T)

fname.close()
ffeature.close()
fpredi.close()
fprob.close()
