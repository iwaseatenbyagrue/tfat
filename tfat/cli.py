# -*- coding: utf-8 -*-

import click


from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from tfat.cli_utils import AliasedGroup

@with_plugins(iter_entry_points('{}.plugins'.format(__package__)))
@click.group(cls=AliasedGroup)
@click.version_option()
@click.help_option()
def base():
    """ tfat - a tool for automating things.
    """
    pass
