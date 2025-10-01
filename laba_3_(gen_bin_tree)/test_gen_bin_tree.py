import unittest
from fl_gen_bin_tree import *


class TestMySolutionG(unittest.TestCase):

    def test_go_left(self):
        """проверка функции go_left на штатную работу"""
        self.assertEqual(go_left(5), 12)
        self.assertEqual(go_left(-1), 0)
        self.assertEqual(go_left(-3), -4)

    def test_go_right(self):
        """проверка функции go_right на штатную работу"""
        self.assertEqual(go_right(5), 8)
        self.assertEqual(go_right(1), 0)
        self.assertEqual(go_right(-3), -8)

    def test_gen_bin_tree(self):
        """проверка функции gen_bin_tree (на выдачу ошибки при отрицательном уровне и на штатную работу)"""
        with self.assertRaises(ValueError):
            gen_bin_tree(1, -10)
        self.assertEqual(gen_bin_tree(2, 2),
                         {'2': [{
                             '6': [None, None]
                         }, {
                             '2': [None, None]
                         }]})


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
