#!/usr/bin/env python3

import yoda, pickle
import numpy as np
import argparse
import glob
import os
import shutil
import numpy as np


patterns=['CMS_2019_I1753680/d27-x01-y03', ' CMS_2019_I1753680/d28-x01-y03']   # EDIT if other path to search
unpatterns=['RAW']            # EDIT if other path to search

pars = argparse.ArgumentParser()
pars.add_argument("output", help="output folder to check")
args=pars.parse_args()
print(args)

outDir = args.output
outDirContent = glob.glob(os.path.join(outDir,'[0-9]*'))
files=[]
for sub in outDirContent:
    files.append(os.path.join(sub,'result.yoda'))

yoda_histograms = []
yoda_path = []
for filename in files:
    for pattern in patterns:
        r = yoda.read(filename, patterns=pattern, unpatterns=unpatterns)
        #r = yoda.read(filename)
        
        if len(r) == 0:
            print('Empty histograms in %s pattern %s' % (filename, pattern) )
        yoda_histograms.append(r)
        yoda_path.append(filename)


print('\n\n-----------------second part---------------------\n\n')

plotinfo = []
#print('yoda_histogram = ')
#print(yoda_histograms)
#print('\n\n\n')
#print('yoda_histo_enum = ')
#print(enumerate(yoda_histograms))
#print('\n\n\n')
#print('path = ')
#print(yoda_path)


for i, file in enumerate(yoda_histograms):
#    print(i)
#    print(file)
    index = 0
    for key in sorted(file):
#        print(key)
        h = file.get(key)
        h = h.mkScatter()
        data_x = np.zeros(len(h.points()))
        data_xerrm = np.zeros(len(h.points()))
        data_xerrp = np.zeros(len(h.points()))
        data_y = np.zeros(len(h.points()))
        data_yerr = np.zeros(len(h.points()))
        data_weight = np.zeros(len(h.points()))
        for t, p in enumerate(h.points()):
            
            if p.y() == 0:
                print('Histogram %s has empty entries %s' % (key, yoda_path[i]))
                head, tail=os.path.split(yoda_path[i])
                try:
                    shutil.rmtree(head)
                except:
                    pass
            plotinfo.append({'title': key.replace('/REF',''),
                                  'x': data_x,
                                  'y': data_y,
                                  'yerr': data_yerr,
                                  'xerr-': data_xerrm,
                                  'xerr+': data_xerrp,
                                  'weight': data_weight})


cmd = './checkMySimulation.py {}'.format(outDir) 
os.system(cmd)