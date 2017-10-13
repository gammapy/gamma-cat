.. include:: ../references.rst

Code
====

This page contains information about the whole code stored in the gamma-cat repository.

Everyone who wants to contribute to gamma-cat should read the following sections, people
who want to use gamma-cat should read `Use <https://www.gamma-cat.readthedocs.io/use/index.html>`__.

Folder structure
----------------

The repository consists of 7 folders:

* ``todo``: Some todo lists stored as .md files
* ``other_data_collections``: Data collections from different catalogs which will be/ are implemented to gamma-cat
* ``model_serialisation``: #TODO: Add description
* ``input``:  Data from which gamma-cat is built from (see section `input` below for more details)
* ``docs``: Final gamma-cat catalog and additional files produced from `input` (see chapter `Use <https://www.gamma-cat.readthedocs.io/use/index.html>`__)
* ``documentation``: Input files used to build this website. 
* ``gammacat``: #TODO: Add data

Moreover, there are some other files, but only `make.py` is of interest (see section `make.py` for more details).

Input
-----

This folder contains all data gamma-cat is built from. For contributors the three folders ``data``, ``sources`` and ``schemas`` are important.

* ``sources`` contains yaml-files with basic information about the gamma-ray sources.
* ``data`` contains the data from publications stored in yaml- and ecsv-files. The folder contains subfolders named by years and there subsubfolders named by reference_ids. E.g. the data from the publication with reference 2015ApJ...802...65A is stored in the folder input/data/2015/2015ApJ...802...65A. All these files are named corresponding to the source_id of the gamma-ray source defined in its definition file.
* ``schemas`` contains files which define the structure of the upper yaml-files.

Now, these input files will be discussed in more detail, firstly the source definition files in `sources`:

The information (and a short description) which can be stored in such a file are defined by some keywords in `basic_source_info.schema.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/basic_source_info.schema.yaml>`__.
It starts with properties, like the `common_name`, the `source_id` used in gamma-cat or the `tevcat_name` and goes on with information about `experiments which investigated this source. Two important information are the `reference_ids`, which are all ADS reference to publication which deal with this source, and the `source_id` from which the names in the data folder are built.
At the end of `basic_source_info.schema.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/basic_source_info.schema.yaml>`__ after the keyword `required`, there are all of the upper information written down which have to be defined in a source definition file.

A good example to get familiar with this is e.g. `tev_000049.yaml <https://www.github.com/gammapy/gamma-cat/input/sources/tev_000029.yaml>`__ and compare it with `basic_source_info.schema.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/basic_source_info.schema.yaml>`__

The folders in /input/data/<year> contain ecsv files with measured fluxes in it, e.g. `tev-000034-sed.ecsv <https://github.com/gammapy/gamma-cat/blob/master/input/data/2010/2010ApJ...715L..49A/tev-000034-sed.ecsv>`__. Additional information like `source_id` or `telescope` are stored as meta data in the file. 

Moreover, there is always a info.yaml file, e.g. `info.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/data/2010/2010ApJ...715L..49A/info.yaml>`__, and the information which can be stored in is defined in `dataset_info.schema.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/schemas/dataset_info.schema.yaml>`__. 

Thirdly, there are yaml files named by the `source_id` in which the model parameters given in the publication are stored.
Analogeously, the information which can/ must be stored in such a yaml file are defined in `dataset_source_info.schemas.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/dataset_source_info.schemas.yaml>`__.

To get familiar with the data files, compare e.g. `tev_000159.yaml <https://www.github.com/gammapy/gamma-cat/input/data/2015/2015arXiv151100309G/tev_000159.yaml>`__ with `dataset_source_info.schemas.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/dataset_source_info.schemas.yaml>`__. 

When you add input data you have to do two things. Firstly, you must update the data status in the corresponding info.yaml file. Secondly, you have to tell gamma-cat about the new data. This is done in `gammacat_database.yaml <https://www.github.com/gammapy/gamma-cat/input/gammacat/gammacat_database.yaml>`__ where you must add the reference_id of the publication of the added data. Gamma-cat will only contain data whose reference_id is listet in `gammacat_database.yaml <https://www.github.com/gammapy/gamma-cat/input/gammacat/gammacat_database.yaml>`__.

make.py
-------

