import sqlite3

from models import Currency


class SubscriptionCRUD:
    """
    Класс для управления подписками пользователей на валюты в базе данных SQLite.

    Атрибуты:
        db_path (str): Путь к файлу базы данных SQLite. По умолчанию "database.db".

    Методы:
        subscribe(user_id: int, currency_id: int):
            Добавляет подписку пользователя на валюту.
        get_user_subscriptions(user_id: int):
            Возвращает список валют, на которые подписан пользователь.
        unsubscribe(user_id: int, currency_id: int):
            Удаляет подписку пользователя на валюту.
    """

    def __init__(self, db_path="database.db"):
        """
        Инициализация объекта SubscriptionCRUD.

        Параметры:
            db_path (str, optional): Путь к файлу базы данных SQLite. По умолчанию "database.db".
        """
        self.db_path = db_path

    def _connect(self):
        """
        Создает подключение к базе данных SQLite.

        Возвращает:
            sqlite3.Connection: Объект соединения с базой данных.
        """
        return sqlite3.connect(self.db_path)

    # CREATE
    def subscribe(self, user_id: int, currency_id: int):
        """
        Добавляет подписку пользователя на конкретную валюту.

        Если подписка уже существует, она не будет добавлена повторно.

        Параметры:
            user_id (int): Идентификатор пользователя.
            currency_id (int): Идентификатор валюты.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT OR IGNORE INTO subscriptions (user_id, currency_id)
            VALUES (?, ?)
        """, (user_id, currency_id))

        conn.commit()
        conn.close()

    # READ
    def get_user_subscriptions(self, user_id: int):
        """
        Получает список валют, на которые подписан пользователь.

        Параметры:
            user_id (int): Идентификатор пользователя.

        Работаем с:
            list of tuples: Список подписок пользователя. Каждый кортеж содержит:
                - id (int): Идентификатор валюты.
                - char_code (str): Символьный код валюты (например, USD, EUR).
                - name (str): Название валюты.
                - value (float): Текущая стоимость валюты.
        Возвращаем:
            list of Currency
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT currencies.id, currencies.num_code, currencies.char_code, currencies.name, currencies.value, currencies.nominal
            FROM subscriptions
            JOIN currencies ON subscriptions.currency_id = currencies.id
            WHERE subscriptions.user_id=?
        """, (user_id,))

        rows = cur.fetchall()
        conn.close()

        mas_subscriptions = []
        for row in rows:
            currency = Currency(row[0], row[1], row[2], row[3], row[4], row[5])
            mas_subscriptions.append(currency)
        return mas_subscriptions

    # DELETE
    def unsubscribe(self, user_id: int, currency_id: int):
        """
        Удаляет подписку пользователя на конкретную валюту.

        Параметры:
            user_id (int): Идентификатор пользователя.
            currency_id (int): Идентификатор валюты.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM subscriptions WHERE user_id=? AND currency_id=?", (user_id, currency_id))
        conn.commit()
        conn.close()
