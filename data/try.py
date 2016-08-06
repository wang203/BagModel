# import pandas
# 
# csv1 = pandas.read_csv('filea1.csv')
# csv2 = pandas.read_csv('file2.csv')
# merged = csv1.merge(csv2, on='id')
# merged.to_csv("output.csv", index=False)

import csv
from collections import OrderedDict

with open('file2.csv','r') as f2:
    reader = csv.reader(f2)
    #fields2 = next(reader,None) # Skip headers
    dict2 = OrderedDict((row[0],row[1:]) for row in reader)

with open('file1.csv','r') as f1:
    reader = csv.reader(f1)
    # fields1 = next(reader,None) # Skip headers
    dict1 = OrderedDict((row[0], row[1:]) for row in reader)

result = OrderedDict()
for d in (dict1, dict2):
    for key, value in d.iteritems():
        result.setdefault(key, []).extend(value)

with open('merged.csv', 'wb') as f:
    w = csv.writer(f)
    for key, value in result.iteritems():
        # print type([key]) #list
        w.writerow([key] + value)
