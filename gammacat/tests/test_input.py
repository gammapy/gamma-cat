# Licensed under a 3-clause BSD style license - see LICENSE.rst
import gammacat


def test_basic_source_info():
    info = gammacat.BasicSourceInfo.read('input/sources/tev-000083.yaml')
    assert info.data['source_id'] == 83
    assert repr(info) == "BasicSourceInfo(id=83)"


def test_paper_source_info():
    info = gammacat.PaperSourceInfo.read('input/papers/2011A%26A...531L..18H/tev-000083.yaml')
    assert info.data['paper_id'] == '2011A&A...531L..18H'
    assert info.data['source_id'] == 83
    assert repr(info) == "PaperInfo(source_id=83, data_id='2011A&A...531L..18H')"


def test_basic_source_list():
    sources = gammacat.BasicSourceList.read()
    assert len(sources.data) > 0
    str(sources)
    sources.data_per_row()
    sources.to_table()


def test_paper_info():
    info = gammacat.PaperInfo.read('input/papers/2011A%26A...531L..18H')
    assert info.id == '2011A&A...531L..18H'
    assert len(info.sources) == 1
    assert repr(info) == "PaperInfo(id='2011A&A...531L..18H')"


def test_paper_list():
    papers = gammacat.PaperList.read()
    assert len(papers.data) > 0


def test_input_data():
    input_data = gammacat.InputData.read()
    assert input_data.path.name == 'input'
    assert len(input_data.papers.data) > 0
    assert len(input_data.sources.data) > 0
