import string

from random import SystemRandom

_sysrandom = SystemRandom()

character_class_map = {
    "lowercase": string.lowercase,
    "uppercase": string.uppercase,
    "punctuation": string.punctuation,
    "whitespace": string.whitespace,
    "digits": string.digits,
    "printable": string.printable,
    "all": map(chr, range(0, 256))
}


def get_random_ints(n, start=0, stop=255):
    """ Get an array of random integers within an inclusive range.

    :param  n:   The number of integers to pick.
    :param  start:  The beginning of the range - default is 0.
    :param  stop:  The end of the range - default is 255.

    :returns: An array of n integers between start and stop.
    """
    return [_sysrandom.randint(start, stop) for x in range(abs(int(n)))]


def get_random_string(n, encoding='hex'):
    """ Get an encoded string of random bytes.

    The resulting string's size will depend on the encoding.

    :param  n:   The number of bytes to use.
    :param  encoding:    The encoding to apply to the result.
                        The default is hex.

    :returns: A string obtained by encoding n bytes.
    """
    return "".join(
        map(chr, get_random_ints(n, start=0, stop=255))
    ).encode(encoding)


def get_random_characters_from_class(n, character_class):

    return [
        _sysrandom.choice(
            character_class_map.get(character_class, "all")
        ) for x in range(0, n)
    ]


def get_random_string_from_rules(n, printable=True, rules={}):

    if sum(rules.values()) > n:
        return None

    rules = dict(filter(lambda pair: pair[1] > 0, rules.items()))

    pw = []
    for rule, count in rules.items():
        pw.extend(get_random_characters_from_class(count, rule))

    if len(pw) == n:
        return pw

    char_pool = "".join(
        filter(bool,  map(character_class_map.get, rules))
    )

    if not char_pool:
        char_pool = character_class_map.get(
            "all" if not printable else "printable"
        )

    pw.extend(
        [_sysrandom.choice(char_pool) for x in range(n - len(pw))]
    )

    _sysrandom.shuffle(pw)

    return "".join(pw)
