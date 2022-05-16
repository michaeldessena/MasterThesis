#!/usr/bin/python3

import argparse
import shutil
import os
import sys
import glob
import yaml
import random

# NEW ANALYSIS, CONDOR_SUBMIT, 

#DEFAULT_FOLDER_FOR_FILES=os.getcwd()
# runRivet{name}.sh and output_logs{name} have to be in the main direcotry of the AFS 

CURRENT_DIR=os.getcwd()
DEFAULT_JOBFLAVOUR="testmatch"

def main(args):
    
    random.seed(5)          ### initialize the seed for the random number generator

    name=args.name          ### name for the analysis
    yml_file=args.config    ### name for the configuration file
    add_seed_for_LHE = args.randomseed
    noCondor =args.nocondor

    # Creating a direcotry in the AFS folder where this script is executed (in Configuration/GenProduction/python)
    
    choices_list=['delete', 'continue', 'exit']             ### list of possible choices fot the input
    dir_name='Configuration/GenProduction/python/'+name     ### the name for the directory in the Configuration/GenProduction/python
    try:           
        os.mkdir(dir_name)                              ### make the direcotry
        print(f'{dir_name} folder has been created')
    except:
        if os.path.exists(dir_name)==True:        ### if the try fail and the direcotry exists ask if the user want to delete, write in it or exit 
            msg=f"The folder {dir_name} alredy exist! Do you want to delete it or write into it? digit exit to quit [delete, continue, exit]"
            choice=''
            choice=input(msg)
            while choice not in choices_list:
                print(f'"{choice}" is not a valid choice!!! retry')
                choice=input(msg)
                choice=choice.lower()

            if  choice == choices_list[0]: # delete = remove the existing folder and recreate a empty one
                print(f'Removing the {dir_name} folder...')
                shutil.rmtree(dir_name)
                print(f'The {dir_name} folder has been deleted')
                os.mkdir(dir_name)
                print(f'{dir_name} folder has been recreated')
            elif choice == choices_list[1]:
                print(f'Keeping the same directory: {dir_name}')
            elif choice == choices_list[2]: # continue = Write in to the existing one so there are different analysis in the same folder
                print('Programm terminated!!')
                sys.exit(0)
        else:
            print(f'error in os.mkdir({dir_name})!!! Job terminated...')
            sys.exit(0)
    # the AFS direcotyr as been created


    # Reading the YML file!!!!!!     
    runcard_template_name=''        # runcard template name 
    variation_file_name=''          # variation file name
    path_eos=os.getcwd()  # default is save in the same AFS directory (less space in AFS than in EOS)

    MyYml=YML_READER(yml_file) # open the YML file. Use getYML method to get all de informations

    ### read 'input'
    runcard_template_name=str(MyYml.getYML('input', 'runcard_template'))
    variation_file_name=str(MyYml.getYML('input', 'variations_file'))
    use_eos=MyYml.getYML('input', 'save_eos')
    if use_eos != None:             ### if save on eos!!
        path_eos = str(MyYml.getYML('input','path_eos'))
    
    run_on_eos=MyYml.getYML('input','run_on_eos')
    run_on_eos_path=None
    if run_on_eos != None:          ### if run on eos!!
        run_on_eos_path=str(MyYml.getYML('input','run_on_eos_path'))

    ### read 'cmsDriver_command'
    cmsDriver_seed=str(MyYml.getYML('cmsDriver_command', 'seed'))
    cmsDriver_datatier=str(MyYml.getYML('cmsDriver_command', 'datatier'))
    cmsDriver_conditions=str(MyYml.getYML('cmsDriver_command', 'conditions'))
    cmsDriver_eventcontent=str(MyYml.getYML('cmsDriver_command', 'eventcontent'))
    cmsDriver_numberEvents=str(MyYml.getYML('cmsDriver_command', 'number_events'))

    ### read 'parameters'
    parameters_sedCommand=MyYml.getYML('parameters', 'sed_command')

    ### read 'mcnntemplate'
    mcnntemplate_type=str(MyYml.getYML('mcnntemplate','type'))
    mcnntemplate_type=mcnntemplate_type.lower()
    mcnntemplate_number=''
    mcnntemplate_seed=''
    poss=['sampling','combinations']
    if mcnntemplate_type not in poss:
        print(f'"mcnntemplate": "type" not in {poss}')
        print('Programm terminated...')
        sys.exit(0)
    if mcnntemplate_type == 'sampling':
        mcnntemplate_number=str(MyYml.getYML('mcnntemplate','number'))
        mcnntemplate_seed=str(MyYml.getYML('mcnntemplate','seed'))
    mcnntemplate_output='output'    # mcnntemplate DEFAULT
    try:
        tmpp=str(MyYml.getYML('mcnntemplate', 'output_name'))
    except:
        pass
    if tmpp:
        mcnntemplate_output=tmpp

    ### read 'rivet_customize'
    rivetCustomize_data=MyYml.getYML('rivet_customize', 'data')

    ### read 'condor'
    condor_jobflavour=DEFAULT_JOBFLAVOUR
    tmp=str(MyYml.getYML('condor', 'jobflavour'))
    if tmp:
        condor_jobflavour=tmp
    condor_queue=str(MyYml.getYML('condor', 'queue'))

    ### read 'FxFx_lhe_files'
    FxFx_lhe_files = None
    use_FxFx=MyYml.getYML('FxFx_lhe', 'use_FxFx')
    if use_FxFx != None:
        FxFx_lhe_files=MyYml.getYML('FxFx_lhe','files')
        #mcnntemplate_number=condor_queue=len(FxFx_lhe_files)  ### we are going to use 1 for each run!!!

    ### Print info
    info=f'''**********  Analisys: {name}  ***********\n
input:
\tRuncard_file = {runcard_template_name}
\tVariation_file = {variation_file_name}
\tpath_eos = {path_eos}
\trun_on_eos = {run_on_eos}
\tpath_run_on_eos = {run_on_eos_path}\n
CMSDriver:
\tseed = {cmsDriver_seed}
\tdatatier = {cmsDriver_datatier}
\tconditions = {cmsDriver_conditions}
\teventcontent = {cmsDriver_eventcontent}
\tnumberEvents = {cmsDriver_numberEvents}\n
Parameters:
\tsed_commands = {parameters_sedCommand}\n
mcnntemplate:
\ttype = {mcnntemplate_type}
\tnumber = {mcnntemplate_number}
\tseed = {mcnntemplate_seed}
\toutput_name = {mcnntemplate_output}\n
rivetCustomize:
\tdata = {rivetCustomize_data}\n
condor:
\tjob_flavour = {condor_jobflavour}
\tqueue = {condor_queue}\n
LHE_files:
\tuse_FxFx = {use_FxFx}
\tFxFx_LHE_files: {FxFx_lhe_files}
********************************************
'''

    print(info)
    ###

    # Coping the RUNCARD TEMPLATE to    """dir_name='Configuration/GenProduction/python/'+name""" 
    try:
        xxxx, tmp_runcard_name=os.path.split(runcard_template_name)
        tmp=os.path.join(dir_name, tmp_runcard_name)
        shutil.copy(runcard_template_name, tmp)
        #tmp=os.path.join(dir_name,runcard_template_name)
        pre, ext = os.path.splitext(tmp)
        os.rename(tmp, pre + '.py')
        runcard=pre+'.py'
    except:
        print(f'Impossible to copy {runcard_template_name} in {dir_name}!')
        xxxx, tmp_runcard_name=os.path.split(runcard_template_name)
        tmp=os.path.join(dir_name, tmp_runcard_name)
        pre, ext = os.path.splitext(tmp)
        if os.path.isfile(tmp):
            print(f'file: "{tmp}" already exists!')
            os.remove(tmp)
            shutil.copy(runcard_template_name, tmp)
            #tmp=os.path.join(dir_name,runcard_template_name)
            os.rename(tmp, pre + '.py')
            runcard=pre+'.py'
        elif os.path.isfile(pre+'.py'):
            print(f'file: "{pre}.py" already exists!')
            os.remove(tmp)
            shutil.copy(runcard_template_name, tmp)
            #tmp=os.path.join(dir_name,runcard_template_name)
            os.rename(tmp, pre + '.py')
            runcard=pre+'.py'
        else:
            print('Program terminated...')
            sys.exit(0)
    
    ### build rivet_customize
    tmp_data=""
    if len(rivetCustomize_data)==0:         ### check there is at least one rivet routine!!!
        print('Rivet DATA routine necessary in the YML file!')
        sys.exit(0)
    #tmp_data=rivetCustomize_data[0]
    #for item in rivetCustomize_data:
    #    tmp_data += "'"+str(item)+"'"
    #for item in rivetCustomize_data:
    #    "".join(item)
    tmp_data="' ,'".join(rivetCustomize_data)
    #string1=''
    #for item in tmp_data:
    #    string1 += str(item)

    rivet_customize_template=f'''import FWCore.ParameterSet.Config as cms

def customise(process):
        process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
        process.rivetAnalyzer.AnalysisNames = cms.vstring('{tmp_data}')
        process.rivetAnalyzer.OutputFile = cms.string('result{name}.yoda')
        process.generation_step+=process.rivetAnalyzer
        process.schedule.remove(process.RAWSIMoutput_step)
        return(process)'''
    
    file_name_rivet_customize=f'Configuration/GenProduction/python/rivet_customize{name}.py'
    with open(file_name_rivet_customize, 'w') as file:
        
        print(f'Creating file: "{file_name_rivet_customize}"')
        file.write(rivet_customize_template)

    print('\n********* RIVET_CUSTOMIZE ***********\n'+rivet_customize_template+'\n******************************\n\n')
    print(f'File: "{file_name_rivet_customize} has been created"\n')
    
    ### run cmsDriver.py 
    #runcard= os.path.join(dir_name, runcard_template_name)
    cmd=f'cmsDriver.py {runcard} -s {cmsDriver_seed} --datatier={cmsDriver_datatier} --conditions {cmsDriver_conditions} --eventcontent {cmsDriver_eventcontent} --no_exec -n {cmsDriver_numberEvents} --python_filename=rivet{name}_cfg.py --customise=Configuration/GenProduction/rivet_customize{name}.py'

    add1 =f'''cat << EOF >> rivet{name}_cfg.py

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
EOF
'''
    

    os.system('source Rivet/rivetSetup.sh')
    os.system('scram b -j8')
    print(cmd)
    os.system(cmd)
    print('ADD:\t'+add1)
    os.system(add1)

    if run_on_eos_path is not None:
        shutil.move(file_name_rivet_customize,f'{run_on_eos_path}/Configuration/GenProduction/python/rivet_customize{name}.py')

    if use_FxFx:
        add_randomSeed=f'''sed -i "/process.source/a process.RandomNumberGeneratorService.generator.initialSeed = 1" rivet{name}_cfg.py'''
        print('ADD:\t'+add_randomSeed)
        os.system(add_randomSeed)

    ### add the parameter that have the variation
    if parameters_sedCommand != None:
        print('\n***** ADD parameters: *****')
        for item in parameters_sedCommand:
            item=str(item)
            item += f' rivet{name}_cfg.py'
            print(item)
            os.system(item)
        print('****************************\n')
    ### MCNNTEMPLATE on the rivet{name}_cfg.py 
    mcnntemplate_command=''
    if mcnntemplate_type=='sampling':
        mcnntemplate_command = f'mcnntemplate {mcnntemplate_type} -n {mcnntemplate_number} -s {mcnntemplate_seed} rivet{name}_cfg.py {variation_file_name}'
    elif mcnntemplate_type=='combinations':
        mcnntemplate_command = f'mcnntemplate {mcnntemplate_type} rivet{name}_cfg.py {variation_file_name}'
    
    if mcnntemplate_output != 'output':
        mcnntemplate_command += f'-o {mcnntemplate_output}'
    
    if os.path.exists(mcnntemplate_output):
        try:
            shutil.rmtree(mcnntemplate_output)
        except:
            print(f'impossible to remove {mcnntemplate_output}')

    print(f'-----> running MCNNTEMPLATE:\n{mcnntemplate_command}')
    os.system(mcnntemplate_command)


    ### Move the MCNNTEMPLATE dir to eos_path if using a eos_path
    output_path=name
    if use_eos:
        output_path= os.path.join(path_eos, name)

    print(' ')
    try:
        shutil.rmtree(output_path)
        print(f'"{output_path}" already exists.. removed the existing one') 
    except:
        pass

