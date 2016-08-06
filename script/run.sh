#!/bin/bash

#cd /N/u/wang203/BigRed2/deep/landmark
caffe train -solver solver.prototxt -gpu 1  2>&1 | tee train.log
#caffe test -model val.prototxt -weights flickrstreet100_train_iter_300.caffemodel -iterations 100 2>&1 | tee log
