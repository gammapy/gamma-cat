# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Classes to read, validate and work with the input data files.
"""
from pprint import pprint
import logging
from collections import OrderedDict
from pathlib import Path
import urllib.parse
import jsonschema
from astropy.table import Table
from .info import gammacat_info
from .utils import load_yaml, NA
from .sed import SEDList
from .lightcurve import LightcurveList

__all__ = [
    'BasicSourceInfo',
    'BasicSourceList',
    'PaperSourceInfo',
    'PaperInfo',
    'PaperList',
    'InputData',
]

log = logging.getLogger(__name__)


class ValidateMixin:
    def validate(self):
        log.debug('Validating {}'.format(self.path))
        try:
            jsonschema.validate(self.data, self.schema)
        except jsonschema.exceptions.ValidationError as ex:
            log.error('Invalid input file: {}'.format(self.path))
            pprint(self.data)
            raise ex


class BasicSourceInfo(ValidateMixin):
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
        return 'BasicSourceInfo(id={})'.format(repr(self.data['source_id']))

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

        if data['papers'] is None or data['papers'][0] is None:
            data['papers'] = ''
        else:
            data['papers'] = ','.join(data['papers'])

        # TODO: write code to handle position
        data.pop('pos', None)

        return data

    def pprint(self):
        return pprint(self.data)

        # @property
        # def yaml(self):
        #     return yaml.safe_dump(self.data, default_flow_style=False)


class PaperSourceInfo(ValidateMixin):
    """All info from one paper for one source.
    """
    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/paper_source_info.schema.yaml')

    def __init__(self, data, path):
        self.data = data
        self.path = path

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = load_yaml(path)
        return cls(data=data, path=path)

    def __repr__(self):
        return 'PaperInfo(source_id={}, data_id={})'.format(
            repr(self.data['source_id']),
            repr(self.data['paper_id']),
        )


class PaperInfo:
    """All info for one paper.
    """

    def __init__(self, id, path, sources):
        self.id = id
        self.path = path
        self.sources = sources
        _source_ids = [source.data['source_id'] for source in sources]
        self._sources_by_id = dict(zip(_source_ids, sources))

    @classmethod
    def read(cls, path):
        path = Path(path)
        id = urllib.parse.unquote(path.parts[-1])

        # TODO: maybe just use an OrderedDict
        sources = []
        for source_path in sorted(path.glob('*.yaml')):
            source_info = PaperSourceInfo.read(source_path)
            sources.append(source_info)

        path = '/'.join(path.parts[-2:])
        # path = '/'.join([path.parts[-2], id])
        return cls(id=id, path=path, sources=sources)

    def to_json(self):
        sources = []
        for source in self.sources:
            data = OrderedDict()
            data['source_id'] = source.data['source_id']
            data['paper_id'] = source.data['paper_id']
            sources.append(data)

        # TODO: This would give the full information from the input files.
        # sources = [dict(_.data for _ in self.sources]

        # This is what it takes to build the URL on Github
        url = self.path.replace('%26', '%2526')

        data = OrderedDict()
        data['id'] = self.id
        data['path'] = self.path
        data['url'] = url
        data['sources'] = sources

        return data

    def __repr__(self):
        return 'PaperInfo(id={})'.format(repr(self.id))

    def validate(self):
        [_.validate() for _ in self.sources]

    def get_source_by_id(self, source_id):
        # returning empty PaperSourceInfo makes sense, because it leads to a key
        # error later and will be treated as missing info
        missing = PaperSourceInfo(data={}, path='')
        return self._sources_by_id.get(source_id, missing)


class BasicSourceList:
    """
    List of `BasicSourceInfo` objects.
    """
    column_spec = load_yaml(gammacat_info.base_dir / 'input/schemas/basic_source_list.schema.yaml')

    def __init__(self, data):
        self.data = data
        # TODO: remove that cache to get simpler code?
        _source_ids = self.source_ids
        self._source_by_id = dict(zip(_source_ids, data))

    @property
    def source_ids(self):
        return [source.data['source_id'] for source in self.data]

    def get_source_by_id(self, source_id):
        try:
            return self._source_by_id[source_id]
        except KeyError:
            raise IndexError('Not found: source_id = {}'.format(source_id))

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/sources'
        paths = path.glob('*.yaml')

        data = []
        for path in paths:
            if path.name in {'example.yaml'}:
                continue
            info = BasicSourceInfo.read(path)
            data.append(info)

        return cls(data=data)

    def to_json(self):
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
        log.info('Validating YAML files in `input/sources`')
        [_.validate() for _ in self.data]


class PaperList:
    """
    List of `PaperInfo` objects.
    """

    def __init__(self, data):
        self.data = data
        _paper_ids = [paper.id for paper in data]
        self._paper_by_id = dict(zip(_paper_ids, data))

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/papers'
        paths = path.glob('*/*')

        data = []
        for path in paths:
            info = PaperInfo.read(path)
            data.append(info)

        return cls(data=data)

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

    def to_json(self):
        """Return data in format that can be written to JSON.

        A dict with `data` key.
        """
        data = []
        for paper in self.data:
            data.append(paper.to_json())
        return OrderedDict(data=data)

    def validate(self):
        log.info('Validating YAML files in `input/papers`')
        for paper in self.data:
            paper.validate()

    def get_paper_by_id(self, paper_id):
        """Get PaperInfo by paper id
        """
        missing = PaperInfo(id=paper_id, path=None, sources=[])
        return self._paper_by_id.get(paper_id, missing)


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

    def __init__(self, schemas=None, sources=None, papers=None,
                 seds=None, lightcurves=None, gammacat_dataset_config=None):
        self.path = gammacat_info.base_dir / 'input'
        self.schemas = schemas
        self.sources = sources
        self.papers = papers
        self.seds = seds
        self.lightcurves = lightcurves
        self.gammacat_dataset_config = gammacat_dataset_config

    @classmethod
    def read(cls):
        """Read all data from disk.
        """
        # Delayed import to avoid circular dependency
        from .cat import GammaCatDataSetConfig
        schemas = Schemas.read()
        sources = BasicSourceList.read()
        papers = PaperList.read()
        seds = SEDList.read()
        lightcurves = LightcurveList.read()
        gammacat_dataset_config = GammaCatDataSetConfig.read()
        return cls(
            schemas=schemas,
            sources=sources,
            papers=papers,
            seds=seds,
            lightcurves=lightcurves,
            gammacat_dataset_config=gammacat_dataset_config,
        )

    def __str__(self):
        ss = 'Input data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of schemas: {}\n'.format(len(self.schemas.data))
        ss += 'Number of YAML files in `input/sources`: {}\n'.format(len(self.sources.data))
        ss += 'Number of entries in `input/gammacat/gamma_cat_dataset.yaml`: {}\n'.format(len(self.gammacat_dataset_config.data))
        ss += 'Number of papers: {}\n'.format(len(self.papers.data))
        ss += 'Number of SEDs: {}\n'.format(len(self.seds.data))
        ss += 'Number of lightcurves: {}\n'.format(len(self.lightcurves.data))
        return ss

    def validate(self):
        log.info('Validating input data ...')
        self.schemas.validate()
        self.sources.validate()
        self.papers.validate()
        self.seds.validate()
        # self.lightcurves.validate()
        self.gammacat_dataset_config.validate(self)
