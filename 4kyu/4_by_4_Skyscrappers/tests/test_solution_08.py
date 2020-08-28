import unittest
from random import randint

from cases import CASES
from solution_08 import seen_from_left, seen_from_right, solve_puzzle, Puzzle


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_seen_from_left(self):
        self.assertEqual(seen_from_left([1, 2, 3, 4]), 4)
        self.assertEqual(seen_from_left([1, 2, 4, 3]), 3)
        self.assertEqual(seen_from_left([1, 3, 2, 4]), 3)

    def test_seen_from_right(self):
        self.assertEqual(seen_from_right([1, 2, 3, 4]), 1)
        self.assertEqual(seen_from_right([1, 2, 4, 3]), 2)
        self.assertEqual(seen_from_right([1, 3, 2, 4]), 1)

    def test_row_clues(self):
        clues = tuple([randint(1, 100) for _ in range(16)])
        expected = [
            (clues[15], clues[4]),
            (clues[14], clues[5]),
            (clues[13], clues[6]),
            (clues[12], clues[7]),
        ]
        p = Puzzle(clues)

        self.assertEqual(p.row_clues, expected)

    def test_col_clues(self):
        clues = tuple([randint(1, 100) for _ in range(16)])
        expected = [
            (clues[0], clues[11]),
            (clues[1], clues[10]),
            (clues[2], clues[9]),
            (clues[3], clues[8]),
        ]
        p = Puzzle(clues)

        self.assertEqual(p.col_clues, expected)

    def _run_case(self, name):
        clues = CASES[name]["clues"]
        expected = CASES[name]["expected"]
        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_default(self):
        self._run_case("default")

    def test_case_default2(self):
        self._run_case("default2")
