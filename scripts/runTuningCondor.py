import os 
import sys
import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('IdNum',help='IdNumber for the job', type=str)
args=parser.parse_args()



sys.path.append('/afs/cern.ch/user/m/mdessena/.local/bin')

#os.system('./runTuningProcess2.sh -d output2par_finale -o training_set_finale --output output_condor_tuning_finale{} --runcardOut MyRuncardCondor_finale_{}.yml --runcard MyRuncard_{}_cond.yml --validation validation_set_finale --hyperpar'.format(args.IdNum,args.IdNum,args.IdNum))
os.system('./runTuningProcess2.sh -d outputTOTALE2 -o training_set2 --output tuning_condor_output{} --runcardOut MyRuncard_{}_out.yml --runcard MyRuncard_{}.yml'.format(args.IdNum, args.IdNum, args.IdNum))