There is a command line interface to run the gamma-cat scripts,
the ``make.py`` file in the top-level folder.

To see the available sub-commands and options::

    $ ./make.py --help

To run the full pipeline, i.e. generate all output files and run all checks::

    $ ./make.py all

After adding/ changing data in the input folder, one should always execute::

	$ ./make.py checks

which checks the format/ structure of the input files.

gammacat package
----------------

The ``make.py`` command line interface just imports and executes functions and classes
from the ``gammacat`` Python package (i.e. the ``.py`` files in the folder with name ``gammacat``).

We list the modules in ``gammacat`` and comment on the code organisation.

The following are more basic modules:

* ``utils.py`` has some helper utility functions (e.g. for JSON / YAML / ECSV I/O)
* ``modeling.py`` has a ``Parameter`` and ``ParameterList`` class to help process
  input spatial and spectral source models from the YAML files.
* ``info.py`` has some helpers for versions, filenames, ...
* ``sed.py`` has a class to process and validate the spectral energy distributions (SEDs)
  in the input folder. The SEDs in the output folder can be read directly with
  ``gammapy.spectrum.FluxPoints``.
* ``lightcurve.py`` has a class to process and validate the lightcurves in the input folder.
  The lightcurves in the output folder can be read directly with ``gammapy.time.LightCurve``.

In additions there are classes in ``gammapy.catalog.gammacat`` that are used in the ``gammacat``
scripts to process the data: ``GammaCatResource``, ``GammaCatResourceIndex``, ``GammaCatDatasetCollection``.

Then there is a hierarchy of higher-level modules (that import from the basic modules
and modules representing lower-level steps in the processing pipeline):

* ``input.py`` has classes to read / clean up / process the data in the ``input`` folder.
* ``collection.py`` has classes to create the files in the ``output`` folder
  (only the dataset files and index files, not the catalog files).
* ``cat.py`` is the code to create the catalog files
* ``checks.py`` is the code to run checks.
  At the moment the methods there just dispatch to methods called ``validate`` or ``check``
  in lower-level modules (such as ``gammacat.input``), and the actual checks are thus
  scattered throughout the ``gammacat`` modules. There's also checks on data content in
  ``gammacat/tests`` (which is probably a bad idea, but pytest is convenient to have asserts)

Tests
-----

There is a folder ``gammacat/tests`` with some unit tests for the code in the ``gammacat`` package,
that can be executed via ``python -m pytest gammacat/tests``

We don't have the relation quite figure out, what goes where:

* ``gammacat/tests``
* ``gammapy/catalog/tests/test_gammacat.py``
* The various check / validate methods throughout ``gammacat`` and executed via ``./make.py check``.


Tools
-----

The following tool is helpful to lint YAML files:

- `yamllint`_

TODO: it's too picky, showing errors for things that are OK.
Figure out how to make it less picky and document that here.

Website build
-------------

The `gamma-cat` website is a static website generated by Python and Sphinx.

We have a `Sphinx test page <tests/index.html>`__ where we can try out things locally
and check if they also work on ReadTheDocs. It's an orphan page, i.e. doesn't show up
for normal users.

We use several Sphinx extensions, and also have our own in `gammacat/sphinx/exts`.

More info soon ... for now this is just a link collection:

* ``sphinxcontrib.rawfiles``
    * Useful example. Not very useful directly, because can't control destination of the copy!?
    * Code: https://bitbucket.org/birkenfeld/sphinx-contrib/src/master/rawfiles/sphinxcontrib/rawfiles.py
    * PyPI: https://pypi.python.org/pypi/sphinxcontrib-rawfiles/
    * Although for now, this is working for what I need: http://www.sphinx-doc.org/en/1.5.1/config.html#confval-html_extra_path
* Looks very useful! http://sphinxcontribdatatemplates.readthedocs.io/en/latest/
* A good Sphinx table extension would be useful: https://github.com/sphinx-doc/sphinx/issues/786
* Not sure if this is useful! https://pythonhosted.org/sphinxcontrib-restbuilder/
* Maybe: https://pypi.python.org/pypi/sphinxcontrib-jsoncall
* Looks interesting, probably not useful here: https://jsdoc-toolkit-rst-template.readthedocs.io/en/latest/
