import tfat.password as pw
import re


def test_get_random_ints():
    n = 16
    firstpw = pw.get_random_ints(n, 0, 10)
    assert firstpw != pw.get_random_ints(n, 0, 10)
    assert max(firstpw) < 11
    assert min(firstpw) > -1
    # There is a small chance this could fail randomly
    assert firstpw.count(firstpw[n-2]) < n
    # Ensure negative numbers are converted to positive
    assert len(pw.get_random_ints(-1)) == 1


def test_get_random_string():
    n = 16
    firstpw = pw.get_random_string(n)
    assert firstpw != pw.get_random_string(n)
    # hex encoded should be double the byte size
    assert len(firstpw) == n * 2
    # There is a small chance this could fail randomly
    assert firstpw.count(firstpw[n-2]) < n


def test_get_random_string_from_rules():
    n = 16

    rules = {
        "lowercase": 12,
        "uppercase": 12,
        "digits": 31,
        "punctuation": 1
    }

    assert pw.get_random_string_from_rules(n, rules=rules) is None

    rules = {
        "lowercase": 2,
        "uppercase": 2,
        "digits": 3,
        "punctuation": 1
    }

    firstpw = pw.get_random_string_from_rules(n, rules=rules)
    assert firstpw is not None
    assert firstpw != pw.get_random_string_from_rules(n, rules=rules)
    assert len(firstpw) == n
    assert len(re.findall(r"\d", firstpw)) >= rules["digits"]

    assert len(pw.get_random_string_from_rules(n, printable=True)) == n
    assert len(pw.get_random_string_from_rules(n, printable=False)) == n


def test_get_random_characters_from_class():
    n = 16
    for char_class in ["all", "lowercase", "strawberry"]:
        assert len(pw.get_random_characters_from_class(n, char_class)) == n
