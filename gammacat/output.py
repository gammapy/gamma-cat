"""
Classes to read, validate and work with the input data files.
"""
import logging
from pathlib import Path
from .info import gammacat_info

__all__ = [
    'OutputData',
    'make_output_data',
]

log = logging.getLogger()


def make_output_data(input_data):
    output_data = OutputData()
    return output_data


class OutputData:
    """
    Read all data from the `output` folder.

    Expose it as Python objects that can be validated and used.
    """

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        else:
            self.path = gammacat_info.base_dir / 'output'

        self.catalog = None

    def read_all(self):
        """Read all data from disk.
        """
        return self

    def write_all(self):
        pass

    def __str__(self):
        ss = 'output data summary:\n'
        ss += 'Path: {}\n'.format(self.path)
        ss += 'Number of sources: {}\n'.format(len(self.sources))
        ss += 'Number of papers: {}\n'.format(len(self.papers))
        return ss
