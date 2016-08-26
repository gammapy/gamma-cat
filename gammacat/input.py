import logging
from pathlib import Path
import yaml
from .info import gammacat_info

__all__ = ['InputData']

log = logging.getLogger()


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
            data = yaml.safe_load(path.open())
            self.sources.append(data)

        return self

    def read_papers(self):
        papers = 'todo'
        self.papers = papers

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
