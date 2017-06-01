# Licensed under a 3-clause BSD style license - see LICENSE.rst
from pathlib import Path
import pytest
from ruamel.yaml import safe_load
from gammacat.info import gammacat_info
from gammacat.modeling import Parameter, Parameters


# pl spectrum example
# path = gammacat_info.base_dir / 'input/data/2011/2011A%26A...529A..49H/tev-000137.yaml'
# pl2 spectrum example
# filename = 'input/data/2016/2016arXiv161005799S/tev-000137.yaml'
# ecpl spectrum example
# TODO: @pytest.parametrize


def test_parameter_list():
    path = gammacat_info.base_dir / 'input/data/2011/2011A%26A...529A..49H/tev-000137.yaml'
    data = safe_load(path.open())['spec']['model']['parameters']
    pars = Parameters.from_dict(data)
    # print(pars)
    # 1 / 0
    # TODO: add assertions that read correctly
