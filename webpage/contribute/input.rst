.. include:: ../references.rst

Input
=====

We've already mentioned it in the introduction: all data entry for gamma-cat happens by editing or adding
text files in the ``input`` folder. We use file formats that are both human- and machine-readable:

* `YAML <https://en.wikipedia.org/wiki/YAML>`__ files for hierarchical data
* `ECSV <https://github.com/astropy/astropy-APEs/blob/master/APE6.rst>`__ files for tabular data

This section describes the format and content of the data entry files for gamma-cat.

All data entry is done in the folder named ``input``. It contains three sub-folders of interest:

* ``sources`` contains yaml-files with basic information about the gamma-ray sources.
* ``data`` contains the data from publications stored in ``YAML`` and ``ECSV`` files. The folder contains subfolders named by years and there subsubfolders named by reference_ids. E.g. the data from the publication with reference ``2015ApJ...802...65A`` is stored in the folder ``input/data/2015/2015ApJ...802...65A``. All these files are named corresponding to the source_id of the gamma-ray source defined in its definition file.
* ``schemas`` contains files which define the structure of the data entry files and descriptions of the properties in the data files.

Now, these input files will be discussed in more detail, firstly the source definition files in `sources`:

The information (and a short description) which can be stored in such a file are defined by some keywords in `basic_source_info.schema.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/schemas/basic_source_info.schema.yaml>`__.
It starts with properties, like the ``common_name``, the ``source_id`` used in gamma-cat or the `tevcat_name` and goes on with information about experiments which investigated this source. Two important information are the ``reference_ids``, which are all ADS reference to publication which deal with this source, and the ``source_id`` from which the names in the data folder are built.
At the end of `basic_source_info.schema.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/schemas/basic_source_info.schema.yaml>`__ after the keyword ``required``, there are all of the upper information written down which have to be defined in a source definition file.

A good example to get familiar with this is e.g. `tev_000049.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/sources/tev-000049.yaml>`__ and compare it with `basic_source_info.schema.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/schemas/basic_source_info.schema.yaml>`__

The folders in /input/data/<year>/<reference> contain ecsv files with measured data in it, e.g. `tev-000034-sed.ecsv <https://github.com/gammapy/gamma-cat/tree/master/input/data/2010/2010ApJ...715L..49A/tev-000034-sed.ecsv>`__, yaml files with model parameters, e.g. `tev-000034.yaml <https://github.com/gammapy/gamma-cat/tree/master/input/data/2010/2010ApJ...715L..49A/tev-000034.yaml>`__, and finally a info yaml file in which all data corresponding to the publication are summarised, e.g. `info.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/data/2010/2010ApJ...715L..49A/info.yaml>`__.

The escv files can be either the measurement of spectral fluxes or of lightcurves. Information about the units of the data and additional information like ``source_id`` or ``telescope`` are stored as meta data in the header of the file.
The naming convention is ``tev-<source_id>-sed.ecsv`` and ``tev-<source_id>-lc.ecsv``, respectively.

The YAML files contain the model parameters given in the publication and are named within gamma-cat as ``dataset-files``.
The information which can/ has to be stored in a yaml file are defined in `dataset_source_info.schemas.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/schemas/dataset_source_info.schema.yaml>`__.

The info.yaml files give an overview about all stored data which is related to the publication and its layout is defined in  `dataset_info.schema.yaml <https://github.com/gammapy/gamma-cat/tree/master/input/schemas/dataset_info.schema.yaml>`__. One important property in a info file is ``data-entry`` with its subinformation ``status``, ``reviewed`` and ``notes``.

Add/ Change data:
-----------------

When you add or change input data you have to do three things. Firstly, you must add or change the data, secondly, you must update the data status in the corresponding ``info.yaml`` file and finally, you have to tell gamma-cat that there is new data. This is done in `gamma_cat_dataset.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/gammacat/gamma_cat_dataset.yaml>`__ where you must add the ``reference_id`` of the publication of the added data. Gamma-cat will only contain data whose ``reference_id`` is listed in `gamma_cat_dataset.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/gammacat/gamma_cat_dataset.yaml>`__.
