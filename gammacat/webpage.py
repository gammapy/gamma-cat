# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make gamma-cat webpage (in combination with Sphinx).
"""
import logging

__all__ = [
    'WebpageConfig',
    'WebpageMaker',
]

log = logging.getLogger(__name__)


class WebpageConfig:
    """Config options for webpage maker."""

    def __init__(self, *, out_path):
        self.out_path = out_path


class WebpageMaker:
    """Make gamma-cat webpage."""

    def __init__(self, config):
        self.config = config

    def run(self):
        log.info('Make webpage ...')
        log.error('Come one. Implement me already, you lazy hog!!!')
