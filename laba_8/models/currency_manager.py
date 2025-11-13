import requests
import sys
import io


def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
                   handle=sys.stdout) -> dict:
    """
    Получает курсы валют с API Центробанка России.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]["Value"]
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException('Упали с исключением')


class CurrencyManager:
    __available_currencies = {
        'USD': {'name': 'Доллар США', 'symbol': '$'},
        'EUR': {'name': 'Евро', 'symbol': '€'},
        'GBP': {'name': 'Фунт стерлингов', 'symbol': '£'},
        'JPY': {'name': 'Японская иена', 'symbol': '¥'},
        'CNY': {'name': 'Китайский юань', 'symbol': '¥'},
        'CHF': {'name': 'Швейцарский франк', 'symbol': 'Fr'},
        'CAD': {'name': 'Канадский доллар', 'symbol': 'C$'},
        'AUD': {'name': 'Австралийский доллар', 'symbol': 'A$'},
        'TRY': {'name': 'Турецкая лира', 'symbol': '₺'},
        'KZT': {'name': 'Казахстанский тенге', 'symbol': '₸'}
    }

    __user_subscriptions = {}

    @classmethod
    def get_all_currencies(cls, url: str = "https://www.cbr-xml-daily.ru/daily_json.js"):
        """Получает актуальные курсы всех доступных валют"""
        currency_codes = list(cls.__available_currencies.keys())

        try:
            rates = get_currencies(currency_codes, url)

            currencies_data = {}
            for code in currency_codes:
                if code in rates and isinstance(rates[code], (int, float)):
                    currencies_data[code] = {
                        'name': cls.__available_currencies[code]['name'],
                        'symbol': cls.__available_currencies[code]['symbol'],
                        'rate': rates[code],
                        'code': code
                    }
                else:
                    currencies_data[code] = {
                        'name': cls.__available_currencies[code]['name'],
                        'symbol': cls.__available_currencies[code]['symbol'],
                        'rate': 0.0,
                        'code': code,
                        'error': 'Курс недоступен'
                    }

            return currencies_data

        except Exception as e:
            print(f"Ошибка при получении курсов валют: {e}")
            return {
                code: {
                    'name': info['name'],
                    'symbol': info['symbol'],
                    'rate': 0.0,
                    'code': code,
                    'error': 'Сервис временно недоступен'
                }
                for code, info in cls.__available_currencies.items()
            }

    @classmethod
    def get_subscribed_currencies(cls, user_id: int, url: str = "https://www.cbr-xml-daily.ru/daily_json.js"):
        """Получает курсы валют, на которые подписан пользователь"""
        if user_id not in cls.__user_subscriptions:
            return {}

        subscribed_codes = cls.__user_subscriptions[user_id]
        all_currencies = cls.get_all_currencies(url)

        return {code: all_currencies[code] for code in subscribed_codes if code in all_currencies}

    @classmethod
    def subscribe_currency(cls, user_id: int, currency_code: str) -> bool:
        """Добавляет валюту в подписки пользователя"""
        if currency_code not in cls.__available_currencies:
            return False

        if user_id not in cls.__user_subscriptions:
            cls.__user_subscriptions[user_id] = []

        if currency_code not in cls.__user_subscriptions[user_id]:
            cls.__user_subscriptions[user_id].append(currency_code)

        return True

    @classmethod
    def unsubscribe_currency(cls, user_id: int, currency_code: str) -> bool:
        """Удаляет валюту из подписок пользователя"""
        if user_id in cls.__user_subscriptions and currency_code in cls.__user_subscriptions[user_id]:
            cls.__user_subscriptions[user_id].remove(currency_code)
            return True
        return False

    @classmethod
    def get_user_subscriptions(cls, user_id: int) -> list:
        """Возвращает список подписок пользователя"""
        return cls.__user_subscriptions.get(user_id, [])

    @classmethod
    def is_subscribed(cls, user_id: int, currency_code: str) -> bool:
        """Проверяет, подписан ли пользователь на валюту"""
        return user_id in cls.__user_subscriptions and currency_code in cls.__user_subscriptions[user_id]

    @classmethod
    def get_available_currency_list(cls):
        """Возвращает список всех доступных валют"""
        return [
            {
                'code': code,
                'name': info['name'],
                'symbol': info['symbol']
            }
            for code, info in cls.__available_currencies.items()
        ]