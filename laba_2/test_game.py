import unittest
from python.laba_2.game import *


class TestMySolutionG(unittest.TestCase):

    def test_perbor(self):
        """провека функции долгого перебора"""
        self.assertEqual(perebor(5, [2, 3, 4, 5, 6, 7]), [5, 4])
        self.assertEqual(perebor(5, [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7]), [5, 8])
        self.assertEqual(perebor(5, [-2, -1, 0, 1, 2, 3, 4]), None)
        self.assertEqual(perebor(5, [6, 7, 8, 9]), None)

    def test_bitperebor(self):
        """провека функции бинарного переборп"""
        self.assertEqual(bitperebor(5, [2, 3, 4, 5, 6, 7]), [5, 2])
        self.assertEqual(bitperebor(5, [-5, -4, -3, -1, 0, 1, 2, 3, 4, 5, 6]),
                         [5, 4])
        self.assertEqual(bitperebor(5, [2, 3, 4]), None)
        self.assertEqual(bitperebor(5, [6, 7, 8, 9, 10]), None)

    def test_vbr_lst(self):
        """провека функции выбора создования массива"""
        with self.assertRaises(ValueError):
            vbr_lst(-1)
        with self.assertRaises(ValueError):
            vbr_lst(3)

    def test_vbr0(self):
        """провека функции составляющая массив из подряд идущих чисел"""
        self.assertEqual(vbr_0(2, 8), [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(vbr_0(-2, 5), [-2, -1, 0, 1, 2, 3, 4, 5])
        with self.assertRaises(ValueError):
            vbr_0(5, 2)

    def test_vbr1(self):
        """провека функции составляющая массив из рандомных чисел"""
        with self.assertRaises(ValueError):
            vbr_1(5, 2, 5)
        with self.assertRaises(ValueError):
            vbr_1(1, 6, 0)
        with self.assertRaises(ValueError):
            vbr_1(1, 6, -2)


if __name__ == '__main__':
    unittest.main()

