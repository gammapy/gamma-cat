# Licensed under a 3-clause BSD style license - see LICENSE.rst
import subprocess
from pathlib import Path
import urllib.parse

__all__ = [
    'gammacat_info',
    'gammacat_tag',
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

    def __str__(self):
        ss = 'GammaCatInfo:\n'
        ss += 'version: {}\n'.format(self.version)
        ss += 'git_version: {}\n'.format(self.git_version)
        ss += 'base_dir: {}\n'.format(self.base_dir)
        return ss


class GammaCatTag:
    """Make and parse string tags.
    """

    def source_paper_filename(self, meta):
        return 'gammacat_' + self.source_paper_str(meta)

    def source_paper_str(self, meta):
        return self.source_str(meta) + '_' + self.paper_str(meta)

    def source_str(self, meta):
        # import IPython; IPython.embed(); 1/0
        return '{source_id:06d}'.format_map(meta)

    def paper_str(self, meta):
        return urllib.parse.quote(meta['paper_id'])
        # return '{paper_id}'.format_map(meta)


gammacat_info = GammaCatInfo()
gammacat_tag = GammaCatTag()
