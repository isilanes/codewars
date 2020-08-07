import unittest

from six_by_six_skyscrappers import seen_from_left, seen_from_right


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_seen_from_left(self):
        self.assertEqual(seen_from_left((1, 2, 3, 4, 5, 6)), 6)
        self.assertEqual(seen_from_left((1, 2, 3, 6, 5, 4)), 4)
        self.assertEqual(seen_from_left((1, 3, 2, 6, 5, 4)), 3)

    def test_seen_from_right(self):
        self.assertEqual(seen_from_right((1, 2, 3, 4, 5, 6)), 1)
        self.assertEqual(seen_from_right((1, 2, 3, 6, 5, 4)), 3)
        self.assertEqual(seen_from_right((1, 3, 2, 6, 5, 4)), 3)
