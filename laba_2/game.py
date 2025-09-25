import random


def perebor(x: int, lst: list):
    '''функция воспроизодящая алгоритм медленого перебора:

    >>> perebor(4, [1, 2, 3, 4])
    >>> [4, 4]
      1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4
      ^ (!= 4)        ^ (!= 4)        ^ (!= 4)        ^ (== 4)

    >>> perebor(4, [1, 2, 3])
    >>> None
    ==> 1, 2, 3 | 1, 2, 3 | 1, 2, 3
        ^ (!= 4)     ^ (!= 4)     ^ (!= 4)
    '''
    k = 0
    for i in lst:
        k += 1
        if x == i:
            return [x, k]
    return None


def bitperebor(x: int, lst: list):
    """функция воспроизодящая алгоритм бинарного перебора

    >>> bitperebor(4, [1, 2, 3, 4])
    >>> [4, 2]
     [1, 2, 3, 4]  =>  [3, 4]  =>  [4]
               (4 > 2)      (4 > 3)


    >>> bitperebor(4, [1, 2, 3,5])
    >>> None
       [1, 2, 3, 5]  =>  [3, 5]  =>  [5]
                  (5 > 2)     (5 > 3)
    """
    k = 0
    while len(lst) > 1:
        n = len(lst) // 2
        k += 1
        if x in lst[n:]:
            lst = lst[n:]
        else:
            lst = lst[:n]
    if lst != [x]:
        return None
    else:
        return [x, k]


def vbr_0(a: int, b: int):
    """ функция создает массив из подряд идущих чисел от a до b
    >>> vbr_0(1, 5)
    >>> [1, 2, 3, 4, 5]"""
    if a > b:
        raise ValueError('Ошибка! Введите корректные границы!')
    lst = []
    for i in range(a, b + 1):
        lst.append(i)
    return lst


def vbr_1(a: int, b: int, c):
    """ функция создает массив из c рандомных чисел между a и b
        >> vbr_1(1, 7, 4)
        >> [1, 3, 4, 7]"""
    if a > b:
        raise ValueError('Ошибка! Введите корректные границы!')
    if c < 1:
        raise ValueError('Ошибка! Введите корректные кол-во элементов!')
    lst = []
    for i in range(c):
        lst.append(random.randint(a, b))
    return lst


def vbr_lst(vbr):
    """ функция позволяет выбрать способ созадния массива"""
    if vbr not in [0, 1, 2]:
        raise ValueError('Ошибка! Выберете предложенные варианты!')
    if vbr == 0:
        a = int(input("Введите нижнию границу массива: "))
        b = int(input("Введите верхнию границу массива: "))
        return vbr_0(a, b)
    elif vbr == 1:
        a = int(input("Введите нижнию границу рандомных чисел: "))
        b = int(input("Введите верхнию границу рандомных чисел: "))
        c = int(input("Введите кол-во элементов в массиве: "))
        return vbr_1(a, b, c)
    else:
        lst = list(
            map(int,
                input("Введите элементы вашего массива ЧЕРЕЗ ПРОБЕЛ").split()))
        return lst


def main():
    """основная функция угадывания числа """
    x = int(input("Введите угадываемое число: "))

    print("Выбирете массив, в котором программа будет угадывать число")
    print("Напишите 0 - создать массив из порядковых чисел")
    print("         1 - создать массив рандомных чисел ")
    print("         2 - предложить свой массив ")
    vbr = int(input("-------> "))

    lst = vbr_lst(vbr)
    lst.sort()

    print(
        "Напишите 0 - чтобы угадать с помощью алгоритма медленного перебора (инкремента)"
    )
    print("         1 - чтобы угадать с помощью алгоритма бинарного поиска")
    sposob = int(input("-------> "))

    if sposob == 0:
        mas = perebor(x, lst)
    else:
        mas = bitperebor(x, lst)

    if type(mas) == list:
        print("Угадываемое число:", mas[0], "Число угадываний", mas[1])
    else:
        print(mas, "Загаданное число в указанном промежутке отсутствует!")
        nn = int(
            input(
                "Вывести загаданное число и массив? (1 - да; 0 - нет) ---> "))
        if nn == 1:
            print("Число: ", x, "   Массив: ", lst)
        else:
            print("Хорошо")

    return mas


main()
