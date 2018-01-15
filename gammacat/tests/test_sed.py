# Licensed under a 3-clause BSD style license - see LICENSE.rst
from numpy.testing import assert_allclose
from gammacat.info import gammacat_info
from gammacat.sed import SED


def test_sed_input():
    filename = gammacat_info.in_path / 'data/2008/2008A%26A...481..401A/tev-000112-sed.ecsv'
    sed = SED.read(filename)
    sed.process()
    assert_allclose(sed.table['dnde'][0], 74.23e-13)


def test_sed_output():
    filename = gammacat_info.out_path / 'data/2008/2008A%26A...481..401A/gammacat_2008A%26A...481..401A_000112_sed.ecsv'
    sed = SED.read(filename)
    assert_allclose(sed.table['dnde'][0], 74.23e-13)
