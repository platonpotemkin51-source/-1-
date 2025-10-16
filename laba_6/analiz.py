import timeit
import matplotlib.pyplot as plt
from python.laba_3.r_gen_bin_tree import gen_bin_tree as build_tree_recursive
from python.laba_5.nr_gen_bin_tree import gen_bin_tree_mas as build_tree_iterative


def benchmark(func, start: int, n, number=1, repeat=5):
    '''функция возвращает минимальное время выполнения переданной
     ей func(start, n) из всех измерений '''
    times = timeit.repeat(lambda: func(start, n), number=number, repeat=repeat)
    return min(times)


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


if __name__ == "__main__":
    main()
