from main import two_sum
import unittest


class TestMySolution(unittest.TestCase):

    def test_twos_simple(self):
        '''проверка штатной работы'''
        self.assertEqual(two_sum([3, 3], 6), [0, 1])
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])

    def test_twos_innums(self):
        '''тест вывода ошибки : неверный тип данных в nums'''
        with self.assertRaises(ValueError):
            two_sum([1, 2, 3, '4'], 5)
        with self.assertRaises(ValueError):
            two_sum([1, 2, 3, 4.1], 5)
        with self.assertRaises(ValueError):
            two_sum([1, 2, [3], 4.1], 5)

    def test_twos_nums(self):
        '''тест вывода ошибки : неверный тип данных nums'''
        with self.assertRaises(ValueError):
      two_sum(1, 5)
        with self.assertRaises(ValueError):
      two_sum(5.0, 5)
        with self.assertRaises(ValueError):
      two_sum('1', 5)

    def test_twos_tar(self):
        '''тест вывода ошибки : неверный тип данных target'''
        with self.assertRaises(ValueError):
            two_sum([1, 2, 3, 4], [5])
        with self.assertRaises(ValueError):
            two_sum([1, 2, 3, 4], '5')
        with self.assertRaises(ValueError):
            two_sum([1, 2, 3, 4], 5.0)

    def test_twos_kolnums(self):
        '''тест вывода ошибки : недостаточно чисел в nums'''
        with self.assertRaises(ValueError):
            two_sum([1], 5)
        with self.assertRaises(ValueError):
            two_sum([], 5)


if __name__ == '__main__':
    unittest.main()



