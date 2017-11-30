# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from .utils import load_yaml, write_yaml
from gammapy.catalog.gammacat import GammaCatResource

__all__ = [
    'SrcInfo',
]

log = logging.getLogger(__name__)

class SrcInfo:
    """Process a basic source info file"""
    resource_type = 'bsi'

    def __init__(self, data):
        self.data = data

    @classmethod
    def read(cls, filename):
        data = load_yaml(filename)
        return cls(data)

    def write(self, filename):
        write_yaml(self.data, filename)