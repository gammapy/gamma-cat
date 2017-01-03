# Licensed under a 3-clause BSD style license - see LICENSE.rst
import gammacat.input


def test_basic_source_info():
    info = gammacat.input.BasicSourceInfo.read('input/sources/tev-000083.yaml')
    assert info.data['source_id'] == 83
    assert repr(info) == "BasicSourceInfo(source_id=83)"


def test_basic_source_list():
    sources = gammacat.input.BasicSourceList.read()
    assert len(sources.data) > 0
    str(sources)
    sources.data_per_row()


def test_dataset_source_info():
    info = gammacat.input.DatasetSourceInfo.read('input/data/2011/2011A%26A...531L..18H/tev-000083.yaml')
    assert info.data['reference_id'] == '2011A&A...531L..18H'
    assert info.data['source_id'] == 83
    assert repr(info) == "DatasetSourceInfo(source_id=83, reference_id='2011A&A...531L..18H')"


def test_input_dataset():
    info = gammacat.input.InputDataset.read('input/data/2011/2011A%26A...531L..18H')
    assert info.reference_id == '2011A&A...531L..18H'
    assert len(info.sources) == 1
    assert repr(info) == "InputDataset(reference_id='2011A&A...531L..18H')"


def test_input_dataset_collection():
    datasets = gammacat.input.InputDatasetCollection.read()
    assert len(datasets.data) > 0
    assert len(datasets.reference_ids) > 0


def test_input_data():
    input_data = gammacat.input.InputData.read()
    assert input_data.path.name == 'input'
    assert len(input_data.datasets.data) > 0
    assert len(input_data.sources.data) > 0
