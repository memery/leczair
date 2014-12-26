import unittest
from stateobj import State, from_dict, to_dict


class StateTest(unittest.TestCase):
    def test_access(self):
        s = State()
        s.field = 3
        self.assertEqual(s.field, 3)

    def test_nested_access(self):
        s = State()
        s.field = State()
        s.field.subfield = 3
        self.assertEqual(s.field.subfield, 3)

    def test_field_creation(self):
        s = State()
        s.field
        s.field.subfield = 3
        self.assertEqual(s.field.subfield, 3)

    def test_nested_field_creation(self):
        s = State()
        s.field.subfield
        s.field.subfield.value = 3
        self.assertEqual(s.field.subfield.value, 3)


class ToFromDictTest(unittest.TestCase):
    def test_empty(self):
        d = {}
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_singleton(self):
        d = {'a': 1}
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_many(self):
        d = dict(enumerate('hello world what a beautiful day'.split()))
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_lists(self):
        d = dict(enumerate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_nested(self):
        d = {'a': {'b': -1784}, 'c': {'d': 51397, 'e': {'f': 42}}}
        self.assertEqual(d, to_dict(from_dict(d)))


