"""
Migrate SED column names to new format.

http://gamma-astro-data-formats.readthedocs.io/en/latest/results/flux_points/index.html
"""
import warnings
from collections import OrderedDict
from pathlib import Path
from astropy.table import Table


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

    expected_names = {
        'e_ref', 'e_min', 'e_max',
        'dnde', 'dnde_err', 'dnde_errn', 'dnde_errp',
        'sigma', 'excess',
    }
    unexpected_colnames = set(table.colnames) - expected_names
    if unexpected_colnames:
        print('ERROR: you need to handle columns: ', unexpected_colnames)
        exit()

    # See https://github.com/astropy/astropy/issues/5438
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        table.write(str(path), format='ascii.ecsv')

"""
- `energy` - Energy in `TeV`
- `energy_min` - Energy measurement bin left edge in `TeV`
- `energy_max` - Energy measurement bin right edge in `TeV`
- `energy_lo` - Sometimes given instead of `energy_min`, where `energy_min = energy - energy_lo`
- `energy_hi` - Sometimes given instead of `energy_max`, where `energy_max = energy + energy_hi`

- `flux` - Differential flux in `cm-2 s-1 TeV-1`
- `flux_err` - Statistical error on `flux` (if symmetric error is given)
- `flux_hi` - Statistical error on `flux`
- `flux_lo` - Statistical error on `flux`
"""

for path in Path('input/papers').glob('*/*/*.ecsv'):
    migrate_sed(path)
