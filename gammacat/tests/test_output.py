# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammacat.output import OutputData


def test_output_data():
    output_data = OutputData().read_all()
    assert len(output_data.gammacat) > 0
    assert len(output_data.datasets) > 0
