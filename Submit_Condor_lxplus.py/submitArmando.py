#!/bin/env python

# v3 by Bermudez Martinez, Jan 2022
# based on Knutsson, Feb 2011
# run with HTCondor

from optparse import OptionParser

import os, sys, re
import time


#
### Parser stuff
#

parser = OptionParser()

def parse_range(astr):
    result=set()
    for part in astr.split(','):
        run=part.split('-')
        result.update(range(int(run[0]),int(run[-1])+1))
    return sorted(result)
    
parser.add_option("-r", "--runs", action="store", help="Runs you want to submit, example: -r 0-13,16,18-22 (default=000)", default="000")
parser.add_option("-d", "--directory", action="store", help="Directory (default=mcruns)", default='mcruns')
parser.add_option("-c", "--configfile", action="store", help="Configuration file for cmsRun (default=rivet_cfg.py) \n Should exist in each in DIRECTOR/RUN", default='rivet_cfg.py')
parser.add_option("-q", "--queue", action="store", help="queue", default='1')

(opts, args) = parser.parse_args()
opts.runs=parse_range(opts.runs)

#
### ask_ok
#
def ask_ok(prompt, retries=4, complaint='You need to answer y/ye/yes or n/no!!!'):
  while True:
    ok = raw_input(prompt)
    if ok in ('y', 'ye', 'yes'): return True
    if ok in ('n', 'no'): sys.exit()
    retries = retries - 1
    if retries < 0: raise IOError('refusenik user')
    print complaint

#
### function to get the name of the output-aida from the config-file
#
def getaidaname(conffile):
  with open(conffile,"r") as inFile:
    for line in inFile:
      if "rivetAnalyzer" and "OutputFile" and "yoda" in line:
        return re.search("\'(.+?)\'", line).group(1)
  inFile.closed


#
### Builder Classes
#
class CommandBuilder:
  def __init__(self, name):
    self._name = name
  def build(self):
    try:
      os.cd(self._name)
      inputfile = open('job_'+name+'.sub', 'w')
      infile += '#!/bin/bash'
      infile += 'echo "hello world from "'+name
    except Exception, e:
      print "Error: %s" % str(e)  

class LXBATCHCommandBuilder(CommandBuilder):
  def __init__(self, name, directory, configfile, queue, aidaout):
    CommandBuilder.__init__(self, name);
    self._directory=directory
    self._configfile=configfile
    self._queue=queue
    self._aidaout=aidaout
  def build(self):
    try:
      cmsswbase = os.getenv('CMSSW_BASE')
      if cmsswbase is None:
        print "you have to run cmsenv in your working area first!"
        return
      
      fulldir = os.getcwd()+"/"+self._directory+"/"+self._name

      submitscriptname="job_"+self._name+".sub"
      script = open(fulldir+"/"+submitscriptname, "w")
      infile=''
      infile += '#!/bin/bash\n'
      infile += 'pwd=`pwd`\n'
      infile += 'echo $pwd\n'
      infile += 'cd '+cmsswbase+'/src\n'
      infile += 'eval `scram runtime -sh`\n'
      infile += 'source Rivet/rivetSetup.sh\n'
      infile += 'cd $TMP\n'
      infile += 'scp /afs/cern.ch/work/a/abermude/public/LHE/mcatnlo/P8/13TeV/DY/DY-13TeV-NNPDF3.0-amcatnlo-P8-$[$SGE_TASK_ID+1].lhe.gz events.lhe.gz\n'
      infile += 'gunzip *.lhe.gz\n'
      infile += 'cp '+fulldir+'/'+self._configfile+' .\n'
      infile += 'sed -i "s/initialSeed = 1/initialSeed = $[$SGE_TASK_ID+1]/" '+self._configfile+'\n'
      infile += 'cmsRun ' + self._configfile + ' >& log_GEN_'+self._name+'.txt\n' #changed &> to >&
      infile += 'ls\n'
      infile += 'mv '+self._aidaout+' '+fulldir+'/out-$[$SGE_TASK_ID+1].yoda\n'
      infile += 'rm *lhe\n'
      script.write(infile)
      script.close()

      scriptname="job_"+self._name+".sh"
      script = open(fulldir+"/"+scriptname, "w")
      infile=''
      infile += 'executable          = '+submitscriptname+'\n'
      infile += 'transfer_executable = True\n'
      infile += 'universe            = vanilla\n'
      #infile += 'output              = submitscript_$(Cluster)_$(Process).out\n'
      #infile += 'error               = submitscript_$(Cluster)_$(Process).out\n'
      #infile += 'log                 = submitscript_$(Cluster)_$(Process).log\n'
      infile += 'should_transfer_files   = IF_NEEDED\n'
      infile += 'when_to_transfer_output = ON_EXIT\n'
      infile += 'environment = "CLUSTER=$(Cluster) SGE_TASK_ID=$(Process)"\n'
      infile += 'RequestMemory = 2524\n'
      infile += '+RequestRuntime     = 18000\n'
      infile += '+MaxRuntime         = 18000\n'
      infile += 'queue '+self._queue+'\n'
      script.write(infile)
      script.close()
      print "Run " + self._name + ":   "

      os.system('cd '+fulldir+';chmod u+x ' + scriptname+';chmod u+x ' + submitscriptname+'; condor_submit '+self._directory+self._name+' '+scriptname)
    except Exception, e:
      print "%s" % str(e) 
      ask_ok('Continue script? (y/n)');

 
#
## Loop the requested runs
#
misscounter = 0
for irun in opts.runs:
  if (irun >= 100):
    run_str='%i' % irun
  elif (irun >= 10 and irun < 100):
    run_str='0%i' % irun
  elif (irun < 10):
    run_str='00%i' % irun

  # get the name of the output .aida-file
  #aidafile_str = getaidaname(os.getcwd()+'/'+opts.directory+'/'+run_str+'/'+opts.configfile)
  aidafile_str = getaidaname(os.getcwd()+'/Configuration/GenProduction/python/rivet_customize.py')

  if (os.path.exists(os.getcwd()+'/'+opts.directory+'/'+run_str+'/'+aidafile_str)==1):
    print "Run " + run_str + ": \n " + aidafile_str + " aidafile_str already exist   "
  else:
#    misscounter=misscounter+1
#    if (irun>0): time.sleep(2) #Don't overload batch. Needed?
    commandBuilder = LXBATCHCommandBuilder(run_str, opts.directory, opts.configfile, opts.queue, aidafile_str) 
    command = commandBuilder.build()


print "\n %i jobs submitted. \n" % misscounter
#AK   if ((os.path.exists(os.getcwd()+'/'+opts.directory+'/'+run_str+'/out.aida'))==0):
#AK     misscounter = misscounter +1 
#AK     print "Run " + run_str + ": missing   %i "  % misscounter


