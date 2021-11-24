SETUP RIVET YODA MCNNTUNES on lxplus
=====================================

Content:

* `Standard CMSSW setup`_
* `RIVET and YODA setup`_
* `MCNNTUNES installation`_
* `Add RIVET plugins`_
* `Generating template and running on CondoHT queue`_
* `Merge different outputs`_
* `Run MCNNTUNES tuning`_


______________________________________________________________

.. _Standard CMSSW setup:

Standard CMSSW setup
--------------------------------------

We need to setup the CMSSW on our lxplus directory, so enter lxplus:

.. code-block:: bash

	ssh mdessena@lxplus.cern.ch -X

now create a direcotry where you want to store you CMSSW environment:

.. code-block:: bash

	mkdir <direcotryname>
	cd <directory name>

now run the following commands:

.. code-block:: bash

	cmsrel CMSSW_11_2_4
	cd CMSSW_11_2_4/src
	cmsenv

.. _RIVET and YODA setup:

RIVET and YODA setup
-------------------------------------

in order to initialize RIVET/YODA follow the instruction at: `This link <https://twiki.cern.ch/twiki/bin/view/CMS/Rivet#Setting_Rivet_in_CMSSW>`_

than run:

.. code-block:: bash

	mkdir Configuration/GenProduction
	mkdir Configuration/GenProduction/python


.. _MCNNTUNES installation:

MCNNTUNES installation
-------------------------------------

MCNNTUNES is installed via PyPl run:

.. code-block:: bash

	pip3 install --user mcnntunes
	export PATH=${PATH}:${USER}/.local/bin


.. _Add RIVET plugins:

Add RIVET plugins
--------------------------------------

Copy the rivet folder from GitLab (NOT CMS internal rivet):

.. code-block:: bash

	git clone https://gitlab.com/hepcedar/rivet.git
	cp -r rivet/analysis/pluginCMS rivet/analysis/pluginCDF Rivet

add the following lines at the rivetSetup.sh file (after the first for loop):

.. code-block::

	for ITEM in pluginCMS pluginCDF
	do
  		export RIVET_REF_PATH=$RIVET_REF_PATH:$CMSSW_BASE/src/Rivet/${ITEM}
  		export RIVET_INFO_PATH=$RIVET_INFO_PATH:$CMSSW_BASE/src/Rivet/${ITEM}
  		export RIVET_PLOT_PATH=$RIVET_PLOT_PATH:$CMSSW_BASE/src/Rivet/${ITEM}
	done

Then run:

.. code-block::

	source Rivet/rivetSetup.sh
	scram b -j8


.. _Generating template and running on CondoHT queue:

Generating template and running on CondoHT queue
---------------------------------------

use mcnntemplate to generate template:

.. code-block:: bash
	
	mcnntemplate sampling -n 150 -s 100 runcard_template1TeV.dat variation.yml

now use the script *newAnalysis2.sh*

.. code-block:: bash

	./newAnalysis2.sh NAME_OF_ANAlYSIS -data DATA -queue N_CONDOR_RUNS -nruns N_EVENT_PYTHIA

for example:

.. code-block:: bash

	./newAnalysis2.sh 13TeV_2params_more -data CMS_2015_PAS_FSQ_15_007 -queue 150 -nruns 4500000

now run:

.. code-block:: bash

	source cmsDriverMulti<NAME_OF_ANAlYSIS>.sh
	condor_submit condor<NAME_OF_ANAlYSIS>.sub

.. _Merge different outputs:

Merge different outputs
---------------------------------------

need to move the outputs directory in the same directory of the *MergeOutput.py* script:

.. code-block:: bash

	python3 MergeOutput.py

**NOTE:** the script need to be edited!

now run the mcnntunes-buildrun

.. code-block:: bash
	mcnntunes-buildruns -n NRUNS -d OUTPUT_DIR -f result.yoda -p params.dat --patterns UNPATTERNS--unpatterns UNPATTERNS -o training_set

for example in our case:

.. code-block::
	mcnntunes-buildruns -n 90 -d outputTOTALE_2params -f result.yoda -p params.dat --patterns CMS_2015_I1384119/d01-x01-y01 CMS_2015_PAS_FSQ_15_007/d01-x01-y01 CMS_2015_PAS_FSQ_15_007/d02-x01-y01 CMS_2015_PAS_FSQ_15_007/d05-x01-y01 CMS_2015_PAS_FSQ_15_007/d06-x01-y01 CMS_2012_PAS_FSQ_12_020/d05-x01-y01 CMS_2012_PAS_FSQ_12_020/d06-x01-y01 CMS_2012_PAS_FSQ_12_020/d08-x01-y01 CMS_2012_PAS_FSQ_12_020/d09-x01-y01 CDF_2015_I1388868/d01-x01-y01 CDF_2015_I1388868/d02-x01-y01 CDF_2015_I1388868/d05-x01-y01 CDF_2015_I1388868/d06-x01-y01 --unpatterns RAW -o training_set_2params


.. _Run MCNNTUNES tuning:

Run MCNNTUNES tuning
---------------------------------------

to run all the tuning process use:

.. code-block:: bash

	./runTuningProcess2 -d OUTPUT_DIR -o training_set --runcard <YML_RUNCARD_NAME>

to get a list of the options use:

.. code-block:: bash

	./runTuningProcess2 -h

Now the output of the tuning is saved in a output direcotry (Default: Simulazione_DATE_TIME)