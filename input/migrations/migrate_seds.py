"""
Migrate SED column names to new format.

http://gamma-astro-data-formats.readthedocs.io/en/latest/results/flux_points/index.html
"""
import warnings
from collections import OrderedDict
from pathlib import Path
from astropy.table import Table

WRITE_OUTPUT = True


def migrate_sed(path):
    print('Migrating SED for', path)
    table = Table.read(str(path), format='ascii.ecsv')

    col_renames = OrderedDict(
        energy='e_ref',
        energy_min='e_min',
        energy_max='e_max',
        flux='dnde',
        flux_err='dnde_err',
        flux_lo='dnde_errn',
        flux_hi='dnde_errp',
    )
    for old_name, new_name in col_renames.items():
        if old_name in table.colnames:
            table.rename_column(old_name, new_name)

    if 'flux_min' in table.colnames:
        table['dnde_errn'] = table['dnde'] - table['flux_min']
        del table['flux_min']
    if 'flux_max' in table.colnames:
        table['dnde_errp'] = table['flux_max'] - table['dnde']
        del table['flux_max']

    expected_names = {
        'e_ref', 'e_min', 'e_max',
        'dnde', 'dnde_err', 'dnde_errn', 'dnde_errp',
        'excess', 'significance',
    }
    unexpected_colnames = set(table.colnames) - expected_names
    if unexpected_colnames:
        print('ERROR: you need to handle columns: ', unexpected_colnames)
        exit()

    if WRITE_OUTPUT:
        # See https://github.com/astropy/astropy/issues/5438
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            table.write(str(path), format='ascii.ecsv')


for path in Path('input/papers').glob('*/*/*.ecsv'):
    migrate_sed(path)
