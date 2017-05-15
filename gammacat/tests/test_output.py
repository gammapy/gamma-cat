# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammacat.output import OutputData


def test_output_data():
    output_data = OutputData().read()
    assert len(output_data.index_dataset['data']) >= 90
