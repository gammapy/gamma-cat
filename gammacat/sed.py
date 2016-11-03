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

    def validate(self):
        log.debug('Validating {}'.format(self.path))
        check_ecsv_column_header(self.path)


class SEDList:
    """
    List of `SED` objects.

    Used to represent the SED data in the input folder.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/papers'
        paths = path.glob('*/*/*.ecsv')

        data = []
        for path in paths:
            sed = SED.read(path)
            sed.table.meta['path'] = str(path)
            data.append(sed)

        return cls(data=data)

    def validate(self):
        for sed in self.data:
            sed.validate()
