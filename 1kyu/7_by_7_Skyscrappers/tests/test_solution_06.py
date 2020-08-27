import unittest
from random import randint

from cases import CASES
from solution_06 import seen_from_left, seen_from_right, solve_puzzle, Puzzle


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

    def _run_case(self, name):
        clues = CASES[name]["clues"]
        expected = CASES[name]["expected"]
        self.assertEqual(solve_puzzle(clues), expected)

    def test_case_medium(self):
        self._run_case("medium")

    def test_case_case2(self):
        self._run_case("case2")

    def test_case_case2extra(self):
        self._run_case("case2extra")

    def test_case_hard(self):
        self._run_case("hard")

    def test_case_hard2(self):
        self._run_case("hard2")

    def test_case_very_hard(self):
        self._run_case("very_hard")

    def test_case_very_hard_2(self):
        self._run_case("very_hard2")

    def test_case_medved(self):
        self._run_case("medved")

    def test_case_random1(self):
        self._run_case("random1")

    def test_case_random2(self):
        self._run_case("random2")

    def test_case_random3(self):
        self._run_case("random3")
