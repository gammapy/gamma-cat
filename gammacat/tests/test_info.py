# Licensed under a 3-clause BSD style license - see LICENSE.rst
from gammacat.info import gammacat_tag


def test_gammacat_info():
    meta = dict(source_id=42)
    assert gammacat_tag.source_str(meta) == '000042'
