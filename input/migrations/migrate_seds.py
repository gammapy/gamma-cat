"""
Migrate SED column names to new format.

http://gamma-astro-data-formats.readthedocs.io/en/latest/results/flux_points/index.html

In the end, we didn't use this script:
https://github.com/gammapy/gamma-cat/pull/31
But I'm keeping it here as an example for potential future migrations.
"""
import warnings
from collections import OrderedDict
from pathlib import Path
from astropy.table import Table

WRITE_OUTPUT = True


def migrate_sed(path):
    print('Migrating SED for', path)
    table = Table.read(str(path), format='ascii.ecsv')

    migrate_sed_data(table)
    migrate_sed_header(table)

    if WRITE_OUTPUT:
        # See https://github.com/astropy/astropy/issues/5438
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            table.write(str(path), format='ascii.ecsv')


def migrate_sed_data(table):
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
        'energy_lo', 'energy_hi',
        'dnde', 'dnde_err', 'dnde_errn', 'dnde_errp',
        'excess', 'significance',
    }
    unexpected_colnames = set(table.colnames) - expected_names
    if unexpected_colnames:
        print('ERROR: you need to handle columns: ', unexpected_colnames)
        exit()

    return table


def migrate_sed_header(table):
    table.meta['sed_type'] = 'diff_flux_points'


def migrate_all_seds():
    for path in Path('input/data').glob('*/*/*.ecsv'):
        migrate_sed(path)


if __name__ == '__main__':
    migrate_all_seds()
