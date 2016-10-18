# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from .input import InputData

__all__ = ['GammaCatMaker']

log = logging.getLogger(__name__)


class GammaCatMaker:
    """
    Make gamma-cat, combining all available data.

    TODO: for now, we gather info from `InputData`.
    This should be changed to gather infor from `OutputData` when available.


    """

    def __init__(self):
        self.input_data = InputData.read()

    def run(self):
        log.info('Making gamma-cat ....')
