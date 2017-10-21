import click
import tfat.options as stdopts
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
@stdopts.config_option()
@stdopts.debug_option()
@stdopts.root_dir_option()
@stdopts.threads_option()
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
        for feed in config['feeds']:
            worker.parse_feed(**feed)

    worker.join()
