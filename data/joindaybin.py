import numpy as np
import sys
from collections import OrderedDict

# def joindaybin(fdata, fgt):
#   data = np.genfromtxt(fdata,dtype='str')
#   gt = np.genfromtxt(fgt,dtype='str')
#   #fout = open('pidgt','w')
#   dict1 = {data[:,1]:data[:,0]}
#   dict2 = {gt[:,0]:gt[:,1]}
#   result = OrderedDict()
#   for d in (dict1,dict2):
#     for key, value in d.iteritems():
#       result.setdefault(key,[]).extend(value)
#   np.savetxt('pidgt',result)
# 
# joindaybin(sys.argv[1], sys.argv[2])

import pandas

csv1 = pandas.read_csv('america2010.daybinpid4join')
csv2 = pandas.read_csv('gtsnowall4join')
merged = csv1.merge(csv2, on='id')
merged.to_csv("output.csv", index=False)

# import csv
# from collections import OrderedDict
# 
# with open('gtsnowall4join','r') as f2:
#     reader = csv.reader(f2)
#     #fields2 = next(reader,None) # Skip headers
#     dict2 = OrderedDict((row[0],row[1:]) for row in reader)
# print 'dict2'
# with open('america2010.daybinpid4join','r') as f1:
#     reader = csv.reader(f1)
#     # fields1 = next(reader,None) # Skip headers
#     dict1 = OrderedDict((row[0], row[1:]) for row in reader)
# print 'dict1'
# result = OrderedDict()
# for d in (dict1, dict2):
#     for key, value in d.iteritems():
#         result.setdefault(key, []).extend(value)
# print 'result'
# with open('pidgt.2010', 'wb') as f:
#     w = csv.writer(f)
#     for key, value in result.iteritems():
#         w.writerow([key] + value)
