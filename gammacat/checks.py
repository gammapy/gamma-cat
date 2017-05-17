# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Automated tests for gamma-cat
"""
import logging
from astropy.utils import lazyproperty
from .input import InputData
from .collection import CollectionData
from .catalog import CatalogChecker

__all__ = [
    'Checker',
]

log = logging.getLogger(__name__)


class Checker:
    def __init__(self, out_path=None):
        self.out_path = out_path

    @lazyproperty
    def input_data(self):
        log.info('Reading input data ...')
        return InputData.read()

    @lazyproperty
    def output_data(self):
        log.info('Reading output data ...')
        return CollectionData.read(path=self.out_path)

    def check_all(self):
        log.info('Run checks: all')
        self.check_input()
        self.check_output()
        self.check_catalog()
        self.check_global()

    def check_input(self):
        log.info('Run checks: input')
        self.input_data.validate()
        print()
        print(self.input_data)

    def check_collection(self):
        log.info('Run checks: collection')
        self.output_data.validate()
        print()
        print(self.output_data)

    def check_catalog(self):
        log.info('Run checks: catalog')
        checker = CatalogChecker()
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
