В ходе лабораторной работы:
- была реализована функция gen_bin_tree() возвращающая бинарное дерево, созданое рекурсивным методом, в формате словоря

      def gen_bin_tree(value: int, levels: int):
        if levels < 0:
            raise ValueError('Ошибка! Введен отрицательный уровень!')
        if levels == 0:
            return None
  
        return {
            f"{value}": [
                gen_bin_tree(go_left(value), levels - 1),
                gen_bin_tree(go_right(value), levels - 1)
            ]
      }

  пример вызова:
  
      >> gen_bin_tree(2, 2)
      >> {'2':[{'6':[None,None]},{'2':[None,None]}]}
  
  - также вспогающие фуекции go_left() и go_right()
- затем для удобства вывода бинарного дерева была создана функция print_tree()
  
      def print_tree(node, level=0):
          if node is not None:
              for key in node.keys():
                  ks = key
              print(" " * (level * 4) + f"-> {ks}")
              print_tree(node[f"{ks}"][0], level + 1)
              print_tree(node[f"{ks}"][1], level + 1)

  пример вывода:

      >> print_tree(gen_bin_tree(2, 2))
    
      >> -> 2
      >>     -> 6
      >>     -> 2
  
  она проверяет существование node, затем опускаясь по уровням дерева выводит соответствующие key
- были написаны тесты к данным функциям
