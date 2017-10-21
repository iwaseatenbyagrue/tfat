import click
import yaml

from multiprocessing import cpu_count
from tfat.logger import logger


def config_option(*args, **kwargs):

    def load_config(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        return yaml.load(value)

    attrs = {
        "type": click.File("rb"),
        "help": "YAML config file to load",
        "callback": load_config,
        "cls": click.Option
    }

    attrs.update(kwargs)

    if not args and attrs.get("cls") == click.Option:
        args = ["--config", "-c"]

    return click.option(*args, **attrs)


def root_dir_option(*args, **kwargs):

    attrs = {
        "help": "Root directory (default is current directory)",
        "type": click.Path(resolve_path=True, file_okay=False),
        "default": ".",
        "cls": click.Option
    }

    attrs.update(kwargs)

    if not args and attrs.get("cls") == click.Option:
        args = ["-r", "--root"]

    return click.option(*args, **attrs)


def threads_option(*args, **kwargs):

    attrs = {
        "help": "Number of threads to use",
        "type": int,
        "default": max(1, cpu_count()/2),
        "show_default": True
    }

    if not args and attrs.get('cls', click.Option) == click.Option:
        args = ["-t", "--threads"]

    return click.option(*args, **attrs)


def debug_option(*args, **kwargs):

    attrs = {
        "help": "Enable debug logging",
        "is_flag": True,
        "cls": click.Option
    }

    attrs.update(kwargs)

    def set_tfat_logging(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return

        if param == "debug":
            logger.setLevel(-1)
        return value

    if not args and attrs.get('cls') == click.Option:
        args = ["-D", "--debug"]

    return click.option(*args, **attrs)
