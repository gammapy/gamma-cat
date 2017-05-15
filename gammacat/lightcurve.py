# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from astropy.table import Table
from .info import gammacat_info

__all__ = [
    'LightCurve',
    'LightCurveList',
]

log = logging.getLogger(__name__)


class LightCurve:
    """
    A single lightcurve.
    """

    def __init__(self, table):
        self.table = table

    @classmethod
    def read(cls, filename, format='ascii.ecsv'):
        log.debug('Reading {}'.format(filename))
        table = Table.read(str(filename), format=format)
        return cls(table=table)


class LightCurveList:
    """
    Collection of all `LightCurve` objects.

    Stored in the `data` attribute -- a Python list of `LightCurve` objects.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/data'
        paths = sorted(path.glob('*/*/tev*lc.ecsv'))

        data = []
        for path in paths:
            lc = LightCurve.read(path)
            lc.table.meta['path'] = str(path)
            data.append(lc)

        return cls(data=data)
