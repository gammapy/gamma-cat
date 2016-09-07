"""
Clean up `tc_dump.txt` to obtain `tevcat.ecsv`
"""
from collections import OrderedDict
from pprint import pprint
from pathlib import Path
import numpy as np
from astropy.io import ascii
from astropy.table import Table
from astropy.coordinates import Angle

filename = 'tgevcat.csv'
filename2 = 'tgevcat-temp.csv'

# Remove unicode characters -- they only cause problems
print('Reading ', filename)
text = Path(filename).read_text()
for a, b in [('\u2013', '-'), ('\u2019', "'")]:
    text = text.replace(a, b)

print('Writing ', filename2)
Path(filename2).write_text(text)

# Read CSV table
print('Reading ', filename2)
t1 = ascii.read(
    table=filename2,
    format='csv',
    quotechar='"',
    fast_reader=False,
    fill_values=[('-', '')],
)
# t1.info('stats')
# t1.show_in_browser(jsviewer=True)

print('Removing ', filename2)
Path(filename2).unlink()

# Make new table and fill with good column names,
# units and values converted to numbers where appropriate

meta = OrderedDict()
meta['catalog_name'] = 'TeGeV'
meta['version'] = '2'
meta['date'] = 'July 2015'
meta['authors'] = 'Alessandro Carosi, Fabrizio Lucarelli, Angelo Antonelli'
meta['url'] = 'http://www.asdc.asi.it/tgevcat/'

t2 = Table(meta=meta)

t2['Source_ID'] = t1['id']
t2['Source_ID'].description = 'Source ID'

t2['Source_Name'] = t1['TEV NAME']
t2['Source_Name'].description = 'Source name'

t2['Other_Names'] = t1['OTHER NAMES']
t2['Other_Names'].description = 'Other common names for the source (separated by "/" if multiple)'

t2['CLASS'] = t1['TYPE']
t2['CLASS'].description = 'Source class (separated by "/" if multiple)'

t2['RA'] = Angle(t1['RA (J2000)'], unit='hourangle').deg
t2['RA'].unit = 'deg'
t2['RA'].description = 'Right Ascension (J2000)'

t2['DEC'] = Angle(t1['Dec (J2000)'], unit='deg').deg
t2['DEC'].unit = 'deg'
t2['DEC'].description = 'Declination (J2000)'

t2['GLON'] = t1['LII(degrees)']
t2['GLON'].unit = 'deg'
t2['GLON'].description = 'Galactic longitude'

t2['GLAT'] = t1['BII(degrees)']
t2['GLAT'].unit = 'deg'
t2['GLAT'].description = 'Galactic latitude'

t2['RA_Err_Stat'] = [Angle(float(_) / 3600., unit='hourangle').deg for _ in t1['ErrRaStat[s]']]
t2['RA_Err_Stat'].unit = 'deg'
t2['RA_Err_Stat'].description = 'Statistical error on RA'

t2['RA_Err_Sys'] = [Angle(float(_) / 3600., unit='hourangle').deg for _ in t1['ErrRaSys[s]']]
t2['RA_Err_Sys'].unit = 'deg'
t2['RA_Err_Sys'].description = 'Systematic error on RA'

t2['DEC_Err_Stat'] = [Angle(float(_), unit='arcsec').deg for _ in t1['ErrDecStat[arcsec]']]
t2['DEC_Err_Stat'].unit = 'deg'
t2['DEC_Err_Stat'].description = 'Statistical error on DEC'

t2['DEC_Err_Sys'] = [Angle(float(_), unit='arcsec').deg for _ in t1['ErrDecSys[arcsec]']]
t2['DEC_Err_Sys'].unit = 'deg'
t2['DEC_Err_Sys'].description = 'Systematic error on DEC'

# Note: missing values can't be stored in bool columns
# Here we fill them with `False`
# TODO: Maybe we should stick with a string column and fill "N/A" or "Unkown"
t2['Is_Extended'] = [True if str(_).strip() == 'YES' else False for _ in t1['EXTENDED']]
t2['Is_Extended'].description = 'Is the source extended?'
# pprint(list(zip(t1['EXTENDED'], t2['Is_Extended'])))

t2['Semimajor'] = [float(_) for _ in t1['SEMIMAJOR[deg]']]
t2['Semimajor'].unit = 'deg'
t2['Semimajor'].description = 'Extension along semi-major axis'

t2['Semimajor_Err'] = [float(_) for _ in t1['ERRMAJOR[deg]']]
t2['Semimajor_Err'].unit = 'deg'
t2['Semimajor_Err'].description = 'Error on Semimajor'

t2['Semiminor'] = [float(_) for _ in t1['SEMIMINOR[deg]']]
t2['Semiminor'].unit = 'deg'
t2['Semiminor'].description = 'Extension along semi-minor axis'

t2['Semiminor_Err'] = [float(_) for _ in t1['ERRMINOR[deg]']]
t2['Semiminor_Err'].unit = 'deg'
t2['Semiminor_Err'].description = 'Error on Semiminor'

