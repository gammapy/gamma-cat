"""
Make a simple HTML webpage.
"""
import logging
import json
from .info import gammacat_info
from .input import InputData

log = logging.getLogger()


def make():
    input_data = InputData.read()

    # path = gammacat_info.base_dir / 'output/sources.ecsv'
    # table = Table.read(str(path), format='ascii.ecsv')

    # Table in CSV format
    # path = gammacat_info.base_dir / 'docs/gammacat.csv'
    # log.info('Writing {}'.format(path))
    # table.write(str(path), format='ascii.csv')

    data = dict(data=input_data.sources.data_per_row(filled=True))
    path = gammacat_info.base_dir / 'docs/gammacat.json'
    log.info('Writing {}'.format(path))
    with path.open('w') as fh:
        json.dump(data, fh, indent=4)
