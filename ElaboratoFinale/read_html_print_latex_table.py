#!/usr/bin/env python3


import re
import os
import argparse

expr='<td>Tune_Parameter_'

parser = argparse.ArgumentParser(description='Print table for latex')
parser.add_argument("data_file", metavar='DATA FILE', type=str,help="input data file")
args = parser.parse_args()

data_file = args.data_file

file=open(data_file, 'r')

lines=file.readlines()
#print(lines)r"(?<=AAA).*?(?=ZZZ)"

table='\\begin{tabular}{l | c}\n'
table+='\tParameter & Value \\\\ \\hline\\hline\n'
    
for i,line in enumerate(lines):
    if expr in line:
        #p = re.compile(r'Tune_Parameter_*:(</td>*)')
        variable=re.search('<td>Tune_Parameter_(.+?)</td>', line)
        if variable:
            variable=variable.group(1)
        value=lines[i+1]
        out_value=re.findall('\d+\.\d+', value)
        
        print(variable ,out_value)
        table+=f'\t{variable} & {out_value[0]}\\\\ \n'

file.close()

table += '\\end{tabular}'
print('\n\n')
print(table)