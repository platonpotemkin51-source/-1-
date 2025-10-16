В ходе лабораторной работы:
- в наш код были импортированы функции генерирующие бинарное дерево разными методами (рекурсивным и без использования рекурсии)

      from python.laba_3.r_gen_bin_tree import gen_bin_tree as build_tree_recursive
      from python.laba_5.nr_gen_bin_tree import gen_bin_tree_mas as build_tree_iterative

- создана функция benchmark()
  
      def benchmark(func, start: int, n, number=1, repeat=5):
          times = timeit.repeat(lambda: func(start, n), number=number, repeat=repeat)
          return min(times)

    возвращает минимальное время выполнения переданной ей func(start, n) из всех измерений
- в функцию main():

      def main():
          test_data = list(range(2, 13))
      
          res_gen_rec = []
          res_gen_no_rec = []
      
          for n in test_data:
              # заполнение res_gen_rec и res_gen_no_rec для дальнейшего
              # сравнения скорость выполнения соответствующих функций
              res_gen_rec.append(benchmark(build_tree_recursive, 4, n, number=1000,
                                           repeat=5))
              res_gen_no_rec.append(
                  benchmark(build_tree_iterative, 4, n, number=1000, repeat=5))
      
          # Визуализация
          plt.plot(test_data, res_gen_rec, label="Рекурсивный")
          plt.plot(test_data, res_gen_no_rec, label="Не рекурсивный")
          plt.xlabel("высота дерева")
          plt.ylabel("время построения дерева (сек)")
          plt.title("Сравнение рекурсивного и не рекурсивного методов")
          plt.legend()
          plt.show()

  - задаем интервал значений соответствующий высотам деревьев

        test_data = list(range(2, 13))
    
  - затем определям массивы в которые позже будет добавлятся время выполнения соответсвующих функций
    
          res_gen_rec = []
          res_gen_no_rec = []

  - затем мы заполняем данные массивы значениями соответствующии времени выполнения соответсвующей функции

        for n in test_data:
            # заполнение res_gen_rec и res_gen_no_rec для дальнейшего
            # сравнения скорость выполнения соответствующих функций
            res_gen_rec.append(benchmark(build_tree_recursive, 4, n, number=1000,
                                         repeat=5))
            res_gen_no_rec.append(
                benchmark(build_tree_iterative, 4, n, number=1000, repeat=5))
    
  - затем визуализируем в графики время выполнения от высоты дерева реализованных разными методами
 
        plt.plot(test_data, res_gen_rec, label="Рекурсивный")
        plt.plot(test_data, res_gen_no_rec, label="Не рекурсивный")
        plt.xlabel("высота дерева")
        plt.ylabel("время построения дерева (сек)")
        plt.title("Сравнение рекурсивного и не рекурсивного методов")
        plt.legend()
        plt.show()

    график:

    
