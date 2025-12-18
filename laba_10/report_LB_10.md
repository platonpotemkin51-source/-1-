# Лабораторная работа 10. Методы оптимизации вычисления кода с помощью потоков, процессов, Cython, отпускания GIL

Цель работы: исследовать методы оптимизации вычисления кода, используя потоки, процессы, Cython и отключение GIL на основе сравнения времени вычисления  функции численного интегрирования методом прямоугольников, реализованной на чистом Python.


Все графики находятся в папке `pict/`
### Подготовка среды

```python
import math
from typing import Callable, Union
import concurrent.futures as ftres
from functools import partial
import timeit
import matplotlib.pyplot as plt
import numpy as np
import time
from integrate_cy import integrate_cos, integrate_x2, integrate_2x, integrate_generic, integrate_cos_nogil
```
## Итерация 1. Задания

```python
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
```

## Что сделал:
--

### Шаг 1 (Итерация 1)

- Написал полный и содержательный docstring для функции integrate(), включая описание назначения каждого аргумента и возвращаемого значения.
Формат docstring соответствует стандартам *PEP 257*.
- Использовал аннотации типов для аргументов и возвращаемых значений функции.
- Создал 3 примера для проверки правильности работы функции, размещённые непосредственно в `docstring` функции `integrate()`. Первый содержит простую тригонометрическую функцию, второй - простая линейная функция, третья - полиномиальную функцию второго порядка.

Код:
```python
'''
>>> integrate(math.cos, 0, math.pi/2, n_iter=10000)  # ∫cos(x)dx = sin(x)|_0^{π/2} = 1
1.0000785377601717

>>> integrate(lambda x: 2*x, 0, 1, n_iter=1000)      # ∫2x dx = x^2|_0^1 = 1
0.9990000000000003

>>> integrate(lambda x: x**2, 0, 2, n_iter=10000)    # ∫x^2 dx = (x^3)/3|_0^2 = 8/3 ≈ 2.6667
2.6662666799999966
'''
```

Запуск тестов:
```python
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
```

Ответ:
```cmd
Trying:
    integrate(math.cos, 0, math.pi/2, n_iter=10000)  # ∫cos(x)dx = sin(x)|_0^{π/2} = 1
Expecting:
    1.0000785377601717
ok
Trying:
    integrate(lambda x: 2*x, 0, 1, n_iter=1000)      # ∫2x dx = x^2|_0^1 = 1
Expecting:
    0.9990000000000003
ok
Trying:
    integrate(lambda x: x**2, 0, 2, n_iter=10000)    # ∫x^2 dx = (x^3)/3|_0^2 = 8/3 ≈ 2.6667
Expecting:
    2.6662666799999966
ok
15 items had no tests:
    __main__
    __main__.bench_0
    __main__.bench_1
    __main__.bench_2
    __main__.bench_3
    __main__.bench_4
    __main__.bench_5
    __main__.bench_6
    __main__.integrate_multiprocess
    __main__.integrate_multiprocess_with_C
    __main__.integrate_multiprocess_with_C_with_C_API
    __main__.integrate_threaded
    __main__.integrate_threaded_nogil
    __main__.integrate_threaded_with_C
    __main__.integrate_threaded_with_C_with_C_API
1 item passed all tests:
   3 tests in __main__.integrate
3 tests in 16 items.
3 passed.
Test passed.
```
- Разработал дополнительные юнит-тесты с помощью ``pytest```, покрывающие 3 ситуации: правильный расчёт известного интеграла (тригонометрическая и полином) и проверку устойчивости к изменению числа итераций.
```python
def test_cos_integral():
    """Проверка интеграла cos(x) на [0, π/2]"""
    result = integrate(math.cos, 0, math.pi/2, n_iter=100000)
    assert abs(result - 1.0) < 1e-4

def test_polynomial():
    """Проверка интеграла полинома x^2 на [0, 2]"""
    result = integrate(lambda x: x**2, 0, 2, n_iter=100000)
    expected = 8/3  # ≈ 2.6666667
    assert abs(result - expected) < 1e-4

def test_iterations_independence():
    """Результат не должен меняться кардинально при увеличении итераций"""
    res1 = integrate(math.sin, 0, math.pi, n_iter=1000)
    res2 = integrate(math.sin, 0, math.pi, n_iter=10000)
    assert abs(res1 - res2) < 0.01  # Разница менее 1%

def test_invalid_args():
    """Проверка обработки некорректных аргументов"""
    with pytest.raises(ValueError):
        integrate(math.cos, 5, 0, n_iter=1000)  # a > b
    with pytest.raises(ValueError):
        integrate(math.cos, 0, 1, n_iter=0)     # n_iter <= 0