#    try:
    shutil.move(mcnntemplate_output, output_path) # move the output directory
    print(f'Move "{mcnntemplate_output}" to "{output_path}"')
#    except:
#        print(f'Move "{mcnntemplate_output}" to "{output_path}"')
#        shutil.move(mcnntemplate_output, output_path)

    ### in every directory of output{name}    --- DA RIVEDERE ---
    
    print(f'List of subdirecotry 0000, 0001 ... in output direcotry {output_path}')
    listOfDir=glob.glob(output_path+os.path.sep+'[0-9]**')
    print(listOfDir)
    print('-----------------\n')
    for dir in listOfDir:
        #print(f'creating file: "{file_name_rivet_customize}"')
        head, tail=os.path.split(dir)       # 0000, 0001, etc..
        #head = os.path.normpath(head)
        #FolderNumber=head.split(os.sep)[-1]
        FolderNumber=tail
        print(FolderNumber+":")
        #print(int(FolderNumber))
        #shutil.copy(f'rivet{name}_cfg.py', os.path.join(output_path,str(FolderNumber).zfill(4)))
        tmp=os.path.join(output_path,str(FolderNumber).zfill(4), 'runcard.dat')
        cmd=f'''sed -i "/process = customise(process)/a process.rivetAnalyzer.OutputFile = cms.string('{os.path.join(output_path,str(FolderNumber).zfill(4),'result.yoda')}')" {tmp}''' 
        print(cmd)
        os.system(cmd)

        dest=os.path.join(output_path,str(FolderNumber).zfill(4), f'rivet{name}_cfg.py')
        print(f'Move "{tmp}" to {dest}\n')
        shutil.move(tmp, dest)

    ### creating runRivet with every configuration in output 
    dir_work=CURRENT_DIR
    if run_on_eos:
        dir_work=run_on_eos_path



