MCNNTUNES in local
======================================

Content:

* `Install MCNNTUNES via PyPl`_
* `Create python3 virtual environment`_
* `Install YODA from source`_
* `Activate your venv and add yoda path to PYTHONPATH`_
* `run MCNNTUNES`_
___________________________________

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

.. _run MCNNTUNES:

run MCNNTUNES
----------------------------------------------------

now you can run mcnntunes!!

check by running

.. code-block:: bash

	mcnntunes -o output preprocess runcard.yml