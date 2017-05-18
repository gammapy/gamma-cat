#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make catalog (multiple steps available)
"""
import logging
import warnings
import click
import os
from gammacat.info import gammacat_info
from gammacat.collection import CollectionConfig, CollectionMaker
from gammacat.catalog import CatalogConfig, CatalogMaker
from gammacat.webpage import WebpageConfig, WebpageMaker
from gammacat.checks import CheckerConfig, Checker

log = logging.getLogger(__name__)


class GlobalConfig:
    """Global config options."""

    def __init__(self, *, log_level, show_warnings, hgps):
        self.log_level = log_level
        self.show_warnings = show_warnings
        self.hgps = hgps

        levels = dict(
            debug=logging.DEBUG,
            info=logging.INFO,
            warning=logging.WARNING,
            error=logging.ERROR,
            critical=logging.CRITICAL,
        )
        logging.basicConfig(level=levels[log_level])
        log.setLevel(level=levels[log_level])

        if not show_warnings:
            warnings.simplefilter('ignore')

        if hgps:
            if 'HGPS_ANALYSIS' not in os.environ:
                raise ValueError("You must set the environment variable HGPS_ANALYSIS.")
            # self.out_path = Path('TODO')
            raise
        else:
            self.out_path = gammacat_info.base_dir / 'docs/data'

    def __repr__(self):
        return 'GlobalConfig({!r})'.format(self.__dict__)


# TODO: decide where to keep the config and how to pass it around
# Best description how it works is here: http://click.pocoo.org/dev/complex/

@click.group(invoke_without_command=True)
@click.option('--log-level', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']))
@click.option('--show-warnings', is_flag=True,
              help='Show warnings?')
@click.option('--hgps', default=False, is_flag=True,
              help='Produce gamma-cat version for HGPS')
@click.pass_context
def cli(ctx, log_level, show_warnings, hgps):
    """
    Make catalog (multiple steps available)
    """
    ctx.obj = GlobalConfig(
        log_level=log_level,
        show_warnings=show_warnings,
        hgps=hgps,
    )
    log.debug('global config: {}'.format(ctx.obj))


@cli.command(name='collection')
@click.option('--step', default='all',
              type=click.Choice(['all', 'sed', 'lightcurve', 'input-index', 'output-index']))
@click.pass_obj
def make_collection(global_config, step):
    """Make gamma-cat data collection."""
    config = CollectionConfig(
        path=global_config.out_path,
        hgps=global_config.hgps,
        step=step,
    )
    CollectionMaker(config).run()


@cli.command(name='catalog')
@click.option('--sources', default='all', help='Either "all" or comma-separated string of source IDs')
@click.pass_obj
def make_catalog(global_config, sources):
    """Make gamma-cat catalog."""
    config = CatalogConfig(
        out_path=global_config.out_path,
        hgps=global_config.hgps,
        source_ids=sources,
    )
    CatalogMaker(config).run()


@cli.command(name='webpage')
def make_webpage():
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
def make_checks(global_config, step):
    """Run automated checks.
    """
    config = CheckerConfig(
        out_path=global_config.out_path,
        step=step,
    )
    Checker(config).run()


@cli.command(name='all')
@click.pass_context
def make_all(ctx):
    """Run all steps.
    """
    log.info('Run all steps ...')
    ctx.invoke(make_collection)
    ctx.invoke(make_catalog)
    ctx.invoke(make_webpage)
    ctx.invoke(make_checks)


if __name__ == '__main__':
    cli()
