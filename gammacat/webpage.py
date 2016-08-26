"""
Make a simple HTML webpage.
"""
import logging
from .info import gammacat_info

log = logging.getLogger()


def make():
    html = '<h1>gamma-cat webpage</h1><p>Coming soon...</p>'
    path = gammacat_info.base_dir / 'docs/index.html'
    log.info('Writing {}'.format(path))
    path.write_text(html)
    # import IPython; IPython.embed()
