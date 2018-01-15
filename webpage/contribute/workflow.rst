.. include:: ../references.rst

Workflow
========

This page describes the git workflow you are recommended to use if you want to contribute to gamma-cat.
In short words, we use the fork-branch-pullrequest way.

If you want to run the ``gamma-cat`` Python scripts locally, go through the Installation chapter.

But contribution can be done without the installation because we have continous integration tests set up on travis-ci that check that everything is working OK. If that is what you want to do, jump over the Installation chapter.

For information about the ``gammacat`` Python packages and the structure of the input files, please go to `Code <http://gamma-cat.readthedocs.io/contribute/code.html>`__

Fork/ clone the repo
--------------------

The first step is forking `gamma-cat <https://www.github.com/gammapy/gamma-cat>`__ into your github account. 
Easily done by clicking on ``fork`` in the right top corner of `gamma-cat <https://www.github.com/gammapy/gamma-cat>`__

Create a folder ``gamma-cat`` (or as you like) on your local machine and in there execute::

	git clone https://github.com/<your username>/gamma-cat.git

Installation (optional)
-----------------------

If you want to run the ``gamma-cat`` Python scripts locally, you need to install Python 3.6 and some Python packages. 
We recommend you to download `Anaconda <https://www.continuum.io/downloads>`__
and then run the following commands in the ``gamma-cat`` folder::

	conda config --set always_yes yes --set changeps1 no
	conda update -q conda
	conda info -a
	# Now install our dependencies
	conda env create -f environment.yml
	# Activation of the installed environment
	source activate gamma-cat

Make changes
------------

This section describes the git workflow for changes and merging your changes into the gamma-cat master branch afterwards.
For details about the code itself, please go to `Code <http://gamma-cat.readthedocs.io/contribute/code.html>`__

If you want to make changes in the ``gamma-cat`` code, go to your local repository and make sure that your master-branch is up-to-date.
Then create a branch from the current status of master by executing::

	git checkout -b <Name of branch>

(Note: If there is a corresponding issue to the changes you do, the name of the branch should be something like `issue_xxx`. Otherwise, we highly recommend you to use resonable and easy names.)

When your work is done and you commited the changes locally(!) go back to the master branch and download all changes which might be done during your work (git pull upstream master). Then, go back to your working branch and execute::

	git rebase master

Then upload the branch to your github account (git push) and open a Pull Request in the browser. A short description of the PR is always useful.