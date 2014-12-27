import unittest
from classes import State


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

    def test_zero(self):
        s = State()
        self.assertFalse(s)

    def test_nonzero(self):
        s = State()
        s.field = 3
        self.assertTrue(s)

    def test_not_contains(self):
        s = State()
        self.assertFalse('field' in s)

    def test_contains(self):
        s = State()
        s.field = 3
        self.assertTrue('field' in s)

    def test_to_from_empty(self):
        d = {}
        self.assertEqual(d, dict(State.from_dict(d)))

    def test_to_from_singleton(self):
        d = {'a': 1}
        self.assertEqual(d, dict(State.from_dict(d)))

    def test_to_from_many(self):
        d = dict(enumerate('hello world what a beautiful day'.split()))
        self.assertEqual(d, dict(State.from_dict(d)))

    def test_to_from_lists(self):
        d = dict(enumerate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        self.assertEqual(d, dict(State.from_dict(d)))

    def test_to_from_nested(self):
        d = {'a': {'b': -1784}, 'c': {'d': 51397, 'e': {'f': 42}}}
        self.assertEqual(d, dict(State.from_dict(d)))