#    if use_FxFx:
#        print('\n------- ADD the LHE file fot FxFx ----------')
#        for i,item in enumerate(FxFx_lhe_files):
#            i=str(i).zfill(4)
#            filename_rivet=f'{output_path}/{i}/rivet{name}_cfg.py'
#            cmd=f'''sed -i "/Beams:frameType/a \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ 'Beams:LHEF = {item}'," {filename_rivet}'''
#            print(cmd)
#            os.system(cmd)
#        print('')

    if use_FxFx:
        print('\n------- ADD the LHE file fot FxFx ----------')
        for i in range(int(mcnntemplate_number)):
            choice = random.choice(FxFx_lhe_files)
            i=str(i).zfill(4)
            filename_rivet=f'{output_path}/{i}/rivet{name}_cfg.py'
            cmd=f'''sed -i "/Beams:frameType/a \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ 'Beams:LHEF = {choice}'," {filename_rivet}'''
            print(cmd)
            os.system(cmd)
        print('')

    runRivet_template=''
    if use_FxFx == True or add_seed_for_LHE == True: 
        runRivet_template=f'''#!/usr/bin/bash

#cd {dir_work}

###
scram project CMSSW CMSSW_11_2_4
cd CMSSW_11_2_4/src
eval `scram runtime -sh`
echo "copy /eos/user/m/mdessena/CMSSW_MEPythia8/CMSSW_11_2_4/src/Rivet !!!!!!!!"
cp -vr /eos/user/m/mdessena/CMSSW_MEPythia8/CMSSW_11_2_4/src/Rivet .
echo "copy /eos/user/m/mdessena/CMSSW_MEPythia8/CMSSW_11_2_4/src/Configuration !!!!!!!!"
cp -vr /eos/user/m/mdessena/CMSSW_MEPythia8/CMSSW_11_2_4/src/Configuration .
echo "copy /eos/user/m/mdessena/CMSSW_MEPythia8/CMSSW_11_2_4/src/GeneratorInterface !!!!!!!!"
cp -vr /eos/user/m/mdessena/CMSSW_MEPythia8/CMSSW_11_2_4/src/GeneratorInterface .
echo "copy {run_on_eos_path}/Configuration/GenProduction/python/rivet_customize{name}.py !!!!!!!!"
cp -v {run_on_eos_path}/Configuration/GenProduction/python/rivet_customize{name}.py Configuration/GenProduction/python/
####
#cp -r {output_path} .

eval `scram runtime -sh`
source Rivet/rivetSetup.sh

i=$(printf "%04d" ${{1}})
k=$(( $RANDOM % 5000 + 1 ))

sed -i "s/initialSeed = 1/initialSeed = ${{k}}/" {output_path}/${{i}}/rivet{name}_cfg.py

mkdir output   #
cp -rv {output_path}/* output/  #

eval `scram runtime -sh`  #

cmsRun output/${{i}}/rivet{name}_cfg.py

#cmsRun {output_path}/${{i}}/rivet{name}_cfg.py
'''
    else:
        runRivet_template=f'''#!/usr/bin/bash

cd {dir_work}

eval `scram runtime -sh`
source Rivet/rivetSetup.sh

i=$(printf "%04d" ${{1}})

cmsRun {output_path}/${{i}}/rivet{name}_cfg.py
'''

