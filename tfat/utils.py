import urllib2
from datetime import datetime


def iter_chunks(fp, chunk_size=2**16):
    """ Retrieve data from a file-like in chunks.
    """
    while True:
        chunk = fp.read(chunk_size)
        if len(chunk):
            yield chunk
        else:
            break


def datetime_from_struct(time_struct):

    return datetime(
        year=time_struct.tm_year,
        month=time_struct.tm_mon,
        day=time_struct.tm_mday,
        hour=time_struct.tm_hour,
        minute=time_struct.tm_min,
        second=time_struct.tm_sec
    )
