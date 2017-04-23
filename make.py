#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make catalog (multiple steps available)
"""
import logging
import warnings
import click
import os

log = logging.getLogger(__name__)


@click.group()
@click.option('--loglevel', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']))
@click.option('--show-warnings', is_flag=True,
              help='Show warnings?')
def cli(loglevel, show_warnings):
    """
    Make catalog (multiple steps available)
    """
    levels = dict(
        debug=logging.DEBUG,
        info=logging.INFO,
        warning=logging.WARNING,
        error=logging.ERROR,
        critical=logging.CRITICAL,
    )
    logging.basicConfig(level=levels[loglevel])
    log.setLevel(level=levels[loglevel])

    if not show_warnings:
        warnings.simplefilter('ignore')


@cli.command(name='output')
@click.option('--step', default='all',
              type=click.Choice(['all', 'sed', 'index']))
def make_output(step):
    """Re-generate files in `output`.
    """
    log.info('Re-generate data files in output folder ...')
    from gammacat.output import OutputDataMaker
    maker = OutputDataMaker()
    if step == 'all':
        maker.make_all()
    elif step == 'sed':
        maker.make_sed_files()
    elif step == 'index':
        maker.make_index_files()


@cli.command(name='cat')
@click.option('--sources', default='all', help='Either "all" or comma-separated string of source IDs')
@click.option('--internal', default=False, is_flag=True)
def make_cat(sources, internal):
    """Make catalog in HGPS format
    """
    from gammacat.cat import GammaCatMaker
    if internal:
        if not 'HGPS_ANALYSIS' in os.environ:
            raise ValueError("Environment variable 'HGPS_ANALYSIS' "
                             " must be set.")
    log.info('Making catalog ...')
    maker = GammaCatMaker()
    maker.setup(source_ids=sources, internal=internal)
    maker.run(internal=internal)


# @cli.command(name='webpage')
# def make_webpage():
#     """Re-generate webpage in `docs`.
#     """
#     log.info('Re-generate webpage in `docs` ...')
#     gammacat.webpage.make()


@cli.command(name='check')
@click.option('--step', default='all',
              type=click.Choice(['all', 'input', 'output', 'global']))
def make_check(step):
    """Run automated checks.
    """
    log.info('Run automated checks ...')
    from gammacat.checks import GammaCatChecker
    maker = GammaCatChecker()
    if step == 'all':
        maker.check_all()
    elif step == 'input':
        maker.check_input()
    elif step == 'output':
        maker.check_output()
    elif step == 'global':
        maker.check_global()


@cli.command(name='web')
def serve_webpage():
    """Serve gamma-cat webpage locally.

    This is equivalent to:

        cd docs && python -m http.server
    """
    # import subprocess
    # import webbrowser
    # from http.server import HTTPServer, SimpleHTTPRequestHandler
    # server_address = ('localhost', 8000)
    # httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    # httpd.serve_forever()
    # subprocess.Popen('cd docs && python -m http.server', shell=True)
    # webbrowser.open('http://localhost:8000/docs')
    # click.pause('asdf')

    print('\nTo serve the gamma-cat webpage locally use these commands:\n')
    print('  cd docs && python -m http.server && cd ..')
    print('  open http://localhost:8000\n')


@cli.command(name='all')
@click.pass_context
def make_all(ctx):
    """Run all steps.
    """
    log.info('Run all steps ...')
    ctx.invoke(make_check)
    ctx.invoke(make_output)
    ctx.invoke(make_cat)
    # ctx.invoke(make_webpage)


if __name__ == '__main__':
    cli()