```
```cmd
Testing started at 19:00 ...
Launching pytest with arguments C:\Users\pc\Desktop\итмо\laba_10\tests\test_integrate.py --no-header --no-summary -q in C:\Users\pc\Desktop\итмо\laba_10\tests

============================= test session starts =============================
collecting ... collected 4 items

test_integrate.py::test_cos_integral PASSED                              [ 25%]
test_integrate.py::test_polynomial PASSED                                [ 50%]
test_integrate.py::test_iterations_independence PASSED                   [ 75%]
test_integrate.py::test_invalid_args PASSED                              [100%]

============================== 4 passed in 0.60s ==============================
```
- Провёл оценку производительности функции с помощью модуля ```timeit```, выполнив серию замеров времени выполнения функции для различного числа итераций.
Зафиксировал полученные временные характеристики.

Код:
```python
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
```
Ответ:
```
Бенчмарк базовой реализации:
--------------------------------------------------
100 итераций         | 0.000115 сек (10 прогонов) | 0.000012 сек/вызов
1 000 итераций       | 0.001112 сек (10 прогонов) | 0.000111 сек/вызов
10 000 итераций      | 0.011094 сек (10 прогонов) | 0.001109 сек/вызов
100 000 итераций     | 0.118765 сек (10 прогонов) | 0.011877 сек/вызов
```

График: Figure_1

---
### Шаг 2 (итерация 2)

Реализованна функция `integrate_threaded`, которая вычисляет интеграл с использованием потоков (ThreadPoolExecutor)

- Аннотировал аргументы
```python
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
```

Cоздаваемый пул тредов будет размера n_jobs
```python
executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
```

partial позволяет "закрепить" несколько аргументов для удобства вызова функции 

```python
spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs)
```

Cоздал потоки с помощью генератораписков (partial позволил)

```python
fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
```

as.completed() берет на вход список фьючерсов и как только какой-то завершился, возвращает результат f.result(), далее, мы эти результаты складываем
```python
return sum(list(f.result() for f in ftres.as_completed(fs)))
```

Зависимость времени выполнения от количества потоков:

Код:

```python
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
```

Ответ:
```cmd
Бенчмарк многопоточности версии (100 000 итераций):
Потоков: 1, время: 0.0110 сек
Потоков: 2, время: 0.0106 сек
Потоков: 4, время: 0.0115 сек
Потоков: 6, время: 0.0111 сек
Потоков: 8, время: 0.0106 сек
```

График: Figure_2

---
### Шаг 3 (итерация 3)

Реализованна функция `integrate_multiprocess`, которая вычисляет интеграл с использованием процессов (ProcessPoolExecutor)

- Аннотировал аргументы
```python
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
```
Реализована практически идентично integrate_threaded только вместо потоков (реализованных при помощи `ThreadPoolExecutor`)
процессы (реализованные при помощи ProcessPoolExecutor)

Зависимость времени выполнения от количества процессов:

Код:
```python
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
```

Ответ:
```cmd
Бенчмарк многопроцессной версии (100 000 итераций):
Процессов: 1, время: 0.7210 сек
Процессов: 2, время: 0.8385 сек
Процессов: 4, время: 1.1296 сек
Процессов: 6, время: 1.6947 сек
Процессов: 8, время: 1.9086 сек
```

График: Figure_3

---
## Шаг 4.1 (итерация 4)

- Оптимизировал функцию integrate с помощью Cython 
в файле `integrate_cy.pyx` записываем данный код (буквально переписываем код с чистого Python на Cython более быстрый и "читаемый" для C)
```
import cython
from libc.math cimport sin, cos, exp, log, sqrt

# Тип указателя на C-функцию: double -> double
ctypedef double (*func_ptr)(double)

@cython.cdivision(True)
cdef double _integrate_c(func_ptr f, double a, double b, int n_iter) noexcept:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
    return acc
