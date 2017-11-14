# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make gamma-cat webpage (in combination with Sphinx).
"""
import logging
import jinja2
from .info import gammacat_info
from .input import BasicSourceList
from .utils import load_json, render_template

__all__ = [
    'WebpageConfig',
    'WebpageMaker',
]

log = logging.getLogger(__name__)

class WebpageConfig:
    """Config options for webpage maker."""

    def __init__(self, *, out_path):
        self.out_path = out_path


class WebpageMaker:
    """Make rst-files for gamma-cat webpage."""

    def __init__(self, config):
        self.config = config
        self.sources_data = BasicSourceList.read().to_dict()['data']

    def run(self):
        log.info('Make webpage ...')

        self.make_source_list()
        self.make_sources()

    def make_source_list(self):

        status_rst = str(gammacat_info.base_dir / 'documentation/data/src_list.rst')

        #TODO: How to convert a PosixPath to normal string?
        TEMPLATE_FILE = str(gammacat_info.base_dir / 'documentation/templates/src_list.txt')

        ctx = {'data' : self.sources_data}
        render_template(TEMPLATE_FILE, status_rst, ctx)

    def make_sources(self):
        sources_folder = str(gammacat_info.base_dir / 'documentation/data/sources/')

        #TODO: How to convert a PosixPath to normal string?
        TEMPLATE_FILE = str(gammacat_info.base_dir / 'documentation/templates/source.txt')

        #TODO: Move this to another place? Maybe collection.py?
        path = gammacat_info.base_dir / 'docs/data/gammacat-datasets.json'
        gammacat_dataset = load_json(path)

        for source in self.sources_data:
            self._make_single_source(gammacat_dataset, TEMPLATE_FILE, source, sources_folder)

        # for source in self.sources_data:
        #     source_rst = sources_folder + '/source' + str(source['source_id']) + '.rst'
        #     available_seds = []

        #     src_id = '{:4d}'.format(source['source_id'])

        #     for ref in source['reference_ids']:
        #         if ref in gammacat_dataset[source['source_id']]['reference_id']:
        #             available_seds.append(ref)
        #     ctx = {'src_id' : src_id, 'src_info' : source, 'av_seds' : available_seds}
        #     render_template(TEMPLATE_FILE, source_rst, ctx)
            # output = template.render(ctx)
            # source_rst_file = open(source_rst, 'w')
            # source_rst_file.write(output)

    def _make_single_source(self, gamcat_dataset, template_file, source, src_folder):
        source_rst = src_folder + '/source' + str(source['source_id']) + '.rst'
        print(source_rst)
        available_seds = []
        src_id = '{:4d}'.format(source['source_id'])
        for ref in source['reference_ids']:
            if ref in gamcat_dataset[source['source_id']]['reference_id']:
                available_seds.append(ref)
            ctx = {'src_id' : src_id, 'src_info' : source, 'av_seds' : available_seds}
            render_template(template_file, source_rst, ctx)
