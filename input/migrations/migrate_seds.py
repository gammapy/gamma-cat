"""
Migrate SED column names to new format.

http://gamma-astro-data-formats.readthedocs.io/en/latest/results/flux_points/index.html
"""
from pathlib import Path


def migrate_sed(path):
    print('Migrating SED for', path)


for path in Path('input/papers').glob('*/*/*.ecsv'):
    migrate_sed(path)
