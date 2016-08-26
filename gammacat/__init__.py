"""
This is the gammacat Python package.

https://github.com/gammapy/gamma-cat
"""
import subprocess
import logging
from pathlib import Path

__all__ = [
    'info',
    'InputData',
]

log = logging.getLogger()


class GammaCatInfo:
    """Gather basic info about gammacat.
    """

    def __init__(self):
        # Git version: http://stackoverflow.com/a/21901260/498873
        git_version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        self.git_version = git_version.decode('ascii').strip()

        # Git
        self.base_dir = Path.cwd().parent

    def __str__(self):
        ss = 'GammaCatInfo:\n'
        ss += 'git_version: {}\n'.format(self.git_version)
        ss += 'base_dir: {}\n'.format(self.base_dir)
        return ss


info = GammaCatInfo()


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
            self.path = info.base_dir / 'input'

        self.sources = None
        self.papers = None

    def read_sources(self):
        filenames = list((self.path / 'sources').glob('[0-9]*.yaml'))
        log.info(filenames)
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
        ss += 'Number of sources: {}\n'.format('TODO')
        ss += 'Number of papers: {}\n'.format('TODO')
        return ss
