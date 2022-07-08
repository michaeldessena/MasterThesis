Primordial kT Tune - MCNNTUNES
=============

Content:

* `Setup Rivet and Run Generator`_

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
    wget -r --no-parent https://gitlab.com/hepcedar/rivet/-/raw/release-3-1-x/analyses/pluginCMS -P Rivet/
    wget -r --no-parent https://gitlab.com/hepcedar/rivet/-/raw/release-3-1-x/analyses/pluginCDF -P Rivet/
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

.. code-block:: bash

    



    
