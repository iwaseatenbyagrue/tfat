# -*- coding: utf-8 -*-
from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins


@with_plugins(iter_entry_points('{}.plugins'.format(__package__)))
@click.group()
@click.version_option()
@click.help_option()
def base():
    """ tfat - a tool for automating things.
    """
    pass
