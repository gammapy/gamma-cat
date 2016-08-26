#!/usr/bin/env python
"""
Import `seed` data into `input` folder.
"""
import click


@click.group()
def cli():
    """
    Import `seed` data into `input` folder.
    """
    pass


@cli.command()
def all():
    """Run all import steps."""
    click.secho('Starting import of data: seed -> input', fg='green')


if __name__ == '__main__':
    cli()
