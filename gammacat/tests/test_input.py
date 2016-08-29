import gammacat


def test_basic_source_info():
    info = gammacat.BasicSourceInfo.read('input/sources/tev-000083.yaml')
    assert info.id == 83


def test_paper_source_info():
    info = gammacat.PaperSourceInfo.read('input/papers/2011A%26A...531L..18H/tev-000083.yaml')
    assert info.paper_id == '2011A&A...531L..18H'
    assert info.source_id == 83


def test_basic_source_list():
    sources = gammacat.BasicSourceList.read()
    assert len(sources.data) > 0


def test_paper_info():
    info = gammacat.PaperInfo.read('input/papers/2011A%26A...531L..18H')
    assert info.id == '2011A&A...531L..18H'
    assert len(info.sources) == 1


def test_paper_list():
    papers = gammacat.PaperList.read()
    assert len(papers.data) > 0


def test_input_data():
    input_data = gammacat.InputData.read()
    assert input_data.path.name == 'input'
    assert len(input_data.papers.data) > 0
    assert len(input_data.sources.data) > 0
