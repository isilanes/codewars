import unittest
from random import randint

from solution_05 import seen_from_left, seen_from_right, solve_puzzle, Puzzle


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

    def test_row_clues(self):
        clues = tuple([randint(1, 100) for _ in range(28)])
        expected = [
            (clues[27], clues[7]),
            (clues[26], clues[8]),
            (clues[25], clues[9]),
            (clues[24], clues[10]),
            (clues[23], clues[11]),
            (clues[22], clues[12]),
            (clues[21], clues[13]),
        ]
        p = Puzzle(clues)

        self.assertEqual(p.row_clues, expected)

    def test_col_clues(self):
        clues = tuple([randint(1, 100) for _ in range(28)])
        expected = [
            (clues[0], clues[20]),
            (clues[1], clues[19]),
            (clues[2], clues[18]),
            (clues[3], clues[17]),
            (clues[4], clues[16]),
            (clues[5], clues[15]),
            (clues[6], clues[14]),
        ]
        p = Puzzle(clues)

        self.assertEqual(p.col_clues, expected)

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

    @unittest.skip("slow")
    def test_case_hard(self):
        clues = [6, 4, 0, 2, 0, 0, 3, 0, 3, 3, 3, 0, 0, 4, 0, 5, 0, 5, 0, 2, 0, 0, 0, 0, 4, 0, 0, 3]

        expected = [
            [2, 1, 6, 4, 3, 7, 5],
            [3, 2, 5, 7, 4, 6, 1],
            [4, 6, 7, 5, 1, 2, 3],
            [1, 3, 2, 6, 7, 5, 4],
            [5, 7, 1, 3, 2, 4, 6],
            [6, 4, 3, 2, 5, 1, 7],
            [7, 5, 4, 1, 6, 3, 2]
        ]

        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_hard_2(self):
        clues = [0, 0, 0, 5, 0, 0, 3, 0, 6, 3, 4, 0, 0, 0, 3, 0, 0, 0, 2, 4, 0, 2, 6, 2, 2, 2, 0, 0]

        expected = [
            [3, 5, 6, 1, 7, 2, 4],
            [7, 6, 5, 2, 4, 3, 1],
            [2, 7, 1, 3, 6, 4, 5],
            [4, 3, 7, 6, 1, 5, 2],
            [6, 4, 2, 5, 3, 1, 7],
            [1, 2, 3, 4, 5, 7, 6],
            [5, 1, 4, 7, 2, 6, 3]
        ]

        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_very_hard(self):
        clues = [0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3]

        expected = [
            [3, 4, 1, 7, 6, 5, 2],
            [7, 1, 2, 5, 4, 6, 3],
            [6, 3, 5, 2, 1, 7, 4],
            [1, 2, 3, 6, 7, 4, 5],
            [5, 7, 6, 4, 2, 3, 1],
            [4, 5, 7, 1, 3, 2, 6],
            [2, 6, 4, 3, 5, 1, 7]
        ]

        self.assertEqual(solve_puzzle(clues), expected)

    @unittest.skip("slow")
    def test_case_very_hard_2(self):
        clues = [0, 0, 5, 3, 0, 2, 0, 0, 0, 0, 4, 5, 0, 0, 0, 0, 0, 3, 2, 5, 4, 2, 2, 0, 0, 0, 0, 5]

        expected = [
            [2, 3, 1, 4, 6, 5, 7],
            [1, 7, 4, 6, 5, 2, 3],
            [3, 6, 5, 7, 2, 1, 4],
            [7, 5, 6, 3, 1, 4, 2],
            [6, 2, 7, 5, 4, 3, 1],
            [5, 4, 2, 1, 3, 7, 6],
            [4, 1, 3, 2, 7, 6, 5]
        ]

        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_medved(self):
        clues = [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]

        expected = [
            [2, 1, 4, 7, 6, 5, 3],
            [6, 4, 7, 3, 5, 1, 2],
            [1, 2, 3, 6, 4, 7, 5],
            [5, 7, 6, 2, 3, 4, 1],
            [4, 3, 5, 1, 2, 6, 7],
            [7, 6, 2, 5, 1, 3, 4],
            [3, 5, 1, 4, 7, 2, 6]
        ]

        self.assertEqual(solve_puzzle(clues), expected)
