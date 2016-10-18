# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from collections import OrderedDict
from astropy.table import Table
from .info import gammacat_info
from .input import InputData
from .utils import MISSING_VAL

__all__ = ['GammaCatMaker']

log = logging.getLogger(__name__)


class GammaCatSource:
    """Gather data for one source in gamma-cat.
    """
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_inputs(cls, basic_source_info):
        data = OrderedDict()

        # import IPython; IPython.embed(); 1/0
        bsi = basic_source_info.data
        data['source_id'] = bsi['source_id']
        try:
            data['common_name'] = bsi['common_name']
        except KeyError:
            data['common_name'] = MISSING_VAL['string']
        data['discoverer'] = bsi.get('discoverer', '')
        try:
            data['gamma_names'] = ','.join(bsi['gamma_names'])
        except KeyError:
            data['gamma_names'] = MISSING_VAL['string']
        try:
            data['ra'] = bsi['pos']['ra']
        except KeyError:
            data['ra'] = MISSING_VAL['number']
        try:
            data['dec'] = bsi['pos']['dec']
        except KeyError:
            data['dec'] = MISSING_VAL['number']

        return cls(data=data)

    def row_dict(self):
        """Data in a row dict format.
        """
        return self.data


class GammaCatMaker:
    """
    Make gamma-cat, combining all available data.

    The strategy is to

    TODO: for now, we gather info from `InputData`.
    This should be changed to gather info from `OutputData` when available.
    """

    def __init__(self):
        self.sources = []
        self.table = None

    def run(self):
        log.info('Making gamma-cat ....')

        self.gather_data()
        self.make_table()
        self.write_table()

    def gather_data(self):
        """Gather data into Python data structures."""
        input_data = InputData.read()
        source_ids = [_.data['source_id'] for _ in input_data.sources.data]

        for source_id in source_ids:
            basic_source_info = input_data.sources.get_source_by_id(source_id)

            source = GammaCatSource.from_inputs(
                basic_source_info=basic_source_info,
            )
            self.sources.append(source)

    def make_table(self):
        """Convert Python data structures to a flat table."""
        rows = [source.row_dict() for source in self.sources]

        meta = OrderedDict()
        meta['name'] = 'gamma-cat'
        meta['description'] = 'A catalog of TeV gamma-ray sources'
        meta['version'] = gammacat_info.version
        meta['url'] = 'https://github.com/gammapy/gamma-cat/'

        # TODO: read catalog YAML file with names in
        # good order, format and description set.
        names = list(rows[0].keys())
        table = Table(rows=rows, meta=meta, names=names)
        self.table = table

    def write_table(self):
        table = self.table

        table.info('stats')
        table.pprint()

        path = gammacat_info.base_dir / 'docs/data/gammacat.ecsv'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='ascii.ecsv')

        path = gammacat_info.base_dir / 'docs/data/gammacat.fits'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='fits', overwrite=True)
