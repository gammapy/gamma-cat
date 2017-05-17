# Licensed under a 3-clause BSD style license - see LICENSE.rst
from collections import OrderedDict
from pprint import pprint
import logging
import json
from pathlib import Path
import ruamel.yaml
import jsonschema
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from gammapy.spectrum.crab import CrabSpectrum

__all__ = [
    'FLUX_TO_CRAB', 'E_INF',
    'ECSVFormatError',
    'NA',
    'load_yaml', 'write_yaml',
    'load_json', 'write_json',
    'print_simbad_pos',
    'table_to_list_of_dict',
    'validate_schema',
    'log_list_difference',
]

log = logging.getLogger(__name__)


def _to_crab_flux():
    # Integral flux above 1 TeV in crab units
    crab = CrabSpectrum('meyer').model
    flux_crab = crab.integral(1 * u.TeV, 1e6 * u.TeV)
    return 100 / flux_crab.to('cm-2 s-1').value


FLUX_TO_CRAB = _to_crab_flux()
E_INF = 1e6 * u.Unit('TeV')


class ECSVFormatError(Exception):
    """ECSV format error"""


class NA:
    """
    Handling of missing values

    NA = "not available"
    """
    fill_value = OrderedDict(
        integer=-999,
        number=np.nan,
        string='',
        array='',
        list=[],
    )

    # @classmethod
    # def fill_str(cls, data, key):
    #     try:
    #         data[key] = cls.fill_value['string']
    #     else:
    #         return data

    @staticmethod
    def fill_value_array(shape):
        return np.ones(shape) * np.nan

    @staticmethod
    def resize_sed_array(array, shape):
        array = array.copy()
        array.resize(shape)
        array[array == 0] = np.nan
        return array

    @classmethod
    def fill_list(cls, data, key):
        try:
            return ','.join(data[key])
        except KeyError:
            return cls.fill_value['string']


def load_yaml(path):
    """Helper function to load data from a YAML file."""
    path = Path(path)
    log.debug('Reading {}'.format(path))
    with path.open() as fh:
        data = ruamel.yaml.round_trip_load(fh)
    return data


def write_yaml(data, path):
    """Helper function to write data to a YAML file."""
    path = Path(path)
    log.info('Writing {}'.format(path))
    with path.open('w') as fh:
        ruamel.yaml.round_trip_dump(data, fh)


def load_json(path):
    """Helper function to load data from a JSON file."""
    path = Path(path)
    log.debug('Reading {}'.format(path))
    with path.open() as fh:
        data = json.load(fh, object_pairs_hook=OrderedDict)
    return data


def write_json(data, path):
    """Helper function to write data to a JSON file."""
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


def table_to_list_of_dict(table):
    """Convert table to list of dict."""
    rows = []
    for row in table:
        data = OrderedDict()
        for name in table.colnames:
            val = row[name]
            if isinstance(val, np.int64):
                val = int(val)
            elif isinstance(val, np.int32):
                val = int(val)
            elif isinstance(val, np.bool_):
                val = bool(val)
            elif isinstance(val, np.float):
                val = float(val)
            elif isinstance(val, np.float32):
                val = float(val)
            elif isinstance(val, np.str):
                val = str(val)
            elif isinstance(val, np.ndarray):
                vals = [float(_) for _ in val]
                val = list(vals)
            else:
                raise ValueError('Unknown type: {} {}'.format(val, type(val)))
            data[name] = val

        rows.append(data)

    return rows


def validate_schema(path, data, schema):
    """Validate data against schema and log errors.
    """
    log.debug('Validating {}'.format(path))
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError as ex:
        log.error('Invalid input file: {}'.format(path))
        pprint(data)
        raise ex


def log_list_difference(actual, expected):
    missing = sorted(set(expected) - set(actual))
    if missing:
        log.error('Missing: {}'.format(missing))

    extra = sorted(set(actual) - set(expected))
    if extra:
        log.error('Extra: {}'.format(extra))
