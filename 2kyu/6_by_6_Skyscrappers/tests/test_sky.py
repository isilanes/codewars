import unittest

from six_by_six_skyscrappers import seen_from_left, seen_from_right, solve_puzzle


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

    @unittest.skip("Final test")
    def test_solver(self):
        clues = (
            3, 2, 2, 3, 2, 1,
            1, 2, 3, 3, 2, 2,
            5, 1, 2, 2, 4, 3,
            3, 2, 1, 2, 2, 4
        )

        expected = (
            (2, 1, 4, 3, 5, 6),
            (1, 6, 3, 2, 4, 5),
            (4, 3, 6, 5, 1, 2),
            (6, 5, 2, 1, 3, 4),
            (5, 4, 1, 6, 2, 3),
            (3, 2, 5, 4, 6, 1)
        )
        self.assertEqual(solve_puzzle(clues), expected)
