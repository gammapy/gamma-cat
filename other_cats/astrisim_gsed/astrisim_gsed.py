"""
Compare and add astrisim/gsed info to gamma-cat

Note: this script must be executed from the gamma-cat repo top-level folder.

See `README.md`
"""
from collections import OrderedDict
from astropy.table import Table
import gammacat


class GammaCatGSEDCheck:
    def __init__(self):
        self.gammacat_sources = gammacat.utils.load_json('docs/data/gammacat-sources.json')['data']
        self.gammacat_papers = gammacat.utils.load_json('docs/data/gammacat-papers.json')['data']
        # self.gammacat_data = gammacat.InputData.read()
        self.gsed_table = Table.read('other_cats/astrisim_gsed/index2.fits')

    def list_missing_info(self):
        """Make list of info that's in astrisim/gsed, but not in gamma-cat yet.
        """
        info = []
        for source in self.gsed_table:
            info.append(self.check_source(source))
        table = Table(rows=info, names=list(info[0]))
        table.write('other_cats/astrisim_gsed/missing_info.csv', format='ascii.fixed_width')
        table[:5].pprint(max_lines=-1)

    def check_source(self, source):
        info = OrderedDict()
        info['tevcat_name'] = str(source['TeVCat']).strip()
        info['gammacat_id'] = self._get_gammacat_id(info['tevcat_name'])
        info['paper_ids'] = self._get_paper_ids(info['gammacat_id'])
        return info

    def _get_gammacat_id(self, tevcat_name):
        """Find the gammacat_id for this source from the TeVCat name"""
        tevcat_names = [_['tevcat_name'].strip() for _ in self.gammacat_sources]
        idx = tevcat_names.index(tevcat_name)
        gammacat_id = self.gammacat_sources[idx]['source_id']
        return gammacat_id

    def _get_paper_ids(self, gammacat_id):
        """Get the list of papers we have with info on that source"""
        paper_ids = []
        for paper in self.gammacat_papers:
            for source in paper['sources']:
                if source['source_id'] == gammacat_id:
                    paper_ids.append(source['paper_id'])
        # print('tevcat_name: {}'.format(tevcat_name))
        # print(locals())
        # gammacat = Table.read('docs/data/gammacat.fits.gz')
        # import IPython; IPython.embed(); 1 / 0
        return ','.join(paper_ids)

    def add_missing_info(self):
        """Add missing info from `astrisim/gsed to gamma-cat.

        TODO: copy over info from FITS files to YAML / ECSV files,
        in the appropritate formats.
        """
        raise NotImplementedError

    def check_consistency(self):
        """Check consistency of info in `astrisim/gsed to gamma-cat.

        TODO: Not sure if it's worth scripting this!?
        """
        raise NotImplementedError


if __name__ == '__main__':
    check = GammaCatGSEDCheck()
    check.list_missing_info()
    # check.add_missing_info()
    # check.check_consistency()
