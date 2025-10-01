def go_left(num : int):
    """ функция, изменяющая число при переходе по левой ветке"""
    res=2 * (num + 1)
    return res


def go_right(num : int):
    """ функция, изменяющая число при переходе по правой ветке"""
    res=2 * (num - 1)
    return res


def gen_bin_tree(value :int, levels : int):
    """
    функция, создавающая словарь, содержащий бинарное дерево

    пример:

    >> gen_bin_tree(2, 2)

    >> {'2':[{'6':[None,None]},{'2':[None,None]}]}
    """
    if levels < 0:
        raise ValueError('Ошибка! Введен отрицательный уровень!')
    if levels == 0:
        return None

    return {f"{value}": [gen_bin_tree(go_left(value), levels - 1),gen_bin_tree(go_right(value), levels - 1)]}


def print_tree(node, level=0):
    """
    функция иллюстрирующая бинарное дерево в более удобный формат

    пример:

    >> print_tree(gen_bin_tree(2, 2))

    >> -> 2
    >>     -> 6
    >>     -> 2
    """
    if node is not None:
        for key in node.keys():
            ks = key
        print(" " * (level * 4) + f"-> {ks}")
        print_tree(node[f"{ks}"][0], level + 1)
        print_tree(node[f"{ks}"][1], level + 1)



tree = gen_bin_tree(15, 6)
print(tree)
print_tree(tree)
