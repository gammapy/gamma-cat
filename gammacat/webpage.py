"""
Make a simple HTML webpage.
"""
import logging
import json
from collections import OrderedDict
from astropy.table import Table
from .info import gammacat_info
from .output import OutputData

log = logging.getLogger()


def make():
    path = gammacat_info.base_dir / 'output/sources.ecsv'
    table = Table.read(str(path), format='ascii.ecsv')

    # Table in CSV format
    path = gammacat_info.base_dir / 'docs/gammacat.csv'
    log.info('Writing {}'.format(path))
    table.write(str(path), format='ascii.csv')

    # Table in JSON format
    # data = []
    # for row in table:
    #     row_data = row.as_void()
    #     if hasattr(row_data, 'filled'):
    #         row_data = row_data.filled()
    #     row_data = OrderedDict(zip(row.colnames, row_data))
    #     import IPython; IPython.embed(); 1/0
    #     data.append(row_data)
    # print(data)
    df = table.to_pandas()

    path = gammacat_info.base_dir / 'docs/gammacat.json'
    log.info('Writing {}'.format(path))
    with path.open('w') as fh:
        df.to_json(fh, orient='records')
        # json.dump(data, fh, indent=4)
        # import IPython; IPython.embed()
