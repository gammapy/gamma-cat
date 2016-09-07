# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Automated tests for gamma-cat
"""
import logging
from .input import InputData

__all__ = ['check_input_files']

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def check_input_files():
    """Check that all inputs files can be read.

    This will throw parse errors if some YAML or ECSV file
    formatting is incorrect.
    """
    input_data = InputData.read()
    input_data.validate()
