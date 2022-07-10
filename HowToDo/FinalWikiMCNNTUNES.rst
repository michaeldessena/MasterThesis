Primordial kT Tune - MCNNTUNES
=============

Content:

* `Setup Rivet and Run Generator`_
* `Install MCNNTUNES via PyPl`_
* `Create python3 virtual environment`_
* `Install YODA from source`_
* `Activate your venv and add yoda path to PYTHONPATH`_
* `Install RIVET`_
* `run MCNNTUNES`_
_________________________________

.. _Setup Rivet and Run Generator:

Setup Rivet and Run Generator
----------------------------

.. code-block:: bash

    cmsrel CMSSW_11_2_4
    cd CMSSW_11_2_4/src
    cmsenv

    git-cms-init
    git-cms-addpkg GeneratorInterface/RivetInterface
    git-cms-addpkg Configuration/Generator
    git clone ssh://git@gitlab.cern.ch:7999/${USER}/Rivet.git
    git remote add cms-gen ssh://git@gitlab.cern.ch:7999/cms-gen/Rivet.git
    cp -r afs/cern.ch/user/m/mdessena/public/Rivet .
    source Rivet/rivetSetup.sh
    scram b -j8

To install MCNNTUNES you can use pip:

.. code-block:: bash

	pip3 install mcnntunes

Download the MyAnalysis_FxFx.sh script, runcard.dat (Need to be edited), template.yml (Need to be edited) and variation.yml 

.. code-block:: bash

    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/MyANALYSIS_FxFx/MyAnalysis_FxFx.py -O MyAnalysis_FxFx.py
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/runcard.dat -O runcard.dat
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/template.yml -O template.yml
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/variation.yml -O variation.yml

.. code-block:: bash

    chmod +rx MyAnalysis_FxFx.py
    ./MyANALYSIS_FxFx.py PrimordialkToutput -c template.yml

Check that the files are submitted to condor correctly! Wait that condor returns all the yoda files (the output is displayed in )..

.. _Install MCNNTUNES via PyPl:

Install MCNNTUNES via PyPl [just first time]
----------------------------------------------------

To install MCNNTUNES you can use pip:

.. code-block:: bash

	pip3 install mcnntunes
	

.. _Create python3 virtual environment:

Create python3 virtual environment [just first time]
----------------------------------------------------

Now, you need to create a python3 virtual environment (venv). This operation is to be done just the first time.

.. code-block:: bash

	mkdir myEnv

To create the environment run:

.. code-block:: bash

	python3 -m venv myEnv --system-site-packages

You may need to install **python-venv**:

.. code-block:: bash

	sudo apt install python3.8-venv

.. _Install YODA from source:

Install YODA from source [just first time]
----------------------------------------------------

The yoda installation from the source is done using the following command:

.. code-block:: bash
	
	wget https://yoda.hepforge.org/downloads/?f=YODA-1.9.1.tar.gz -O YODA-1.9.1.tar.gz
	tar -xf YODA-1.9.1.tar.gz
	cd YODA-1.9.1/
	./configure --prefix=/home/michael/myEnv/ PYTHON_VERSION='3.8' (set your python3 version)
	make -j2
	make -j2 install

.. _Activate your venv and add yoda path to PYTHONPATH:

Activate your venv and add yoda path to PYTHONPATH [every time]
----------------------------------------------------

Now you need to activate you environment to do this use:

.. code-block:: bash

	source MyEnvNAME/bin/activate 

launch a python interactive session whit:

.. code-block:: bash

	python3

than in the pyhton session type:

.. code-block:: python
	
	import yoda
	print(yoda.__file__)


Now need to append output path to the $PYTHONPATH variable

.. code-block:: bash

	export PYTHONPATH=${PYTHONPATH}:/home/michael/myEnv/lib/python3.8/site-packages

.. _Install RIVET:

Install RIVET
---------------------

In order to install Rivet on your pc use the following commands (`rivet installation <https://gitlab.com/hepcedar/rivet/-/blob/release-3-1-x/doc/tutorials/installation.md>`_):

.. code-block:: bash

	mkdir myEnvNAME/rivet
	cd myEnvNAME/rivet
	wget https://gitlab.com/hepcedar/rivetbootstrap/raw/3.1.4/rivet-bootstrap
	chmod +x rivet-bootstrap

now, to install locally:
	
.. code-block:: bash

	./rivet-bootstrap

to change location and install options use:

.. code-block:: bash

	INSTALL_PREFIX=${PATH_TO_myEnvNAME}/myEnvNAME/rivet MAKE="make -j8" ./rivet-bootstrap

wait a lot of time when installation ended a command to use to set all the variables is displayed, for example:

.. code-block:: bash

	source ${PATH_TO_myEnvNAME}/myEnvNAME/rivet/rivetenv.sh

you can add this line to your *myEnvNAME/bin/activate* file, and to reset when deactivate the **$PYTHONPATH** add the following lines to the file:

.. code-block:: bash

	_OLD_VIRTUAL_PYTHONPATH="$PYTHONPATH"

this one before the changes to $PYTHONPATH to store the paths. AND, in the deactivate function add:

.. code-block:: bash

	if [ -n "${_OLD_VIRTUAL_PYTHONPATH:-}" ] ; then
        PYTHONPATH="${_OLD_VIRTUAL_PYTHONPATH:-}"
        export PYTHONPATH
        unset _OLD_VIRTUAL_PYTHONPATH
    fi

try tipe **rivet + TAB** if completetion is avaiable everythings go well!

.. _run MCNNTUNES:

run MCNNTUNES [locally]
----------------------------------------------------

Now you can run mcnntunes!! check by running. 

On local pc download the following script:

.. code-block:: bash
    mkdir PrimordialkTTunes
    cd PrimordialkTTunes
    scp -r <name>@lxplus.cern.ch:<path_to_PrimordialkToutput> .
    scp -r <name>@lxplus.cern.ch:<path_to_Rivet> .

.. code-block:: bash

    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/runTuningProcess.py -O runTuningProcess.py
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/MY-mcnntunes-buildruns.py -O MY-mcnntunes-buildruns.py
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/checkMySimulation.py -O checkMySimulation.py 
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/checkEMPTYyodaFILE.py -O checkEMPTYyodaFILE.py 
    wget https://raw.githubusercontent.com/michaeldessena/MasterThesis/main/HowToDo/script/runcardMCNNTUNES_PerBin.yml -O runcardMCNNTUNES_PerBin.yml

    chmod +rx checkMySimulation.py
    chmod +rx checkEMPTYyodaFILE.py    
    ./checkMySimulation PrimordialkToutput
    ./checkEMPTYyodaFILE PrimordialkToutput
    ./checkMySimulation PrimordialkToutput

    python3 MY-mcnntunes-buildruns.py -n <number_of_folder_in_PrimordialkToutput> -d PrimordialkToutput -f result.yoda -p params.dat --patterns CMS_2019_I1753680/d27-x01-y03@0.1:5.0d CMS_2019_I1753680/d28-x01-y03@0.001:0.006 --unpatterns RAW -o training_set --expData ../Rivet
    
The following script run all MCNNTUNES steps:

.. code-block:: bash

    ./runTuningProcess.py PrimordialkToutput -r runcardMCNNTUNES_PerBin.yml -o TunePerBinModel 
