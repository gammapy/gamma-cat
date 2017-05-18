# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Classes to read, validate and work with the output data files.
"""
import logging
from collections import OrderedDict
from pathlib import Path
from astropy.utils import lazyproperty
from .lightcurve import LightCurve
from .info import gammacat_info, GammaCatStr
from .input import InputData, SEDList
from .utils import write_json, load_json, log_list_difference

__all__ = [
    'CollectionConfig',
    'CollectionData',
    'CollectionMaker',
]

log = logging.getLogger(__name__)


class CollectionConfig:
    """
    Configuration options (mainly directory and filenames).
    """

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        else:
            self.path = gammacat_info.base_dir / 'docs/data'

        self.gammacat_yaml = self.path / 'gammacat.yaml'
        self.gammacat_ecsv = self.path / 'gammacat.ecsv'
        self.gammacat_fits = self.path / 'gammacat.fits.gz'

        # Index files
        self.index_datasets_json = self.path / 'gammacat-datasets.json'
        self.index_sources_json = self.path / 'gammacat-sources.json'

    def make_filename(self, meta, *, relative_to_index):
        """
        relative -- is relative to index file?
        """

        if relative_to_index:
            path = Path('')
        else:
            path = self.path

        path = path / 'data' / meta['reference_folder']

        tag = GammaCatStr.dataset_filename(meta)

        if meta['datatype'] == 'sed':
            path = path / '{}_sed.ecsv'.format(tag)
        elif meta['datatype'] == 'lc':
            path = path / '{}_lc.ecsv'.format(tag)
        else:
            raise ValueError('Invalid datatype: {}'.format(meta['datatype']))

        return path

    def make_sed_path(self, sed, *, relative_to_index):
        # TODO: introduce DataSetLocation abstraction that holds
        # the `reference_folder` as an attribute?
        # (deriving it here from the path is weird!)
        # import IPython; IPython.embed(); 1/0
        meta = sed.table.meta.copy()
        meta['datatype'] = 'sed'
        meta['reference_folder'] = Path(sed.resource.location).parts[-2]
        return self.make_filename(meta, relative_to_index=relative_to_index)

    def list_of_files(self, pattern='*'):
        """Make list of all files in the output folder"""
        return list([
            str(_.relative_to(self.path))
            for _ in self.path.rglob(pattern)
            if _.is_file()
        ])


class CollectionData:
    """Access data from the output folder.

    Expose it as Python objects that can be validated and used.
    """

    def __init__(self, config=None, index_dataset=None, index_sources=None):
        self.config = config
        self.index_dataset = index_dataset
        self.index_sources = index_sources

    @classmethod
    def read(cls, path=None):
        """Read all data from disk.
        """
        config = CollectionConfig(path)
        index_dataset = load_json(config.index_datasets_json)
        index_sources = load_json(config.index_sources_json)

        return cls(
            config=config,
            index_dataset=index_dataset,
            index_sources=index_sources,
        )

    def __str__(self):
        ss = 'Output data summary:\n'
        ss += 'Path: {}\n'.format(self.config.path)
        # TODO: put more info here! Write a summary YAML or JSON file in the repo instead!
        ss += 'Number of sources: {}\n'.format('TODO')
        ss += 'Number of datasets: {}\n'.format(len(self.index_dataset['data']))
        ss += 'Number of files: {}\n'.format(len(self.index_dataset['files']))
        return ss

    def validate(self):
        log.info('Validating output data ...')

        self.validate_list_of_files()
        # TODO:
        # self.datasets.validate()
        # self.seds.validate()
        # # self.lightcurves.validate()
        # self.gammacat_dataset_config.validate(self)

    def validate_list_of_files(self):
        actual = self.config.list_of_files()
        expected = self.index_dataset['files']
        log_list_difference(actual, expected)

        # TODO: this is a hack, not a real check
        # Change this filelist validation to work with index files !!!
        expected_files_sed = self.config.list_of_files('data/*/*sed*.ecsv')

        expected_files_extra = [
            'README.md',
            'gammacat-datasets.json',
            'gammacat-sources.json',
            'gammacat.fits.gz',
            'gammacat.ecsv',
            'gammacat.yaml',
        ]

        expected_files = expected_files_extra + expected_files_sed
        log_list_difference(actual, expected_files)


class CollectionMaker:
    """Make gamma-cat data collection (from the input files)."""

    def __init__(self, path=None):
        self.config = CollectionConfig(path=path)

    @lazyproperty
    def input_data(self):
        log.info('Reading input data ...')
        return InputData.read()

    @lazyproperty
    def output_data(self):
        log.info('Reading output data ...')
        return CollectionData.read()

    def process_all(self):
        self.make_index_file_for_input()

        self.process_seds()
        self.process_lightcurves()
        # self.process_all_basic_source_infos()  # TODO
        # self.process_all_dataset_source_infos()  # TODO

        # self.make_index_file_for_output()  # TODO

    def process_seds(self):
        for sed in self.input_data.seds.data:
            log.debug('Processing SED: {}'.format(sed.resource.location))
            sed.process()

            path = self.config.make_sed_path(sed, relative_to_index=False)
            path.parent.mkdir(parents=True, exist_ok=True)
            log.info('Writing {}'.format(path))
            sed.table.write(str(path), format='ascii.ecsv')

    def process_lightcurves(self):
        for filename in self.input_data.lightcurve_file_list:
            log.debug('Processing lightcurve: {}'.format(filename))
            lightcurve = LightCurve.read(filename)
            lightcurve.process()

            # TODO: put this in a good location! (same relative path as in input?)
            path = self.config.path / 'lightcurve.ecsv'
            path.parent.mkdir(parents=True, exist_ok=True)
            log.info('Writing {}'.format(path))
            lightcurve.table.write(str(path), format='ascii.ecsv')

    def make_index_file_for_input(self):
        data = OrderedDict()
        data['info'] = gammacat_info.info_dict
        # TODO: the following line should be changed to OUTPUT
        data['data'] = self.input_data.datasets.to_dict()['data']
        data['files'] = self.config.list_of_files()
        path = self.config.index_datasets_json
        write_json(data, path)

    # TODO: change this to be a bundled results file.
    # This is *not* an index file -> rename!
    # def make_index_files_sources(self):
    #     data = OrderedDict()
    #     data['info'] = gammacat_info.info_dict
    #     data['data'] = self.input_data.sources.to_dict()['data']
    #     path = self.config.index_sources_json
    #     write_json(data, path)
