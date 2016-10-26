import sys
import numpy as np
from astropy.table import Table, Column
from astropy.units import cds


## open file


tab = Table.read(sys.argv[1], format='fits')


## renaming column-names to SED format


tab.rename_column('mjd_mid_exp', 'TIME')
tab.rename_column('mjd_start', 'TIME_MIN')
tab.rename_column('mjd_end', 'TIME_MAX')
tab.rename_column('integral_flux', 'FLUX')
tab.rename_column('sigma_int_flux_stat', 'FLUX_ERR')
tab.rename_column('experiment', 'TELESCOPE')
tab.rename_column('reference', 'PAPER')


## deleting unused columns


del tab['sigma_int_flux_sys']
del tab['alpha']
del tab['sigma_alpha_stat']
del tab['sigma_alpha_sys']
del tab['e_thr']
del tab['e_cut']
del tab['duration']
del tab['fflag']


## setting formats


tab.replace_column('TIME', tab['TIME'].astype(float))
tab.replace_column('TIME_MIN', tab['TIME_MIN'].astype(float))
tab.replace_column('TIME_MAX', tab['TIME_MAX'].astype(float))


## setting units


tab['TIME'].unit = tab['TIME_MAX'].unit = tab['TIME_MIN'].unit = cds.MJD
tab['FLUX'].unit = tab['FLUX_ERR'].unit = cds.Crab


## write file


tab.write(sys.argv[2], format='ascii.ecsv')


# hdulist = pyfits.open(sys.argv[1])
# hdulist.info()
# prihdr = hdulist[0].header
# sechdr = hdulist[1].header

# tbdata = hdulist[1].data

# print tbdata.field(0)

# data_rows = [(tbdata.field(0)), (tbdata.field(1)), (tbdata.field(2)), (tbdata.field(4)), (tbdata.field(11)), (tbdata.field(13)))]

# t = Table(rows=data-rows, names=('TIME', 'TIME_MIN', 'TIME_MAX', 'FLUX', 'FLUX_ERR', 'TELESCOPE', 'REFERENCE'), dtype=('f8', 'f8', 'f8', 'f8', 'f8', 'S30', 'S30'))

# t = Table()

# t['TIME'] = Column([(tbdata.field(0)], unit='MJD', dtype='float32')
# t['TIME_MIN'] = Column((tbdata.field(1), unit='MJD', dtype='float32')
# t['TIME_MAX'] = Column((tbdata.field(2), unit='MJD', dtype='float32')
# t['FLUX'] = Column((tbdata.field(3), unit='Crab', dtype='float32')
# t['FLUX_ERR'] = Column((tbdata.field(4), unit='Crab', dtype='float32')
# t['TELESCOPE'] = Column((tbdata.field(11), unit='', dtype='string')
# t['REFERENCE'] = Column((tbdata.field(13), unit='', dtype='string')

# fh = StringIO()
# t.write(fh, format='ascii.ecsv')
# table_string = fh.getvalue()
# print(table_string)

# col1 = pyfits.Column(name='TIME', format='30A', array=tbdata.field(0))
# col2 = pyfits.Column(name='TIME_MIN', format='30A', array=tbdata.field(1))
# col3 = pyfits.Column(name='TIME_MAX', format='30A', array=tbdata.field(2))
# col4 = pyfits.Column(name='FLUX', format='E', array=tbdata.field(3))
# col5 = pyfits.Column(name='FLUX_ERR', format='E', array=tbdata.field(4))
# col6 = pyfits.Column(name='TELESCOPE', format='30A', array=tbdata.field(11))
# col7 = pyfits.Column(name='REFERENCE', format='30A', array=tbdata.field(13))

# cols = pyfits.ColDefs([col1, col2,  col3, col4, col5, col6, col7])

# tbhdu = pyfits.BinTableHDU.from_columns(cols)

# tbhdu.writeto(sys.argv[2])
