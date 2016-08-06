#!/bin/bash
#PBS -l walltime=12:00:00
#PBS -q gpu
#PBS -j oe
#PBS -N landmark_10_test

cd /N/u/wang203/BigRed2/deep/landmark/
aprun caffe test -model test.prototxt -weights finetune_train_iter_25000 -iterations 29727 -gpu 0
