import numpy as np


for year in range(2007,2016):
  fout = open('/l/vision/wang203/bagmodel/data/metadata/binimg'+str(year), 'w')
  with open('/l/vision/wang203/bagmodel/data/metadata/data'+str(year),'r') as f:
    filedata = f.readlines()
    for lineidx in range(len(filedata)):
      data = filedata[lineidx].split()
      binid = data[0]
      bingt = data[1]
      i = 3
      while True:
        pid = data[i] 
        uid = data[i+1]
        i += 4
        fout.write(binid+" "+bingt+" "+uid+" "+pid+"\n")
        if i == len(data): break           
