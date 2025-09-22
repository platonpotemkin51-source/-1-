import unittest
from python.laba_2.game import *

class TestMySolutionG(unittest.TestCase):
    def test_perbor(self):
        self.assertEqual(perebor(5, [2, 3, 4, 5, 6, 7]), [5, 4])
        self.assertEqual(perebor(5, [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7]), [5, 8])
        self.assertEqual(perebor(5, [-2, -1, 0, 1, 2, 3, 4]), None)
        self.assertEqual(perebor(5, [6, 7,8 ,9]), None)

    def test_bitperebor(self):
        self.assertEqual(bitperebor(5, [2, 3, 4, 5, 6, 7]), [5, 2])
        self.assertEqual(bitperebor(5, [-5, -4, -3, -1, 0, 1, 2, 3, 4, 5, 6]), [5, 4])
        self.assertEqual(bitperebor(5, [2, 3, 4]), None)
        self.assertEqual(bitperebor(5, [6, 7, 8, 9, 10]), None)

    def test_vbr_lst(self):
        with self.assertRaises(ValueError):
            vbr_lst(-1)
        with self.assertRaises(ValueError):
            vbr_lst(3)

    def test_vbr0(self):
        self.assertEqual(vbr_0(2, 8), [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(vbr_0(-2, 5), [-2, -1, 0, 1, 2, 3, 4, 5])
        with self.assertRaises(ValueError):
            vbr_0(5, 2)

    def test_vbr1(self):
        with self.assertRaises(ValueError):
            vbr_1(5, 2, 5)
        with self.assertRaises(ValueError):
            vbr_1(1, 6, 0)
        with self.assertRaises(ValueError):
            vbr_1(1, 6, -2)

