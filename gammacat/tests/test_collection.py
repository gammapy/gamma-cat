# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammacat.collection import CollectionData


def test_output_data():
    output_data = CollectionData().read()
    assert len(output_data.index_dataset['data']) >= 90
