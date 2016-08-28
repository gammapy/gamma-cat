import gammacat


def test_output_data():
    output_data = gammacat.OutputData().read_all()
    assert output_data.path.name == 'output'
    # assert len(output_data.papers_catalog) > 0
    assert len(output_data.sources_catalog) > 0
    # assert len(output_data.catalog) > 0
