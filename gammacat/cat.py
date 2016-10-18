# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from .info import gammacat_info
from .input import InputData

__all__ = ['GammaCatMaker']

log = logging.getLogger(__name__)


class GammaCatMaker:
    """
    Make gamma-cat, combining all available data.

    TODO: for now, we gather info from `InputData`.
    This should be changed to gather info from `OutputData` when available.


    """

    def __init__(self):
        self.input_data = InputData.read()

    def run(self):
        log.info('Making gamma-cat ....')

        self.load_basic_source_info()
        self.add_paper_info()
        self.write()

    def write(self):
        table = self.gammacat_table

        path = gammacat_info / 'docs/data/gammacat.ecsv'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='ascii.ecsv')

        path = gammacat_info / 'docs/data/gammacat.fits'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='ascii.ecsv')
