from gammacat import BasicSourceInfo


def test_basic_source_info():
    info = BasicSourceInfo.read('input/sources/000074.yaml')
    assert info.id == 74

# def test_basic_source_info():
#     info = BasicSourceInfo.read('input/sources/000074.yaml')
#     assert info.id == 74
