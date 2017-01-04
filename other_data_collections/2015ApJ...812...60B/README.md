# AGN spectra from Biteau & Williams (2015)

This folder contains spectral data for AGN from Biteau & Williams (2015)

* Paper on ADS: [2015ApJ...812...60B](https://ui.adsabs.harvard.edu/?#abs/2015ApJ...812...60B)
* Obtained by Jonathan Biteau on Jan 4, 2016 via email with the permission to add it to gamma-cat.

> I'd be happy if this dataset was accessible from your platform.
> Please let me know if you have any question on the attached datafiles,
> which list all the spectral points included in our study in two slightly different formats.

The two data files are:
* `BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv`
* `BiteauWilliams2015_AllData_TeVCat_v2016_12_20.ecsv`

It looks like the content of the two files is basically the same:
* 737 rows, i.e. spectral points
* Extra columns `ra` and `dec` in `ASDC` irrelevant for us
* Extra columns `freq_err` and `ul_flag` in `ASDC` file never filled

These are the files Janathan sent, and Christoph Deil
* wrote an ECSV header
* fixed some data issues (see git commits for that file)

From the `biteau.py` script, we're adding the data from the `ASDC` file to `gamma-cat`.
