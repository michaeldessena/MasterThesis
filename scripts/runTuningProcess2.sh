#!/bin/bash

#########################################################################################################
#       Automatic process for run tuning using MCNNTUNES                                                #
#                                                                                                       #
#       ./runTuningProcess.sh -d output -n NUMRUNS -o training_set --runcard MyRuncard                  #
#       -d : 	 output folder with the result of simulation (default output)                           #
#       -o : 	 folder with training set (default training_set_[DATE]_[TIME])                          #
#       -n :  	 runs number [if not is calculated by the number of runs in the output directory]       #
#       --runcard: yml file whit the configuration for mcnntunes (dafult: MyCP5+runcardtemplate.yml)    #
#       --validation run the validation test (default false)    [validation_set]                        #
#       --hyperpar run the hyperparameters tuning (dafault false)                                       #
#	--output 	output folder name!!
#	--runcardOut    name output runcard!!
#       -h ;  print help message                                                                        #                                                                    
#                                                                                                       #
#       Author: Dessena Michael                                                                         #
#########################################################################################################

#eval `scram runtime -sh`

# current date and time
d=$(date +%Y%m%d)
t=$(date +%H%M%S)
dd=$(date)

dirDATA=output
OUTPUT=Simulazione_${d}_${t}    # new folder where save the tuning results
TRAINING=training_set_${d}_${t}     # new training set (if a existing trainset is insert whit "-o training set" this in changed and the inserted training set is used)
RUNCARDfile=MyCP5_runcardtemplate.yml   # this is the tamplate of runcard. The program make a copy of this file and change the training set. (mcnntunes save automatically the runcard used in the OUTPUT folder)

Nruns=0
VALIDATION="false"
HYPER="false"
MyRuncard_check="false"
MyVALIDATIONSET=validation_set


x=0
argc=("$@")
argc+=("aadsdefbgsbsa") # add 1 argument to the array to end the cycle on all the arguments
for arg in "${argc[@]}"
do
    case $x in 
        "-d" )
            dirDATA=${arg} ;;
        "-o" )
            TRAINING=${arg} ;;
        "-n" )
            Nruns=${arg} ;;
        "--output" )
            OUTPUT=${arg} ;;
        "--runcardOut" )
            MyRUNCARD=${arg}
            MyRuncard_check="true" ;;
        "--runcard" )
            RUNCARDfile=${arg} ;;
        "--validation" )
            VALIDATION="true"
            MyVALIDATIONSET=${arg} ;;
        "--hyperpar" )
            HYPER="true" ;;
        "-h" )
            echo "        
		Type: ./runTuningProcess.sh -[OPTIONS] [VALUE]

       	Automatic process for run tuning using MCNNTUNES                                                        
       	./runTuningProcess.sh -d output -n NUMRUNS -o training_set --runcard MyRuncard                  
       	-d :		output folder with the result of simulation (default output)                           
       	-o :		folder with training set (default training_set_[DATE]_[TIME])                         
       	-n :		runs number [if not is calculated by the number of runs in the output directory]       
       	--runcard :	yml file whit the configuration for mcnntunes (dafult: MyCP5+runcardtemplate.yml)
       	--validation :	run the validation test (default false)    [validation_set]                        
       	--hyperpar :	run the hyperparameters tuning (dafault false)                                       
       	--output :	output folder name
       	--runcardOut :	name output runcard
       	-h :		print help message "
        exit 1 ;;
    esac
    x=$arg
done

if [ ! -d "${dirDATA}" ]; then
    echo "ATTENTION: Chosen data directory ${dirDATA} doesn't exist !!!"
    exit 1
elif [ ! -d "${TRAINING}" ]; then
    echo "ATTENTION: Chosen training_set directory ${TRAINING} doesn't exist !!!"
elif [ ! -f "${RUNCARDfile}" ]; then
    echo "ATTENTION: runcard file ${RUNCARDfile} not found !!!"
else
    echo "Options ok !!!"
fi

echo "STARTING the tuning process whit following parameters:"
echo "data Direcotry = ${dirDATA}"
echo "training set = ${TRAINING}"
echo "runcard = ${RUNCARDfile}"
echo "Validation = ${VALIDATION}"
echo "Validation set = ${MyVALIDATIONSET}"
echo "Hyper par = ${HYPER}"
echo "Output direcotry = ${OUTPUT}"
echo " "
echo " "

echo "Coping the content of ${dirDATA} directory"
mkdir ${OUTPUT}
cp -r ${dirDATA}/* ${OUTPUT}          # here we are creating a copy of the output file of the simulation 
echo "The content of ${dirDATA} has been copied in ${OUTPUT}"
if [[ "${MyRuncard_check}" == "false" ]]; then
    MyRUNCARD=MyRuncard_${d}${t}.yml
fi
cp ${RUNCARDfile} ${MyRUNCARD}

# check for RUN numbers
if [[ ${Nruns} -eq 0 ]]; then
    i=0
    for file in `ls ${OUTPUT}/00*/result.yoda`; do
        i=$((i+1))
    done
    Nruns=${i}
fi

if [ -d "${dirDATA}" ] && [ ! -d "${TRAINING}" ]; then

    mcnntunes-buildruns -n ${Nruns} -d ${OUTPUT} -f result.yoda -p params.dat --patterns d01 d02 d05 d06 --unpatterns RAW -o ${TRAINING}

fi

if [ -d "${dirDATA}" ]; then

    sed -i "s/.\/training_set/.\/${TRAINING}/" ${MyRUNCARD}
    if [[ "${VALIDATION}" == "true" ]]; then
        sed -i "s/.\/validation_set/.\/${MyVALIDATIONSET}/" ${MyRUNCARD}
    fi

    echo "-----> Running PREPROCESS"
    mcnntunes -o ${OUTPUT} preprocess ${MyRUNCARD}
    
    echo "-----> Running MODEL"
    mcnntunes -o ${OUTPUT} model ${MyRUNCARD}
    
    if [[ "${VALIDATION}" == "true" ]]; then
        echo "-----> Running BENCHMARK"
        mcnntunes -o ${OUTPUT} benchmark ${MyRUNCARD}
    fi


    if [[ "${HYPER}" == "true" ]]; then
        echo "-----> Running OPTIMIZE"
        mcnntunes -o ${OUTPUT} optimize ${MyRUNCARD}
    fi

    echo "-----> Running TUNE"
    mcnntunes -o ${OUTPUT} tune ${MyRUNCARD}
    
    

    

    echo "Removing data folders from ${OUTPUT}"
    rm -r ${OUTPUT}/0*
    rm -rf ${OUTPUT}/GenInformation  || true
    echo "Data folders removed !!!"
    rm ${MyRUNCARD}
    echo "${MyRUNCARD} has been removed !!!"

cat << EOF >> ./listOfSimulation.txt

- ${dd}

output folder: ${OUTPUT}
data folder: ${dirDATA} 
runs number: ${Nruns}
training set folder: ${TRAINING}
-------------------------------------------------------
EOF

else
    echo "Need a output file: -d filename"
    echo "type source runTuningProcess.sh -h"
    echo "to use help"
fi
