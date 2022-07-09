#!/usr/bin/python3

import os
import sys
import shutil
import glob
import argparse
import timeit

RESULT_YODAFILE='result.yoda'

def orderedList(output):
    dirContentList_rude=glob.glob(os.path.join(output, '[0-9]*'))
    dirContentList=[]
    for item in dirContentList_rude:
        tmp=item.split(os.path.sep)[-1]
        dirContentList.append(tmp)
    dirContentList.sort()
    return dirContentList

def main(args):
    output=args.output
    dirContentList=orderedList(output)
    
    for item in dirContentList:
        sub=os.path.join(output, item)
        yodaresult=os.path.join(output, item, RESULT_YODAFILE)
        if os.path.exists(yodaresult):
            print('{} exist'.format(yodaresult))
        else:
            shutil.rmtree(sub)
            print('{} doesn t exist --- /// --- {} REMOVED!!!'.format(yodaresult, sub))

    dirContentList=orderedList(output)
    print(dirContentList)
    last=1
    for j in range(len(dirContentList)):
        j_str=str(j).zfill(4)
        if os.path.exists(os.path.join(output, j_str)):
            print('{} exist!!!'.format(j_str))
        else:
            last_dir=dirContentList.pop()
            shutil.move(os.path.join(output, str(last_dir)), os.path.join(output, j_str))
            print('Moved: {} -------> {}'.format(str(last_dir), j_str) )
    print(len(dirContentList))
        


#if __name__=='__main__':
    
parser = argparse.ArgumentParser(description='check the result.yoda file presence in MCNNTUNES output folders')
parser.add_argument("output", metavar='OUTPUT', help="Data folder to check")
args = parser.parse_args()

main(args)

