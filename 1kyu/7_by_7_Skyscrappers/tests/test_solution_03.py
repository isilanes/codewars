import unittest

from solution_03 import seen_from_left, seen_from_right, solve_puzzle


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_seen_from_left(self):
        self.assertEqual(seen_from_left([1, 2, 3, 4, 5, 6, 7]), 7)
        self.assertEqual(seen_from_left([1, 2, 3, 7, 6, 5, 4]), 4)
        self.assertEqual(seen_from_left([1, 3, 2, 6, 5, 7, 4]), 4)

    def test_seen_from_right(self):
        self.assertEqual(seen_from_right([1, 2, 3, 4, 5, 6, 7]), 1)
        self.assertEqual(seen_from_right([1, 2, 3, 7, 6, 5, 4]), 4)
        self.assertEqual(seen_from_right([1, 3, 2, 6, 5, 7, 4]), 2)

    @unittest.skip("not yet")
    def test_case_1(self):
        clues = [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]

        expected = [
            [1, 5, 6, 7, 4, 3, 2],
            [2, 7, 4, 5, 3, 1, 6],
            [3, 4, 5, 6, 7, 2, 1],
            [4, 6, 3, 1, 2, 7, 5],
            [5, 3, 1, 2, 6, 4, 7],
            [6, 2, 7, 3, 1, 5, 4],
            [7, 1, 2, 4, 5, 6, 3]
        ]

        self.assertEqual(solve_puzzle(clues), expected)

    @unittest.skip("Very hard")
    def test_case_2(self):
        clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1]

        expected = [
            [7, 6, 2, 1, 5, 4, 3],
            [1, 3, 5, 4, 2, 7, 6],
            [6, 5, 4, 7, 3, 2, 1],
            [5, 1, 7, 6, 4, 3, 2],
            [4, 2, 1, 3, 7, 6, 5],
            [3, 7, 6, 2, 1, 5, 4],
            [2, 4, 3, 5, 6, 1, 7]
        ]

        self.assertEqual(solve_puzzle(clues), expected)

    @unittest.skip("VERY hard")
    def test_case_2_extra(self):
        clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]

        expected = [
            [7, 6, 2, 1, 5, 4, 3],
            [1, 3, 5, 4, 2, 7, 6],
            [6, 5, 4, 7, 3, 2, 1],
            [5, 1, 7, 6, 4, 3, 2],
            [4, 2, 1, 3, 7, 6, 5],
            [3, 7, 6, 2, 1, 5, 4],
            [2, 4, 3, 5, 6, 1, 7]
        ]

        self.assertEqual(solve_puzzle(clues), expected)
