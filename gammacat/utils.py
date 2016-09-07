# Licensed under a 3-clause BSD style license - see LICENSE.rst
from collections import OrderedDict
import logging
import json
from pathlib import Path
import yaml
import numpy as np
from astropy.coordinates import SkyCoord

log = logging.getLogger()

MISSING_VAL = OrderedDict(
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


def load_json(path):
    """Helper function to load data from a JSON file."""
    path = Path(path)
    with path.open() as fh:
        data = json.load(fh, object_pairs_hook=OrderedDict)
    return data


def write_json(data, path):
    path = Path(path)
    log.info('Writing {}'.format(path))
    with path.open('w') as fh:
        json.dump(data, fh, indent=4)


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


def yaml_make_ordereddict_work():
    """
    Teach YAML how to work with OrderedDict.

    http://stackoverflow.com/a/21048064/498873
    """
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)


def table_to_list_of_dict(table):
    """Convert table to list of dict."""
    rows = []
    for row in table:
        data = OrderedDict()
        for name in table.colnames:
            val = row[name]
            if isinstance(val, np.int64):
                val = int(val)
            elif isinstance(val, np.bool_):
                val = bool(val)
            elif isinstance(val, np.float):
                val = float(val)
            elif isinstance(val, np.str):
                val = str(val)
            else:
                raise ValueError('Unknown type: {} {}'.format(val, type(val)))
            data[name] = val

        rows.append(data)

    return rows
