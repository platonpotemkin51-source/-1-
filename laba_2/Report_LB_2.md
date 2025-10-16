В ходе лабараторной:
- были созданы функции perebor() и bitperebor() 

  - perebor():

        def perebor(x: int, lst: list):
            k = 0
            for i in lst:
                k += 1
                if x == i:
                    return [x, k]
            return None

  эта функция перебирает поочереди все элементы массива list, пока не найдет элемент равный x

  - bitperebor():

        def bitperebor(x: int, lst: list):
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

  эта функция находит искомый элемент x в массиве list с помощью алгоритма бинарного поиска

- затем реализовалась функция vbr_lst позволяющая выбирать способ создания массива list, а также вспомогательные vbr_0 и vbr_1
- в итоге пользователю представлялась возможность выбора способа создания массива и метода поиска ("угадывания") числа
- так же были прописаны тесты к данным функциям

     
