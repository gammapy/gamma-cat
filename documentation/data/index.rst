.. include:: ../references.rst

.. _data:

Data
====

Gamma-cat sources
-----------------

.. include:: src_list.rst

.. _data-overview:

Overview
--------

With gamma-cat, we provide two data products:

1. A source catalog
2. The full data collection

The following sections describe how to download them.

For now the latest version of the files is here: https://github.com/gammapy/gamma-cat/tree/master/docs/data

TODO: set up an easier way to download the files, directly from this page.

.. _data-cat:

Source catalog
--------------

The source catalog is available as a single table in a single file.
It contains only part of the data available in gamma-cat.

* ``gammacat.fits.gz`` -- Main version of the source catalog (in FITS format)
* ``gammacat.ecsv`` -- Partial source catalog (in ECSV format)
* ``gammacat.yaml`` -- Partial source catalog (in YAML format)

Why multiple formats?

* FITS is the main format for the catalog we release.
  It supports vector columns, which we use for spectral points.
* The ECSV and YAML variant are more for us working on gamma-cat,
  to have a text-based, version control friendly format where it's
  easy to see which changes occurred from one version to the next.

.. _data-set:

Data collection
---------------

The full data collection is available as a collection of files
in ECSV and JSON format.

* ``gammacat-datasets.json`` -- Main index file, with links to all other data files
* ``gammacat-sources.json`` -- TODO: remove?
* TODO: add "bundled" version of the files, with all information put in a single large JSON
  (or alternatively, equivalently HDF5) file.
