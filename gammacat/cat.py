# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from collections import OrderedDict
from astropy.table import Table, Column
from astropy.coordinates import SkyCoord, Angle
from .info import gammacat_info
from .input import InputData
from .utils import NA, load_yaml

__all__ = ['GammaCatMaker']

log = logging.getLogger(__name__)


class GammaCatSource:
    """Gather data for one source in gamma-cat.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_inputs(cls, basic_source_info, paper_source_info):
        data = OrderedDict()

        bsi = basic_source_info.data
        cls.fill_basic_info(data, bsi)
        cls.fill_position_info(data, bsi)

        psi = paper_source_info.data
        cls.fill_spectral_info(data, psi)
        cls.fill_morphology_info(data, psi)

        return cls(data=data)

    @staticmethod
    def fill_basic_info(data, bsi):
        data['source_id'] = bsi['source_id']
        data['common_name'] = bsi.get('common_name', NA.fill_value['string'])
        data['gamma_names'] = NA.fill_list(bsi, 'gamma_names')

        data['discoverer'] = bsi.get('discoverer', NA.fill_value['string'])

    @staticmethod
    def fill_position_info(data, bsi):
        try:
            data['ra'] = bsi['pos']['ra']
        except KeyError:
            data['ra'] = NA.fill_value['number']
        try:
            data['dec'] = bsi['pos']['dec']
        except KeyError:
            data['dec'] = NA.fill_value['number']

        icrs = SkyCoord(data['ra'], data['dec'], unit='deg')
        galactic = icrs.galactic
        data['glon'] = galactic.l.deg
        data['glat'] = galactic.b.deg

    @staticmethod
    def fill_spectral_info(data, psi):
        try:
            data['spec_type'] = psi['spec']['type']
        except KeyError:
            data['spec_type'] = NA.fill_value['string']
        try:
            data['spec_theta'] = psi['spec']['theta']
        except KeyError:
            data['spec_theta'] = NA.fill_value['number']

        try:
            data['spec_norm'] = psi['spec']['norm']['val']
        except KeyError:
            data['spec_norm'] = NA.fill_value['number']
        try:
            data['spec_norm_err'] = psi['spec']['norm']['err']
        except KeyError:
            data['spec_norm_err'] = NA.fill_value['number']
        try:
            data['spec_norm_err_sys'] = psi['spec']['norm']['err_sys']
        except KeyError:
            data['spec_norm_err_sys'] = NA.fill_value['number']

        try:
            data['spec_index'] = psi['spec']['index']['val']
        except KeyError:
            data['spec_index'] = NA.fill_value['number']
        try:
            data['spec_index_err'] = psi['spec']['index']['err']
        except KeyError:
            data['spec_index_err'] = NA.fill_value['number']
        try:
            data['spec_index_err_sys'] = psi['spec']['index']['err_sys']
        except KeyError:
            data['spec_index_err_sys'] = NA.fill_value['number']

    @staticmethod
    def fill_morphology_info(data, psi):
        try:
            data['morph_type'] = psi['morph']['type']
        except KeyError:
            data['morph_type'] = NA.fill_value['string']
        try:
            val = psi['morph']['sigma']['val']
        except KeyError:
            val = NA.fill_value['number']
        # TODO: the explicit conversion to degree shpuld be avoided and
        # rather made globally
        data['morph_sigma'] = Angle(val, 'deg').degree

        try:
            err = psi['morph']['sigma']['err']
        except KeyError:
            err = NA.fill_value['number']
        data['morph_sigma_err'] = Angle(err, 'deg').degree

        try:
            val = psi['morph']['sigma2']['val']
        except KeyError:
            val = NA.fill_value['number']
        data['morph_sigma2'] = Angle(val, 'deg').degree

        try:
            err = psi['morph']['sigma2']['err']
        except KeyError:
            err = NA.fill_value['number']
        data['morph_sigma2_err'] = Angle(err, 'deg').degree

        try:
            val = psi['morph']['pa']['val']
        except KeyError:
            val = NA.fill_value['number']
        data['morph_pa'] = Angle(val, 'deg').degree
        try:
            err = psi['morph']['pa']['err']
        except KeyError:
            err = NA.fill_value['number']
        data['morph_pa_err'] = Angle(err, 'deg').degree
        try:
            data['morph_pa_frame'] = psi['morph']['pa']['frame']
        except KeyError:
            data['morph_pa_frame'] = NA.fill_value['string']



    def row_dict(self):
        """Data in a row dict format.
        """
        return self.data


class GammaCatSchema:
    """Helper class to apply the schema."""

    def __init__(self):
        self.colspecs = load_yaml(gammacat_info.base_dir / 'input/schemas/gamma_cat.yaml')

    def format_table(self, in_table):
        """Make a new table, formatting things according to this schema.

        * Drop columns that are not in schema or table (but emit warning)
        * Order columns by schema.
        * Make dtype, fmt, description as given in the schema
        """
        table = Table(meta=in_table.meta)
        for colspec in self.colspecs:
            name = colspec['name']
            col = Column(
                data=in_table[name],
                name=colspec['name'],
                dtype=colspec['dtype'],
                # fmt=colspec['fmt'],
                unit=colspec['unit'],
                description=colspec['description'],
            )
            table.add_column(col)

        return table

        # @property
        # def names(self):
        #     return [_['name'] for _ in self.colspecs]
        #
        # @property
        # def dtype(self):
        #     return [_['dtype'] for _ in self.colspecs]

        # def filter_row_keys(self, rows):
        #     for row in rows:
        #         for key in list(row.keys()):
        #             if key not in names:
        #                 del row[key]


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

            # for now choose the first valid paper in the list
            paper_id = basic_source_info.data['papers'][0]
            paper_info = input_data.papers.get_paper_by_id(paper_id)
            paper_source_info = paper_info.get_source_by_id(source_id)

            source = GammaCatSource.from_inputs(
                basic_source_info=basic_source_info,
                paper_source_info=paper_source_info,
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

        schema = GammaCatSchema()
        # schema.filter_row_keys(rows)
        # table = Table(rows=rows, meta=meta, names=schema.names, dtype=schema.dtype)
        table = Table(rows=rows)
        table = schema.format_table(table)
        self.table = table

    def write_table(self):
        table = self.table

        # table.info('stats')
        # table.pprint()

        path = gammacat_info.base_dir / 'docs/data/gammacat.ecsv'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='ascii.ecsv')

        path = gammacat_info.base_dir / 'docs/data/gammacat.fits.gz'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='fits', overwrite=True)
