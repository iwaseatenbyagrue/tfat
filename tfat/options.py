import click
import yaml

from multiprocessing import cpu_count

def config_option(*args, **kwargs):

    def load_config(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        return yaml.load(value)

    attrs = {
        "type": click.File("rb"),
        "help": "YAML config file to load",
        "callback": load_config
    }

    attrs.update(kwargs)

    if not args and attrs.get('cls', click.Option) == click.Option:
        args = ["--config", "-c"]

    return click.option(*args, **attrs)


def root_dir_option(*args, **kwargs):

    attrs = {
        "help": "Root directory",
        "type": click.Path(resolve_path=True, file_okay=False),
        "default": "."
    }

    if not args and attrs.get('cls', click.Option) == click.Option:
        args = ["-r", "--root"]

    return click.option(*args, **attrs)


def threads_option(*args, **kwargs):


    attrs = {
        "help": "Number of threads to use",
        "type": int,
        "default": max(1, cpu_count()/2)
    }

    if not args and attrs.get('cls', click.Option) == click.Option:
        args = ["-t", "--threads"]

    return click.option(*args, **attrs)
