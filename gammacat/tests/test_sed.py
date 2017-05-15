# Licensed under a 3-clause BSD style license - see LICENSE.rst
from numpy.testing import assert_allclose
from gammacat.sed import SED


def test_sed_input():
    sed = SED.read('input/data/2008/2008A%26A...481..401A/tev-000112-sed.ecsv')
    sed.process()
    assert_allclose(sed.table['dnde'][0], 74.23e-13)


def test_sed_output():
    sed = SED.read('docs/data/sources/000112/gammacat_000112_2008A%26A...481..401A_sed.ecsv')
    assert_allclose(sed.table['dnde'][0], 74.23e-13)
