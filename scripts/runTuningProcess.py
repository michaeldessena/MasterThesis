#!/usr/bin/python3

import os
import sys
import shutil
import glob
import argparse
import yaml
from datetime import datetime
import timeit

yesChoice = ['yes', 'y']
noChoice = ['no', 'n']

def ReadRuncard(args,runcard):

    training_set=''
    validation_set=''
    with open(runcard, 'r') as stream:
        data = yaml.safe_load(stream)
        #print(data)

        ### training set
        try: 
            training_set = data['input']['folders']
        except:
            print('folders key not found in {}'.format(args.runcard))
            sys.exit()

        if args.training_set is not None:

            data['input']['folders']=args.training_set
            training_set = data['input']['folders']


        ### validation set
        if args.validation == True:
            try:
                validation_set = data['input']['benchmark_folders']
            except:
                print('benchmark_folders key not found in {}'.format(args.runcard))
                sys.exit()

            if args.validation_set is not None:

                data['input']['benchmark_folders'] = args.validation_set
                validation_set = data['input']['benchmark_folders']

    with open(runcard, 'w') as f:
        yaml.safe_dump(data, f)

    return training_set, validation_set
            
if __name__=='__main__':

    ### DATE AND TIME START ###
    tic=timeit.default_timer()  ### starting time
    date_time = datetime.now() 
    date_time_str = date_time.strftime("%Y%m%d_%H%M%S")
    

    ### ARGPARSER DEFINITION ###
    parser = argparse.ArgumentParser(description='Run all the MCNNTUNES tuning program')
    parser.add_argument("data_folder", metavar='DATA FOLDER', help="input data folder")
    parser.add_argument("-r","--runcard", help=".yml file containing the mcnntunes runcard", required=True)
    parser.add_argument("-t","--training_set", default=None, nargs='+', help="training set folder (or a list), if you want to automatically change in runcard", required=False)
    parser.add_argument("-v", "--validation", default=False, help="if you want to run benchmark mode", dest='validation', action='store_true')
    parser.add_argument("-vs","--validation_set", default=None, nargs='+', help="validation set folder, if you want to automatically change in runcard", required=False)
    parser.add_argument("-hyper", "--hyperpar", default=False, help="launch also the hyperparameters tuning", dest='hyperpar', action='store_true')
    parser.add_argument("-o","--output", help="output folders name (default: {})".format('Simulation_'+date_time_str), default='Simulation_'+date_time_str, required=False)
    parser.set_defaults(validation=False, hyperpar=False)
    args = parser.parse_args()

    ### BODY ###
    Dir = os.getcwd()
    data_folder = args.data_folder
    runcard_file = args.runcard
    training_set = args.training_set
    validation_bool = args.validation
    validation_set = args.validation_set
    hyperpar_bool = args.hyperpar
    outputDir= args.output

    training_set_true=''
    validation_set_true=''
    training_set_true, validation_set_true = ReadRuncard(args, runcard_file)
    

    info='''########################################
            RUNNING OPTIONS
########################################
Info:
    data_folder:\t{data_folder}
    runcard:\t\t{runcard}
    training_set:\t{training_set}
    validation:\t\t{validation_bool}
    validation_set:\t{validation_set}
    hyperparameters:\t{hyperpar_bool}
    output_folder:\t{outputDir}
########################################\n\n'''.format(data_folder=data_folder, runcard=runcard_file, validation_bool=validation_bool, hyperpar_bool=hyperpar_bool, outputDir=outputDir, training_set=training_set_true, validation_set=validation_set_true)

    print(info)

    ### start mcnntunes ###

    ### copy the data_folder content in the output_folder
    check=os.path.exists(outputDir)
    if check==True:
        inp=''
        while inp not in yesChoice and inp not in noChoice:
            inp_str='ATTENTION: {} already exist!!! do you want to delete the existing one? [y/n] '.format(outputDir)
            inp=input(inp_str)
            inp=inp.lower()

        if inp in yesChoice:
            shutil.rmtree(outputDir)
        elif inp in noChoice:
            sys.exit()
        else:
            print('Killed')
            sys.exit()

    print('Coping {data_folder} content'.format(data_folder=data_folder))
    shutil.copytree(data_folder, outputDir)
    print('The content of {data_folder} has been copied in {outputDir}'.format(data_folder=data_folder, outputDir=outputDir))

    ### run preprocess
    print('\n\nRun ---------> PREPROCESS')
    cmd='mcnntunes -o {outputDir} preprocess {runcard_file}'.format(outputDir=outputDir, runcard_file=runcard_file)
    os.system(cmd)

    new_runcard = os.path.join(outputDir, 'runcard.yml')  ### because a copy of the runcard is stored by mcnntunes!

    ###run model
    print('\n\nRun ---------> MODEL')
    cmd='mcnntunes -o {outputDir} model {runcard_file}'.format(outputDir=outputDir, runcard_file= new_runcard)
    os.system(cmd)

    ###run benchmark
    if validation_bool==True:
        print('\n\nRun ---------> BENCHMARK')
        cmd='mcnntunes -o {outputDir} benchmark {runcard_file}'.format(outputDir=outputDir, runcard_file= new_runcard)
        os.system(cmd)

    ###run optimize
    if hyperpar_bool==True:
        print('\n\nRun ---------> OPTIMIZE')
        cmd='mcnntunes -o {outputDir} optimize {runcard_file}'.format(outputDir=outputDir, runcard_file= new_runcard)
        os.system(cmd)
    
    ###run tune
    print('\n\nRun ---------> TUNE')
    cmd='mcnntunes -o {outputDir} tune {runcard_file}'.format(outputDir=outputDir, runcard_file= new_runcard)
    os.system(cmd)

    ### Remove data folders from output folder
    dataSubdirList = glob.glob(os.path.join(outputDir, '[0-9]*'))
    
    print('\n\nRemoving data folders from {}'.format(outputDir))
    for subdir in dataSubdirList:
        shutil.rmtree(subdir)

    print('Data folders removed from {}'.format(outputDir))

    toc=timeit.default_timer() ### final time
    total_time = toc-tic  ### elapsed time in second

    print(f'''########################################
            TUNE ENDED
########################################
        Total time = {total_time} sec''')
