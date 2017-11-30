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

    def __init__(self, data, resource):
        self.data = data
        self.resource = resource

    @classmethod
    def read(cls, filename):
        data = load_yaml(filename)
        resource = cls._read_resource_info(data, filename)
        return cls(data=data, resource=resource)

    @classmethod
    def _read_resource_info(cls, data, location):
        file_id = -1
        return GammaCatResource(
            source_id=data['source_id'],
            reference_id=data['reference_ids'],
            file_id=file_id,
            type=cls.resource_type,
            location=location
        )

    def write(self, filename):
        write_yaml(self.data, filename)
