SETUP RIVET YODA MCNNTUNES on lxplus
=====================================

Content:

* `Standard CMSSW setup`_
* `RIVET and YODA setup`_
* `MCNNTUNES installation`_

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