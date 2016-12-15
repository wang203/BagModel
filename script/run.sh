#!/bin/bash

#cd /N/u/wang203/BigRed2/deep/landmark
# caffe train -solver solver.prototxt -gpu 1  2>&1 | tee train.log



caffe train -solver /l/vision/wang203/bagmodel/script/s2vt/s2vt_solver.prototxt -gpu 1











# caffe test -model /l/vision/wang203/bagmodel/model/placesCNN_upgraded/place205train_val.prototxt -weights /l/vision/wang203/bagmodel/model/placesCNN_upgraded/placemodelfile/placeft_iter_100000.caffemodel -iterations 100 -gpu 1 2>&1 | tee log

#placedir='/l/vision/wang203/bagmodel/model/placesCNN_upgraded'
#echo $placedir
# caffe train -solver /l/vision/wang203/bagmodel/model/placesCNN_upgraded/place205solver.prototxt -weights /l/vision/wang203/bagmodel/model/placesCNN_upgraded/places205CNN_iter_300000_upgraded.caffemodel -gpu 1
