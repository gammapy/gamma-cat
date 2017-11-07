.. include:: ../references.rst

.. Input
.. =====

We've already mentioned it in the introduction: all data entry for gamma-cat happens by editing or adding
text files in the ``input`` folder. We use file formats that are both human- and machine-readable:

* `YAML <https://en.wikipedia.org/wiki/YAML>`__ files for hierarchical data
* `ECSV <https://github.com/astropy/astropy-APEs/blob/master/APE6.rst>`__ files for tabular data

This section describes the format and content of the data entry files for gamma-cat.

All data entry is done in the folder named ``input``. It contains three sub-folders of interest:

* ``sources`` contains yaml-files with basic information about the gamma-ray sources.
* ``data`` contains the data from publications stored in ``YAML`` and ``ECSV`` files. The folder contains subfolders named by years and there subsubfolders named by reference_ids. E.g. the data from the publication with reference ``2015ApJ...802...65A`` is stored in the folder ``input/data/2015/2015ApJ...802...65A``. All these files are named corresponding to the source_id of the gamma-ray source defined in its definition file.
* ``schemas`` contains files which define the structure of the data entry files.

Now, these input files will be discussed in more detail, firstly the source definition files in `sources`:

The information (and a short description) which can be stored in such a file are defined by some keywords in `basic_source_info.schema.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/basic_source_info.schema.yaml>`__.
It starts with properties, like the ``common_name``, the ``source_id`` used in gamma-cat or the `tevcat_name` and goes on with information about experiments which investigated this source. Two important information are the ``reference_ids``, which are all ADS reference to publication which deal with this source, and the ``source_id`` from which the names in the data folder are built.
At the end of `basic_source_info.schema.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/basic_source_info.schema.yaml>`__ after the keyword ``required``, there are all of the upper information written down which have to be defined in a source definition file.

A good example to get familiar with this is e.g. `tev_000049.yaml <https://www.github.com/gammapy/gamma-cat/input/sources/tev_000029.yaml>`__ and compare it with `basic_source_info.schema.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/basic_source_info.schema.yaml>`__

The folders in /input/data/<year> contain ecsv files with measured fluxes in it, e.g. `tev-000034-sed.ecsv <https://github.com/gammapy/gamma-cat/blob/master/input/data/2010/2010ApJ...715L..49A/tev-000034-sed.ecsv>`__. Additional information like ``source_id`` or ``telescope`` are stored as meta data in the file.

Moreover, there is always a info.yaml file, e.g. `info.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/data/2010/2010ApJ...715L..49A/info.yaml>`__, and the information which can be stored in is defined in `dataset_info.schema.yaml <https://github.com/gammapy/gamma-cat/blob/master/input/schemas/dataset_info.schema.yaml>`__.

Thirdly, there are YAML files named by the ``source_id`` in which the model parameters given in the publication are stored.
Analogously, the information which can/ must be stored in such a yaml file are defined in `dataset_source_info.schemas.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/dataset_source_info.schemas.yaml>`__.

To get familiar with the data files, compare e.g. `tev_000159.yaml <https://www.github.com/gammapy/gamma-cat/input/data/2015/2015arXiv151100309G/tev_000159.yaml>`__ with `dataset_source_info.schemas.yaml <https://www.github.com/gammapy/gamma-cat/input/schemas/dataset_source_info.schemas.yaml>`__.

When you add input data you have to do two things. Firstly, you must update the data status in the corresponding ``info.yaml`` file. Secondly, you have to tell gamma-cat about the new data. This is done in `gammacat_database.yaml <https://www.github.com/gammapy/gamma-cat/input/gammacat/gammacat_database.yaml>`__ where you must add the ``reference_id`` of the publication of the added data. Gamma-cat will only contain data whose ``reference_id`` is listed in `gammacat_database.yaml <https://www.github.com/gammapy/gamma-cat/input/gammacat/gammacat_database.yaml>`__.

