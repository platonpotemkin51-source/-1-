import math
from typing import Callable, Union
import concurrent.futures as ftres
from functools import partial
import timeit
import matplotlib.pyplot as plt
import numpy as np
import time
from integrate_cy import integrate_cos, integrate_x2, integrate_2x, integrate_generic, integrate_cos_nogil



def integrate(f: Callable[[float], float],
              a: Union[int, float],
              b: Union[int, float],
              *,
              n_iter: int = 100_000) -> float:
    """
    Вычисляет определённый интеграл функции f на отрезке [a, b]
    методом средних прямоугольников.

    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция. Принимает один аргумент типа float,
        возвращает значение типа float.
    a : Union[int, float]
        Нижний предел интегрирования.
    b : Union[int, float]
        Верхний предел интегрирования.
    n_iter : int, optional
        Количество разбиений отрезка [a, b] (по умолчанию 100000).

    Returns
    -------
    float
        Приближённое значение интеграла ∫_{a}^{b} f(x) dx.

    Notes
    -----
    Метод прямоугольников имеет первый порядок точности.
    Точность результата зависит от гладкости функции и числа n_iter.

    Examples
    --------
    >>> integrate(math.cos, 0, math.pi/2, n_iter=10000)  # ∫cos(x)dx = sin(x)|_0^{π/2} = 1
    1.0000785377601717

    >>> integrate(lambda x: 2*x, 0, 1, n_iter=1000)      # ∫2x dx = x^2|_0^1 = 1
    0.9990000000000003

    >>> integrate(lambda x: x**2, 0, 2, n_iter=10000)    # ∫x^2 dx = (x^3)/3|_0^2 = 8/3 ≈ 2.6667
    2.6662666799999966
    """
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительный")
    if a >= b:
        raise ValueError("a должен быть меньше b")

    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_threaded(f: Callable[[float], float],
                       a: Union[int, float],
                       b: Union[int, float],
                       *,
                       n_jobs: int = 2,
                       n_iter: int = 100_000) -> float:
    """
    Вычисляет интеграл с использованием потоков (ThreadPoolExecutor).

    Отрезок [a, b] делится на n_jobs частей, каждая часть вычисляется
    в отдельном потоке функцией integrate.

    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция.
    a, b : Union[int, float]
        Пределы интегрирования.
    n_jobs : int, optional
        Количество потоков (по умолчанию 2).
    n_iter : int, optional
        Общее число итераций (по умолчанию 100000).

    Returns
    -------
    float
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs должен быть положительным")
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")

    # Делим работу между потоками
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    # Создаем частичную функцию с зафиксированными аргументами
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    # Создаем задачи для каждого потока
    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    # Собираем результаты
    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)


def integrate_multiprocess(f: Callable[[float], float],
                           a: Union[int, float],
                           b: Union[int, float],
                           *,
                           n_jobs: int = 2,
                           n_iter: int = 100_000) -> float:
    """
    Вычисляет интеграл с использованием процессов (ProcessPoolExecutor).

    Каждый процесс работает в отдельном интерпретаторе Python,
    что позволяет обойти ограничение GIL для CPU-задач.

    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция.
    a, b : Union[int, float]
        Пределы интегрирования.
    n_jobs : int, optional
        Количество процессов (по умолчанию 2).
    n_iter : int, optional
        Общее число итераций (по умолчанию 100000).

    Returns
    -------
    float
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")

    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)



def integrate_multiprocess_with_C(f: Callable[[float], float],
                           a: Union[int, float],
                           b: Union[int, float],
                           *,
                           n_jobs: int = 2,
                           n_iter: int = 100_000) -> float:
    """
    Вычисляет интеграл с использованием процессов (ProcessPoolExecutor).

    Каждый процесс работает в отдельном интерпретаторе Python,
    что позволяет обойти ограничение GIL для CPU-задач.

    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция.
    a, b : Union[int, float]
        Пределы интегрирования.
    n_jobs : int, optional
        Количество процессов (по умолчанию 2).
    n_iter : int, optional
        Общее число итераций (по умолчанию 100000).

    Returns
    -------
    float
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")

    # Важно: функция integrate должна быть доступна в дочерних процессах
    # В реальном коде лучше вынести её в отдельный модуль

    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate_generic, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)


def integrate_multiprocess_with_C_with_C_API(a: Union[int, float],
                           b: Union[int, float],
                           *,
                           n_jobs: int = 2,
                           n_iter: int = 100_000) -> float:
    """
    Вычисляет интеграл с использованием процессов (ProcessPoolExecutor).

    Каждый процесс работает в отдельном интерпретаторе Python,
    что позволяет обойти ограничение GIL для CPU-задач.

    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция.
    a, b : Union[int, float]
        Пределы интегрирования.
    n_jobs : int, optional
        Количество процессов (по умолчанию 2).
    n_iter : int, optional
        Общее число итераций (по умолчанию 100000).

    Returns
    -------
    float
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")

    # Важно: функция integrate должна быть доступна в дочерних процессах
    # В реальном коде лучше вынести её в отдельный модуль

    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate_cos, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)

