from pathlib import Path
import json
import yaml
import numpy as np
from astropy.table import Table

MISSING_VAL = dict(
    integer=-999,
    number=np.nan,
    string='',
    array='',
)


def load_yaml(path):
    """Helper function to load data from a YAML file."""
    path = Path(path)
    with path.open() as fh:
        data = yaml.safe_load(fh)
    return data


def make_table(row_data, column_def):
    """Helper function to make an Astropy Table from row data.

    The main reason this is needed is that it's hard to construct
    a table with missing data.
    """
    pass
