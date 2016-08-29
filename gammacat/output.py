"""
Classes to read, validate and work with the input data files.
"""
import logging
from pathlib import Path
from astropy.table import Table
from .info import gammacat_info
from .input import InputData

__all__ = [
    'OutputData',
    'make_output_data',
]

log = logging.getLogger()


def make_output_data():
    """Make output data.

    - Catalog with info from `input/sources`
    - TODO: catalog with info from `input/papers`
    - TODO: combined and prioritized catalog with all data.
    """
    input_data = InputData.read()

    table = input_data.sources.to_table()
    filename = gammacat_info.base_dir / 'output/sources.ecsv'
    log.info('Writing {}'.format(filename))
    table.write(str(filename), format='ascii.ecsv')


    # import IPython; IPython.embed()


class OutputData:
    """
    Read all data from the `output` folder.

    Expose it as Python objects that can be validated and used.
    """

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        else:
            self.path = gammacat_info.base_dir / 'output'

        self.sources_catalog = None
        # self.papers_catalog = None
        # self.catalog = None

    def read_all(self):
        """Read all data from disk.
        """
        filename = str(self.path / 'sources.ecsv')
        self.sources_catalog = Table.read(filename, format='ascii.ecsv')

        return self

    def write_all(self):
        pass

    def __str__(self):
        ss = 'output data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of sources: {}\n'.format(len(self.sources_catalog))
        # ss += 'Number of papers: {}\n'.format(len(self.papers_catalog))
        return ss
