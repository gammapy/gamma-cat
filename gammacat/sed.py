# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from astropy.table import Table

__all__ = [
    'SED',
]

log = logging.getLogger(__name__)


class SED:
    """Process and validate an SED file."""

    expected_colnames_output = [
        'e_ref', 'e_min', 'e_max',
        'dnde', 'dnde_err', 'dnde_errn', 'dnde_errp', 'dnde_ul', 'is_ul',
        'excess', 'significance',
    ]

    expected_colnames_input = expected_colnames_output + [
        'e_lo', 'e_hi', 'e_ref_err',
        'dnde_min', 'dnde_max',
        'e2dnde', 'e2dnde_err', 'e2dnde_errn', 'e2dnde_errp', 'e2dnde_ul',
    ]

    required_meta_keys = [
        'data_type', 'reference_id', 'source_id', 'telescope',
    ]

    allowed_meta_keys = required_meta_keys + [
        'file_id', 'source_name', 'comments', 'url', 'UL_CONF',
    ]

    def __init__(self, table, path):
        self.table = table
        self.path = path

    @classmethod
    def read(cls, path, format='ascii.ecsv'):
        log.debug('Reading {}'.format(path))
        table = Table.read(str(path), format=format)
        return cls(table=table, path=path)

    def process(self):
        """Apply fixes."""
        table = self.table
        self.validate_input()

        self._process_energy_ranges(table)
        self._process_flux_errrors(table)
        self._process_ul_conf(table)

        self._add_missing_defaults(table)
        self._process_e2dnde_inputs(table)
        self._make_it_uniform(table)
        self._process_column_order(table)

        self.validate_output()

    @staticmethod
    def _process_energy_ranges(table):
        """
        Sometimes energy bin ranges are given as `(e_lo, e_hi)`,
        Those columns are not standard in the SED spec.
        We convert those to `(e_min, e_max)`
        """
        if 'e_lo' in table.colnames:
            table['e_min'] = table['e_ref'] - table['e_lo']
            del table['e_lo']

        if 'e_hi' in table.colnames:
            table['e_max'] = table['e_ref'] + table['e_hi']
            del table['e_hi']

        if 'e_ref_err' in table.colnames:
            del table['e_ref_err']

    @staticmethod
    def _process_flux_errrors(table):
        """
        Sometimes flux errors are given as `(dnde_min, dnde_max)`,
        i.e. 68% confidence level (1 sigma) limits.
        Those columns are not standard in the SED spec.
        We convert those to `dnde_errn` and `dnde_errp`.
        """
        if 'dnde_min' in table.colnames:
            table['dnde_errn'] = table['dnde'] - table['dnde_min']
            del table['dnde_min']
        if 'dnde_max' in table.colnames:
            table['dnde_errp'] = table['dnde_max'] - table['dnde']
            del table['dnde_max']

    @staticmethod
    def _process_ul_conf(table):
        m = table.meta
        if 'UL_CONF' in m:
            if m['UL_CONF'] == '1 sigma':
                # Assuming here that's the two-sided central interval
                m['UL_CONF'] = 0.84

    @staticmethod
    def _add_missing_defaults(table):
        """
        Add default units and description.
        """
        for colname in table.colnames:
            if colname.startswith('e_') and not table[colname].unit:
                table[colname].unit = 'TeV'

            if colname.startswith('dnde') and not table[colname].unit:
                table[colname].unit = 'cm^-2 s^-1 TeV^-1'

            if colname == 'excess':
                table[colname].unit = 'count'

    @staticmethod
    def _make_it_uniform(table):
        """
        Make column units and description uniform
        """
        cols = [
            dict(name='e_ref', unit='TeV', description='Energy'),
            dict(name='e_min', unit='TeV', description='Energy bin minimum'),
            dict(name='e_max', unit='TeV', description='Energy bin maximum'),
            dict(name='dnde', unit='cm-2 s-1 TeV-1', description='Differential photon flux at `e_ref`'),
            dict(name='dnde_err', unit='cm-2 s-1 TeV-1', description='Statistical error (1 sigma) on `dnde`'),
            dict(name='dnde_errn', unit='cm-2 s-1 TeV-1', description='Statistical negative error (1 sigma) on `dnde`'),
            dict(name='dnde_errp', unit='cm-2 s-1 TeV-1', description='Statistical positive error (1 sigma) on `dnde`'),
            dict(name='dnde_ul', unit='cm-2 s-1 TeV-1', description='Upper limit (at `UL_CONF` level) on `dnde`'),
            dict(name='is_ul', description='Is this a flux upper limit?'),
            dict(name='excess', unit='count', description='Excess counts'),
            dict(name='significance', description='Excess significance'),
        ]
        for col in cols:
            name = col['name']
            if name in table.colnames:
                if name not in ['is_ul', 'significance']:
                    table[name] = table[name].quantity.to(col['unit'])
                table[name].description = col['description']

    @staticmethod
    def _process_e2dnde_inputs(table):
        """
        If `e2dnde` is given instead of `dnde`
        -> convert to `dnde` to have uniform standard.
        """
        colnames = [_ for _ in table.colnames if _.startswith('e2')]

        for colname in colnames:
            dnde_colname = colname[2:]
            dnde = table[colname].quantity / table['e_ref'].quantity ** 2
            table[dnde_colname] = dnde.to('cm^-2 s^-1 TeV^-1')
            del table[colname]

    def _process_column_order(self, table):
        """
        Establish a standard column order.
        """
        # See "Select or reorder columns" section at
        # http://astropy.readthedocs.io/en/latest/table/modify_table.html
        colnames = [_ for _ in self.expected_colnames_output if _ in table.colnames]

        # Don't silently drop columns!
        dropped_colnames = sorted(set(table.colnames) - set(colnames))
        if dropped_colnames:
            log.error(
                'SED file {} - dropping columns: {}'
                ''.format(self.path, dropped_colnames)
            )

        self.table = table[colnames]

    def validate_input(self):
        log.debug('Validating {}'.format(self.path))
        self._validate_input_colnames()
        self._validate_input_meta()
        self._validate_input_consistency()

    def _validate_input_colnames(self):
        table = self.table
        unexpected_colnames = sorted(set(table.colnames) - set(self.expected_colnames_input))
        if unexpected_colnames:
            log.error(
                'SED file {} contains invalid columns: {}'
                ''.format(self.path, unexpected_colnames)
            )

    def _validate_input_meta(self):
        meta = self.table.meta

        missing = sorted(set(self.required_meta_keys) - set(meta.keys()))
        if missing:
            log.error('SED file {} contains missing meta keys: {}'.format(self.path, missing))

        extra = sorted(set(meta.keys()) - set(self.allowed_meta_keys))
        if extra:
            log.error('SED file {} contains extra meta keys: {}'.format(self.path, extra))

        if ('comments' in meta) and not isinstance(meta['comments'], str):
            log.error('SED file {} contains invalid meta key comments (should be str): {}'
                      ''.format(self.path, meta['comments']))

    def _validate_input_consistency(self):
        table = self.table
        meta = table.meta
        colnames = table.colnames

        has_ul_col = len({'dnde_ul', 'e2dnde_ul'} & set(colnames)) > 0

        if ('UL_CONF' in meta) and not has_ul_col:
            log.error('SED file {} contains "UL_CONF" in meta, but no upper limit column.'.format(self.path))

        if has_ul_col and ('UL_CONF' not in meta):
            log.error('SED file {} contains an upper limit column, but not "UL_CONF" in meta.'.format(self.path))

    def validate_output(self):
        table = self.table
        unexpected_colnames = sorted(set(table.colnames) - set(self.expected_colnames_output))
        if unexpected_colnames:
            log.error(
                'SED file {} contains invalid columns: {}'
                ''.format(self.path, unexpected_colnames)
            )

        meta = table.meta
        if 'UL_CONF' in meta and not (0 < meta['UL_CONF'] < 1):
            log.error('SED file {} contains invalid meta "UL_CONF" value: {}'.format(self.path, meta['UL_CONF']))
