import sys
from .aws import get_instances_as_table, extract_data_from_objects, loop

def test_get_instances_as_table():
    x = get_instances_as_table('arena-staging')
    x.write(sys.stdout)

def test_extract_data_from_objects():
    class Test:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    x = Test(1, {'c':2, 'd':3})
    y = {'b':3, 'd':4}
    assert extract_data_from_objects([x, y]) == \
            [{'a': 1,
              'b.c': 2,
              'b.d': 3},
             {'b': 3,
              'd': 4}]

def test_loop():
    class Test:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    x = Test(1, {'c':2, 'd':3})
    y = {'c':3, 'd':4}
    assert loop('', {'a':x, 'b':y}) == \
        [[('.a.a', 1),
         [('.a.b.c', 2), ('.a.b.d', 3)]],
         [('.b.c', 3), ('.b.d', 4)]]

