"""
Automated tests for gamma-cat
"""
import logging
from pprint import pprint
from pathlib import Path
import yaml

__all__ = ['check_input_files']

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def check_input_files():
    """Check that all inputs files can be read.

    This will throw parse errors if some YAML or ECSV file
    formatting is incorrect.
    """
    for path in Path('input').glob('**/*.yaml'):
        log.debug('Checking: %s', path)

        data = yaml.safe_load(path.open())
        if log.level == logging.DEBUG:
            pprint(data)
            print(yaml.safe_dump(data, default_flow_style=False))
