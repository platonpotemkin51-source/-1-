from main import two_sum
import unittest

class TestMySolution(unittest.TestCase):

  def test_simple(self):
    self.assertEqual(two_sum([3,3],6),[0,1])
    self.assertEqual(two_sum([2,7,11,15],9),[0,1])
    self.assertEqual(two_sum([3,2,4],6),[1,2])
    with self.assertRaises(ValueError):   # неверный тип данных в nums
      two_sum([1,2,3,'4'],5)
    with self.assertRaises(ValueError):   #
      two_sum([1,2,3,4.1],5)
    with self.assertRaises(ValueError):   #
      two_sum([1,2,[3],4.1],5)
    with self.assertRaises(ValueError):   # неверный тип данных nums
      two_sum(1,5)
    with self.assertRaises(ValueError):   #
      two_sum(5.0,5)
    with self.assertRaises(ValueError):   #
      two_sum('1',5)
    with self.assertRaises(ValueError):   # неверный тип данных target
      two_sum([1,2,3,4],[5])
    with self.assertRaises(ValueError):   #
      two_sum([1,2,3,4],'5')
    with self.assertRaises(ValueError):   #
      two_sum([1,2,3,4],5.0)
    with self.assertRaises(ValueError):   # недостаточно чисел в nums
      two_sum([1],5)
    with self.assertRaises(ValueError):   #
      two_sum([],5)






if __name__=='__main__':
  unittest.main()