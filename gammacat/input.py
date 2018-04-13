# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Classes to read, validate and work with the input data files.
"""
import logging
from collections import OrderedDict
from pathlib import Path
import urllib.parse
from astropy.table import Table
from .info import gammacat_info
from .utils import load_yaml, NA, validate_schema
from .sed import SED
from .lightcurve import LightCurve

__all__ = [
    'BasicSourceInfo',
    'BasicSourceList',
    'DatasetSourceInfo',
    'InputData',
    'InputDataset',
    'InputDatasetCollection',
]

log = logging.getLogger(__name__)


class BasicSourceInfo:
    """All basic info for a source.
    """
    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/basic_source_info.schema.yaml')

    def __init__(self, data, path):
        self.data = data
        self.path = path

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = load_yaml(path)
        return cls(data=data, path=path)

    def __repr__(self):
        return 'BasicSourceInfo(source_id={})'.format(repr(self.data['source_id']))

    def to_dict(self, filled=False):
        """Data as a flat OrderedDict that can be stored in a table row."""
        data = OrderedDict()

        if filled:
            for name, spec in self.schema['properties'].items():
                try:
                    datatype = spec['type']
                except KeyError:
                    datatype = 'string'

                # TODO: write code to handle position
                if name == 'pos':
                    continue

                try:
                    data[name] = NA.fill_value[datatype]
                except TypeError:
                    data[name] = NA.fill_value[datatype[0]]

        data.update(self.data)

        if data['reference_ids'] is None or data['reference_ids'][0] is None:
            data['reference_ids'] = ''
        else:
            data['reference_ids'] = data['reference_ids']

        # TODO: write code to handle position
        data.pop('pos', None)

        return data

    def validate(self):
        validate_schema(path=self.path, data=self.data, schema=self.schema)


class DatasetSourceInfo:
    """All info from one dataset for one source.
    """
    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/dataset_source_info.schema.yaml')

    def __init__(self, data, path):
        self.data = data
        self.path = path

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = load_yaml(path)
        return cls(data=data, path=path)

    def __repr__(self):
        return 'DatasetSourceInfo(source_id={}, reference_id={})'.format(
            repr(self.data['source_id']),
            repr(self.data['reference_id']),
        )

    def validate(self):
        validate_schema(path=self.path, data=self.data, schema=self.schema)


class InputDataset:
    """All info for one dataset.
    """

    def __init__(self, reference_id, path, sources):
        log.debug(f'Creating InputDataset for path={path}')
        self.reference_id = reference_id
        self.path = path
        self.sources = sources
        # TODO: remove this cache
        _source_ids = [source.data['source_id'] for source in sources]
        self._sources_by_id = dict(zip(_source_ids, sources))

    @classmethod
    def read(cls, path):
        path = Path(path)
        reference_id = urllib.parse.unquote(path.parts[-1])

        # TODO: maybe just use an OrderedDict
        sources = []
        for source_path in sorted(path.glob('tev-*.yaml')):
            source_info = DatasetSourceInfo.read(source_path)
            sources.append(source_info)

        path = '/'.join(path.parts[-2:])
        return cls(reference_id=reference_id, path=path, sources=sources)

    def to_dict(self):
        sources = []
        for source in self.sources:
            data = OrderedDict()
            data['source_id'] = source.data['source_id']
            data['reference_id'] = source.data['reference_id']
            sources.append(data)

        # TODO: This would give the full information from the input files.
        # sources = [dict(_.data for _ in self.sources]

        # This is what it takes to build the URL on Github
        url = self.path.replace('%26', '%2526')

        data = OrderedDict()
        data['reference_id'] = self.reference_id
        data['path'] = self.path
        data['url'] = url
        data['sources'] = sources

        return data

    def __repr__(self):
        return 'InputDataset(reference_id={})'.format(repr(self.reference_id))

    def validate(self):
        [_.validate() for _ in self.sources]

    def get_source_by_id(self, source_id):
        # return self._sources_by_id.get(source_id)
        try:
            return self._sources_by_id[source_id]
        except KeyError:
            data = dict(source_id=source_id, reference_id='')
            return DatasetSourceInfo(data=data, path=None)


class BasicSourceList:
    """
    List of `BasicSourceInfo` objects.
    """
    column_spec = load_yaml(gammacat_info.base_dir / 'input/schemas/basic_source_list.schema.yaml')

    def __init__(self, data):
        self.data = data

    @property
    def source_ids(self):
        return [source.data['source_id'] for source in self.data]

    def get_source_by_id(self, source_id):
        idx = self.source_ids.index(source_id)
        return self.data[idx]

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/sources'
        paths = path.glob('*.yaml')

        data = []
        for path in paths:
            info = BasicSourceInfo.read(path)
            data.append(info)

        return cls(data=data)

    def to_dict(self):
        """Return data in format that can be written to JSON.

        A dict with `data` key.
        """
        return OrderedDict(data=self.data_per_row(filled=True))

    def data_per_row(self, filled=False):
        """Data as list of dicts (per-row)"""
        return [
            source.to_dict(filled=filled)
            for source in self.data
        ]

    def validate(self):
        # TODO: validate `column_spec` schema?

        log.info('Validating YAML files in `input/sources`')
        [_.validate() for _ in self.data]

class InputInfo:
    """All basic info about the data of a single publication.
    """

    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/dataset_info.schema.yaml')

    def __init__(self, data, path):
        self.data = data
        self.path = path

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = load_yaml(path)
        return cls(data=data, path=path)

    def validate(self):
        validate_schema(path=self.path, data=self.data, schema=self.schema)

class InputInfoCollection:
    """List of InputInfo objects.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/data'
        paths = path.glob('*/*/info.yaml')

        data = []
        for path in paths:
            info = InputInfo.read(path)
            data.append(info)

        return cls(data=data)

    def to_list(self):
        data = []
        for infodata in self.data:
            data.append(infodata.path)
        return data

    def validate(self):
        log.info('Validating info.yaml files in `input/data`')
        [_.validate() for _ in self.data]

