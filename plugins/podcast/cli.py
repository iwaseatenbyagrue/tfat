import click
import yaml

from .downloader import PodcastDownloader
from logging import StreamHandler
from tfat.pipeline import Pipeline
from tfat.logger import get_handler_with_default_formatter


@click.group("podcast")
def cli():
    """ tfat-podcast 0.1 - build and update a podcast collection.
    """
    pass


@cli.command()
@click.option(
    "-r", "--root", help="Root directory",
    type=click.Path(resolve_path=True, file_okay=False), default="."
)
@click.option(
    "-c", "--config", type=click.File('rb'),
    help="Configuration file to get feeds from"
)
@click.option(
    "-t", "--threads", default=4, type=int,
    help="Number of threads to use"
)
@click.option(
    "-D", "--debug", is_flag=True,
    help="Enable debug logging"
)
@click.argument(
    "url", nargs=-1, metavar="URL", type=str
)
def download(url, root, config, threads, debug):
    """ Download (missing) episodes of podcasts.
    """

    worker = PodcastDownloader(
        root=root,
        threads=threads
    )

    if debug:
        worker.logger.setLevel(-1)

    worker.logger.addHandler(get_handler_with_default_formatter(StreamHandler))

    if len(url):
        map(worker.parse_feed, url)

    if config:
        cfg = yaml.load(config)
        for feed in cfg['feeds']:
            worker.parse_feed(**feed)

    worker.join()
