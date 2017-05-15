# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammacat.info import GammaCatStr


def test_gammacat_str():
    assert GammaCatStr.source_id_str(42) == '000042'

    meta = dict(source_id=42, reference_id='2015A&A...577A.131H')
    assert GammaCatStr.dataset_filename(meta) == 'gammacat_2015A%26A...577A.131H_000042'
