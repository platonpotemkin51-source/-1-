def perebor(x: int, lst: list):
    k = 0
    for i in lst:
        k += 1
        if x == i:
            break
    return [x, k]
def bitperebor(x: int, lst: list):
    k=0
    while len(lst) > 1:
        n = len(lst) // 2
        k+=1
        if x > n:
            lst = lst[n:]
        else:
            lst = lst[:n]
    return [x,k]
def main():
    print("Введите угадываемое число")
    x = int(input())

    print("Введите нижнию границу интервала")
    a = int(input())
    print("Введите верхнию границу интервала")
    b = int(input())
    lst = range(a, b + 1)

    print("Введите 0 либо 1")
    print("0 - чтобы угадать с помощью алгоритма медленного перебора (инкремента)")
    print("1 - чтобы угадать с помощью алгоритма бинарного поиска")
    sposob = int(input())

    mas=[]

    if sposob == 0:
        mas=perebor(x, lst)
    else:
        mas=bitperebor(x, lst)
    print("Угадываемое число:", mas[0],"Число угадываний", mas[1])

main()
