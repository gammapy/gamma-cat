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


def rawgit_url(filename, location='master', mode='production'):
    """
    Construct the rawgit URL to download directly files from the repo.

    More info:
    * https://rawgit.com/
    * https://github.com/rgrove/rawgit/wiki/Frequently-Asked-Questions

    URL is

    Parameters
    ----------
    filename : str
        Filename in the repo.
    location : str
        Name of a branch, tag or commit.
    mode : {'development', 'production'}
        Where to fetch the files from

    Examples
    --------
    >>> filename = 'papers/2006/2006A%2526A...456..245A/tev-000065.ecsv'
    >>> rawgit_url(filename, mode='production')
    TODO
    >>> rawgit_url(filename, mode='development')
    TODO
    """
    if mode == 'development':
        base_url = 'https://rawgit.com/gammapy/gamma-cat'
    elif mode == 'production':
        base_url = 'https://cdn.rawgit.com/gammapy/gamma-cat'

    url = '/'.join([base_url, location, filename])

    return url