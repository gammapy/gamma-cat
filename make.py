#!/usr/bin/env python
"""
Make catalog (multiple steps available)
"""
import logging
import click
import gammacat

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@click.group()
def cli():
    """
    Make catalog (multiple steps available)
    """
    pass


@cli.command(name='output')
def make_output():
    """Re-generate files in `output`.
    """
    log.info('Re-generate files in `output` ...')
    print(gammacat.info)
    input_data = gammacat.InputData().read_all()
    print(input_data)


@cli.command(name='webpage')
def make_webpage():
    """Re-generate webpage in `docs`.
    """
    log.info('Re-generate webpage in `docs` ...')


@cli.command(name='all')
@click.pass_context
def make_all(ctx):
    """Run all steps.
    """
    log.info('Run all steps ...')
    ctx.invoke(make_output)
    ctx.invoke(make_webpage)


@cli.command(name='tests')
def make_tests():
    """Run automated tests
    """
    log.info('Run automated tests ...')
    gammacat.tests.check_input_files()


if __name__ == '__main__':
    cli()
