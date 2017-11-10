# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make gamma-cat webpage (in combination with Sphinx).
"""
import logging
import jinja2
from .info import gammacat_info
from .input import BasicSourceList
from .utils import load_json

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

        self.make_status()
        self.make_sources()

    def make_status(self):

        status_rst = str(gammacat_info.base_dir / 'documentation/user_doc/status.rst')

        templateLoader = jinja2.FileSystemLoader( searchpath = '/')
        templateEnv = jinja2.Environment (loader = templateLoader )

        #TODO: How to convert a PosixPath to normal string?
        TEMPLATE_FILE = str(gammacat_info.base_dir / 'gammacat/templates/status.rst')
        template = templateEnv.get_template( TEMPLATE_FILE )

        templateVars = {'data' : self.sources_data}
        output = template.render(templateVars)

        status_rst_file = open(status_rst, 'w')
        status_rst_file.write(output)

    def make_sources(self):
        sources_folder = str(gammacat_info.base_dir / 'documentation/user_doc/sources/')
        templateLoader = jinja2.FileSystemLoader( searchpath = '/')
        templateEnv = jinja2.Environment (loader = templateLoader )

        #TODO: How to convert a PosixPath to normal string?
        TEMPLATE_FILE = str(gammacat_info.base_dir / 'gammacat/templates/source.rst')
        template = templateEnv.get_template( TEMPLATE_FILE )

        #TODO: Move this to another place? Maybe collection.py?
        path = gammacat_info.base_dir / 'docs/data/gammacat-datasets.json'
        gammacat_dataset = load_json(path)

        for source in self.sources_data:
            source_rst = sources_folder + '/source' + str(source['source_id']) + '.rst'
            available_seds = []

            #TODO: Convert source_id differently
            if(source['source_id'] < 10):
                src_id = '00000' + str(source['source_id'])
            elif(source['source_id'] >9 and source['source_id'] < 100):
                src_id = '0000' + str(source['source_id'])
            else:
                src_id = '000' + str(source['source_id'])

            for ref in source['reference_ids']:
                if ref in gammacat_dataset[source['source_id']]['reference_id']:
                    available_seds.append(ref)
            templateVars = {'src_id' : src_id, 'src_info' : source, 'av_seds' : available_seds}
            output = template.render(templateVars)
            source_rst_file = open(source_rst, 'w')
            source_rst_file.write(output)
            print(output)

        # for source in self.sources_data:
        #     source_id = source['source_id']
        #     
        #     common_name = source['common_name']
        #     gamma_names = source['gamma_names']
        #     for gam in gamma_names:
        #         gam = '{}\t'.format(gam)
        #     other_names = source['other_names']
        #     for oth in other_names:
        #         oth = '{:<20}'.format(oth)
        #     where = source['where']
        #     classes = source['classes']
        #     discoverer = source['discoverer']
        #     date_discovery = source['discovery_date']
        #     references = source['reference_ids']
        #     templateVars = { 'common_name' : common_name, 'gam_names' : gamma_names, 'oth_names' : other_names}
        #     output = template.render(templateVars)
        #     source_rst_file = open(source_rst, 'w')
        #     source_rst_file.write(output)
            # print('rstFile:\n')
            # print(output)

        # print(type(references))
        # print(type(gamma_names))










# class WebpageMaker:
#     """Make gamma-cat webpage."""

#     def __init__(self, config):
#         self.config = config

#     def run(self):
#         log.info('Make webpage ...')
#         log.error('Come one. Implement me already, you lazy hog!!!')