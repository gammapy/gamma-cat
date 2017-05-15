# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Check that gamma-cat can be accessed via Gammapy all-right.

Most checks go in `gammapy/catalog/tests/test_gammacat.py`.

This is just some quick checks to make sure we notice when
we make a change in the `gamma-cat` repo that breaks `gammapy`. 
"""
from numpy.testing import assert_allclose


# def test_cat():
#     from gammapy.catalog import SourceCatalogGammaCat
#     cat = SourceCatalogGammaCat()
#     table = cat['W 28'].flux_points.table
#     # fp = FluxPoints.read('$GAMMA_CAT/docs/data/sources/000112/gammacat_000112_2008A%26A...481..401A_sed.ecsv')
#     assert_allclose(table['dnde'][0], 42) # 7.423e-12)
