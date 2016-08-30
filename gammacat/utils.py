from pathlib import Path
import json
import yaml
import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord

MISSING_VAL = dict(
    integer=-999,
    number=np.nan,
    string='',
    array='',
)


def load_yaml(path):
    """Helper function to load data from a YAML file."""
    path = Path(path)
    with path.open() as fh:
        data = yaml.safe_load(fh)
    return data


def make_table(row_data, column_def):
    """Helper function to make an Astropy Table from row data.

    The main reason this is needed is that it's hard to construct
    a table with missing data.
    """
    pass


def print_simbad_pos(name):
    """Print YAML snipped for SIMBAD position.
    """
    pos = SkyCoord.from_name(name)
    template = (
        'pos:\n'
        '  simbad_id: {name}\n'
        '  ra: {pos.ra.deg}\n'
        '  dec: {pos.dec.deg}\n'
    )
    s = template.format(name=name, pos=pos)
    print(s)
