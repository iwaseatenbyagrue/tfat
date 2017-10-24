import feedparser
import os.path
import shutil
import time
import traceback
import urllib2
import errno

from tfat.pipeline import Pipeline
from tfat import utils


class PodcastDownloader(Pipeline):

    def __init__(self, root=".", name=None, **kwargs):

        self._root = os.path.abspath(root)

        if not os.path.exists(self._root):
            raise AttributeError("root directory does not exist")

        self.logger = PodcastDownloader.logger.getChild("podcast")
        super(PodcastDownloader, self).__init__(**kwargs)

    def _log(self, data, err, pipe):

        if err:
            self.logger.error(
                "err {}: {}".format(
                    data.get("destination", "unknown"),
                    err[1]
                )
            )
            self.logger.debug("data: {}".format(data))

        else:
            self.logger.info(
                "completed {}".format(data["destination"])
            )

    @property
    def tasks(self):
        return [
            self.create_download_destination,
            self.create_download_request,
            self.download_content
        ] + self._tasks

    @property
    def callbacks(self):
        return [
            self._log
        ] + self._callbacks

    def create_download_destination(self, data, context={}):

        if "destination" not in data:
            download_name = "{} - {}".format(
                utils.datetime_from_struct(
                    data["entry"].get("published_parsed") or
                    data["entry"].get("updated_parsed")
                ).strftime("%Y%m%d"),
                data["entry"]["title"]
            )

            data["destination"] = os.path.join(
                self._root, data["name"], download_name
            )

        if not os.path.exists(os.path.dirname(data["destination"])):
            # There is a reasonable chance of a race condition here.
            # So long as the destination dir is created, no harm done.
            try:
                os.mkdir(os.path.dirname(data["destination"]))
            except (OSError) as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise(e)
        return data

    def create_download_request(self, data, context={}):

        url = filter(
            lambda content: content["type"].startswith("audio/"),
            data["entry"].get("media_content", []) +
            data["entry"].get("links", [])
        )[0]["url"]

        data["destination"] = "{}{}".format(
            data["destination"],
            os.path.splitext(url)[1]
        )

        if os.path.exists(data["destination"]):
            return data

        req = urllib2.Request(url)

        if os.path.exists("{}.part".format(data["destination"])):

            req.add_header(
                "Range",
                "{}-".format(os.path.getsize(
                    "{}.part".format(data["destination"])
                ))
            )

        data["req"] = req

        return data

    def download_content(self, data, context={}):

        if "req" not in data:
            return data

        with open("{}.part".format(data["destination"]), "ab") as fp:
            for chunk in utils.iter_chunks(urllib2.urlopen(data["req"])):
                fp.write(chunk)

        shutil.move(
            "{}.part".format(data["destination"]),
            data["destination"]
        )

        return data

    def parse_feed(self, url=None, name=None):

        feed = feedparser.parse(url)

        if name is None:
            name = feed.feed["title"]

        for episode in feed.entries:
            self.queue({
                "root_dir": self._root,
                "entry": episode,
                "name": name
            })
