import gammacat


def test_basic_source_info():
    info = gammacat.BasicSourceInfo.read('input/sources/tev-000074.yaml')
    assert info.id == 'tev-000074'


def test_paper_source_info():
    info = gammacat.PaperSourceInfo.read('input/papers/2011A%26A...531L..18H/tev-000234.yaml')
    assert info.paper_id == '2011A&A...531L..18H'
    assert info.source_id == 'tev-000234'


def test_paper_info():
    info = gammacat.PaperInfo.read('input/papers/2011A%26A...531L..18H')
    assert info.id == '2011A&A...531L..18H'
    assert len(info.sources) == 1


def test_input_data():
    input_data = gammacat.InputData().read_all()
    assert input_data.path.name == 'input'
    assert len(input_data.papers) > 0
    assert len(input_data.sources) > 0
