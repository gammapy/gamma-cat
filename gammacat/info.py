import subprocess
from pathlib import Path

__all__ = ['info']


class GammaCatInfo:
    """Gather basic info about gammacat.
    """

    def __init__(self):
        # Git version: http://stackoverflow.com/a/21901260/498873
        git_version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        self.git_version = git_version.decode('ascii').strip()

        # Git
        self.base_dir = Path.cwd().parent

    def __str__(self):
        ss = 'GammaCatInfo:\n'
        ss += 'git_version: {}\n'.format(self.git_version)
        ss += 'base_dir: {}\n'.format(self.base_dir)
        return ss


info = GammaCatInfo()
