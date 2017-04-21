# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammapy.utils.scripts import make_path
from .utils import load_json


class GammaCatDataStore(object):
    """
    Data store for gamma-cat.

    Gives access to all data from https://github.com/gammapy/gamma-cat .

    See also: GammaCatSourceCatalog

    TODO: move this class to gammapy.catalog.
    """

    def __init__(self, registry):
        self.registry = registry

    @classmethod
    def from_file(cls, filename='$GAMMA_CAT/docs/data/gammacat-datasets.json'):
        registry = GammaCatDataStoreRegistry.from_file(filename)
        return cls(registry=registry)

    def info(self):
        return self.registry.info()


class GammaCatDataStoreRegistry(object):
    """
    Data store registry for gamma-cat.

    Helper class to query and locate things.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, filename):
        filename = str(make_path(filename))
        data = load_json(filename)
        return cls(data=data)

    def info(self):
        ss = 'version = {}'.format(self.data['version'])
        return ss
