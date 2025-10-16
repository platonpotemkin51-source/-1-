В ходе лабораторной работы:
- была реализована функция gen_bin_tree_mas() возвращающая массив, который содержит информацию о узлах бинарного дерева
(от первого уровня до самого последнего, слева направо внутри уровня ); также функции переходов к следующим узлам (влево и вправо)
передаются в gen_bin_tree_mas() через анонимную функцию lambda

      def gen_bin_tree_mas(start: int,
                           lvl: int,
                           go_left=lambda n: 2 * (n + 1),
                           go_right=lambda n: 2 * (n - 1)):
          tree = [start]
          if lvl < 0:
              raise ValueError('Ошибка! Введен отрицательный уровень!')
          for i in range(lvl - 1):
              for j in range((2**i) - 1, len(tree)):
                  tree.append(go_left(tree[j]))
                  tree.append(go_right(tree[j]))
          return tree

  пример вывода:
  
      >>> gen_bin_tree_mas(4, 3)
      >>> [4, 10, 6, 22, 18, 14, 10]
  
- была создана функция sp_tree() для преобразования массива (который вовращает функции gen_bin_tree_mas())

      def sp_tree(a):
          lvl = int(log2(len(a) + 1))
          if log2(len(a) + 1) % 1 != 0:
              raise ValueError('Ошибка!')
          m = [[] for i in range(2**lvl)]
          for i in range(lvl - 1):
              lvl -= 1
              l = m
              m = []
              k = 0
              for x in a[len(a) - (2**lvl):]:
                  m.append({f'{x}': l[k]})
                  k += 1
              for j in range(len(m)):
                  a.pop(-1)
              if len(m) > 2:
                  m = [[m[i], m[i + 1]] for i in range(0, len(m) - 1, 2)]

          return {f'{a[0]}': m}

  - сначала функция определяет высоту дерева

        lvl = int(log2(len(a) + 1))

  - затем создается нулевой массив

        m = [[] for i in range(2**lvl)]

  - затем начинается цикл for, в котором постепено в словарь вписываются по целому уравню дерева, после чего
     они группируются по два элемента (что необходимо для дальнейшего штатного формирования словаря) до втого уровня;
     последним шагом стартовый элемент ставим "во главу" словаря 

        for i in range(lvl - 1):
            lvl -= 1
            l = m
            m = []
            k = 0
            for x in a[len(a) - (2**lvl):]:
                m.append({f'{x}': l[k]})
                k += 1
            for j in range(len(m)):
                a.pop(-1)
            if len(m) > 2:
                m = [[m[i], m[i + 1]] for i in range(0, len(m) - 1, 2)]
    
        return {f'{a[0]}': m}

пример вывода:

        >>> tree = [4, 10, 6, 22, 18, 14, 10]
        >>> sp_tree(tree)
        >>> {'4': [{'10': [{'22': []}, {'18': []}]}, {'6': [{'14': []}, {'10': []}]}]}

- также были написаны тесты к данным фуекциям 

