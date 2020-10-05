import unittest

from find_the_unknown_digit import solve_runes


CASES = [
    ("1+1=?", 2),
    ("123*45?=5?088", 6),
    ("-5?*-1=5?", 0),
    ("19--45=5?", -1),
    ("??*??=302?", 5),
    ("?*11=??", 2),
    ("??*1=??", 2,),
]


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_solve_runes(self):
        for runes, expected in CASES:
            self.assertEqual(solve_runes(runes), expected)
