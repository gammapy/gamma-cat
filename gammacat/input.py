"""
Classes to read, validate and work with the input data files.
"""
from pprint import pprint
import logging
from pathlib import Path
import urllib.parse
import yaml
from .info import gammacat_info

__all__ = [
    'InputData',
    'BasicSourceInfo',
    'PaperSourceInfo',
    'PaperInfo',
]

log = logging.getLogger()


class BasicSourceInfo:
    """All basic info for a source.

    Examples
    --------
    >>> from gammacat import BasicSourceInfo
    >>> info = BasicSourceInfo.read('input/sources/000074.yaml')
    >>> info
    BasicSourceInfo(id=60)
    >>> info.pprint()
    ...
    """

    def __init__(self, id, data):
        self.id = id
        self.data = data

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = yaml.safe_load(path.open())
        id = data['source_id']
        return cls(id=id, data=data)

    def __repr__(self):
        return 'BasicSourceInfo(id={})'.format(self.id)

    def pprint(self):
        return pprint(self.data)

    @property
    def yaml(self):
        return yaml.safe_dump(self.data, default_flow_style=False)

    def validate(self):
        raise NotImplementedError


class PaperSourceInfo:
    """All info from one paper for one source.

    Examples
    --------
    >>> from gammacat import PaperSourceInfo
    >>> info = PaperSourceInfo.read('input/papers/2011A%26A...531L..18H/source_000234.yaml')
    >>> info
    TODO
    """

    def __init__(self, paper_id, source_id, data):
        self.paper_id = paper_id
        self.source_id = source_id
        self.data = data

    @classmethod
    def read(cls, path):
        path = Path(path)
        data = yaml.safe_load(path.open())
        return cls(paper_id=data['paper_id'], source_id=data['source_id'], data=data)

    def __repr__(self):
        return 'PaperInfo(id={})'.format(self.id)

    def validate(self):
        raise NotImplementedError


class PaperInfo:
    """All info for one paper.

    Examples
    --------
    >>> from gammacat import PaperInfo
    >>> info = PaperInfo.read('input/papers/2011A%26A...531L..18H')
    >>> info
    PaperInfo(id=60)
    >>> info.pprint()
    """

    def __init__(self, id, sources):
        self.id = id
        self.sources = sources

    @classmethod
    def read(cls, path):
        path = Path(path)
        id = urllib.parse.unquote(path.name)

        sources = []
        for source_path in path.glob('*.yaml'):
            source_info = PaperSourceInfo.read(source_path)
            sources.append(source_info)

        return cls(id=id, sources=sources)

    def __repr__(self):
        return 'PaperInfo(id={})'.format(self.id)

    def validate(self):
        raise NotImplementedError


class InputData:
    """
    Read and expose data from the `input` folder.

    Examples
    --------
    >>> from gammacat import InputData
    >>> input_data = InputData().read_all()
    >>> print(input_data)
    """

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        else:
            self.path = gammacat_info.base_dir / 'input'

        self.sources = []
        self.papers = []

    def read_sources(self):
        paths = (self.path / 'sources').glob('*.yaml')

        for path in paths:
            if path.name in {'example.yaml'}:
                continue
            info = BasicSourceInfo.read(path)
            self.sources.append(info)

        return self

    def read_papers(self):
        paths = (self.path / 'papers').glob('*')

        for path in paths:
            info = PaperInfo.read(path)
            self.papers.append(info)

        return self

    def read_all(self):
        """Read all data from disk.
        """
        self.read_sources()
        self.read_papers()
        return self

    def __str__(self):
        ss = 'Input data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of sources: {}\n'.format(len(self.sources))
        ss += 'Number of papers: {}\n'.format(len(self.papers))
        return ss
