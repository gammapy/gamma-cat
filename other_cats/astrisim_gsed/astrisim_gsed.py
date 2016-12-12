"""
Compare and add astrisim/gsed info to gamma-cat

Note: this script must be executed from the gamma-cat repo top-level folder.

See `README.md`
"""
from pathlib import Path
from collections import OrderedDict
from astropy.io import fits
from astropy.table import Table
import gammacat


class AstriSimGSED:
    def __init__(self):
        self.gammacat_sources = gammacat.utils.load_json('docs/data/gammacat-sources.json')['data']
        self.gammacat_papers = gammacat.utils.load_json('docs/data/gammacat-papers.json')['data']
        self.gsed_table = Table.read('other_cats/astrisim_gsed/index2.fits')

    def list_missing_info(self):
        """Make list of info that's in astrisim/gsed, but not in gamma-cat yet.
        """
        info = []
        for source in self.gsed_table:
            info.append(self.check_source(source))
        table = Table(rows=info, names=list(info[0]))
        filename = 'other_cats/astrisim_gsed/missing_info.csv'
        print('Writing {}'.format(filename))
        table.write(filename, format='ascii.fixed_width')

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
        return ','.join(paper_ids)

    def dump_sed_to_ecsv(self):
        """Dump SED info to ECSV files.

        We will then do the other steps of adding this data to gamma-cat manually,
        i.e. find the right paper / folder / file to put the info and add info
        to the header.
        """
        base_path = Path('other_cats/astrisim_gsed/data/')
        for path in base_path.glob('*.fits'):
            source_name = path.parts[-1].replace('.fits', '')
            hdu_list = fits.open(str(path))
            hdu_names = [_.name for _ in hdu_list][1:]
            hdu_names = [name for name in hdu_names if 'MAP' not in name]
            for hdu_name in hdu_names:
                # print(path, source_name, hdu_name)
                table = Table.read(str(path), format='fits')
                table.rename_column('ENERGY', 'e_ref')
                table.rename_column('FLUX', 'dnde')
                table.rename_column('FLUX_ERROR_MIN', 'dnde_errn')
                table.rename_column('FLUX_ERROR_MAX', 'dnde_errp')

                table.meta['SOURCE_NAME'] = source_name
                try:
                    del table.meta['HISTORY']
                except:
                    pass

                filename = base_path / (source_name + '_' + hdu_name + '.ecsv')
                print('Writing {}'.format(filename))
                table.write(str(filename), format='ascii.ecsv', overwrite=True)
                # import IPython; IPython.embed(); 1/0

    def check_consistency(self):
        """Check consistency of info in `astrisim/gsed to gamma-cat.

        TODO: Not sure if it's worth scripting this!?
        """
        raise NotImplementedError


if __name__ == '__main__':
    gsed = AstriSimGSED()
    gsed.list_missing_info()
    gsed.dump_sed_to_ecsv()
    # check.check_consistency()
