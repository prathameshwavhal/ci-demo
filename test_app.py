from app import add

def test_add():
    assert add(2, 3) == 5

def test_fail():
    assert add(2, 2) == 4

def test_third():
    assert add(2, 7) == 10