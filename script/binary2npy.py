import numpy as np
import sys
import caffe

blob = caffe.proto.caffe_pb2.BlobProto()
data = open( '/l/vision/wang203/bagmodel/model/placesCNN_upgraded/places205CNN_mean.binaryproto' , 'rb' ).read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
out = arr[0]
print arr.shape
# np.save('/l/vision/wang203/bagmodel/model/placesCNN_upgraded/places205CNN_mean.npy' , out )
