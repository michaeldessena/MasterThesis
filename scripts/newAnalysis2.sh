#!/usr/bin/bash

eval `scram runtime -sh`

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
QUEUE=10
DATA=CMS_2018_I1680318
NRUNS=2500000

x=0
argc=("$@")
argc+=("aadsdefbgsbsa") # add 1 argument to the array to end the cycle on all the arguments
for arg in "${argc[@]}"
do
    case $x in 
        "-data" )
            DATA=${arg} ;;
        "-queue" )
            QUEUE=${arg} ;;
        "-nruns" )
            NRUNS=${arg} ;;
        "-h" )
            echo "        
Type: ./newAnalysis NAME -[OPTIONS] [VALUE]
        NAME : name for the analysis
        -data :  data name RIVET ANAlYSIS (default CMS_2018_I1680318)
        -queue : number of condor submissions (default 10)
        
        example: ./newAnalysis 13TeV -data CMS_2018_I1680318 -queue 10"
        exit 1 ;;
    esac
    x=$arg
done


if [ -d "output" ]; then
  mv output Configuration/GenProduction/python/output${1}
fi

cat << here > ./cmsDriverMulti${1}.sh
#!/usr/bin/bash

# Change process name in Matthias' config files
i=0
eval \`scram runtime -sh\`

for file in \`ls Configuration/GenProduction/python/output${1}/*/runcard.dat\`; do
  
  if [[ \$i -lt 10 ]]; then
    cp \$file Configuration/GenProduction/python/MinBias_${1}_000\${i}.py
  elif [[ \$i -lt 100 ]]; then
    cp \$file Configuration/GenProduction/python/MinBias_${1}_00\${i}.py
  elif [[ \$i -lt 1000 ]]; then
    cp \$file Configuration/GenProduction/python/MinBias_${1}_0\${i}.py
  else
    cp \$file Configuration/GenProduction/python/MinBias_${1}_\${i}.py
  fi
  
  sed "s#result${1}.yoda#result${1}_\${i}.yoda#g" Configuration/GenProduction/python/rivet_customize${1}.py > Configuration/GenProduction/python/rivet_customize${1}_\${i}.py    
  i=\$((i+1))
done

source Rivet/rivetSetup.sh
scram b
j=0

for file in \`ls Configuration/GenProduction/python/MinBias_${1}_*.py\`; do
  cmsDriver.py \$file -s GEN --datatier=GEN-SIM-RAW --conditions auto:mc --eventcontent RAWSIM --no_exec -n ${NRUNS} --python_filename=rivet${1}_\${j}_cfg.py --customise=Configuration/GenProduction/rivet_customize${1}_\${j}.py
  cat << EOF >> rivet${1}_\${j}_cfg.py

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
EOF
  j=\$((j+1))
done
here

chmod +rx cmsDriverMulti${1}.sh

cat << here > ./condor${1}.sub
executable            = runRivet${1}.sh
arguments             = \$(ProcId)
output                = output_logs/rivet.\$(ClusterId).\$(ProcId).out
error                 = output_logs/rivet.\$(ClusterId).\$(ProcId).err
log                   = output_logs/rivet.\$(ClusterId).log
+JobFlavour           = "testmatch"
queue ${QUEUE}
here

cat << here > ./runRivet${1}.sh
#!/usr/bin/bash

cd ${SCRIPT_DIR}
eval \`scram runtime -sh\`
source Rivet/rivetSetup.sh
cmsRun rivet${1}_\${1}_cfg.py
if [[ \${1} -lt 10 ]]; then
  cp result${1}_\${1}.yoda Configuration/GenProduction/python/output${1}/000\${1}/result.yoda
elif [[ \${1} -lt 100 ]]; then 
  cp result${1}_\${1}.yoda Configuration/GenProduction/python/output${1}/00\${1}/result.yoda
elif [[ \${1} -lt 1000 ]]; then 
  cp result${1}_\${1}.yoda Configuration/GenProduction/python/output${1}/0\${1}/result.yoda
else
  cp result${1}_\${1}.yoda Configuration/GenProduction/python/output${1}/\${1}/result.yoda
fi

here

chmod +rx runRivet${1}.sh

cat << here > ./Configuration/GenProduction/python/rivet_customize${1}.py
import FWCore.ParameterSet.Config as cms

def customise(process):
        process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
#        process.rivetAnalyzer.AnalysisNames = cms.vstring('ATLAS_2010_S8591806', 'CMS_2010_S8547297', 'CMS_2010_S8656010', 'CMS_QCD_10_002')
        process.rivetAnalyzer.AnalysisNames = cms.vstring('${DATA}')
        process.rivetAnalyzer.OutputFile = cms.string('result${1}.yoda')
        process.generation_step+=process.rivetAnalyzer
        process.schedule.remove(process.RAWSIMoutput_step)
        return(process)
here
