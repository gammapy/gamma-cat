import gammacat


def test_basic_source_info():
    info = gammacat.BasicSourceInfo.read('input/sources/tev-000074.yaml')
    assert info.id == 'tev-000074'


def test_paper_source_info():
    info = gammacat.PaperSourceInfo.read('input/papers/2011A%26A...531L..18H/tev-000234.yaml')
    assert info.paper_id == '2011A&A...531L..18H'
    assert info.source_id == 'tev-000234'