t2['Rotation_Angle'] = [float(_) for _ in t1['ROTATION ANGLE[deg]']]
t2['Rotation_Angle'].unit = 'deg'
# TODO: check and document orientation of rotation angle
t2['Rotation_Angle'].description = 'Rotation angle (TODO: orientation unclear)'

t2['Flux_Diff'] = [float(_) for _ in t1['DIFF. FLUX NORMALIZATION[x TeV^-1 cm^-2 s^-1]']]
t2['Flux_Diff'].unit = 'TeV^-1 cm^-2 s^-1'
# TODO: check and document energy at which flux is quoted
t2['Flux_Diff'].description = 'Differential flux (TODO: at 1 TeV?)'

t2['Flux_Diff_Err_Stat'] = [float(_) for _ in t1['DIFF. FLUX NORMALIZATION ERRSTAT[x TeV^-1 cm^-2 s^-1]']]
t2['Flux_Diff_Err_Stat'].unit = 'TeV^-1 cm^-2 s^-1'
t2['Flux_Diff_Err_Stat'].description = 'Statistical error on Flux_Diff'

t2['Flux_Diff_Err_Sys'] = [float(_) for _ in t1['DIFF. FLUX NORMALIZATION ERRSYS[x TeV^-1 cm^-2 s^-1]']]
t2['Flux_Diff_Err_Sys'].unit = 'TeV^-1 cm^-2 s^-1'
t2['Flux_Diff_Err_Sys'].description = 'Systematic error on Flux_Diff'

t2['Spectral_Index'] = [float(_) for _ in t1['SPECTRAL SLOPE']]
t2['Spectral_Index'].description = 'Spectral index'

t2['Spectral_Index_Err_Stat'] = [float(_) for _ in t1['ERRSLOPESTAT']]
t2['Spectral_Index_Err_Stat'].description = 'Statistical error on Spectral_Index'

t2['Spectral_Index_Err_Sys'] = [float(_) for _ in t1['ERRSLOPESYS']]
t2['Spectral_Index_Err_Sys'].description = 'Systematic error on Spectral_Index'

t2['Flux_Int'] = [1e-12 * float(_) for _ in t1['INTEGRAL FLUX']]
t2['Flux_Int'].unit = 'cm^-2 s^-1'
# TODO: check and document energy above which flux is quoted
t2['Flux_Int'].description = 'Integral flux (TODO: above which energy?)'

t2['Flux_Int_Err_Stat'] = [1e-12 * float(_) for _ in t1['ErrFluxStat[x 10^-12 cm^-2 s^-1]']]
t2['Flux_Int_Err_Stat'].unit = 'cm^-2 s^-1'
t2['Flux_Int_Err_Stat'].description = 'Statistical error on Flux_Int'

t2['Flux_Int_Err_Sys'] = [1e-12 * float(_) for _ in t1['ErrFluxSys[x 10^-12 cm^-2 s^-1]']]
t2['Flux_Int_Err_Sys'].unit = 'cm^-2 s^-1'
t2['Flux_Int_Err_Sys'].description = 'Systematic error on Flux_Int'

# TODO: add 'OTHER SPECTRAL COMPONENTS'

# TODO: re-compute this from other flux columns using Gammapy for consistency.
t2['Flux_Crab'] = [float(_) for _ in t1['Flux in CU[%]']]
t2['Flux_Crab'].unit = ''
t2['Flux_Crab'].description = 'Flux in Crab units'

# TODO: add 'THR ENERGY [GeV]'
# TODO: add 'MIN ZENITH[deg]', 'MAX ZENITH[deg]', 'MEAN ZENITH[deg]'

# TODO: for now this is a float column, because there's values like '<0.66'
# We should split parse this into float columns
# t2['Distance'] = [float(_) for _ in t1['DISTANCE[kPc]']]
# t2['Distance'].unit = 'kpc'
t2['Distance'] = t1['DISTANCE[kPc]']
t2['Distance'].description = 'Distance to astrophysical source from Earth'

# TODO: what is the difference between the distance measures?
# t2['Distance2'] = [float(_) for _ in t1['Distance']]
# t2['Distance2'].unit = 'kpc'
t2['Distance2'] = t1['Distance']
t2['Distance2'].description = 'Distance to astrophysical source from Earth (TODO: difference to Distance?)'

t2['Discoverer'] = t1['Discoverer']
t2['Discoverer'].description = 'Discoverer'

t2['Observatory'] = t1['Observatory']
t2['Observatory'].description = 'Observatory'
# TODO: add 'START TIME[MJD]', 'END OBSERVATION[MJD]', 'EXPOSURE TIME[ksec]'

# TODO: add 'POS. ERROR CIRCLE[deg]'
# TODO: add 'Diff. Flux. Norm. Energy[TeV]'

t2['Reference'] = t1['REFERENCE']
t2['Reference'].description = 'Reference'

t2['Comments'] = t1['COMMENTS']
t2['Comments'].description = 'Comments'

# import IPython; IPython.embed()

# t2.info()
# t2.info('stats')
# t2.show_in_browser(jsviewer=True)
# import IPython; IPython.embed()

filename = 'tgevcat.ecsv'
print('Writing', filename)
t2.write(filename, format='ascii.ecsv')
