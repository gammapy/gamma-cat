# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from collections import OrderedDict
from pprint import pprint
import numpy as np
from astropy import units as u
from astropy.units import Quantity
from astropy.table import Table, Column
from astropy.coordinates import SkyCoord, Angle
from gammapy.spectrum.models import PowerLaw, PowerLaw2, ExponentialCutoffPowerLaw
from gammapy.spectrum import CrabSpectrum
from .info import gammacat_info
from .input import InputData
from .utils import NA, load_yaml, write_yaml, table_to_list_of_dict, validate_schema

__all__ = [
    'GammaCatMaker',
    'GammaCatSchema',
    'GammaCatSource',
    'GammaCatDataSetConfig',
    'GammaCatDatasetConfigSource',
]

log = logging.getLogger(__name__)

# TODO: replace flux factor by reading the correct units from the schema
FLUX_FACTOR = 1E-12


def _to_crab_flux():
    # Integral flux above 1 TeV in crab units
    crab = CrabSpectrum('meyer').model
    flux_crab = crab.integral(1 * u.TeV, 1e6 * u.TeV)
    return 100 / flux_crab.to('cm-2 s-1').value

FLUX_TO_CRAB = _to_crab_flux()


class GammaCatSource:
    """Gather data for one source in gamma-cat.
    """

    SED_ARRAY_LEN = 40

    def __init__(self, data):
        self.data = data
        self.fill_derived_spectral_info()

    @classmethod
    def from_inputs(cls, basic_source_info, dataset_source_info, sed_info):
        data = OrderedDict()

        bsi = basic_source_info.data
        cls.fill_basic_info(data, bsi)

        dsi = dataset_source_info.data
        cls.fill_position_info(data, dsi)
        cls.fill_data_info(data, dsi)
        cls.fill_spectral_info(data, dsi)
        cls.fill_morphology_info(data, dsi)

        cls.fill_sed_info(data, sed_info)
        return cls(data=data)

    @staticmethod
    def fill_basic_info(data, bsi):
        data['source_id'] = bsi['source_id']
        data['common_name'] = bsi.get('common_name', NA.fill_value['string'])

        data['gamma_names'] = NA.fill_list(bsi, 'gamma_names')
        data['fermi_names'] = NA.fill_list(bsi, 'fermi_names')
        data['other_names'] = NA.fill_list(bsi, 'other_names')

        data['where'] = bsi.get('where', NA.fill_value['string'])
        classes = bsi.get('classes', NA.fill_value['list'])
        data['classes'] = ','.join(classes)

        data['discoverer'] = bsi.get('discoverer', NA.fill_value['string'])
        data['seen_by'] = NA.fill_list(bsi, 'seen_by')
        data['discovery_date'] = bsi.get('discovery_date', NA.fill_value['string'])

        data['tevcat_id'] = bsi.get('tevcat_id', NA.fill_value['number'])
        data['tevcat2_id'] = bsi.get('tevcat2_id', NA.fill_value['string'])
        data['tevcat_name'] = bsi.get('tevcat_name', NA.fill_value['string'])

        data['tgevcat_id'] = bsi.get('tgevcat_id', NA.fill_value['number'])
        data['tgevcat_name'] = bsi.get('tgevcat_name', NA.fill_value['string'])

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

        data['reference_ids'] = NA.fill_list(bsi, 'reference_ids')

    @staticmethod
    def fill_position_info(data, dsi):
        try:
            data['pos_glon'] = Angle(dsi['pos']['glon']['val']).degree
            data['pos_glat'] = Angle(dsi['pos']['glat']['val']).degree

            galactic = SkyCoord(data['pos_glon'], data['pos_glat'], frame='galactic', unit='deg')
            data['pos_ra'] = galactic.icrs.ra.deg
            data['pos_dec'] = galactic.icrs.dec.deg

        except KeyError:
            try:
                data['pos_ra'] = Angle(dsi['pos']['ra']['val']).degree
                data['pos_dec'] = Angle(dsi['pos']['dec']['val']).degree

                icrs = SkyCoord(data['pos_ra'], data['pos_dec'], unit='deg')
                data['pos_glon'] = icrs.galactic.l.deg
                data['pos_glat'] = icrs.galactic.b.deg
            except KeyError:
                data['pos_ra'] = NA.fill_value['number']
                data['pos_dec'] = NA.fill_value['number']
                data['pos_glon'] = NA.fill_value['number']
                data['pos_glat'] = NA.fill_value['number']

        try:
            x_err = Angle(dsi['pos']['glon']['err']).degree
            y_err = Angle(dsi['pos']['glat']['err']).degree
        except KeyError:
            try:
                x_err = Angle(dsi['pos']['ra']['err']).degree
                y_err = Angle(dsi['pos']['dec']['err']).degree
            except KeyError:
                x_err = NA.fill_value['number']
                y_err = NA.fill_value['number']

        data['pos_err'] = np.sqrt(x_err * y_err)

    @staticmethod
    def fill_data_info(data, dsi):
        try:
            data['significance'] = dsi['data']['significance']
        except KeyError:
            data['significance'] = NA.fill_value['number']

        try:
            data['livetime'] = dsi['data']['livetime']
        except KeyError:
            data['livetime'] = NA.fill_value['number']

    @staticmethod
    def fill_spectral_info(data, dsi):
        data['reference_id'] = dsi.get('reference_id', NA.fill_value['string'])
        try:
            data['spec_type'] = dsi['spec']['type']
        except KeyError:
            data['spec_type'] = 'none'
        try:
            data['spec_erange_min'] = dsi['spec']['erange']['min']
        except KeyError:
            data['spec_erange_min'] = NA.fill_value['number']
        try:
            data['spec_erange_max'] = dsi['spec']['erange']['max']
        except KeyError:
            data['spec_erange_max'] = NA.fill_value['number']
        try:
            data['spec_theta'] = Angle(dsi['spec']['theta']).degree
        except KeyError:
            data['spec_theta'] = NA.fill_value['number']

        try:
            data['spec_norm'] = dsi['spec']['norm']['val'] * FLUX_FACTOR
        except KeyError:
            data['spec_norm'] = NA.fill_value['number']
        try:
            data['spec_norm_err'] = dsi['spec']['norm']['err'] * FLUX_FACTOR
        except KeyError:
            data['spec_norm_err'] = NA.fill_value['number']
        try:
            data['spec_norm_err_sys'] = dsi['spec']['norm']['err_sys'] * FLUX_FACTOR
        except KeyError:
            data['spec_norm_err_sys'] = NA.fill_value['number']
        try:
            data['spec_ref'] = dsi['spec']['ref']
        except KeyError:
            data['spec_ref'] = NA.fill_value['number']

        try:
            data['spec_index'] = dsi['spec']['index']['val']
        except KeyError:
            data['spec_index'] = NA.fill_value['number']
        try:
            data['spec_index_err'] = dsi['spec']['index']['err']
        except KeyError:
            data['spec_index_err'] = NA.fill_value['number']
        try:
            data['spec_index_err_sys'] = dsi['spec']['index']['err_sys']
        except KeyError:
            data['spec_index_err_sys'] = NA.fill_value['number']

        try:
            data['spec_ecut'] = dsi['spec']['ecut']['val']
        except KeyError:
            data['spec_ecut'] = NA.fill_value['number']
        try:
            data['spec_ecut_err'] = dsi['spec']['ecut']['err']
        except KeyError:
            data['spec_ecut_err'] = NA.fill_value['number']

    @staticmethod
    def fill_sed_info(data, sed_info, shape=(SED_ARRAY_LEN,)):
        """
        Fill flux point info data.
        """
        try:
            data['sed_reference_id'] = sed_info.table.meta['reference_id']
        except KeyError:
            data['sed_reference_id'] = NA.fill_value['string']
        try:
            e_ref = sed_info.table['e_ref'].data
            data['sed_e_ref'] = NA.resize_sed_array(e_ref, shape)
        except KeyError:
            data['sed_e_ref'] = NA.fill_value_array(shape)
        try:
            e_min = sed_info.table['e_min'].data
            data['sed_e_min'] = NA.resize_sed_array(e_min, shape)
        except KeyError:
            data['sed_e_min'] = NA.fill_value_array(shape)

        try:
            e_max = sed_info.table['e_max'].data
            data['sed_e_max'] = NA.resize_sed_array(e_max, shape)
        except KeyError:
            data['sed_e_max'] = NA.fill_value_array(shape)

        try:
            dnde = sed_info.table['dnde'].data
            data['sed_dnde'] = NA.resize_sed_array(dnde, shape)
        except KeyError:
            data['sed_dnde'] = NA.fill_value_array(shape)
        try:
            dnde_err = sed_info.table['dnde_err'].data
            data['sed_dnde_err'] = NA.resize_sed_array(dnde_err, shape)
        except KeyError:
            data['sed_dnde_err'] = NA.fill_value_array(shape)
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
        try:
            dnde_ul = sed_info.table['dnde_ul'].data
            data['sed_dnde_ul'] = NA.resize_sed_array(dnde_ul, shape)
        except KeyError:
            data['sed_dnde_ul'] = NA.fill_value_array(shape)

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
        emin, emax = 1 * u.TeV, 1E6 * u.TeV
        flux_above_1TeV = spec_model.integral_error(emin, emax)
        data['spec_flux_above_1TeV'] = flux_above_1TeV[0].value
        data['spec_flux_above_1TeV_err'] = flux_above_1TeV[1].value

        data['spec_flux_above_1TeV_crab'] = data['spec_flux_above_1TeV'] * FLUX_TO_CRAB
        data['spec_flux_above_1TeV_crab_err'] = data['spec_flux_above_1TeV_err'] * FLUX_TO_CRAB

        # Integral flux above erange_min
        emin, emax = data['spec_erange_min'] * u.TeV, 1e6 * u.TeV
        try:
            flux_above_erange_min = spec_model.integral_error(emin, emax)
            data['spec_flux_above_erange_min'] = flux_above_erange_min[0].value
            data['spec_flux_above_erange_min_err'] = flux_above_erange_min[1].value
        except ValueError:
            data['spec_flux_above_erange_min'] = NA.fill_value['number']
            data['spec_flux_above_erange_min_err'] = NA.fill_value['number']

        # Energy flux between 1 TeV and 10 TeV
        emin, emax = 1 * u.TeV, 1E6 * u.TeV
        energy_flux = spec_model.energy_flux_error(emin, emax)
        data['spec_energy_flux_1TeV_10TeV'] = energy_flux[0].value
        data['spec_energy_flux_1TeV_10TeV_err'] = energy_flux[1].value

        # Differential flux at 1 TeV
        dnde = spec_model.evaluate_error(1 * u.TeV)
        data['spec_norm_1TeV'] = dnde[0].value
        data['spec_norm_1TeV_err'] = dnde[1].value

    def _get_spec_model(self, data):
        # TODO: what about systematic errors?

        spec_type = data['spec_type']
        pars, errs = {}, {}

        if spec_type == 'pl':
            pars['amplitude'] = Quantity(data['spec_norm'], 'cm-2 s-1 TeV-1')
            errs['amplitude'] = Quantity(data['spec_norm_err'], 'cm-2 s-1 TeV-1')
            pars['index'] = Quantity(data['spec_index'], '')
            errs['index'] = Quantity(data['spec_index_err'], '')
            pars['reference'] = Quantity(data['spec_ref'], 'TeV')
            model = PowerLaw(**pars)
        elif spec_type == 'pl2':
            # TODO: what parameter to use to pass emin here correctly??
            # TODO: put default max of 1e10 TeV
            pars['amplitude'] = Quantity(data['spec_norm'], 'cm-2 s-1')
            errs['amplitude'] = Quantity(data['spec_norm_err'], 'cm-2 s-1')
            pars['index'] = Quantity(data['spec_index'], '')
            errs['index'] = Quantity(data['spec_index_err'], '')
            pars['emin'] = Quantity(data['spec_erange_min'], 'TeV')
            emax = data['spec_erange_max']
            if np.isnan(emax):
                emax = 1e5
            pars['emax'] = Quantity(emax, 'TeV')
            model = PowerLaw2(**pars)
        elif spec_type == 'ecpl':
            from uncertainties import ufloat
            pars['amplitude'] = Quantity(data['spec_norm'], 'cm-2 s-1 TeV-1')
            errs['amplitude'] = Quantity(data['spec_norm_err'], 'cm-2 s-1 TeV-1')
            pars['index'] = Quantity(data['spec_index'], '')
            errs['index'] = Quantity(data['spec_index_err'], '')
            pars['reference'] = Quantity(data['spec_ref'], 'TeV')
            lambda_ = 1. / ufloat(data['spec_ecut'], data['spec_ecut_err'])
            pars['lambda_'] = Quantity(lambda_.n, 'TeV-1')
            errs['lambda_'] = Quantity(lambda_.s, 'TeV-1')
            model = ExponentialCutoffPowerLaw(**pars)
        else:
            # return generic model, as all parameters are NaN it will evaluate to NaN
            pars['amplitude'] = Quantity(data['spec_norm'], 'cm-2 s-1 TeV-1')
            errs['amplitude'] = Quantity(data['spec_norm_err'], 'cm-2 s-1 TeV-1')
            pars['index'] = Quantity(data['spec_index'], '')
            errs['index'] = Quantity(data['spec_index_err'], '')
            pars['reference'] = Quantity(data['spec_ref'], 'TeV')
            model = PowerLaw(**pars)

        model.parameters.set_parameter_errors(errs)
        return model

    @staticmethod
    def fill_morphology_info(data, dsi):
        try:
            data['morph_type'] = dsi['morph']['type']
        except KeyError:
            data['morph_type'] = 'none'

        try:
            val = Angle(dsi['morph']['sigma']['val']).degree
        except KeyError:
            val = NA.fill_value['number']
        data['morph_sigma'] = val

        try:
            err = dsi['morph']['sigma']['err']
        except KeyError:
            err = NA.fill_value['number']
        data['morph_sigma_err'] = Angle(err, 'deg').degree

        try:
            val = dsi['morph']['sigma2']['val']
        except KeyError:
            val = NA.fill_value['number']
        data['morph_sigma2'] = Angle(val, 'deg').degree

        try:
            err = dsi['morph']['sigma2']['err']
        except KeyError:
            err = NA.fill_value['number']
        data['morph_sigma2_err'] = Angle(err, 'deg').degree

        try:
            val = dsi['morph']['pa']['val']
        except KeyError:
            val = NA.fill_value['number']
        data['morph_pa'] = Angle(val, 'deg').degree
        try:
            err = dsi['morph']['pa']['err']
        except KeyError:
            err = NA.fill_value['number']
        data['morph_pa_err'] = Angle(err, 'deg').degree
        try:
            data['morph_pa_frame'] = dsi['morph']['pa']['frame']
        except KeyError:
            data['morph_pa_frame'] = NA.fill_value['string']

    def row_dict(self):
        """Data in a row dict format.
        """
        return self.data


