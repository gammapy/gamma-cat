"""
Clean up `tc_dump.txt` to obtain `tevcat.ecsv`
"""
from collections import OrderedDict

from astropy.coordinates import Angle
from astropy.table import Table

# Parse text file into a table
rows = []
for line in open('tc_dump.txt').readlines():
    line = line.replace('\t', '    ')
    source_name = line[:30].strip()
    ra_str = line[30:50].strip()
    dec_str = line[50:70].strip()
    url = line[70:].strip()
    source_id = int(url.split('=')[-1])
    rows.append([source_name, source_id, ra_str, dec_str])

meta = OrderedDict()
meta['catalog_name'] = 'TeVCat'
meta['date'] = 'June 11, 2016'
meta['authors'] = 'Scott Wakely, Deirdre Horan'
meta['url'] = 'http://tevcat.uchicago.edu/'

names = ['source_name', 'source_id', 'ra_str', 'dec_str']
table = Table(rows=rows, names=names, meta=meta)

table['source_name'].description = 'Source canonical name'

table['source_id'].description = 'Source identification number'

table['ra'] = Angle(table['ra_str'], unit='hourangle').deg
table['ra'].unit = 'deg'
table['ra'].format = '%.5f'
table['ra'].description = 'Right Ascension (J2000)'
del table['ra_str']

table['dec'] = Angle(table['dec_str'], unit='deg').deg
table['dec'].unit = 'deg'
table['dec'].format = '%.5f'
table['dec'].description = 'Declination (J2000)'
del table['dec_str']

filename = 'tevcat.ecsv'
print('Writing', filename)
table.write(filename, format='ascii.ecsv')
