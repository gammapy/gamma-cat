.. include:: ../references.rst

Workflow
========

**This page gives an overview how to make changes or additions to Gamma-Cat like e.g. add data, fix bugs or whatever.**
It is *not* a tutorial which explains the tools (git, Github, Sphinx etc.) or the code (Python etc.)

If you want to run the ``gamma-cat`` Python scripts locally, go through the Installation chapter.
But contribution can be done without the installation because we have continous integration tests set up on travis-ci that check that everything is working OK. If that is what you want to do, jump over the Installation chapter.
For information about the ``gammacat`` Python packages and the structure of the input files, please go to `Code <http://gamma-cat.readthedocs.io/contribute/code.html>`__

Pull requests
-------------
Contribution can be done via pull requests on Github (hence you need an Github account).
We like them small and easy to review.
To get familiar with git and github you can look at `<https://help.github.com>`__ or simply use google for more information.

The general contribution cycle is roughly as follows:
1. Get the latest version of the ``master`` branch
2. Checkout a new ``feature`` branch for you changes/ additions
3. Make fixes, changes and additions locally
4. Make a pull request
5. Someone of us reviews the pull request, gives feedback and finally merges it
6. Update to the new latest verion of the ``master`` branch

Then you are done and you can start using the new Gamma-Cat version or do further improvements in a new pull request.
It is possible and normal do work on different tasks in parallel using git branches.

*So how large should one pull request be?*

Our experience is that the smaller the better and each pull request should only handle one task, e.g. for every data entry or every bug fix make a single pull request. 
Working on a pull request for an hour or maximum a day and having a diff of around 100 lines to review is pleasant.

Pull requests that drag on for a few days or having a diff of 1000 lines of code are almost always painful and inefficient for both, the person who makes it and the reviewer.

If your pull request is related to an issue, it is recommended to name it analogeously, e.g. ``Fix bug in issue 45``. This will make things easier for us.

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
