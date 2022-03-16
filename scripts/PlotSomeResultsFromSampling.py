#!/usr/bin/env python3

import os
import random
import glob
import argparse

FILENAME='result.yoda'
PARAMS='params.dat'

parser = argparse.ArgumentParser(description='evaluate chi^2 from .yoda files')
parser.add_argument("folder", metavar='FOLDER', help="Folder with 0000/, 0001/, 0002/ subfolder ")
parser.add_argument("-o","--output", type=str, help="output filename (default: rivet-plots)")
parser.add_argument("-n", "--nruns", type=int, required=True)
args = parser.parse_args()

folder=args.folder
output_rivet_mkhtl=args.output
nruns=args.nruns

list_of_dirs = glob.glob(os.path.join(folder,'*[0-9]'))
print(len(list_of_dirs))

max=len(list_of_dirs)-1
results_command=''
extract=[-1]
parameters_used=''
for run in range(nruns):
    number=-1
    n_extraction=0
    while number in extract:
        number=random.randint(0,max)
        n_extraction+=1
    extract.append(number)
    print(run, ' :', n_extraction)
    number_str=str(number)
    number_folder=number_str.zfill(4)
    filename=FILENAME
    yodafile_path=os.path.join(folder, number_folder, filename)
    yodafile_path+=' '
    results_command+=yodafile_path
    params_filename=PARAMS
    paramsfile_path=os.path.join(folder, number_folder, params_filename)
    
    parameters_used += f' \n----- FOLDER:{os.path.join(folder, number_folder)} -----\n' 
    with open(paramsfile_path,'r') as file:
        stream=file.readlines()
        for line in stream:
            parameters_used+=line
            parameters_used+='\n'

cmd='rivet-mkhtml '
cmd+=results_command

if output_rivet_mkhtl:
    cmd+='-o {}'.format(output_rivet_mkhtl)

print('\n\nCOMMAND:')
print(cmd)

os.system(cmd)


with open(os.path.join(output_rivet_mkhtl, 'params_used.dat'), 'w') as file:
    file.write(parameters_used)
print(f"added file {os.path.join(output_rivet_mkhtl, 'params_used.dat')}")
