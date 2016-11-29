# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from collections import OrderedDict
import numpy as np
from astropy.table import Table, Column
from astropy.coordinates import SkyCoord, Angle
from gammapy.spectrum.models import PowerLaw, PowerLaw2, ExponentialCutoffPowerLaw
from .info import gammacat_info
from .input import InputData
from .utils import NA, load_yaml

__all__ = ['GammaCatMaker']

log = logging.getLogger(__name__)


#TODO: replace flux factor by reading the correct units from the schema
FLUX_FACTOR = 1E-12

class GammaCatSource:
    """Gather data for one source in gamma-cat.
    """

    def __init__(self, data):
        self.data = data
        self.fill_derived_spectral_info()

    @classmethod
    def from_inputs(cls, basic_source_info, paper_source_info, sed_info):
        data = OrderedDict()

        bsi = basic_source_info.data
        cls.fill_basic_info(data, bsi)
        cls.fill_position_info(data, bsi)

        psi = paper_source_info.data
        cls.fill_data_info(data, psi)
        cls.fill_spectral_info(data, psi)
        cls.fill_morphology_info(data, psi)

        cls.fill_sed_info(data, sed_info)
        return cls(data=data)

    @staticmethod
    def fill_basic_info(data, bsi):
        data['source_id'] = bsi['source_id']
        data['common_name'] = bsi.get('common_name', NA.fill_value['string'])
        data['gamma_names'] = NA.fill_list(bsi, 'gamma_names')
        data['other_names'] = NA.fill_list(bsi, 'other_names')
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
    def fill_data_info(data, psi):
        try:
            data['significance'] = psi['data']['significance']
        except KeyError:
            data['significance'] = NA.fill_value['number']

        try:
            data['livetime'] = psi['data']['livetime']
        except KeyError:
            data['livetime'] = NA.fill_value['number']


    @staticmethod
    def fill_spectral_info(data, psi):
        data['paper_id'] = psi.get('paper_id', NA.fill_value['string'])
        try:
            data['spec_type'] = psi['spec']['type']
        except KeyError:
            data['spec_type'] = NA.fill_value['string']
        try:
            data['spec_erange_min'] = psi['spec']['erange']['min']
        except KeyError:
            data['spec_erange_min'] = NA.fill_value['number']
        try:
            data['spec_erange_max'] = psi['spec']['erange']['max']
        except KeyError:
            data['spec_erange_max'] = NA.fill_value['number']
        try:
            data['spec_theta'] = psi['spec']['theta']
        except KeyError:
            data['spec_theta'] = NA.fill_value['number']

        try:
            data['spec_norm'] = psi['spec']['norm']['val'] * FLUX_FACTOR
        except KeyError:
            data['spec_norm'] = NA.fill_value['number']
        try:
            data['spec_norm_err'] = psi['spec']['norm']['err'] * FLUX_FACTOR
        except KeyError:
            data['spec_norm_err'] = NA.fill_value['number']
        try:
            data['spec_norm_err_sys'] = psi['spec']['norm']['err_sys'] * FLUX_FACTOR
        except KeyError:
            data['spec_norm_err_sys'] = NA.fill_value['number']
        try:
            data['spec_ref'] = psi['spec']['ref']
        except KeyError:
            data['spec_ref'] = NA.fill_value['number']

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

        try:
            data['spec_ecut'] = psi['spec']['ecut']['val']
        except KeyError:
            data['spec_ecut'] = NA.fill_value['number']
        try:
            data['spec_ecut_err'] = psi['spec']['ecut']['err']
        except KeyError:
            data['spec_ecut_err'] = NA.fill_value['number']

    @staticmethod
    def fill_sed_info(data, sed_info, shape=(40,)):
        """
        Fill flux point info data.
        """
        #if len(sed_info.table) > 0:
        #    from IPython import embed; embed(); 1/0
        try:
            e_ref = sed_info.table['e_ref'].data
            data['sed_e_ref'] = NA.resize_sed_array(e_ref, shape)
        except KeyError:
            data['sed_e_ref'] = NA.fill_value_array(shape)
        try:
            dnde = sed_info.table['dnde'].data
            data['sed_dnde'] = NA.resize_sed_array(dnde, shape)
        except KeyError:
            data['sed_dnde'] = NA.fill_value_array(shape)
        try:
            dnde_errp = sed_info.table['dnde_errp'].data
            data['sed_dnde_errp'] = NA.resize_sed_array(dnde_errp, shape)
        except KeyError:
            data['sed_dnde_errp'] = NA.fill_value_array(shape)
        try:
            dnde_errn = sed_info.table['dnde_errn'].data
            data['sed_dnde_errn'] = NA.resize_sed_array(dnde_errn, shape)
        except KeyError:
            data['sed_dnde_errn'] = NA.fill_value_array(shape)

    def fill_derived_spectral_info(self):
        """
        Fill derived spectral info computed from basic parameters
        """
        data = self.data
        # total errors
        data['spec_norm_err_tot'] = np.hypot(data['spec_norm_err'], data['spec_norm_err_sys'])
        data['spec_index_err_tot'] = np.hypot(data['spec_index_err'], data['spec_index_err_sys'])

        spec_model = self._get_spec_model(data)

        # Integral flux above 1 TeV
        emin, emax = 1, 1E6 # TeV
        flux_above_1TeV = spec_model.integral(emin, emax)
        data['spec_flux_above_1TeV'] = flux_above_1TeV.n

        data['spec_flux_above_1TeV_err'] = flux_above_1TeV.s

        # Energy flux between 1 TeV and 10 TeV
        emin, emax = 1, 10 # TeV
        energy_flux = spec_model.energy_flux(emin, emax)

        data['spec_energy_flux_1TeV_10TeV'] = energy_flux.n
        data['spec_energy_flux_1TeV_10TeV_err'] = energy_flux.s

        norm_1TeV = spec_model(1) # TeV
        data['spec_norm_1TeV'] = norm_1TeV.n
        data['spec_norm_1TeV_err'] = norm_1TeV.s


    def _get_spec_model(self, data):
        from uncertainties import ufloat
        spec_type = data['spec_type']

        # TODO: what about systematic errors?
        index = ufloat(data['spec_index'], data['spec_index_err'])
        amplitude = ufloat(data['spec_norm'], data['spec_norm_err'])
        reference = data['spec_ref']

        if spec_type == 'pl':
            model = PowerLaw(index, amplitude, reference)
        elif spec_type == 'pl2':
            model = PowerLaw2(amplitude, index, reference, 1E10)
        elif spec_type == 'ecpl':
            lambda_ = 1. / ufloat(data['spec_ecut'], data['spec_ecut_err'])
            model = ExponentialCutoffPowerLaw(index, amplitude, reference, lambda_)
        else:
            #return generic model, as all parameters are NaN it will
            # evaluate to NaN
            model = PowerLaw(index, amplitude, reference)
        return model

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
        # TODO: the explicit conversion to degree should be avoided and
        # rather made on the whole column
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
            paper_info = self.choose_paper(input_data, basic_source_info.data['papers'])
            paper_source_info = paper_info.get_source_by_id(source_id)
            sed_info = input_data.seds.get_sed_by_source_id(source_id)

            # TODO: right now this implies, that a GammaCatSource object can only
            # handle the information from one paper, maybe this should be changed
            source = GammaCatSource.from_inputs(
                basic_source_info=basic_source_info,
                paper_source_info=paper_source_info,
                sed_info=sed_info
            )
            self.sources.append(source)

    def choose_paper(self, input_data, paper_ids, method='first-available'):
        """Choose paper refrence for singel source according to different criteria"""

        if method == 'first-available':
            # choose the first paper in the list, where info on the source
            # is actually available
            for paper_id in paper_ids:
                paper_info = input_data.papers.get_paper_by_id(paper_id)
                if len(paper_info.sources) > 0:
                    break
            return paper_info

        elif method == 'first':
            # choose first entry of the list
            return input_data.papers.get_paper_by_id(paper_ids[0])

        elif method == 'latest':
            # choose latest paper
            raise NotImplementedError
        else:
            raise ValueError('Not a valid method.')

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
        path = gammacat_info.base_dir / 'docs/data/gammacat.fits.gz'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='fits', overwrite=True)

        #path = gammacat_info.base_dir / 'docs/data/gammacat.ecsv'
        #log.info('Writing {}'.format(path))
        #table.write(str(path), format='ascii.ecsv')

