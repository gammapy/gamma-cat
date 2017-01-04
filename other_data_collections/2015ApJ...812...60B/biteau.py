"""
Script to check and ingest Biteau & Williams (2015) data for gamma-cat.
"""
from astropy.table import Table


class BiteauMaker:
    def __init__(self):
        path = 'other_data_collections/2015ApJ...812...60B/'
        filename = path + 'BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'
        filename2 = path + 'BiteauWilliams2015_AllData_TeVCat_v2016_12_20.ecsv'

        print('Reading {}'.format(filename))
        self.table = Table.read(filename, format='ascii.ecsv', delimiter='|')

        print('Reading {}'.format(filename2))
        self.table2 = Table.read(filename2, format='ascii.ecsv', delimiter='|')

    def run_basic_checks(self):
        self.table.info('stats')
        self.table2.info('stats')

        self.table.show_in_browser(jsviewer=True)
        self.table2.show_in_browser(jsviewer=True)

    def run_checks(self):
        # self.table.info('stats')
        # self.table.pprint()
        # ref_id = self.table['reference_id']
        table = self.table.group_by('reference_id')
        table.groups.keys.pprint(max_lines=-1)

if __name__ == '__main__':
    maker = BiteauMaker()
    # biteau.run_basic_checks()
    maker.run_checks()
