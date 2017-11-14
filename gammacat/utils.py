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
from astropy.table import Table
from gammapy.spectrum.crab import CrabSpectrum
from gammapy.catalog.gammacat import GammaCatResource

__all__ = [
    'FLUX_TO_CRAB', 'E_INF',
    'ECSVFormatError',
    'NA', 'render_template',
    'load_yaml', 'write_yaml',
    'load_json', 'write_json',
    'print_simbad_pos',
    'table_to_list_of_dict',
    'validate_schema',
    'log_list_difference',
    'TableProcessor',
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

def render_template(infile, outfile, ctx=None):
    """Helper function to render Jinja templates."""
    # For examples how to use Jinja, see https://gits.github.com/wrunk/1317933
    # from flask import render_template
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader('/'))
    template = env.get_template(infile)
    if ctx is None:
        ctx = dict()
    text = template.render(**ctx)
    with open(outfile, 'w') as fh:
        fh.write(text)

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


class TableProcessor:
    """Shared code between SED and Lightcurve processing classes."""
    resource_type = None

    def __init__(self, table, resource):
        self.table = table
        self.resource = resource

    @classmethod
    def read(cls, filename, format='ascii.ecsv'):
        log.debug('Reading {}'.format(filename))
        table = Table.read(str(filename), format=format)
        resource = cls._read_resource_info(table, filename)
        return cls(table=table, resource=resource)

    @classmethod
    def _read_resource_info(cls, table, location):
        m = table.meta
        return GammaCatResource(
            source_id=m['source_id'],
            reference_id=m['reference_id'],
            file_id=m.get('file_id', -1),
            type=cls.resource_type,
            location=location,
        )

    def validate_table_colnames(self, expected_colnames):
        unexpected_colnames = sorted(set(self.table.colnames) - set(expected_colnames))
        if unexpected_colnames:
            log.error(
                'Resource {} contains invalid columns: {}'
                ''.format(self.resource, unexpected_colnames)
            )

    def make_table_columns_uniform(self, col_specs):
        """Make column units and description uniform."""
        for col_spec in col_specs:
            name = col_spec['name']
            if name in self.table.colnames:
                if 'unit' in col_spec:
                    self.table[name] = self.table[name].quantity.to(col_spec['unit'])

                self.table[name].description = col_spec['description']

    def validate_input_meta(self):
        meta = self.table.meta

        missing = sorted(set(self.required_meta_keys) - set(meta.keys()))
        if missing:
            log.error('Resource {} contains missing meta keys: {}'.format(self.resource, missing))

        extra = sorted(set(meta.keys()) - set(self.allowed_meta_keys))
        if extra:
            log.error('Resource {} contains extra meta keys: {}'.format(self.resource, extra))

        if ('comments' in meta) and not isinstance(meta['comments'], str):
            log.error('Resource {} contains invalid meta key comments (should be str): {}'
                      ''.format(self.resource, meta['comments']))
