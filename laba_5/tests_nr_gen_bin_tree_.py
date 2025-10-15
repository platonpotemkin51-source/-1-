import unittest
from nr_gen_bin_tree import *


class TestMySolutionG(unittest.TestCase):

    def test_gen_bin_tree_mas(self):
        """проверка функции gen_bin_tree_mas
         (на выдачу ошибки при отрицательном уровне и на штатную работу)"""
        with self.assertRaises(ValueError):
            gen_bin_tree_mas(1, -10)
        self.assertEqual(gen_bin_tree_mas(2, 2), [2, 6, 2])

    def test_sp_tree(self):
        """проверка функции sp_tree
        (на выдачу ошибки и на штатную работу)"""
        with self.assertRaises(ValueError):
            sp_tree([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(
            sp_tree([4, 10, 6, 22, 18, 14, 10]), {
                '4': [{
                    '10': [{
                        '22': []
                    }, {
                        '18': []
                    }]
                }, {
                    '6': [{
                        '14': []
                    }, {
                        '10': []
                    }]
                }]
            })


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
