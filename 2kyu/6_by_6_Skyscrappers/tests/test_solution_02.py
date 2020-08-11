import unittest

from solution_02 import seen_from_left, seen_from_right, solve_puzzle


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

    def test_case_1(self):
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

    def test_case_2(self):
        clues = (0, 0, 0, 2, 2, 0,
                 0, 0, 0, 6, 3, 0,
                 0, 4, 0, 0, 0, 0,
                 4, 4, 0, 3, 0, 0)

        expected = ((5, 6, 1, 4, 3, 2),
                    (4, 1, 3, 2, 6, 5),
                    (2, 3, 6, 1, 5, 4),
                    (6, 5, 4, 3, 2, 1),
                    (1, 2, 5, 6, 4, 3),
                    (3, 4, 2, 5, 1, 6))

        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_3(self):
        clues = (0, 3, 0, 5, 3, 4,
                 0, 0, 0, 0, 0, 1,
                 0, 3, 0, 3, 2, 3,
                 3, 2, 0, 3, 1, 0)

        expected = ((5, 2, 6, 1, 4, 3),
                    (6, 4, 3, 2, 5, 1),
                    (3, 1, 5, 4, 6, 2),
                    (2, 6, 1, 5, 3, 4),
                    (4, 3, 2, 6, 1, 5),
                    (1, 5, 4, 3, 2, 6))

        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_random_1(self):
        clues = (3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3)
        expected = (
            (3, 5, 6, 4, 1, 2),
            (2, 4, 5, 3, 6, 1),
            (5, 1, 2, 6, 3, 4),
            (4, 6, 1, 5, 2, 3),
            (6, 2, 3, 1, 4, 5),
            (1, 3, 4, 2, 5, 6)
        )
        self.assertEqual(solve_puzzle(clues), expected)
