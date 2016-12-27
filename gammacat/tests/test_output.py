# Licensed under a 3-clause BSD style license - see LICENSE.rst
import gammacat


def test_output_data():
    output_data = gammacat.OutputDataReader().read_all()
    assert len(output_data.gammacat) > 0
    assert len(output_data.datasets) > 0
