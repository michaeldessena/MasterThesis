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
    source Rivet/rivetSetup.sh
    scram b -j8

To install MCNNTUNES you can use pip:

.. code-block:: bash

	pip3 install mcnntunes

Download the MyAnalysis_FxFx.sh script, runcard.dat (Need to be edited), template.yml (Need to be edited) and variation.yml 

.. code-block:: bash

    curl -s https://github.com/michaeldessena/MasterThesis/blob/8ce8884fb9f20ddf24b8f3f01e69a1af09168ab8/MyANALYSIS_FxFx/MyAnalysis_FxFx.py -o MyAnalysis_FxFx.py
    curl -s https://github.com/michaeldessena/MasterThesis/blob/8ce8884fb9f20ddf24b8f3f01e69a1af09168ab8/HowToDo/script/runcard.dat -o runcard.dat
    curl -s https://github.com/michaeldessena/MasterThesis/blob/8ce8884fb9f20ddf24b8f3f01e69a1af09168ab8/HowToDo/script/template.yml -o template.yml
    curl -s https://github.com/michaeldessena/MasterThesis/blob/8ce8884fb9f20ddf24b8f3f01e69a1af09168ab8/HowToDo/script/variation.yml -o variation.yml

.. code-block:: bash

    chmod +rx MyAnalysis_FxFx.py
    ./MyANALYSIS_FxFx.py PrimordialkToutput -c template.yml

Check that the files are submitted to condor correctly! Wait that condor returns all the yoda files..

.. code-block:: bash

    

    
