# Licensed under a 3-clause BSD style license - see LICENSE.rst
import gammacat.utils


def test_rawgit_url():
    url = gammacat.utils.rawgit_url('LICENSE.rst')
    assert url == 'https://cdn.rawgit.com/gammapy/gamma-cat/master/LICENSE.rst'

    url = gammacat.utils.rawgit_url('LICENSE.rst', mode='development')
    assert url == 'https://rawgit.com/gammapy/gamma-cat/master/LICENSE.rst'
