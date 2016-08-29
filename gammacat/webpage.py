"""
Make a simple HTML webpage.
"""
import logging
import json
from collections import OrderedDict
from astropy.table import Table
from .info import gammacat_info
from .output import OutputData
from .input import InputData

log = logging.getLogger()


def make():
    input_data = InputData.read()

    path = gammacat_info.base_dir / 'output/sources.ecsv'
    table = Table.read(str(path), format='ascii.ecsv')

    # Table in CSV format
    path = gammacat_info.base_dir / 'docs/gammacat.csv'
    log.info('Writing {}'.format(path))
    table.write(str(path), format='ascii.csv')

    data = input_data.sources.to_dict()
    path = gammacat_info.base_dir / 'docs/gammacat.json'
    log.info('Writing {}'.format(path))
    with path.open('w') as fh:
        json.dump(data, fh, indent=4)
