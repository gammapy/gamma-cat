"""
Script to check and ingest Biteau & Williams (2015) data for gamma-cat.
"""
from astropy.table import Table


class Biteau:
    def __init__(self):
        filename = 'other_data_collections/2015ApJ...812...60B/BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'
        self.table = Table.read(filename, format='ascii.ecsv', delimiter='|')

    def run_checks(self):
        # self.table.pprint()
        self.table.show_in_browser(jsviewer=True)
        self.table.info('stats')


if __name__ == '__main__':
    biteau = Biteau()
    biteau.run_checks()
