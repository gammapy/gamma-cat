.. Source catalog
.. --------------

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