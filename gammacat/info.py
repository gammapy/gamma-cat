# Licensed under a 3-clause BSD style license - see LICENSE.rst
import subprocess
from pathlib import Path

__all__ = ['gammacat_info']


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

    def __str__(self):
        ss = 'GammaCatInfo:\n'
        ss += 'version: {}\n'.format(self.version)
        ss += 'git_version: {}\n'.format(self.git_version)
        ss += 'base_dir: {}\n'.format(self.base_dir)
        return ss


gammacat_info = GammaCatInfo()