class InputDatasetCollection:
    """
    Represents all data in ``input/data``.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/data'
        paths = list(path.glob('*/*'))
        data = [InputDataset.read(path) for path in paths]
        return cls(data=data)

    @property
    def reference_ids(self):
        return [dataset.reference_id for dataset in self.data]

    def to_table(self):
        """Convert info of `sources` list into a Table.
        """
        meta = OrderedDict()
        meta['name'] = 'todo'
        meta['version'] = 'todo'
        meta['url'] = 'todo'

        # rows = self.data_per_row(filled=True)
        rows = [OrderedDict(spam=99)]
        return Table(rows=rows, meta=meta, masked=True)

    def to_dict(self):
        """Return data in format that can be written to JSON.

        A dict with `data` key.
        """
        data = []
        for dataset in self.data:
            data.append(dataset.to_dict())
        return OrderedDict(data=data)

    def validate(self):
        log.info('Validating YAML files in `input/data`')
        for dataset in self.data:
            dataset.validate()

    def get_dataset_by_reference_id(self, reference_id):
        """Get dataset for a given reference_id
        """
        # TODO: this is not a good way to handle things.
        # Remove once gamma-cat script is set up in a better way.
        if reference_id is None:
            return InputDataset(reference_id=None, path=None, sources=[])

        idx = self.reference_ids.index(reference_id)
        return self.data[idx]


class Schemas:
    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/schemas'
        paths = path.glob('*.yaml')

        data = []
        for path in paths:
            info = load_yaml(path)
            data.append(info)

        return cls(data=data)

    def validate(self):
        log.info('Validating YAML files in `input/schemas')
        # For now (and maybe always) we don't have any checks here.
        # This just shows that the schema files can be parsed OK.
        # for schema in self.data:
        #     log.debug(schema)


class InputData:
    """
    Read all data from the `input` folder.

    Expose it as Python objects that can be validated and used.
    """

    def __init__(self, schemas=None, sources=None, datasets=None,
                 ref_infos=None, gammacat_dataset_config=None):
        self.path = gammacat_info.base_dir / 'input'
        self.schemas = schemas
        self.sources = sources
        self.datasets = datasets
        self.ref_infos = ref_infos
        # TODO: self.lightcurves, self.seds
        self.gammacat_dataset_config = gammacat_dataset_config

    @property
    def src_info_list(self):
        """List of all basic source info files in input/sources"""
        path = gammacat_info.base_dir / 'input/sources'
        return sorted(path.glob('tev*.yaml'))

    @property
    def lightcurve_file_list(self):
        """List of all lightcurve files in the input folder."""
        path = gammacat_info.base_dir / 'input/data'
        return sorted(path.glob('*/*/tev*lc*.ecsv'))

    @property
    def sed_file_list(self):
        """List of all SED files in the input folder."""
        path = gammacat_info.base_dir / 'input/data'
        paths = path.glob('*/*/tev*sed*.ecsv')
        return sorted(paths)

    @property
    def info_yaml_list(self):
        """List of all info files in the input folder."""
        path = gammacat_info.base_dir / 'input/data'
        paths = path.glob('*/*/info.yaml')
        return sorted(paths)

    @property
    def dataset_file_list(self):
        """List of all dataset files in the input folder."""
        path = gammacat_info.base_dir / 'input/data'
        paths = path.glob('*/*/tev*.yaml')
        return sorted(paths)

    @classmethod
    def read(cls):
        """Read all data from disk."""
        # Delayed import to avoid circular dependency
        from .catalog import DatasetConfig
        schemas = Schemas.read()
        sources = BasicSourceList.read()
        datasets = InputDatasetCollection.read()
        ref_infos = InputInfoCollection.read()
        #TODO: lightcurves, seds
        gammacat_dataset_config = DatasetConfig.read()
        return cls(
            schemas=schemas,
            sources=sources,
            datasets=datasets,
            ref_infos=ref_infos,
            gammacat_dataset_config=gammacat_dataset_config,
        )

    def __str__(self):
        ss = 'Input data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of schemas: {}\n'.format(len(self.schemas.data))
        ss += '\n'
        ss += 'Number of YAML files in `input/sources`: {}\n'.format(len(self.sources.data))
        ss += 'Number of entries in `input/gammacat/gamma_cat_dataset.yaml`: {}\n'.format(
            len(self.gammacat_dataset_config.data))
        ss += '\n'
        ss += 'Number of folders in `input/data`: {}\n'.format(len(self.datasets.data))
        ss += 'Number of total datasets in `input/gammacat/gamma_cat_dataset.yaml`: {}\n'.format(
            len(self.gammacat_dataset_config.reference_ids))
        ss += '\n'
        ss += 'Number of SEDs: {}\n'.format(len(self.sed_file_list))
        ss += 'Number of lightcurves: {}\n'.format(len(self.lightcurve_file_list))
        return ss

    def validate(self):
        log.info('Validating input data ...')
        self.schemas.validate()
        self.sources.validate()
        self.datasets.validate()
        self.ref_infos.validate()

        for filename in self.sed_file_list:
            SED.read(filename=filename).process()

        for filename in self.lightcurve_file_list:
            LightCurve.read(filename=filename).process()

        self.gammacat_dataset_config.validate(self)
