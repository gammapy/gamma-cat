# tevcat

## What is this?

TeVCat is here:

* http://tevcat.uchicago.edu/
* http://tevcat2.uchicago.edu/

It isn't openly available for download.

The `tc_dump.txt` file with the columns `source_name`, `ra`, `dec`
and `url` (which contains the TeVCat 1 integer source ID) was
obtained on June 11, 2016 via email from Scott Wakely.

Having those integer source IDs is needed to cross-link this
catalog and gamma-sky.net to TeVCat.

## Data and scripts

The `tevcat.py` script cleans up `tc_dump.txt` to obtain `tevcat.ecsv`.
