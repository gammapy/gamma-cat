# Licensed under a 3-clause BSD style license - see LICENSE.rst
import gammacat


def test_basic_source_info():
    info = gammacat.BasicSourceInfo.read('input/sources/tev-000083.yaml')
    assert info.data['source_id'] == 83
    assert repr(info) == "BasicSourceInfo(source_id=83)"


def test_basic_source_list():
    sources = gammacat.BasicSourceList.read()
    assert len(sources.data) > 0
    str(sources)
    sources.data_per_row()


def test_dataset_source_info():
    info = gammacat.DatasetSourceInfo.read('input/data/2011/2011A%26A...531L..18H/tev-000083.yaml')
    assert info.data['reference_id'] == '2011A&A...531L..18H'
    assert info.data['source_id'] == 83
    assert repr(info) == "DatasetSourceInfo(source_id=83, reference_id='2011A&A...531L..18H')"


def test_input_dataset():
    info = gammacat.InputDataset.read('input/data/2011/2011A%26A...531L..18H')
    assert info.reference_id == '2011A&A...531L..18H'
    assert len(info.sources) == 1
    assert repr(info) == "InputDataset(reference_id='2011A&A...531L..18H')"


def test_input_dataset_collection():
    papers = gammacat.InputDatasetCollection.read()
    assert len(papers.data) > 0
    assert len(papers.reference_ids) > 0


def test_input_data():
    input_data = gammacat.InputData.read()
    assert input_data.path.name == 'input'
    assert len(input_data.datasets.data) > 0
    assert len(input_data.sources.data) > 0