class GammaCatSchema:
    """Helper class to apply the schema."""

    def __init__(self):
        self.colspecs = load_yaml(gammacat_info.base_dir / 'input/gammacat/gamma_cat_columns.yaml')

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


class GammaCatMaker:
    """
    Make gamma-cat, combining all available data.

    TODO: for now, we gather info from `InputData`.
    This should be changed to gather info from `OutputData` when available.
    """

    def __init__(self):
        self.sources = []
        self.table = None

    def run(self, internal):
        log.info('Making gamma-cat ....')

        self.gather_data(internal=internal)
        self.make_table()
        self.write_table(internal=internal)
        self.write_yaml_text_dump(internal=internal)

    def gather_data(self, internal=False):
        """Gather data into Python data structures."""
        input_data = InputData.read(internal=internal)
        source_ids = [_.data['source_id'] for _ in input_data.sources.data]

        for source_id in source_ids:
            basic_source_info = input_data.sources.get_source_by_id(source_id)
            log.info('Processing : {}'.format(basic_source_info))
            try:
                config = input_data.gammacat_dataset_config.get_source_by_id(source_id)
                reference_id = config.get_reference_id(internal=internal)
            except IndexError:
                reference_id = None

            # TODO: right now this implies, that a GammaCatSource object can only
            # handle the information from one dataset, maybe this should be changed
            dataset = input_data.datasets.get_dataset_by_reference_id(reference_id)
            dataset_source_info = dataset.get_source_by_id(source_id)
            sed_info = input_data.seds.get_sed_by_source_and_reference_id(source_id, dataset.reference_id)

            source = GammaCatSource.from_inputs(
                basic_source_info=basic_source_info,
                dataset_source_info=dataset_source_info,
                sed_info=sed_info
            )
            self.sources.append(source)

    def make_table(self):
        """Convert Python data structures to a flat table."""
        rows = [source.row_dict() for source in self.sources]

        # Passing Quantity objects to `Table(rows=rows)` doesn't work.
        # So for now, we drop units here
        # (we could also make Table column by column ourselves
        for colname in rows[0].keys():
            if isinstance(rows[0][colname], Quantity):
                print('Found Quantity:', colname)
                unit = rows[0][colname].unit
                for idx, row in enumerate(rows):
                    d = row[colname]
                    if d.unit != unit:
                        # This should never happen.
                        # But it did due to a coding error in the past.
                        print('colname:', colname)
                        print('row:', row)
                        raise RuntimeError('Inconsistent units!')
                    else:
                        rows[idx][colname] = d.value

        meta = OrderedDict()
        meta['name'] = 'gamma-cat'
        meta['description'] = 'A catalog of TeV gamma-ray sources'
        meta['version'] = gammacat_info.version
        meta['url'] = 'https://github.com/gammapy/gamma-cat/'

        schema = GammaCatSchema()
        # schema.filter_row_keys(rows)
        # table = Table(rows=rows, meta=meta, names=schema.names, dtype=schema.dtype)
        # import IPython; IPython.embed(); 1/0

        # This is just for debugging ...
        # for colname in rows[0].keys():
        #     print(colname)
        #     d = [row[colname] for row in rows]
        #     print(colname)
        #     print(d)
        #     Table(data={colname: d})

        table = Table(rows=rows)
        table = schema.format_table(table)

        # Sort sources by right ascension `ra`
        # And where `ra` is identical, use `dec` and `source_id` to order.
        table.sort(['ra', 'dec', 'source_id'])

        self.table = table

    def write_table(self, internal=False):
        table = self.table

        # table.info('stats')
        # table.pprint()
        if internal:
            path = gammacat_info.internal_dir / 'gammacat-hess-internal.fits.gz'
        else:
            path = gammacat_info.base_dir / 'docs/data/gammacat.fits.gz'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='fits', overwrite=True)

        # path = gammacat_info.base_dir / 'docs/data/gammacat.ecsv'
        # log.info('Writing {}'.format(path))
        # table.write(str(path), format='ascii.ecsv')

    def write_yaml_text_dump(self, internal=False):
        column_selection = [_ for _ in self.table.colnames if not 'sed_' in _]
        table = self.table[column_selection]
        data = table_to_list_of_dict(table)

        if internal:
            path = gammacat_info.internal_dir / 'gammacat-hess-internal.yaml'
        else:
            path = gammacat_info.base_dir / 'docs/data/gammacat.yaml'

        log.info('Writing {}'.format(path))
        write_yaml(data, path)


