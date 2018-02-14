# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Classes to read, validate and work with the output data files.
"""
import logging
from collections import OrderedDict
from pathlib import Path
from astropy.utils import lazyproperty
from gammapy.catalog.gammacat import GammaCatResourceIndex, GammaCatResource
from .src_info import SrcInfo
from .sed import SED
from .lightcurve import LightCurve
from .dataset import DataSet
from .info import gammacat_info, GammaCatStr
from .input import InputData
from .utils import write_json, load_json, log_list_difference, load_yaml

__all__ = [
    'CollectionConfig',
    'CollectionData',
    'CollectionMaker',
]

log = logging.getLogger(__name__)

# TODO: Rewrite this complete file:
# E.g. three main classes 'CollectionConfig', InputCollection', 'OutputCollection'
# because many things are used by input collection and output collection
# hence we should find a way to not write code doubled

class CollectionConfig:
    """
    Configuration options (mainly directory and filenames).
    """

    def __init__(self, *, in_path, out_path, step=None):
        self.in_path = in_path
        self.out_path = out_path
        self.step = step

        self.gammacat_yaml = self.out_path / 'gammacat.yaml'
        self.gammacat_ecsv = self.out_path / 'gammacat.ecsv'
        self.gammacat_fits = self.out_path / 'gammacat.fits.gz'

        # Index files
        self.index_datasets_json = self.out_path / 'gammacat-datasets.json'
        self.index_sources_json = self.out_path / 'gammacat-sources.json'
        self.index_input_json = self.in_path / 'input-datasets.json'

    def bsi_files(self, relative_to_repo=False):
        filenames = self.list_of_files('sources/*.yaml')
        if relative_to_repo:
            filenames = [str(self.out_path / filename) for filename in filenames]
        return filenames

    def sed_files(self, relative_to_repo=False):
        filenames = self.list_of_files('data/*/*sed*.ecsv')
        if relative_to_repo:
            filenames = [str(self.out_path / filename) for filename in filenames]
        return filenames

    def lc_files(self, relative_to_repo=False):
        filenames = self.list_of_files('data/*/*lc*.ecsv')
        if relative_to_repo:
            filenames = [str(self.out_path / filename) for filename in filenames]
        return filenames

    def ds_files(self, relative_to_repo=False):
        filenames = self.list_of_files('data/*/*ds*.yaml')
        if relative_to_repo:
            filenames = [str(self.out_path / filename) for filename in filenames]
        return filenames

    def make_filename(self, meta, *, relative_to_index):
        """
        relative -- is relative to index file?
        """

        if relative_to_index:
            path = Path('')
        else:
            path = self.out_path

        path = path / 'data' / meta['year']

        tag = GammaCatStr.data_filename(meta)

        if meta['datatype'] == 'sed':
            if meta['file_id'] != -1:
                path = path / '{}-sed-{}.ecsv'.format(tag, meta['file_id'])
            else:
                path = path / '{}-sed.ecsv'.format(tag)
        elif meta['datatype'] == 'lc':
            if meta['file_id'] != -1:
                path = path / '{}-lc-{}.ecsv'.format(tag, meta['file_id'])
            else:
                path = path / '{}-lc.ecsv'.format(tag)
        elif meta['datatype'] == 'ds':
            if meta['file_id'] != -1:
                path = path / '{}-{}.yaml'.format(tag, meta['file_id'])
            else:
                path = path / '{}.yaml'.format(tag)
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
        meta['year'] = sed.resource.reference_id[:4]
        meta['file_id'] = sed.resource.file_id
        return self.make_filename(meta, relative_to_index=relative_to_index)

    def make_lc_path(self, lc, *, relative_to_index):
        meta = lc.table.meta.copy()
        meta['datatype'] = 'lc'
        meta['year'] = lc.resource.reference_id[:4]
        meta['file_id'] = lc.resource.file_id
        return self.make_filename(meta, relative_to_index=relative_to_index)

    def make_dataset_path(self, dataset, *, relative_to_index):
        meta = OrderedDict()
        meta['datatype'] = 'ds'
        meta['reference_id'] = dataset.resource.reference_id
        meta['file_id'] = dataset.resource.file_id
        meta['year'] = dataset.resource.reference_id[:4]
        meta['source_id'] = dataset.resource.source_id
        return self.make_filename(meta, relative_to_index=relative_to_index)

    def list_of_files(self, pattern='*'):
        """Make list of all files in the output folder"""
        return list([
            str(_.relative_to(self.out_path))
            for _ in self.out_path.rglob(pattern)
            if _.is_file()
        ])

    @lazyproperty
    def resource_index(self):
        data = load_json(self.index_datasets_json)
        return GammaCatResourceIndex.from_list(data)

    @lazyproperty
    def index_sources(self):
        return load_json(self.index_sources_json)


class CollectionData:
    """Access data from the output folder.

    Expose it as Python objects that can be validated and used.
    """

    def __init__(self, in_path, out_path):
        # TODO: it's weird that we create a config object here!?
        self.config = CollectionConfig(in_path=in_path, out_path=out_path, step=None)

    # TODO: put more info here! Write a summary YAML or JSON file in the repo instead!
    def __str__(self):
        ss = 'Collection data summary:\n'
        ss += 'Path: {}\n'.format(self.config.out_path)
        ss += 'Number of sources: {}\n'.format('TODO')
        ss += 'Number of resources: {}\n'.format(len(self.config.resource_index.resources))
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
        expected = [str(_.location) for _ in self.config.resource_index.resources]
        log_list_difference(actual, expected)

        # TODO: this is a hack, not a real check
        # Change this filelist validation to work with index files !!!
        expected_files_sed = self.config.sed_files()

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

    def __init__(self, config):
        self.config = config
        self.info_file_list = self.input_data.info_yaml_list

    def run(self):
        log.info('Make collection ...')
        step = self.config.step
        if step == 'all':
            self.process_all()
        elif step == 'input-index':
            self.make_index_file_for_input()
        elif step == 'source-info':
            self.process_src_info()
        elif step == 'dataset':
            self.process_datasets()
        elif step == 'sed':
            self.process_seds()
        elif step == 'lightcurve':
            self.process_lightcurves()
        elif step == 'output-index':
            self.make_index_file_for_output()
        else:
            raise ValueError('Invalid step: {}'.format(step))

    @lazyproperty
    def input_data(self):
        log.info('Reading input data ...')
        return InputData.read()

    def process_all(self):
        self.make_index_file_for_input()

        self.process_src_info()
        self.process_datasets()
        self.process_seds()
        self.process_lightcurves()

        self.make_index_file_for_output()

    def process_seds(self):
        for filename in self.input_data.sed_file_list:
            log.debug('Processing SED: {}'.format(filename))
            sed = SED.read(filename)
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

            path = self.config.make_lc_path(lightcurve, relative_to_index=False)
            path.parent.mkdir(parents=True, exist_ok=True)
            log.info('Writing {}'.format(path))
            lightcurve.table.write(str(path), format='ascii.ecsv')

    def process_src_info(self):
        for filename in self.input_data.src_info_list:
            log.debug(' Processing basic source info file: {}'.format(filename))
            src_info = SrcInfo.read(filename)
            path = self.config.out_path / 'sources' / filename.parts[-1]
            src_info.write(path)

    def process_datasets(self):
        for info_filename in self.input_data.info_yaml_list:
            info_data = load_yaml(info_filename)
            status = info_data['data_entry']['status']
            # review = info_data['data_entry']['reviewed']
            log.debug('Processing reference: {}'.format(info_data['reference_id']))
            # TODO: This is if you want to make sure that all data are reviewed
            # if status == 'complete' and review == 'yes':
            # if status == 'complete':
            for dataset_filename in info_data['datasets']:
                if dataset_filename.endswith('yaml'):
                    filename = info_filename.parent / dataset_filename
                    dataset = DataSet.read(filename)

                    path = self.config.make_dataset_path(dataset, relative_to_index=False)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    dataset.write(path)

    def make_index_file_for_input(self):
        resources = []
        for info_filename in self.input_data.info_yaml_list:
            info_data = load_yaml(info_filename)
            if info_data['data_entry']['status'] == 'missing':
                continue
            # TODO: Decide which datasets are copied to output collection by the keywords in 
            # 'status' and 'reviewed' in info.yaml
            # e.g if info_data['data_entry']['status'] == 'complete':
            for dataset in info_data['datasets']:
                resource = GammaCatResource(0, 'empty')
                if dataset.endswith('yaml'):
                    resource = DataSet.read(info_filename.parent / dataset).resource
                elif dataset.endswith('ecsv'):
                    if 'lc' in dataset:
                        resource = LightCurve.read(info_filename.parent / dataset).resource
                    elif 'sed' in dataset:
                        resource = SED.read(info_filename.parent / dataset).resource
                resource.location = str(info_filename.parent.relative_to(self.config.in_path) / dataset)
                resources.append(resource)

        ri = GammaCatResourceIndex(resources).sort()

        path = self.config.index_input_json
        write_json(ri.to_list(), path)

    def make_index_file_for_output(self):
        resources = []
        for filename in self.config.sed_files():
            resource = SED.read(self.config.out_path / filename).resource
            resource.location = filename
            resources.append(resource)
        for filename in self.config.lc_files():
            resource = LightCurve.read(self.config.out_path / filename).resource
            resource.location = filename
            resources.append(resource)
        for filename in self.config.ds_files():
            resource = DataSet.read(self.config.out_path / filename).resource
            resource.location = filename
            resources.append(resource)
        for filename in self.config.bsi_files():
            resource = SrcInfo.read(self.config.out_path / filename).resource
            resource.location = filename
            resources.append(resource)

        ri = GammaCatResourceIndex(resources).sort()

        path = self.config.index_datasets_json
        write_json(ri.to_list(), path)

