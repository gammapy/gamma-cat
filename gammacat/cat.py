# Licensed under a 3-clause BSD style license - see LICENSE.rst
import logging
from collections import OrderedDict
from astropy.table import Table, Column
from .info import gammacat_info
from .input import InputData
from .utils import MissingValues, load_yaml

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
            data['common_name'] = MissingValues.string
        data['discoverer'] = bsi.get('discoverer', '')
        try:
            data['gamma_names'] = ','.join(bsi['gamma_names'])
        except KeyError:
            data['gamma_names'] = MissingValues.string
        try:
            data['ra'] = bsi['pos']['ra']
        except KeyError:
            data['ra'] = MissingValues.number
        try:
            data['dec'] = bsi['pos']['dec']
        except KeyError:
            data['dec'] = MissingValues.number

        return cls(data=data)

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
                #fmt=colspec['fmt'],
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

        path = gammacat_info.base_dir / 'docs/data/gammacat.fits'
        log.info('Writing {}'.format(path))
        table.write(str(path), format='fits', overwrite=True)
