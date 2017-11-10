# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make gamma-cat webpage (in combination with Sphinx).
"""
import logging
import jinja2
from .info import gammacat_info
from .input import BasicSourceList

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

        #TODO: Make a list simple with numbers from 0 to 166
        source_ids = []
        for source in self.sources_data:
            source_ids.append(source['source_id'])

        templateVars = {'source_ids' : sorted(source_ids)}

        #TODO: More compact saving of file?
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

        for source in self.sources_data:
            source_id = source['source_id']
            source_rst = sources_folder + '/source' + str(source_id) + '.rst'
            common_name = source['common_name']
            gamma_names = source['gamma_names']
            for gam in gamma_names:
                gam = '{}\t'.format(gam)
            other_names = source['other_names']
            for oth in other_names:
                oth = '{:<20}'.format(oth)
            where = source['where']
            classes = source['classes']
            discoverer = source['discoverer']
            date_discovery = source['discovery_date']
            references = source['reference_ids']
            templateVars = { 'common_name' : common_name, 'gam_names' : gamma_names, 'oth_names' : other_names}
            output = template.render(templateVars)
            source_rst_file = open(source_rst, 'w')
            source_rst_file.write(output)
            print('rstFile:\n')
            print(output)

        # print(type(references))
        # print(type(gamma_names))










# class WebpageMaker:
#     """Make gamma-cat webpage."""

#     def __init__(self, config):
#         self.config = config

#     def run(self):
#         log.info('Make webpage ...')
#         log.error('Come one. Implement me already, you lazy hog!!!')
