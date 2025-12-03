import requests
import sys
import math
import logging
import json


def get_currencies(currency_codes: list,
                   url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
                   handle=sys.stdout,
                   test_response: dict = None) -> dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    # Если переданы тестовые данные, используем их
    if test_response is not None:
        data = test_response
    else:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status(
            )  # Выбрасывает HTTPError при статусе != 200
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            raise ConnectionError(f"API недоступно: {str(e)}")

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в ответе: {str(e)}")
        # print(data)

    if "Valute" not in data:
        raise KeyError("Ключ 'Valute' отсутствует в ответе API")

    currencies = {}

    for code in currency_codes:
        code = code.upper()
        if code in data["Valute"]:
            currencies[code] = data["Valute"][code]["Value"]
        else:
            #currencies[code] = f"Код валюты '{code}' не найден."
            raise KeyError(f"Валюта '{code}' отсутствует в данных ЦБ")

        try:
            nomb = float(currencies[code])
        except:
            raise TypeError(
                f"Курс валюты '{code}' имеет неверный тип: {type(currencies[code])}"
            )

    return currencies


def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax² + bx + c = 0

    Args:
        a, b, c: Коэффициенты уравнения

    Returns:
        Список корней уравнения

    Raises:
        TypeError: Если коэффициенты не числа
        ValueError: Если дискриминант отрицательный или a=b=0
    """
    # Проверка типов
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            #logging.error(f"Parameter '{name}' must be a number, got: {value}")
            raise TypeError(f"Коэффициент '{name}' должен быть числом")

    # Проверка на вырожденный случай
    if a == 0 and b == 0:
        #logging.critical("Оба коэффициента a и b равны нулю - уравнение вырождено")
        raise ValueError(
            "Оба коэффициента a и b равны нулю - уравнение вырождено")

    # Линейное уравнение
    if a == 0:
        return [-c / b]

    # Квадратное уравнение
    D = b**2 - 4 * a * c
    logging.debug(f"Discriminant: {D}")

    if D < 0:
        #logging.warning("Discriminant < 0: no real roots")
        raise ValueError(f"Дискриминант отрицательный: D={D}")

    sqrt_D = math.sqrt(D)
    x1 = (-b + sqrt_D) / (2 * a)
    x2 = (-b - sqrt_D) / (2 * a)

    # Округляем для красивого вывода
    return [round(x1, 4), round(x2, 4)]
