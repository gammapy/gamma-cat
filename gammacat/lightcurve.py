# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from astropy.table import Table
from gammapy.catalog.gammacat import GammaCatResource

__all__ = [
    'LightCurve',
]

log = logging.getLogger(__name__)


def validate_table_colnames(table, expected_colnames, resource):
    unexpected_colnames = sorted(set(table.colnames) - set(expected_colnames))
    if unexpected_colnames:
        log.error(
            'Resource {} contains invalid columns: {}'
            ''.format(resource, unexpected_colnames)
        )


class LightCurve:
    """Process and validate a lightcurve file."""

    expected_colnames_output = [
        'time', 'time_min', 'time_max',
        'e_min', 'e_max',
        'flux', 'flux_err', 'flux_ul',
        'index', 'index_err',
        'significance',
    ]

    expected_colnames_input = expected_colnames_output + [
    ]

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
            type='lightcurve',
            location=location,
        )

    def process(self):
        """Apply fixes."""
        table = self.table
        self.validate_input()
        # self._process_column_order(table)
        # self.validate_output()

    def validate_input(self):
        log.debug('Validating {}'.format(self.resource))
        validate_table_colnames(self.table, self.expected_colnames_input, self.resource)
        # self._validate_input_meta()
        # self._validate_input_consistency()
