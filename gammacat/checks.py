# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Automated tests for gamma-cat
"""
import logging
from astropy.utils import lazyproperty
from .input import InputData
from .output import OutputData

__all__ = [
    'GammaCatChecker',
]

log = logging.getLogger(__name__)


class GammaCatChecker:
    def __init__(self):
        pass

    @lazyproperty
    def input_data(self):
        log.info('Reading input data ...')
        return InputData.read()

    @lazyproperty
    def output_data(self):
        log.info('Reading output data ...')
        return OutputData.read()

    def check_all(self):
        log.info('Run checks: all')
        self.check_input()
        self.check_output()
        self.check_global()

    def check_input(self):
        log.info('Run checks: input')
        self.input_data.validate()
        print()
        print(self.input_data)

    def check_output(self):
        log.info('Run checks: output')
        self.output_data.validate()
        print()
        print(self.output_data)

    def check_global(self):
        """Global consistency checks.
        
        E.g. are the files in input and output consistent.
        This helps to identify e.g. if there are stale files
        (e.g. after file renames) still lying around in the output folder.
        """
        log.info('Run checks: global')
        # TODO: implement
