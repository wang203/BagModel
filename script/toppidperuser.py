import numpy as np
import sys

numpidperuser = 3
year = sys.argv[1]
fin = open('/l/vision/wang203/bagmodel/data/datafile/pidbingtuidsortppredipprobfeature'+str(year),'r')
fout = open('/l/vision/wang203/bagmodel/data/datafile/toppidlist'+str(year),'w')
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
    line[4] = 1 # cont sequence indicator
    linelist.append(str(line))
    problist.append(prob)
  else:
    line[4] = 0 # cont sequence indicator
    if len(problist)>=3:
      toppididx = sorted(range(len(problist)), key=lambda i : problist[i])[-3:]
      fout.write(linelist[toppididx[2]]+"\n"+linelist[toppididx[1]]+"\n"+linelist[toppididx[0]]+"\n")
    elif problist:
      toppididx = sorted(range(len(problist)), key=lambda i : problist[i])
      for i in range(len(toppididx)-1,-1,-1):
        fout.write(linelist[toppididx[i]]+'\n')
    linelist = [str(line)]
    problist = [prob]
    lastuid = uid
    lastbinid = binid
  line = fin.readline().split()
fout.close()

