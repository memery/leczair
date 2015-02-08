import unittest
from frozenstate import empty, single, append, concat, from_dict, to_dict

class StateTest(unittest.TestCase):
    # TODO: also test append & concat

    def test_access(self):
        s = single('field', 3)
        self.assertEqual(s.field, 3)

    def test_nested_creation(self):
        s = single('field.subfield', 3)
        self.assertEqual(s.field.subfield, 3)

    def test_automatic_creation(self):
        s = single('field', 3)
        self.assertFalse(s.otherfield)

    def test_zero(self):
        s = empty()
        self.assertFalse(s)

    def test_nonzero(self):
        s = single('field', 3)
        self.assertTrue(s)

    def test_not_contains(self):
        s = empty()
        self.assertFalse('field' in s)

    def test_contains(self):
        s = single('field', 3)
        self.assertTrue('field' in s)

    def test_from_dict(self):
        s = from_dict({'a': 1})
        self.assertEqual(s.a, 1)

    def test_nested_from_dict(self):
        s = from_dict({'a': {'b': {'c': 1}}})
        self.assertEqual(s.a.b.c, 1)

    def test_to_from_empty(self):
        d = {}
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_to_from_singleton(self):
        d = {'a': 1}
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_to_from_many(self):
        d = dict(zip('abcdefg', 'hello world what a beautiful day'.split()))
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_to_from_lists(self):
        d = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
        self.assertEqual(d, to_dict(from_dict(d)))

    def test_to_from_nested(self):
        d = {'a': {'b': -1784}, 'c': {'d': 51397, 'e': {'f': 42}}}

