# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Classes to read, validate and work with the input data files.
"""
import logging
from pathlib import Path
from astropy.table import Table
from .info import gammacat_info, gammacat_tag
from .input import InputData
from .utils import write_json

__all__ = [
    'OutputDataConfig',
    'OutputDataReader',
    'OutputDataMaker',
]

log = logging.getLogger(__name__)


class OutputDataConfig:
    """
    Configuration options (mainly directory and filenames).
    """
    path = gammacat_info.base_dir / 'docs/data'

    gammacat_ecsv = path / 'gammacat.ecsv'
    gammacat_fits = path / 'gammacat.fits.gz'

    sources_json = path / 'gammacat-sources.json'

    datasets_json = path / 'gammacat-datasets.json'
    datasets_ecsv = path / 'gammacat-datasets.ecsv'

    @staticmethod
    def make_filename(meta, datatype):
        tag = gammacat_tag.source_dataset_filename(meta)
        source_path = OutputDataConfig.path / 'sources' / gammacat_tag.source_str(meta)

        if datatype == 'sed':
            path = source_path / '{}_sed.ecsv'.format(tag)
        elif datatype == 'lc':
            path = source_path / '{}_lc.ecsv'.format(tag)
        else:
            raise ValueError('Invalid datatype: {}'.format(datatype))

        return path


class OutputDataReader:
    """
    Read all data from the output folder.

    Expose it as Python objects that can be validated and used.

    TODO: rename this class to `GammaCat` ?
    """

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        else:
            self.path = OutputDataConfig.path

        self.gammacat = None
        self.datasets = None

    def read_all(self):
        """Read all data from disk.
        """
        path = OutputDataConfig.gammacat_fits
        self.gammacat = Table.read(str(path), format='fits')

        path = OutputDataConfig.datasets_ecsv
        self.datasets = Table.read(str(path), format='ascii.ecsv')

        return self

    def __str__(self):
        ss = 'output data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of sources: {}\n'.format(len(self.gammacat))
        ss += 'Number of datasets: {}\n'.format(len(self.datasets))
        return ss


class OutputDataMaker:
    """
    Generate output data from input data.

    TODO: some of the columns are lists and can't be written to FITS.
    Remove those or replace with comma-separated strings.
    """

    def __init__(self):
        self.input_data = InputData.read()

    def make_all(self):
        self.make_source_table_json()
        self.make_dataset_table_json()
        self.make_dataset_table_ecsv()
        self.make_sed_files()

    def make_source_table_json(self):
        data = self.input_data.sources.to_json()
        path = OutputDataConfig.sources_json
        write_json(data, path)

    def make_dataset_table_json(self):
        data = self.input_data.datasets.to_json()
        path = OutputDataConfig.datasets_json
        write_json(data, path)

    def make_dataset_table_ecsv(self):
        table = self.input_data.datasets.to_table()
        path = OutputDataConfig.datasets_ecsv
        log.info('Writing {}'.format(path))
        table.write(str(path), format='ascii.ecsv')

    def make_sed_files(self):
        for sed in self.input_data.seds.data:
            log.debug('Processing SED: {}'.format(sed.path))

            sed.process()

            path = OutputDataConfig.make_filename(meta=sed.table.meta, datatype='sed')
            path.parent.mkdir(parents=True, exist_ok=True)
            log.info('Writing {}'.format(path))
            sed.table.write(str(path), format='ascii.ecsv')
