from func import get_currencies,solve_quadratic

def demonstrate_quadratic():
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КВАДРАТНОГО УРАВНЕНИЯ")
    print("=" * 50)

    # 1. INFO: Успешное решение
    print("\n1. Успешное решение (два корня):")
    print("solve_quadratic(1, -3, 2) →")
    try:
        result = solve_quadratic(1, -3, 2)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # 2. WARNING: Отрицательный дискриминант
    print("\n2. Отрицательный дискриминант (WARNING):")
    print("solve_quadratic(1, 0, 1) →")
    try:
        result = solve_quadratic(1, 0, 1)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # 3. ERROR: Некорректные данные
    print("\n3. Некорректные данные (ERROR):")
    print('solve_quadratic("abc", 1, 2) →')
    try:
        result = solve_quadratic("abc", 1, 2)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # 4. CRITICAL: Полностью невозможная ситуация
    print("\n4. Невозможная ситуация (CRITICAL):")
    print("solve_quadratic(0, 0, 5) →")
    try:
        result = solve_quadratic(0, 0, 5)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

demonstrate_quadratic()