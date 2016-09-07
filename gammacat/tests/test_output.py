# Licensed under a 3-clause BSD style license - see LICENSE.rst
import gammacat


def test_output_data():
    output_data = gammacat.OutputDataReader().read_all()
    assert output_data.path.name == 'output'
    # assert len(output_data.papers_catalog) > 0
    assert len(output_data.sources_catalog) > 0
    # assert len(output_data.catalog) > 0
