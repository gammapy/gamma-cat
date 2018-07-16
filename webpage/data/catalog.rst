.. include:: ../references.rst

Source catalog
--------------

The source catalog is available as a single table in a single file.
It contains only part of the data available in gamma-cat.

* `gammacat.fits.gz <../output/gammacat.fits.gz>`__ -- Main version of the source catalog (in FITS format)
* `gammacat.ecsv <../output/gammacat.ecsv>`__ -- Partial source catalog (in ECSV format)
* `gammacat.yaml <../output/gammacat.yaml>`__ -- Partial source catalog (in YAML format)

Why multiple formats?

* FITS is the main format for the catalog we release.
  It supports vector columns, which we use for spectral points.
* The ECSV and YAML variant are more for us working on gamma-cat,
  to have a text-based, version control friendly format where it's
  easy to see which changes occurred from one version to the next.

We recommend to have a look at `gamma_cat_columns <https://github.com/gammapy/gamma-cat/blob/master/input/gamma_cat_config/gamma_cat_columns.yaml>`__ in which all columns of the catalog are defined together with additional information, e.g. description and datatype of the entry.
Moreover, in `gamma_cat_dataset <https://github.com/gammapy/gamma-cat/blob/master/input/gammacat/gamma_cat_dataset.yaml>`__ for each source the reference_id of the data in the catalog is given (more precicely, this file tells the python scripts which references are used to create the catalog).
