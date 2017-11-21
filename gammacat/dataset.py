# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from .utils import load_yaml, write_yaml
from gammapy.catalog.gammacat import GammaCatResource

__all__ = [
    'DataSet',
]

log = logging.getLogger(__name__)


class DataSet:
    """Process a dataset file."""
    resource_type = 'ds'

    def __init__(self, data, resource):
        log.debug('DataSet.__init__()')
        self.resource = resource
        self.data = data

    @classmethod
    def read(cls, filename):
        data = load_yaml(filename)
        resource = cls._read_resource_info(data, filename)
        return cls(data=data, resource=resource)

    @classmethod
    def _read_resource_info(cls, data, location):
        file_id = data.get('file_id', GammaCatResource._NA_FILL['file_id'])
        return GammaCatResource(
            source_id=data['source_id'],
            reference_id=data['reference_id'],
            file_id=file_id,
            type=cls.resource_type,
            location=location
        )

    def write(self, filename):
        write_yaml(self.data, filename)
