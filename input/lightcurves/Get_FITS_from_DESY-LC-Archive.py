import sys
import DESYLCArchiveToECSV

## This is a Python-script to dump the FITS Lightcurves from the DESY LC Archive to ECSV files
## URL: https://astro.desy.de/gamma_astronomy/magic/projects/light_curve_archive/index_eng.html
## This Script needs DESYLCArchiveToECSV.py
## links and source names are stored in a dictionary
## links can be added if the DESY LC Archive gets extended
## source names can be easily edited and changed to tev-id for example

url = {
    "tev-000138":"http://www-zeuthen.desy.de/multi-messenger/GammaRayData/1es1959+650_combined_lc_v0.2.fits", 
    "tev-000049":"http://www-zeuthen.desy.de/multi-messenger/GammaRayData/mrk421_combined_lc_v0.2.fits", 
    "tev-000091":"http://www-zeuthen.desy.de/multi-messenger/GammaRayData/mrk501_combined_lc_v0.2.fits"
}

for key, val in url.items():
	DESYLCArchiveToECSV.main(val, key)
