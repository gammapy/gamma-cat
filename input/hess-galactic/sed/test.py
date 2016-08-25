"""
Test if all ECSV files can be read OK.
"""
from glob import glob
from astropy.table import Table

for filename in glob('*.ecsv'):
    print('Reading ', filename)
    table = Table.read(filename, format='ascii.ecsv')

print('All is good!')
