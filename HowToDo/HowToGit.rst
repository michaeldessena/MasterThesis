How to use Git
===============

Content:

* `Git vs Github`_
* `GitHub Workflow`_
* `Git and Github minimal guide`_
* `Setup Git`_
* `Git commit`_
* `New branches`_
* `Merge branches`_
* `Push an existing repository to Github`_



______________________________________________________________

.. _Git vs Github:

Git vs Github
----------------

Git and Github are not the same thing. Github si just a website it give a UI to what Git does. Git controll stuff, your codes, your files...


.. _GitHub Workflow:

GitHub Workflow
------------------

Github work as a remote repository where all the users can upload/download their files and submit their changes to existing files.
Git can automatically merge different code files togheter.
What Github do for us is to track all the **commit** (all the changes submission) after that you do all your commits you can push all this changes to the main repository. 
After some times you need to refresh your local repository making a pull from the main repository.

What you can to is open new branch a copy of the master branch at a specific moment in time 


.. _Git and Github minimal guide:

Git and Github minimal guide
===========================

Create a new repository on `Github <https://github.com/>` and upload commit ecc.. 

.. _Setup Git: 

Setup Git
---------

First step create a new direcotory o your pc open a terminal:

.. code-block:: bash

	mkdir <projectdir>
	cd <projectdir>

Now you need to initialize the new direcotry running:

.. code-block:: bash

	git init

This make the new direcotry a Git repository now Git can track all your file exc..

.. _Git commit:

Git commit
------------

Now you can create file modify all the files you want to modify localy on your pc. When, you are ready for the submission on github follow this steps: 
Then run:

.. code-block:: bash

	git add <filename>

of if you want to add everything

.. code-block:: bash

	git add .

you can in every moment type:

.. code-block:: bash

	git status

to check the modified file ready for the commit or added for the commit.

Now, you can commit you changes creating a commit

.. code-block:: bash

	git commit -m "A messsage for the commit"

.. _New branches:

New branches
---------

Now if you want create a new brach and not modify your master branch you need to run:

.. code-block:: bash
	
	git checkout -b <newBranchName>

now, you are switched to the new branch and you can submit your file as before:

.. code-block:: bash

	git add .
	git commit -m "changes on the new branch"


now you can change the branch with the following code:

.. code-block:: bash

	git checkout <theBranchIWant>

now your switched to another branch


.. _Merge branches:

Merge branches
--------------

now if you are on a branch (not the master) and you want merge it with the master, you can run:

.. code-block:: bash

	git merge <master_brench>

now you can switch on your master again and see the changes:

.. code-block:: bash
	
	git checkout <master_brench>

.. _Push an existing repository to Github:

Push an existing repository to Github
----------------------------------------

Now if you want to add a remote repository (github repository on server), use:

.. code-block:: bash

	git remote add origin <Github link>


(you can chenage the name from origin to another one, the url is stored with the name you choose).
Now you can do the push: 

.. code-block:: bash

	git push -u origin master

NOTE: before if you are not sure you are on the master branch (or the other branch you want):

.. code-block:: bash

	git checkout <master_branch>


Git global config
---------------

Now, you can configure your global options using:

.. code-block:: bash

	git config --global user.name "MYNAME"
	git config --global user.email "myemail"

MYNAME is the name that the other user can see and identify me!


Git pull from a remote repository branch
---------------------

.. code-block:: bash
	
	git pull origin <branch>

for example:

.. code-block:: bash

	git pull origin <branch>

IMPORTANT: if you do some change in your local repository and you don't have the latest version of the remote repository if you try to do the push you get an error!

anyway if you want to do the push:

.. code-block:: bash

	git push -u origin <branch>