#cp result${name}_\${{1}}.yoda ${output_path}/${{i}}/result.yoda
#rm result${name}_\${{1}}.yoda
    print(f'Creating "runRivet{name}.sh" scriptfile')
    with open(f'runRivet{name}.sh', 'w') as runRivetFile:
        runRivetFile.write(runRivet_template)
    print('\n******** runRivet ********\n'+runRivet_template+'\n*******************************\n')
    print(f'"runRivet{name}.sh" has been created\n')

    print(f'Adding permission to runRivet{name}.sh\n')
    os.system(f'chmod +rx runRivet{name}.sh')
    

    try:
        os.mkdir(f'output_logs{name}')
        print(f'output_logs{name} folder has been created!')
    except:
        print(f'output_logs{name} already exist')
    print('')

    ### Creating the condor.sub file
    condor_template=f'''executable            = runRivet{name}.sh
arguments             = $(ProcId)
output                = output_logs{name}/rivet.$(ClusterId).$(ProcId).out
error                 = output_logs{name}/rivet.$(ClusterId).$(ProcId).err
log                   = output_logs{name}/rivet.$(ClusterId).log
+JobFlavour           = "{condor_jobflavour}"
request_memory        = 2000M
queue {condor_queue}'''
    
    print(f'Creating "condor{name}.sub" scriptfile')
    with open(f'condor{name}.sub', 'w') as condorFile:
        condorFile.write(condor_template)
    print('\n******** CONDOR SUBMIT SCRIPT ********\n'+condor_template+'\n*******************************\n')
    print(f'"condor{name}.sub" has been created')

    if noCondor==False:
        os.system(f'condor_submit condor{name}.sub')



### CLASS to read the configuration file
class YML_READER():
    def __init__(self, file_name):
        self.file_name=file_name
        with open(file_name) as file:
            self.infile=yaml.load(file, Loader=yaml.SafeLoader)
        
    def getYML(self, node, key):
        try:
            return self.infile[node][key]
        except:
            print(f'not found [{key}] in node [{node}] in the YML runcard {self.file_name}')
            return None

if __name__=='__main__':
    
    try:
        cmsswbase = os.getenv('CMSSW_BASE')
    except:
        cmsswbas = None

    if cmsswbase is None:
      print('you have to run "cmsenv" in your working area first! [CMSSW_*_*_*/src/]')
      sys.exit(0)
    print(f'{cmsswbase} okay!')
    

    parser = argparse.ArgumentParser(description='Perform a new analysis, pythia8, rivet...')
    parser.add_argument("name", type=str, help='Name of the new Analysis (REQUIRED)')
    parser.add_argument("-c", "--config", help="configurations file YML format", required=True)
    parser.add_argument("--randomseed", default=False, action='store_true', help="Add a random seed to the job to use if generating ME events")
    parser.add_argument("--nocondor", default=False, action='store_true', help="build everything but not submit it to condor")
    args = parser.parse_args()

    main(args)