```
Чтобы максимально оптимировать код для уменьшения взаимодействия с C-API нам необходимо обращатся к
C-функциям `from libc.math cimport sin, cos, exp, log, sqrt`

Примеры:
```
def integrate_sin(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(sin, a, b, n_iter)

def integrate_cos(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(cos, a, b, n_iter)
```

Также в них мы уже можем указывать контроль ошибок т.к. нет noexcept который запрешал это делать 

Но оставим функцию принимающую любые функции (чтобы их в дальнейшем сравнить)
```
def integrate_generic(object f, double a, double b, int n_iter=100_000):
    """Используется ТОЛЬКО если f — произвольная Python-функция."""
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    cdef object local_f = f
    for i in range(n_iter):
        x = a + i * step
        acc += local_f(x) * step
    return acc
```
## Шаг 4.2 (Сравнение время выполнения функции без потоков и процессов (сравнить с итерацией 1))

Код:
```python
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
```

```python

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
```

Ответ:
```cmd
Бенчмарк сравнения integrate | integrate с оптимизацией на C | integrate с оптимизацией на C и с оптимизацией на C-API
Оптимизированная 0.0011332200025208294
Без оптимизации C-API 0.010414800001308322
Базовая 0.01114536999957636
```

График: Figure_4

## Шаг 4.3 (Сравнение время выполнения функций базовой реализации и с оптимизацией)

В новых функциях меняется только `spawn`
`integrate_multiprocess_with_C` 
```python
spawn = partial(executor.submit, integrate_generic, f, n_iter=n_iter // n_jobs)
```

`integrate_multiprocess_with_C_with_C_API`
```python
spawn = partial(executor.submit, integrate_cos, n_iter=n_iter // n_jobs)
```

Код:
```python
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
```
Ответ:
```cmd
Бенчмарк сравнения integrate_multiprocess | integrate_multiprocess_with_C | integrate_multiprocess_with_C_with_C_API 
Процессов: 1, время: 0.7865 сек
Процессов: 2, время: 0.8476 сек
Процессов: 4, время: 1.0994 сек
Процессов: 6, время: 1.7008 сек
Процессов: 8, время: 1.9473 сек
--------------------------------------------------------------------------------
Процессов: 1, время: 0.7486 сек
Процессов: 2, время: 0.8708 сек
Процессов: 4, время: 1.2694 сек
Процессов: 6, время: 1.8493 сек
Процессов: 8, время: 2.3819 сек
--------------------------------------------------------------------------------
Процессов: 1, время: 0.7462 сек
Процессов: 2, время: 0.8577 сек
Процессов: 4, время: 1.1405 сек
Процессов: 6, время: 1.8089 сек
Процессов: 8, время: 2.9319 сек
```
1. `integrate_multiprocess_with_C_with_C_API`
2. `integrate_multiprocess_with_C`
3. `integrate_multiprocess`

График: Figure_5

---

## Шаг 4.3 (Сравнение время выполнения функций базовой реализации и с оптимизацией)

Аналогично процессам также в функциях меняется только `spawn`

Код:
```python
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
```

Ответ:
```cmd
Бенчмарк сравнения integrate_threaded | integrate_threaded_with_C | integrate_threaded_with_C_with_C_API 
Процессов: 1, время: 0.0127 сек
Процессов: 2, время: 0.0107 сек
Процессов: 4, время: 0.0123 сек
Процессов: 6, время: 0.0128 сек
Процессов: 8, время: 0.0116 сек
--------------------------------------------------------------------------------
Процессов: 1, время: 0.0014 сек
Процессов: 2, время: 0.0015 сек
Процессов: 4, время: 0.0017 сек
Процессов: 6, время: 0.0019 сек
Процессов: 8, время: 0.0019 сек
--------------------------------------------------------------------------------
Потоков: 1, время: 0.0120 сек
Потоков: 2, время: 0.0107 сек
Потоков: 4, время: 0.0114 сек
Потоков: 6, время: 0.0113 сек
Потоков: 8, время: 0.0117 сек
```

1. `integrate_threaded_with_C_with_C_API`
2. `integrate_threaded_with_C`
3. `integrate_threaded`


График: Figure_6

---

## Шаг 5 (Итерация 5)

Для отключения GIL необходимо при напиcании функции на Cython добавить `nogil`
```
@cython.cdivision(True)
cpdef double integrate_c_cos_nogil(double a, double b, int n_iter=100_000) nogil:
    """
    Интегрирует cos(x) на [a, b] без удержания GIL.
    Полностью безопасен для многопоточности.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += cos(x) * step

    return acc
```

Для оптимизации с C-API также пропишем:

```
def integrate_cos_nogil(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return integrate_c_cos_nogil(a, b, n_iter)
```

Потом сравним время выполнение максимально оптимизированной функции с потоками `integrate_threaded_with_C_with_C_API` и и функцию с теми же оптимизациями,
но ещё применив noGIL `integrate_threaded_nogil`(который отпускает GIL и позволяет реализовать многопоточность не имитируя)

`integrate_threaded_nogil` также отличается только `spawn`
```python
spawn = partial(executor.submit, integrate_cos_nogil, n_iter=n_iter // n_jobs)
```

Код:
```python
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
```

Ответ:
```cmd
Процессов: 1, время: 0.0022 сек
Процессов: 2, время: 0.0019 сек
Процессов: 4, время: 0.0024 сек
Процессов: 6, время: 0.0027 сек
--------------------------------------------------------------------------------
Процессов: 1, время: 0.0015 сек
Процессов: 2, время: 0.0017 сек
Процессов: 4, время: 0.0023 сек
Процессов: 6, время: 0.0023 сек
```
1. `integrate_threaded_with_C_with_C_API`
2. `integrate_threaded_nogil`

График: Figure_7