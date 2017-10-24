import click
import tfat.options as stdopts


from .downloader import PodcastDownloader
from logging import StreamHandler
from os.path import expanduser
from tfat.pipeline import Pipeline
from tfat.logger import get_handler_with_default_formatter

@click.group("download")
@click.version_option(version="0.1", prog_name="tfat-download")
def cli():
    """ Build and update a podcast collection.
    """
    pass


@cli.command()
@stdopts.config_option()
@stdopts.debug_option()
@stdopts.root_dir_option(default=expanduser("~/Podcasts"), show_default=True)
@stdopts.threads_option()
@click.argument(
    "url", nargs=-1, metavar="URL", type=str
)
def podcast(url, root, config, threads, debug):
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
