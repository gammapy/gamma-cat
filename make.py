#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make catalog (multiple steps available)
"""
import logging
import warnings
import click
import os
from gammacat.collection import CollectionMaker
from gammacat.catalog import CatalogMaker
from gammacat.webpage import WebpageMaker
from gammacat.checks import Checker

log = logging.getLogger(__name__)


@click.group()
@click.option('--loglevel', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']))
@click.option('--show-warnings', is_flag=True,
              help='Show warnings?')
@click.option('--hgps', default=False, is_flag=True,
              help='Produce gamma-cat version for HGPS')
def cli(loglevel, show_warnings, hgps):
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

    if hgps:
        if 'HGPS_ANALYSIS' not in os.environ:
            raise ValueError("Environment variable 'HGPS_ANALYSIS' "
                             " must be set.")


@cli.command(name='collection')
@click.option('--step', default='all',
              type=click.Choice(['all', 'sed', 'lightcurve', 'input-index', 'output-index']))
def make_collection(step):
    """Make gamma-cat data collection."""
    log.info('Make collection ...')
    maker = CollectionMaker()
    if step == 'all':
        maker.process_all()
    elif step == 'input-index':
        maker.make_index_file_for_input()
    elif step == 'sed':
        maker.process_seds()
    elif step == 'lightcurve':
        maker.process_lightcurves()
    # TODO: implement this!
    # elif step == 'output-index':
    #     maker.make_index_file_for_output()


@cli.command(name='catalog')
@click.option('--sources', default='all', help='Either "all" or comma-separated string of source IDs')
def make_catalog(sources):
    """Make gamma-cat catalog."""
    log.info('Make catalog ...')
    maker = CatalogMaker()
    maker.setup(source_ids=sources, internal=internal)
    maker.run(internal=internal)


@cli.command(name='webpage')
def make_webpage():
    """Make gamma-cat webpage.
    """
    log.info('Make webpage ...')
    maker = WebpageMaker()
    maker.run()


@cli.command(name='check')
@click.option('--step', default='all',
              type=click.Choice(['all', 'input', 'collection', 'catalog', 'global']))
def make_check(step):
    """Run automated checks.
    """
    log.info('Run checks ...')
    maker = Checker()
    if step == 'all':
        maker.check_all()
    elif step == 'input':
        maker.check_input()
    elif step == 'collection':
        maker.check_collection()
    elif step == 'catalog':
        maker.check_catalog()
    elif step == 'global':
        maker.check_global()


@cli.command(name='all')
@click.pass_context
def make_all(ctx):
    """Run all steps.
    """
    log.info('Run all steps ...')
    checker = Checker()
    checker.check_input()

    ctx.invoke(make_collection)
    checker.check_collection()

    ctx.invoke(make_catalog)
    checker.check_catalog()

    ctx.invoke(make_webpage)

    checker.check_global()


if __name__ == '__main__':
    cli()
