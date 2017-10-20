import logging

PREFIX = "tfat"

logger = logging.getLogger(PREFIX)

logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())

formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
)


def get_handler_with_default_formatter(klass, *args, **kwargs):

    handler = klass(*args, **kwargs)
    handler.setFormatter(formatter)

    return handler
