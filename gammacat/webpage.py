# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make gamma-cat webpage (in combination with Sphinx).
"""
import logging
from gammapy.catalog import GammaCatResourceIndex
from .input import BasicSourceList
from .info import gammacat_info
from .utils import load_json, jinja_env

__all__ = [
    'WebpageConfig',
    'WebpageMaker',
]

log = logging.getLogger(__name__)


def get_resource_index():
    path = gammacat_info.base_dir / 'docs/data/gammacat-datasets.json'
    return GammaCatResourceIndex.from_list(load_json(path))


class WebpageConfig:
    """Config options for webpage maker."""

    def __init__(self, *, out_path):
        self.out_path = out_path


class WebpageMaker:
    """Make rst-files for gamma-cat webpage."""

    def __init__(self, config):
        self.config = config
        self.resources = get_resource_index()
        # TODO: we shouldn't be accessing stuff from the input folder
        # in the webpage generation! Change to use output folder.
        self.sources_data = BasicSourceList.read().to_dict()['data']

    def run(self):
        log.info('Make webpage ...')
        self.make_source_list_page()
        self.make_source_detail_pages()

    def make_source_list_page(self):
        # Prepare context
        ctx = {'sources': self.sources_data}

        # Render context and save to file
        template = jinja_env.get_template('source_list.txt')
        txt = template.render(ctx)
        path = gammacat_info.base_dir / 'documentation/data/source_list.rst'
        log.info(f'Writing {path}')
        path.write_text(txt)

    def make_source_detail_pages(self):
        path = gammacat_info.base_dir / 'documentation/data/sources/'
        path.mkdir(exist_ok=True)
        for source in self.sources_data:
            self.make_source_detail_page(source)

    def make_source_detail_page(self, source):
        # Prepare context
        resources = self.resources.query(f'source_id == {source["source_id"]}')
        ctx = {'source': source, 'resources': resources}

        # Render context and save to file
        template = jinja_env.get_template('source_detail.txt')
        txt = template.render(ctx)
        path = gammacat_info.base_dir / f'documentation/data/sources/source_{source["source_id"]}.rst'
        log.info(f'Writing {path}')
        path.write_text(txt)

