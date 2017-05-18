# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from .utils import TableProcessor

__all__ = [
    'LightCurve',
]

log = logging.getLogger(__name__)


class LightCurve(TableProcessor):
    """Process and validate a lightcurve file."""
    resource_type = 'lightcurve'

    expected_colnames_output = [
        'time', 'time_min', 'time_max',
        'e_min', 'e_max',
        'flux', 'flux_err', 'flux_ul',
        'index', 'index_err',
        'significance',
    ]

    expected_colnames_input = expected_colnames_output + [
    ]

    output_cols = [
        dict(name='time', unit='MJD', description='Observation time'),
        dict(name='time_min', unit='MJD', description='Observation start time'),
        dict(name='time_max', unit='MJD', description='Observation stop time'),
        dict(name='e_min', unit='TeV', description='Energy bin minimum'),
        dict(name='e_max', unit='TeV', description='Energy bin maximum'),
        dict(name='flux', unit='cm-2 s-1', description='Integral photon flux'),
        dict(name='flux_err', unit='cm-2 s-1', description='Statistical error (1 sigma) on `flux`'),
        dict(name='flux_ul', unit='cm-2 s-1', description='Upper limit (at `UL_CONF` level) on `flux`'),
        dict(name='is_ul', description='Is this a flux upper limit?'),
        dict(name='index', description='Spectral index'),
        dict(name='index_err', description='Statistical error (1 sigma) on `index`'),
        dict(name='significance', description='Excess significance'),
    ]

    required_meta_keys = [
        'data_type', 'reference_id', 'source_id', 'telescope',
    ]

    allowed_meta_keys = required_meta_keys + [
        'file_id', 'source_name', 'comments', 'url', 'UL_CONF',
    ]

    def process(self):
        """Apply fixes."""
        table = self.table
        self.validate_input()

        # TODO: this is not working, not sure why.
        # ValueError: The unit 'MJD' is unrecognized.  It can not be converted to other units.
        # from make_table_columns_uniform, but code here works!???
        # with u.add_enabled_units([MJD]):
        #     print(MJD.find_equivalent_units())
        #     u.Unit('MJD')
        #     u.Quantity(42, 's').to('MJD')
        #     make_table_columns_uniform(table, self.output_cols)

        # self._process_column_order(table)
        # self.validate_output()

    def validate_input(self):
        log.debug('Validating {}'.format(self.resource))
        self.validate_table_colnames(self.expected_colnames_input)
        # self._validate_input_meta()
        # self._validate_input_consistency()
