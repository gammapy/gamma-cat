# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Automated tests for gamma-cat
"""
import logging
from pathlib import Path
from astropy.utils import lazyproperty
from .input import InputData
from .collection import CollectionConfig, CollectionData
from gammapy.catalog import SourceCatalogGammaCat

__all__ = [
    'CheckerConfig',
    'Checker',
    'CatalogChecker',
]

log = logging.getLogger(__name__)

class CheckerConfig:
    """Config for Checker"""

    def __init__(self, *, step, in_path, out_path):
        self.step = step
        self.in_path = in_path
        self.out_path = out_path


class Checker:
    def __init__(self, config):
        self.config = config

    def run(self):
        log.info('Run checks ...')
        step = self.config.step
        if step == 'all':
            self.check_all()
        elif step == 'input':
            self.check_input()
        elif step == 'collection':
            self.check_collection()
        elif step == 'catalog':
            self.check_catalog()
        elif step == 'global':
            self.check_global()
        else:
            raise ValueError('Invalid step: {}'.format(step))

    @lazyproperty
    def input_data(self):
        log.info('Reading input data ...')
        return InputData.read()

    @lazyproperty
    def collection_data(self):
        log.info('Reading collection data ...')
        return CollectionData(in_path=self.config.in_path, out_path=self.config.out_path)

    @lazyproperty
    def catalog(self):
        log.info('Reading catalog ...')
        filename = CollectionConfig(in_path=self.config.in_path, out_path=self.config.out_path).gammacat_fits
        return SourceCatalogGammaCat(filename=filename)

    def check_all(self):
        log.info('Run checks: all')
        self.check_input()
        self.check_collection()
        self.check_catalog()
        self.check_global()

    def check_input(self):
        log.info('Run checks: input')
        self.input_data.validate()

    def check_collection(self):
        log.info('Run checks: collection')
        self.collection_data.validate()
        print()
        print(self.collection_data)

    def check_catalog(self):
        log.info('Run checks: catalog')
        checker = CatalogChecker(self.catalog)
        checker.run()

    def check_global(self):
        """Global checks.
        
        Consistency between input, collection, catalog, webpage.
        
        E.g. are the files in input and output consistent.
        This helps to identify e.g. if there are stale files
        (e.g. after file renames) still lying around in the output folder.
        """
        log.error('Implement me!!!')
        # TODO: implement


class CatalogChecker:
    """Check format and content of the catalog."""

    def __init__(self, catalog):
        self.catalog = catalog

    def run(self):
        self.check_table(self.catalog.table)
        self.check_sources()

    @staticmethod
    def check_table(table):
        # TODO: remove of put something else?
        # These aren't useful, and if we keep them should be done via pytest
        # to give good errors (showing the actual values).
        # assert len(table) == 162
        # assert len(table.columns) == 82
        pass

    def check_sources(self):
        log.info('Checking catalog sources ...')
        for source in self.catalog:
            self.check_source(source)

    @staticmethod
    def check_source(source):
        log.debug('Checking source: {}'.format(source.name))

        # TODO: fix the following check!
        # This is failing at the moment because spectral points are taken from input folder
        # for this source: input/data/2015/2015A%26A...577A.131H/tev-000045-sed.ecsv
        # try:
        #     source.flux_points
        # except LookupError:
        #     pass
        # source.spectral_model()
        # source.spatial_model()
        # TODO: move over checks from gamma-cat-status to here
        # on spectral model, flux points, spatial model
