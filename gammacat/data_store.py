# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammapy.utils.scripts import make_path
from .utils import load_json

__all__ = [
    'GammaCatDataStore',
]


class GammaCatDataStore(object):
    """
    Data store for gamma-cat.

    Gives access to all data from https://github.com/gammapy/gamma-cat .

    See also: GammaCatSourceCatalog

    TODO: move this class to gammapy.catalog.
    """

    def __init__(self, data_index):
        self.data_index = data_index

    @classmethod
    def from_index_file(cls, filename='$GAMMA_CAT/docs/data/gammacat-datasets.json'):
        filename = str(make_path(filename))
        data_index = load_json(filename)
        return cls(data_index=data_index)

    def info(self):
        ss = 'version = {}'.format(self.data_index['info']['version'])
        return ss
