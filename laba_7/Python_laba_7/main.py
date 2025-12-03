import logging
import sys
import io
from logger import logger
from func import get_currencies, solve_quadratic

currency_list = ['USD', 'EUR', 'GBP', 'DFG']

# # Вариант 1: Обычный поток вывода (по умолчанию)
# @logger
# def get_currencies_default(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
#     return get_currencies(currency_codes, url)
#
# # Вариант 2: С явным указанием handle
# @logger(handle=sys.stdout)
# def get_currencies_stdout(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
#     return get_currencies(currency_codes, url)
#


# Настройка файлового логгера
def setup_file_logger():
    # Создаем логгер
    file_logger = logging.getLogger("currency_file")
    file_logger.setLevel(logging.INFO)

    # Удаляем существующие обработчики (чтобы не дублировать логи)
    if file_logger.handlers:
        file_logger.handlers.clear()

    # Создаем обработчик для файла
    file_handler = logging.FileHandler('currency.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Создаем обработчик для консоли (опционально)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Форматирование
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    file_logger.addHandler(file_handler)
    file_logger.addHandler(console_handler)  # Также выводим в консоль

    return file_logger


# Создаем и настраиваем логгер
file_logger = setup_file_logger()


@logger(handle=file_logger)
def solve_quadratic_log(a, b, c):
    return solve_quadratic(a, b, c)


#solve_quadratic_log(0, 0, 1)


# Обертываем функцию с файловым логированием
@logger(handle=file_logger)
def get_currencies_file_log(currency_codes,
                            url="https://www.cbr-xml-daily.ru/daily_json.js"):
    return get_currencies(currency_codes, url)


#
# currency_data = get_currencies_file_log(currency_list, 'https://www.google.com')
#
# if currency_data:
#     print(currency_data)
# # Демонстрация работы

