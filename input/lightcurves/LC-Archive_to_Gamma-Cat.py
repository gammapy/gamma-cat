import sys
import pyfits
import numpy as np

hdulist = pyfits.open(sys.argv[1])
# hdulist.info()
# prihdr = hdulist[0].header
# sechdr = hdulist[1].header

tbdata = hdulist[1].data

col1 = pyfits.Column(name='TIME', format='30A', array=tbdata.field(0))
col2 = pyfits.Column(name='TIME_MIN', format='30A', array=tbdata.field(1))
col3 = pyfits.Column(name='TIME_MAX', format='30A', array=tbdata.field(2))
col4 = pyfits.Column(name='FLUX', format='E', array=tbdata.field(3))
col5 = pyfits.Column(name='FLUX_ERR', format='E', array=tbdata.field(4))
col6 = pyfits.Column(name='TELESCOPE', format='30A', array=tbdata.field(11))
col7 = pyfits.Column(name='REFERENCE', format='30A', array=tbdata.field(13))

cols = pyfits.ColDefs([col1, col2,  col3, col4, col5, col6, col7])

tbhdu = pyfits.BinTableHDU.from_columns(cols)

tbhdu.writeto(sys.argv[2])
