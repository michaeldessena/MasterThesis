#!/usr/bin/python3

import argparse
import os

DEFAULT_FILENAME='result.yoda'
### ARGPARSER DEFINITION ###
parser = argparse.ArgumentParser(description='Make rivet-mkhtml for each folder')
parser.add_argument("folders", metavar='DATA FOLDERs', nargs='+', help="input data folders")
parser.add_argument('-f','--file', type=str, help="filename for the yoda file", default=DEFAULT_FILENAME)
parser.add_argument('-o','--output', type=str, help="output folder name", default='rivet-plots')
args = parser.parse_args()

directories=args.folders
filename=args.file
output=args.output

listYES=[]
listNO=[]

for dir in directories:
    

    pathToYoda = os.path.join(dir, '0000', filename)
    pathToOutput = os.path.join(dir, output)  
    
    check=os.path.exists(pathToYoda)
    if check==True:
        listYES.append(dir)
        
        cmd = f'rivet-mkhtml {pathToYoda} -o {pathToOutput}'
        print(cmd)
        os.system(cmd)

    elif check==False:
        listNO.append(dir)
        print(f'''"{dir}" doesn't contains {pathToYoda}''')

info = '****** Folders YES *******\n'
for item in listYES:
    info += item
    info += '\n'

info += '****** Folders NO *******'
for item in listNO:
    info += item
    info += '\n'

print(info)