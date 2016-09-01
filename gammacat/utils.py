# Licensed under a 3-clause BSD style license - see LICENSE.rst
from pathlib import Path
import yaml
import numpy as np
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
