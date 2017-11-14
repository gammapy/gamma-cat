#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make catalog (multiple steps available)
"""
from pathlib import Path
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


class GlobalConfig:
    """Global config options."""

    def __init__(self, *, log_level, show_warnings):
        self.log_level = log_level
        self.show_warnings = show_warnings

        logging.basicConfig(level=log_level)

        if not show_warnings:
            warnings.simplefilter('ignore')

        self.out_path = gammacat_info.base_dir / 'docs/data'

    def __repr__(self):
        return 'GlobalConfig({!r})'.format(self.__dict__)


# TODO: decide where to keep the config and how to pass it around
# Best description how it works is here: http://click.pocoo.org/dev/complex/

@click.group(invoke_without_command=True)
@click.option('--log-level', default='INFO',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']))
@click.option('--show-warnings', is_flag=True, help='Show warnings?')
@click.pass_context
def cli(ctx, log_level, show_warnings):
    """
    Make catalog (multiple steps available)
    """
    ctx.obj = GlobalConfig(
        log_level=log_level,
        show_warnings=show_warnings,
    )
    log.debug('global config: {}'.format(ctx.obj))


@cli.command(name='collection')
@click.option('--step', default='all',
              type=click.Choice(['all', 'sed', 'lightcurve', 'dataset', 'input-index', 'output-index']))
@click.pass_obj
def cli_collection(global_config, step):
    """Make gamma-cat data collection."""
    config = CollectionConfig(
        path=global_config.out_path,
        step=step,
    )
    CollectionMaker(config).run()


@cli.command(name='catalog')
@click.option('--sources', default='all', help='Either "all" or comma-separated string of source IDs')
@click.pass_obj
def cli_catalog(global_config, sources):
    """Make gamma-cat catalog."""
    config = CatalogConfig(
        out_path=global_config.out_path,
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
@click.pass_obj
def cli_checks(global_config, step):
    """Run automated checks.
    """
    config = CheckerConfig(
        out_path=global_config.out_path,
        step=step,
    )
    Checker(config).run()


@cli.command(name='clean')
def cli_clean():
    """Remove all auto-generated files"""
    # TODO: this list of files & folders is incomplete
    cmd = 'rm -r documentation/_build documentation/data/sources documentation/data/source_list.rst'
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
