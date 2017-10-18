import tfat.password as pw


def test_get_random_ints():
    n = 16
    firstpw = pw.get_random_ints(n,0,10)
    assert firstpw != pw.get_random_ints(n,0,10)
    assert max(firstpw) < 11
    assert min(firstpw) > -1
    # There is a small chance this could fail randomly
    assert firstpw.count(firstpw[n-2]) < n

def test_get_random_string():
    n = 16
    firstpw = pw.get_random_string(n)
    assert firstpw != pw.get_random_string(n)
    # hex encoded should be double the byte size
    assert len(firstpw) == n * 2
    # There is a small chance this could fail randomly
    assert firstpw.count(firstpw[n-2]) < n
    
