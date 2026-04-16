from app import add

def test_add():
    assert add(2, 3) == 5

def test_fail():
    assert add(2, 2) == 99

def test_bullshit():
    assert add(2, 7) == 9