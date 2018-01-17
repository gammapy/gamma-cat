#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Command line tool to make gamma-cat.
"""
import logging
import warnings
import subprocess
import click
from gammacat.info import gammacat_info
from gammacat.collection import CollectionConfig, CollectionMaker
from gammacat.catalog import CatalogConfig, CatalogMaker
from gammacat.webpage import WebpageConfig, WebpageMaker
from gammacat.checks import CheckerConfig, Checker

log = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.option('--log-level', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']))
@click.option('--show-warnings', is_flag=True, help='Show warnings?')
def cli(log_level, show_warnings):
    """
    Command line tool to make gamma-cat.

    Example usage:

        ./make.py --help
        ./make.py all --clean --webpage

    """
    logging.basicConfig(level=log_level.upper())
    if not show_warnings:
        warnings.simplefilter('ignore')


@cli.command(name='collection')
@click.option('--step', default='all',
              type=click.Choice(['all', 'source-info', 'sed', 'lightcurve', 'dataset', 'input-index', 'output-index']))
def cli_collection(step):
    """Make gamma-cat data collection."""
    config = CollectionConfig(
        in_path=gammacat_info.in_path,
        out_path=gammacat_info.out_path,
        step=step,
    )
    CollectionMaker(config).run()


@cli.command(name='catalog')
@click.option('--sources', default='all', help='Either "all" or comma-separated string of source IDs')
def cli_catalog(sources):
    """Make gamma-cat catalog."""
    config = CatalogConfig(
        out_path=gammacat_info.out_path,
        source_ids=sources,
    )
    CatalogMaker(config).run()


@cli.command(name='webpage')
def cli_webpage():
    """Make gamma-cat webpage.
    """
    config = WebpageConfig(
        out_path='todo',
    )
    WebpageMaker(config).run()


@cli.command(name='checks')
@click.option('--step', default='all',
              type=click.Choice(['all', 'input', 'collection', 'catalog', 'global']))
def cli_checks(step):
    """Run automated checks.
    """
    config = CheckerConfig(
        in_path=gammacat_info.in_path,
        out_path=gammacat_info.out_path,
        step=step,
    )
    Checker(config).run()


@cli.command(name='clean')
def cli_clean():
    """Remove all auto-generated files"""
    # TODO: this list of files & folders is incomplete
    cmd = ' '.join([
        'rm', '-r',
        'webpage/_build',
        'webpage/use/sources',
        'webpage/use/source_list.rst',
        'webpage/use/publication_list.rst',
    ])
    log.info(f'Executing command: {cmd}')
    subprocess.call(cmd, shell=True)


@cli.command(name='all')
@click.option('--clean', is_flag=True, help='Run clean step?')
@click.option('--no-collection', is_flag=True, help='Skip collection step?')
@click.option('--no-catalog', is_flag=True, help='Skip catalog step?')
@click.option('--no-checks', is_flag=True, help='Skip checks step?')
@click.option('--webpage', is_flag=True, help='Run webpage step?')
@click.pass_context
def cli_all(ctx, clean, no_collection, no_catalog, no_checks, webpage):
    """Run all steps."""
    log.info('Run all steps ...')

    if clean:
        ctx.invoke(cli_clean)

    if not no_collection:
        ctx.invoke(cli_collection)

    if not no_catalog:
        ctx.invoke(cli_catalog)

    if not no_checks:
        ctx.invoke(cli_checks)

    if webpage:
        ctx.invoke(cli_webpage)


if __name__ == '__main__':
    cli()
