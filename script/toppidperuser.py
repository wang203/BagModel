import csv
import numpy as np
import sys

numpidperuser = 3
year = sys.argv[1]
fin = open('/l/vision/wang203/bagmodel/data/datafile/pidbingtuidsortppredipprobfeature'+str(year),'r')
fout = open('/l/vision/wang203/bagmodel/data/datafile/toppidlist'+str(year),'w')
fbin = open('/l/vision/wang203/bagmodel/data/datafile/toppidbin'+str(year),'w')
fuser = open('/l/vision/wang203/bagmodel/data/datafile/toppiduser'+str(year),'w')
line = fin.readline().split()
lastuid = 0
lastbinid = 0
pidlist = []
problist = []
while line:
  # print line
  binid = line[1]
  uid = line[3]
  pid = line[0]
  prob = line[5]
  if binid == lastbinid and uid == lastuid:
    linelist.append(str(line))
    problist.append(prob)
  else:
    if len(problist)>=3:
      toppididx = sorted(range(len(problist)), key=lambda i : problist[i])[-3:]
      fout.write(linelist[toppididx[2]]+"\n"+linelist[toppididx[1]]+"\n"+linelist[toppididx[0]]+"\n")
      fuser.write(userstr+str(1)+"\n"+str(1)+"\n")
      fbin.write(binstr+str(1)+"\n"+str(1)+"\n")
    elif problist:
      toppididx = sorted(range(len(problist)), key=lambda i : problist[i])
      for i in range(len(toppididx)-1,-1,-1):
        fout.write(linelist[toppididx[i]]+'\n')
      fuser.write(userstr)
      fbin.write(binstr)
      for i in range(len(toppididx)-2,-1,-1):
        fbin.write(str(1)+'\n')
        fuser.write(str(1)+'\n')

    if binid == lastbinid:
      userstr = str(0)+"\n"
      binstr = str(1)+"\n"
    else:
      userstr = str(0)+"\n"
      binstr = str(0)+"\n"

    linelist = [str(line)]
    problist = [prob]
    if binid == lastbinid:
      lastuid = uid
    else:
      lastuid = uid
      lastbinid = binid
  line = fin.readline().split()
fout.close()

