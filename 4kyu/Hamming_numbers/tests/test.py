import unittest

from hamming_numbers import hamming


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def hamming_1(self):
        self.assertEqual(hamming(1), 1)

