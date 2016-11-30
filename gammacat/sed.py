# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from astropy.table import Table
from .info import gammacat_info
from .utils import check_ecsv_column_header

__all__ = ['SED', 'SEDList']

log = logging.getLogger(__name__)


class SED:
    """
    Spectral energy distribution (SED)

    Represents on SED.
    """

    def __init__(self, table, path):
        self.table = table
        self.path = path

    @classmethod
    def read(cls, path, format='ascii.ecsv'):
        log.debug('Reading {}'.format(path))
        table = Table.read(str(path), format=format)
        return cls(table=table, path=path)

    def process(self):
        """Apply fixes."""
        table = self.table
        self._process_energy_ranges(table)
        self._process_flux_errrors(table)

    @staticmethod
    def _process_energy_ranges(table):
        """
        Sometimes energy bin ranges are given as `(e_lo, e_hi)`,
        Those columns are not standard in the SED spec.
        We convert those to `(e_min, e_max)`
        """
        if 'e_lo' in table.colnames:
            table['e_min'] = table['e_ref'] - table['e_lo']
            del table['e_lo']
        if 'e_hi' in table.colnames:
            table['e_max'] = table['e_ref'] + table['e_hi']
            del table['e_hi']

    @staticmethod
    def _process_flux_errrors(table):
        """
        Sometimes flux errors are given as `(dnde_min, dnde_max)`,
        i.e. 68% confidence level (1 sigma) limits.
        Those columns are not standard in the SED spec.
        We convert those to `dnde_errn` and `dnde_errp`.
        """
        if 'dnde_min' in table.colnames:
            table['dnde_errn'] = table['dnde'] - table['dnde_min']
            del table['dnde_min']
        if 'dnde_max' in table.colnames:
            table['dnde_errp'] = table['dnde_max'] - table['dnde']
            del table['dnde_max']

    def validate(self):
        log.debug('Validating {}'.format(self.path))
        check_ecsv_column_header(self.path)
        self.process()
        self._validate_colnames()

    def _validate_colnames(self):
        expected_names = {
            'e_ref', 'e_min', 'e_max',
            'energy_lo', 'energy_hi',
            'dnde', 'dnde_err', 'dnde_errn', 'dnde_errp', 'dnde_ul',
            'excess', 'significance',
        }
        table = self.table
        unexpected_colnames = set(table.colnames) - expected_names
        if unexpected_colnames:
            log.error(
                'SED file {} contains invalid columns: {}'
                ''.format(self.path, unexpected_colnames)
            )


class SEDList:
    """
    List of `SED` objects.

    Used to represent the SED data in the input folder.
    """

    def __init__(self, data):
        self.data = data
        _source_ids = [sed.table.meta['source_id'] for sed in data]
        self._sed_by_source_id = dict(zip(_source_ids, data))

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/papers'
        paths = sorted(path.glob('*/*/*.ecsv'))

        data = []
        for path in paths:
            sed = SED.read(path)
            sed.table.meta['path'] = str(path)
            data.append(sed)

        return cls(data=data)

    def validate(self):
        for sed in self.data:
            sed.validate()

    def get_sed_by_source_id(self, source_id):
        missing = SED(table={}, path='')
        return self._sed_by_source_id.get(source_id, missing)
