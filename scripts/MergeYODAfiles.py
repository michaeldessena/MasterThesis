import argparse
import os
import glob
import shutil

DEFAULT_FILENAME='result.yoda'
### ARGPARSER DEFINITION ###
parser = argparse.ArgumentParser(description='Run all the MCNNTUNES tuning program')
parser.add_argument("folders", metavar='DATA FOLDERs', nargs='+', help="input data folders")
parser.add_argument('-f','--file', type=str, help="filename for the yoda file", default=DEFAULT_FILENAME)
parser.add_argument('-o','--output', type=str, help="output folder name")
args = parser.parse_args()

directories=args.folders
filename=args.file
outputFolder=args.output

### check folder have same number of run
allFolders=[]
numbersOfFiles=[]
for dir in directories:
    dirList = glob.glob(os.path.join(dir, '[0-9]*'))
    counter=0
    for item in dirList:
        counter+=1
    numbersOfFiles.append(counter)
    allFolders.append(dirList)

print(allFolders)
print(numbersOfFiles)

nruns=max(numbersOfFiles)

os.mkdir(outputFolder)

j=0
for i in range(nruns):
    save=True
    for dirs in allFolders:
        if os.path.exists(os.path.join(dirs[i], filename))==False:
            save=False

    if save==True:    
        os.mkdir(os.path.join(outputFolder,str(j).zfill(4)))
        
        files=glob.glob(os.path.join(dirs[i], '*.dat'))
        for file in files:
            shutil.copy(file, os.path.join(outputFolder, str(j).zfill(4)))
            print(f'copy {file} to {os.path.join(outputFolder, str(j).zfill(4))}')
        try:
            files=glob.glob(os.path.join(dirs[i], '*.py'))
            for file in files:
                shutil.copy(file, os.path.join(outputFolder, str(j).zfill(4)))
                print(f'copy {file} to {os.path.join(outputFolder, str(j).zfill(4))}')
        except:
            print('NOT copy *.py')
            pass
        cmd='yodamerge '
        for dirs in allFolders:
            cmd += str(os.path.join(dirs[i], filename))
            cmd += ' '
        cmd += '-o {}'.format(os.path.join(outputFolder, str(j).zfill(4), filename))
        print(cmd)
        os.system(cmd)
        j+=1
        
