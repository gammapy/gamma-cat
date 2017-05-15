# Licensed under a 3-clause BSD style license - see LICENSE.rst
import subprocess
import os
from collections import OrderedDict
from pathlib import Path
import urllib.parse
from astropy.time import Time

__all__ = [
    'gammacat_info',
    'GammaCatStr',
    'rawgit_url',
]


class GammaCatInfo:
    """Gather basic info about gammacat.
    """

    def __init__(self):
        # Git version: http://stackoverflow.com/a/21901260/498873
        git_version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        self.git_version = git_version.decode('ascii').strip()

        # TODO: implement stable versions
        self.version = self.git_version

        # Git repository base directory
        self.base_dir = Path(__file__).parent.parent

        # Internal gammacat version path
        hgps_analysis_dir = os.environ.get('HGPS_ANALYSIS')
        if hgps_analysis_dir:
            self.internal_dir = Path(hgps_analysis_dir) / 'data/catalogs/gammacat-hess-internal/'

        self.description = "An open data collection and source catalog for gamma-ray astronomy"

        self.datetime = str(Time.now())

    def __str__(self):
        ss = 'GammaCatInfo:\n'
        ss += 'version: {}\n'.format(self.version)
        ss += 'git_version: {}\n'.format(self.git_version)
        ss += 'base_dir: {}\n'.format(self.base_dir)
        return ss

    @property
    def info_dict(self):
        """Dict with some info that can be written to file headers."""
        info = OrderedDict()
        info['name'] = 'gammacat'
        info['version'] = self.version
        info['git_version'] = self.git_version
        info['description'] = self.description
        info['datetime'] = self.datetime
        return info


class GammaCatStr:
    """Make and parse strings (e.g. filenames).
    """

    @staticmethod
    def dataset_filename(meta):
        return 'gammacat_' + GammaCatStr.dataset_str(meta)

    @staticmethod
    def dataset_str(meta):
        ss = GammaCatStr.reference_id_str(meta['reference_id'])
        ss += '_'
        ss += GammaCatStr.source_id_str(meta['source_id'])
        return ss

    @staticmethod
    def source_id_str(source_id):
        return '{:06d}'.format(source_id)

    @staticmethod
    def reference_id_str(reference_id):
        return urllib.parse.quote(reference_id)


gammacat_info = GammaCatInfo()


def rawgit_url(filename, location='master', mode='production'):
    """
    Construct the rawgit URL to download directly files from the repo.

    More info:
    * https://rawgit.com/
    * https://github.com/rgrove/rawgit/wiki/Frequently-Asked-Questions

    URL is

    Parameters
    ----------
    filename : str
        Filename in the repo.
    location : str
        Name of a branch, tag or commit.
    mode : {'development', 'production'}
        Where to fetch the files from

    Examples
    --------
    >>> filename = 'input/data/2006/2006A%2526A...456..245A/tev-000065.ecsv'
    >>> rawgit_url(filename, mode='production')
    TODO
    >>> rawgit_url(filename, mode='development')
    TODO
    """
    if mode == 'development':
        base_url = 'https://rawgit.com/gammapy/gamma-cat'
    elif mode == 'production':
        base_url = 'https://cdn.rawgit.com/gammapy/gamma-cat'

    url = '/'.join([base_url, location, filename])

    return url
