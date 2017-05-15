# Licensed under a 3-clause BSD style license - see LICENSE.rst
import pytest
from numpy.testing import assert_allclose
from gammacat.lightcurve import LightCurve


@pytest.mark.skip
def test_lc():
    lc = LightCurve.read('input/data/2011/2011ApJ...738....3A/tev-000014-lc.ecsv')
    lc.process()
    assert_allclose(lc.table['flux'][0], 42)
