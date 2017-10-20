import logging
import sys

from Queue import Queue, Empty
from threading import Thread, Event


class Pipeline(object):

    """ A task and callback based processing pipeline
    """

    logger = logging.getLogger(__name__)

    def __init__(self, tasks=[], callbacks=[], threads=1, context={}):

        self._queue = Queue()
        self._tasks = tasks
        self._callbacks = callbacks

        # Signalling for workers to cease work
        self._halt = Event()

        # Empty thread pool
        self._threads = []

        self._context = context

        self._start_workers(threads)

    def _start_workers(self, threads):
        self.logger.debug("initalising {} threads".format(threads))

        for x in range(threads):

            t = Thread(
                target=self._worker,
                kwargs={
                    "tasks": self.tasks,
                    "callbacks": self.callbacks
                }
            )
            t.name = "{}.{}".format(self.__class__.__name__, t)

            t.daemon = True

            t.start()
            self._threads.append(t)

    @property
    def tasks(self):
        return self._tasks

    @property
    def threads(self):
        return len(self._threads)

    @property
    def callbacks(self):
        return self._callbacks

    def join(self):
        self.logger.debug("join() called")
        self._queue.join()

    def halt(self):
        self.logger.info("halting")
        if not self._halt.is_set():
            self._halt.set()

    def queue(self, *args):
        for arg in args:
            self._queue.put(arg)

    def get_context(self):
        """ Return a view of the pipeline's context.
        """

        return self._context.viewitems()

    def _worker(self, tasks=[], callbacks=[]):

        """

        """
        self.logger.debug("worker started")

        while not self._halt.is_set():
            try:
                data = self._queue.get()
                self.logger.debug(
                    "worker job received: {}".format(data)
                )

                err = None

                try:
                    for task in tasks:
                        data = task(
                            data, context=self.get_context()
                        )
                except:
                    err = sys.exc_info()

                for cb in callbacks:
                    cb(data, err, self.get_context())

                self._queue.task_done()
                self.logger.debug(
                    "worker job completed: {}, err: {}".format(data, err)
                )

            except Empty:
                pass