class GammaCatDatasetConfigSource:
    """
    Configuration how to assemble `gamma-cat` for one source.
    """

    def __init__(self, data):
        self.data = data

    @property
    def reference_ids(self):
        pid = self.data['reference_id']

        if isinstance(pid, str):
            return [_.strip() for _ in pid.split(',')]
        elif pid is None:
            return []
        else:
            raise ValueError('Invalid reference_id list: {}'.format(pid))

    def get_reference_id(self, internal=False):
        """Choose reference_id to use for given source.

        For now, we always use the last one listed.
        """
        reference_id = self.reference_ids[-1]
        if not internal and reference_id == 'gammacat-hess-internal':
            reference_id = self.reference_ids[-2]
        return reference_id


class GammaCatDataSetConfig:
    """
    Configuration how to assemble `gamma-cat` for all sources.
    """
    schema = load_yaml(gammacat_info.base_dir / 'input/schemas/gamma_cat_dataset.schema.yaml')

    def __init__(self, data, path):
        self.data = data
        self.path = path

    @classmethod
    def read(cls):
        path = gammacat_info.base_dir / 'input/gammacat/gamma_cat_dataset.yaml'
        data = load_yaml(path)
        return cls(data=data, path=path)

    @property
    def source_ids(self):
        return [_['source_id'] for _ in self.data]

    @property
    def source_configs(self):
        for source_id in self.source_ids:
            yield self.get_source_by_id(source_id)

    @property
    def reference_ids(self):
        pids = set()
        for source_config in self.source_configs:
            pids.update(source_config.reference_ids)

        return sorted(pids)

    def get_source_by_id(self, source_id):
        idx = self.source_ids.index(source_id)
        return GammaCatDatasetConfigSource(data=self.data[idx])

    def validate(self, input_data):
        log.info('Validating `input/gammacat/gamma_cat_dataset.yaml`')
        validate_schema(path=self.path, data=self.data, schema=self.schema)
        self.validate_source_ids(input_data)
        self.validate_reference_ids(input_data)

    def validate_source_ids(self, input_data):
        """Check that all sources are listed.
        """
        source_id_basic = input_data.sources.source_ids
        source_id_gammacat = self.source_ids

        gammacat_missing = sorted(set(source_id_basic) - set(source_id_gammacat))
        if gammacat_missing:
            log.error('Sources in `input/sources`, but not in `input/gammacat/gamma_cat_dataset.yaml`: {}'
                      ''.format(gammacat_missing))

        basic_missing = sorted(set(source_id_gammacat) - set(source_id_basic))
        if basic_missing:
            log.error('Sources in `input/gammacat/gamma_cat_dataset.yaml`, but not in `input/sources`: {}'
                      ''.format(basic_missing))

    def validate_reference_ids(self, input_data):
        """Check that all reference_ids are listed.

        TODO: this is not a good check. One dataset could have multiple sources, i.e. should be listed multiple times.
        """
        reference_ids_folders = input_data.datasets.reference_ids
        reference_ids_gammacat = self.reference_ids

        gammacat_missing = sorted(set(reference_ids_gammacat) - set(reference_ids_folders))
        if gammacat_missing:
            log.error('Datasets in `input/gammacat/gamma_cat_dataset.yaml`, but not in `input/data`: {}'
                      ''.format(gammacat_missing))

        folders_missing = sorted(set(reference_ids_folders) - set(reference_ids_gammacat))
        if folders_missing:
            log.error('Sources in `input/data`, but not in `input/gammacat/gamma_cat_dataset.yaml`: {}'
                      ''.format(folders_missing))
