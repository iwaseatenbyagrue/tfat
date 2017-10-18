from random import SystemRandom

_sysrandom = SystemRandom()

def get_random_ints(n,start=0,stop=255):
    """ Get an array of random integers within an inclusive range.
    
    :param  n:   The number of integers to pick.
    :param  start:  The beginning of the range - default is 0.
    :param  stop:  The end of the range - default is 255.
    
    :returns: An array of n integers between start and stop.
    """
    return [_sysrandom.randint(start, stop) for x in range(int(n))]

def get_random_string(n, encoding='hex'):
    """ Get an encoded string of random bytes.
    
    The actual size of the string might be different depending on encoding
    
    :param  n:   The number of bytes to use.
    :param  encoding:    The encoding to apply to the result.
                        The default is hex.
    :returns: A string obtained by encoding n bytes.
    """
    return "".join(
            map(chr,get_random_ints(n, start=0, stop=255))
        ).encode(encoding)
