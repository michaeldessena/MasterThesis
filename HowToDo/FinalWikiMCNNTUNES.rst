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

    