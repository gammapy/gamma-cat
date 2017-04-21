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
    'OutputData',
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


class OutputData:
    """Access data from the output folder.

    Expose it as Python objects that can be validated and used.
    """

    def __init__(self, gammacat=None, datasets=None):
        self.path = OutputDataConfig.path
        self.gammacat = gammacat
        self.datasets = datasets

    @classmethod
    def read(cls):
        """Read all data from disk.
        """
        path = OutputDataConfig.gammacat_fits
        gammacat = Table.read(str(path), format='fits')

        path = OutputDataConfig.datasets_ecsv
        datasets = Table.read(str(path), format='ascii.ecsv')

        return cls(
            gammacat=gammacat,
            datasets=datasets,
        )

    def __str__(self):
        ss = 'Output data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of sources: {}\n'.format(len(self.gammacat))
        ss += 'Number of datasets: {}\n'.format(len(self.datasets))
        return ss

        # ss += 'Number of YAML files in `input/sources`: {}\n'.format(len(self.sources.data))
        # ss += 'Number of entries in `input/gammacat/gamma_cat_dataset.yaml`: {}\n'.format(
        #     len(self.gammacat_dataset_config.data))
        # ss += '\n'
        # ss += 'Number of folders in `input/data`: {}\n'.format(len(self.datasets.data))
        # ss += 'Number of total datasets in `input/gammacat/gamma_cat_dataset.yaml`: {}\n'.format(
        #     len(self.gammacat_dataset_config.reference_ids))
        # ss += '\n'
        # ss += 'Number of SEDs: {}\n'.format(len(self.seds.data))
        # ss += 'Number of lightcurves: {}\n'.format(len(self.lightcurves.data))
        # return ss

    def validate(self):
        log.info('Validating output data ...')

        # TODO:
        # self.gammacat.validate()
        # self.datasets.validate()
        # self.seds.validate()
        # # self.lightcurves.validate()
        # self.gammacat_dataset_config.validate(self)


class OutputDataMaker:
    """
    Generate output data from input data.

    TODO: some of the columns are lists and can't be written to FITS.
    Remove those or replace with comma-separated strings.
    """

    def __init__(self):
        self.input_data = InputData.read()

    def make_all(self):
        self.make_sed_files()
        self.make_index_files()

    def make_index_files(self):
        self.make_source_table_json()
        self.make_dataset_table_json()
        self.make_dataset_table_ecsv()

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