def integrate_threaded_with_C(f: Callable[[float], float],
                       a: Union[int, float],
                       b: Union[int, float],
                       *,
                       n_jobs: int = 2,
                       n_iter: int = 100_000) -> float:
    """
    integrate_threaded с оптимизацией через C
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs должен быть положительным")
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")

    # Делим работу между потоками
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    # Создаем частичную функцию с зафиксированными аргументами
    spawn = partial(executor.submit, integrate_generic, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    # Создаем задачи для каждого потока
    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    # Собираем результаты
    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)


def integrate_threaded_with_C_with_C_API(a: Union[int, float],
                       b: Union[int, float],
                       *,
                       n_jobs: int = 2,
                       n_iter: int = 100_000) -> float:
    """
    integrate_threaded с оптимизацией через C и оптимизацией C-API
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs должен быть положительным")
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")

    # Делим работу между потоками
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    # Создаем частичную функцию с зафиксированными аргументами
    spawn = partial(executor.submit, integrate_cos, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    # Создаем задачи для каждого потока
    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    # Собираем результаты
    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)

def integrate_threaded_nogil(a: Union[int, float],
                       b: Union[int, float],
                       *,
                       n_jobs: int = 2,
                       n_iter: int = 100_000) -> float:
    """
    Вычисляет интеграл с использованием потоков (ThreadPoolExecutor).

    Отрезок [a, b] делится на n_jobs частей, каждая часть вычисляется
    в отдельном потоке функцией integrate.

    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция.
    a, b : Union[int, float]
        Пределы интегрирования.
    n_jobs : int, optional
        Количество потоков (по умолчанию 2).
    n_iter : int, optional
        Общее число итераций (по умолчанию 100000).

    Returns
    -------
    float
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs должен быть положительным")
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")

    # Делим работу между потоками
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    # Создаем частичную функцию с зафиксированными аргументами
    spawn = partial(executor.submit, integrate_cos_nogil, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = []

    # Создаем задачи для каждого потока
    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        fs.append(spawn(left, right))

    # Собираем результаты
    results = [f.result() for f in ftres.as_completed(fs)]
    executor.shutdown()

    return sum(results)


# --------------------- benchmarks -----------------------

def bench_0():
    """Замер времени для разного числа итераций для базовой реализации"""

    setups = [
        ("100 итераций", 100),
        ("1 000 итераций", 1000),
        ("10 000 итераций", 10000),
        ("100 000 итераций", 100000)
    ]
    setups_for_plt = [
        "100",
        "1 000",
        "10 000",
        "100 000",
    ]
    times_for_plt = []
    print("Бенчмарк базовой реализации:")
    print("-" * 50)
    for name, n in setups:
        time = timeit.timeit(
            stmt="integrate(math.cos, 0, math.pi/2, n_iter=n)",
            setup=f"from integrates import integrate, math; n={n}",
            number=10
        )
        times_for_plt.append(time/10)
        print(f"{name:20} | {time:.6f} сек (10 прогонов) | {time / 10:.6f} сек/вызов")

    plt.bar(setups_for_plt, times_for_plt)

    plt.xlabel('Количество итераций')
    plt.ylabel('Время выполнения')
    plt.title('Анализ производительности integrate от количества итераций')

    plt.show()

def bench_1(time_integrate):
    """Бенчмарк многопоточности версии (100 000 итераций)"""
    result = integrate_threaded(math.sin, 0, math.pi, n_jobs=4, n_iter=100_000)
    print(f"∫sin(x)dx от 0 до π = {result} (ожидается 2.0)")

    # Бенчмарк
    print("\nБенчмарк многопоточности версии (100 000 итераций):")

    times_potok = []
    n_jobs_x_potok = [1, 2, 4, 6, 8]

    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_threaded(math.cos, 0, math.pi/2, n_jobs={n_jobs}, n_iter=100_000)',  # код для выполнения
            setup='import math; from __main__ import integrate_threaded',
            number=10
        )

        times_potok.append(time / 10)
        print(f"Потоков: {n_jobs}, время: {time / 10:.4f} сек")

    plt.bar(n_jobs_x_potok, times_potok)

    plt.axhline(y=time_integrate / 10, color='red', linestyle='--', label=f'{time_integrate / 10:.4f}')

    plt.xlabel('Количество потоков')
    plt.ylabel('Время выполнения')
    plt.title('Анализ производительности')
    plt.legend()

    plt.show()

def bench_2(time_integrate):
    """Бенчмарк многопроцессной версии (100 000 итераций)"""

    result = integrate_multiprocess(math.sin, 0, math.pi, n_jobs=4, n_iter=100_000)
    print(f"\n∫sin(x)dx от 0 до π = {result} (ожидается 2.0)")

    # Бенчмарк
    print("\nБенчмарк многопроцессной версии (100 000 итераций):")

    times_proc = []
    n_jobs_x = [1, 2, 4, 6, 8]
    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_multiprocess(math.cos, 0, math.pi/2, n_jobs={n_jobs}, n_iter=100_000)',
            setup='import math; from __main__ import integrate_multiprocess',
            number=10
        )
        times_proc.append(time/10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    plt.bar(n_jobs_x, times_proc)

    plt.axhline(y=time_integrate, color='red', linestyle='--', label=f'{time_integrate:.4f}')

    plt.xlabel('Количество процессов')
    plt.ylabel('Время выполнения')
    plt.title('Анализ производительности')
    plt.legend()

    plt.show()

def bench_3(time_integrate, time_integrate_with_c, time_integrate_with_c_no_C_API):
    """Бенчмарк сравнения integrate | integrate с оптимизацией на C | integrate с оптимизацией на C и с оптимизацией на C-API"""
    print("\nБенчмарк сравнения integrate | integrate с оптимизацией на C | integrate с оптимизацией на C и с оптимизацией на C-API")

    print('Оптимизированная', time_integrate_with_c / 10)
    print('Без оптимизации C-API', time_integrate_with_c_no_C_API / 10)
    print('Базовая', time_integrate / 10)

    plt.bar(['Оптимизированная', 'Без оптимизации C-API', 'Базовая'],
            [time_integrate_with_c / 10, time_integrate_with_c_no_C_API / 10, time_integrate / 10])

    plt.xlabel('')
    plt.ylabel('Время выполнения')
    plt.title('Анализ производительности базовой и оптимизированной при помощи C функций')

    plt.show()

def bench_4(time_integrate):
    """Бенчмарк сравнения integrate_multiprocess | integrate_multiprocess_with_C | integrate_multiprocess_with_C_with_C_API"""
    print("\nБенчмарк сравнения integrate_multiprocess | integrate_multiprocess_with_C | integrate_multiprocess_with_C_with_C_API ")

    times_proc_with_c_with_C_API = []
    times_proc_with_c = []
    times_proc = []
    n_jobs_x = [1, 2, 4, 6, 8]
    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_multiprocess_with_C(math.cos, 0, math.pi / 2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_multiprocess_with_C',
            number=10
        )
        times_proc_with_c.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    print("-"*80)

    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_multiprocess_with_C_with_C_API(0, math.pi / 2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_multiprocess_with_C_with_C_API',
            number=10
        )
        times_proc_with_c_with_C_API.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    print("-" * 80)

    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_multiprocess(math.cos, 0, math.pi/2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_multiprocess',
            number=10
        )
        times_proc.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    x = np.arange(len(n_jobs_x))
    width = 0.25

    plt.bar(x - width, times_proc_with_c_with_C_API, width, label='оптимизированный c C-API')
    plt.bar(x, times_proc_with_c, width, label='оптимизированный без C-API')
    plt.bar(x + width, times_proc, width, label='базовый')

    plt.axhline(y=time_integrate, color='red', linestyle='--', label=f'{time_integrate:.4f}')
    plt.xlabel('Количество потоков')
    plt.ylabel('Время (с)')
    plt.title('Сравнение производительности integrate_multiprocess | integrate_multiprocess_with_C | integrate_multiprocess_with_C_with_C_API')
    plt.xticks(x, n_jobs_x)
    plt.legend()

    plt.show()

def bench_5(time_integrate):
    """Бенчмарк сравнения integrate_threaded | integrate_threaded_with_C | integrate_threaded_with_C_with_C_API"""

    print("\nБенчмарк сравнения integrate_threaded | integrate_threaded_with_C | integrate_threaded_with_C_with_C_API ")

    times_potok_with_c_with_C_API = []
    times_potok_with_c = []
    times_potok = []
    n_jobs_x = [1, 2, 4, 6, 8]
    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_threaded_with_C(math.cos, 0, math.pi / 2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_threaded_with_C',
            number=10
        )
        times_potok_with_c.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    print("-" * 80)

    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_threaded_with_C_with_C_API(0, math.pi / 2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_threaded_with_C_with_C_API',
            number=10
        )
        times_potok_with_c_with_C_API.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    print("-" * 80)

    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit(
            stmt=f'integrate_threaded(math.cos, 0, math.pi/2, n_jobs={n_jobs}, n_iter=100_000)',  # код для выполнения
            setup='import math; from __main__ import integrate_threaded',
            number=10
        )

        times_potok.append(time / 10)
        print(f"Потоков: {n_jobs}, время: {time / 10:.4f} сек")

    x = np.arange(len(n_jobs_x))
    width = 0.25

    plt.bar(x - width, times_potok_with_c_with_C_API, width, label='оптимизированный c C-API')
    plt.bar(x, times_potok_with_c, width, label='оптимизированный без C-API')
    plt.bar(x + width, times_potok, width, label='базовый')

    plt.axhline(y=time_integrate, color='red', linestyle='--', label=f'{time_integrate:.4f}')
    plt.xlabel('Количество потоков')
    plt.ylabel('Время (с)')
    plt.title('Сравнение производительности integrate_threaded | integrate_threaded_with_C | integrate_threaded_with_C_with_C_API')
    plt.xticks(x, n_jobs_x)
    plt.legend()
    plt.yscale('log')

    plt.show()

def bench_6(
       # time_integrate
):
    times_potok_with_c_with_C_API = []
    times_potok_with_c_nogil = []
    n_jobs_x = [1, 2, 4, 6]

    for n_jobs in [1, 2, 4, 6]:
        time = timeit.timeit(
            stmt=f'integrate_threaded_with_C_with_C_API(0, math.pi / 2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_threaded_with_C_with_C_API',
            number=10
        )
        times_potok_with_c_with_C_API.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    print("-" * 80)

    for n_jobs in [1, 2, 4, 6]:
        time = timeit.timeit(
            stmt=f'integrate_threaded_nogil(0, math.pi / 2, n_jobs={n_jobs}, n_iter=100_000)',
            # код для выполнения
            setup='import math; from __main__ import integrate_threaded_nogil',
            number=10
        )
        times_potok_with_c_nogil.append(time / 10)
        print(f"Процессов: {n_jobs}, время: {time / 10:.4f} сек")

    x = np.arange(len(n_jobs_x))
    width = 0.25

    plt.bar(x - width, times_potok_with_c_with_C_API, width, label='оптимизированный ')
    plt.bar(x, times_potok_with_c_nogil, width, label='оптимизированный c nogil')


    # plt.axhline(y=time_integrate, color='red', linestyle='--', label=f'{time_integrate:.4f}')
    plt.xlabel('Количество потоков')
    plt.ylabel('Время (с)')
    plt.title(
        'Сравнение производительности integrate_threaded_with_C_with_C_API и integrate_threaded_nogil')
    plt.xticks(x, n_jobs_x)
    plt.legend()

    plt.show()



# if __name__ == "__main__":
#     import doctest
#     doctest.testmod(verbose=True)

if __name__ == "__main__":

    time_integrate = timeit.timeit(
        stmt='integrate(math.cos, 0, math.pi / 2, n_iter=100_000)',  # код для выполнения
        setup='import math; from __main__ import integrate',
        number=10  # количество повторов
    )

    time_integrate_with_c = timeit.timeit(
        stmt='integrate_cos(0.0, math.pi / 2, n_iter=100_000)',  # код для выполнения
        setup='import math; from __main__ import integrate_cos',
        number=10  # количество повторов
    )

    time_integrate_with_c_no_C_API = timeit.timeit(
        stmt='integrate_generic(math.cos, 0, math.pi / 2, n_iter=100_000)',  # код для выполнения
        setup='import math; from __main__ import integrate_generic',
        number=10  # количество повторов
    )

    # bench_0()
    # bench_1(time_integrate)
    # bench_2(time_integrate)
    # bench_3(time_integrate, time_integrate_with_c, time_integrate_with_c_no_C_API)
    # bench_4(time_integrate)
    # bench_5(time_integrate)
    bench_6()