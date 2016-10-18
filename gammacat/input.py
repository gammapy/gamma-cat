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
from .utils import load_yaml, MissingValues

__all__ = [
    'BasicSourceInfo',
    'BasicSourceList',
    'PaperSourceInfo',
    'PaperInfo',
    'PaperList',
    'InputData',
]

log = logging.getLogger(__name__)


class BasicSourceInfo:
    """All basic info for a source.
    """
    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/basic_source_info.schema.yaml')

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = load_yaml(path)
        return cls(data=data)

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
                    data[name] = getattr(MissingValues, datatype)
                except TypeError:
                    data[name] = getattr(MissingValues, datatype[0])

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

    def validate(self):
        try:
            jsonschema.validate(self.data, self.schema)
        except jsonschema.exceptions.ValidationError as ex:
            log.error('Invalid source_id: {}'.format(self.data['source_id']))
            print(self.data)
            raise ex


class PaperSourceInfo:
    """All info from one paper for one source.
    """
    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/paper_source_info.schema.yaml')

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = load_yaml(path)
        return cls(data=data)

    def __repr__(self):
        return 'PaperInfo(source_id={}, data_id={})'.format(
            repr(self.data['source_id']),
            repr(self.data['paper_id']),
        )

    def validate(self):
        jsonschema.validate(self.data, self.schema)


class PaperInfo:
    """All info for one paper.
    """

    def __init__(self, id, path, sources):
        self.id = id
        self.path = path
        self.sources = sources

    @classmethod
    def read(cls, path):
        path = Path(path)
        id = urllib.parse.unquote(path.parts[-1])

        sources = []
        for source_path in path.glob('*.yaml'):
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


class BasicSourceList:
    """
    List of `BasicSourceInfo` objects.
    """
    column_spec = load_yaml(gammacat_info.base_dir / 'input/schemas/basic_source_list.schema.yaml')

    def __init__(self, data):
        self.data = data

    def get_source_by_id(self, source_id):
        for source in self.data:
            if source.data['source_id'] == source_id:
                return source
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

    def to_table(self):
        """Convert info of `sources` list into a Table.
        """
        meta = OrderedDict()
        meta['name'] = 'todo'
        meta['version'] = 'todo'
        meta['url'] = 'todo'

        rows = self.data_per_row(filled=True)
        table = Table(rows=rows, meta=meta, masked=True)
        return table

    def to_json(self):
        """Return data in format that can be written to JSON.

        A dict with `data` key.
        """
        return OrderedDict(data=self.data_per_row(filled=True))

    # def data_per_column(self):
    #     """Data as dict of lists (per-column)"""
    #     row_data = self.data_per_row()
    #     col_data = OrderedDict()
    #
    #     col_names = [_['name'] for _ in self.columns]
    #     for name in col_names:
    #         col_data[name] = [row.get(name, None) for row in row_data]
    #
    #     return col_data

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

    def __init__(self, sources=None, papers=None, schemas=None):
        self.path = gammacat_info.base_dir / 'input'
        self.sources = sources
        self.papers = papers
        self.schemas = schemas

    @classmethod
    def read(cls):
        """Read all data from disk.
        """
        sources = BasicSourceList.read()
        papers = PaperList.read()
        schemas = Schemas.read()
        return cls(sources=sources, papers=papers, schemas=schemas)

    def __str__(self):
        ss = 'Input data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of sources: {}\n'.format(len(self.sources.data))
        ss += 'Number of papers: {}\n'.format(len(self.papers.data))
        ss += 'Number of schemas: {}\n'.format(len(self.schemas.data))
        return ss

    def validate(self):
        log.info('Validating input data ...')
        self.sources.validate()
        self.papers.validate()
        self.schemas.validate()
