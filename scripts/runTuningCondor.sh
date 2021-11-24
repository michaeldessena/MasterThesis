#!/usr/bin/bash

#SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd /afs/cern.ch/user/m/mdessena/Results/CMSSW_11_2_4/src
eval `scram runtime -sh`
export PATH=${PATH}:/afs/cern.ch/user/m/mdessena/.local/bin
#source runTuningProcess2.sh -d output2par_val -o training_set3 --runcard MyRuncard_${1}_cond.yml --validation --hyperpar

python3 runTuningCondor.py "${@}"