from models.currency import Currency
import sqlite3
from utils.currencies_api import get_all_currencies_data


class CurrencyRatesCRUD:
    """
    Класс для управления курсами валют в базе данных SQLite.

    Атрибуты:
        db_path (str): Путь к файлу базы данных SQLite. По умолчанию "database.db".

    Методы:
        create(currency: Currency):
            Добавляет новую валюту в таблицу currencies.
        _read() -> list[tuple]:
            Возвращает все записи из таблицы currencies.
            Но преобразованный в список объектов Currency
        find_by_char_code(char_code: str) -> Currency | None:
            Находит валюту по ее буквенного коду (char_code).
        _update(updates: dict):
            Обновляет значения валют по словарю {"USD": 92.5, ...}.
        update_from_api() -> bool:
            Получает данные с API и обновляет или добавляет валюты в базе.
        _delete(currency_id: int):
            Удаляет валюту по её id.

    Формат таблицы currencies в SQLite:
        CREATE TABLE currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT NOT NULL,
            char_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            value REAL NOT NULL,
            nominal INTEGER NOT NULL
        );

    Формат объектов Currency:
        Currency(
            num_code: str,      # числовой код валюты
            char_code: str,     # буквенный код валюты
            name: str,          # название валюты
            value: float,       # текущий курс валюты
            nominal: int        # номинал валюты (обычно 1, 10, 100)
        )

    Примеры использования:
        >> crud = CurrencyRatesCRUD()
        >> usd = Currency("840", "USD", "US Dollar", 92.5, 1)
        >> crud.create(usd)  # добавление новой валюты

        >> all_currencies = crud._read()
        >> print(all_currencies)
        [(1, "840", "USD", "US Dollar", 92.5, 1), (2, "978", "EUR", "Euro", 101.2, 1)]

        >> currency = crud.find_by_char_code("USD")
        >> print(currency.name, currency.value)
        US Dollar 92.5

        >> crud._update({"USD": 93.0, "EUR": 102.0})
        >> success = crud.update_from_api()  # обновление всех валют из API
        >> print(success)
        True

        >> crud._delete(1)  # удаление валюты с id=1
    """

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # CREATE
    def create(self, currency: Currency):
        """Добавляет новую валюту в базу данных."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO currencies (num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?)
        """, (currency.num_code, currency.char_code, currency.name, currency.value, currency.nominal))

        conn.commit()
        conn.close()

    # READ all
    def _read(self):
        """Возвращает список всех валют из базы в виде кортежей."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, num_code, char_code, name, value, nominal FROM currencies")
        rows = cur.fetchall()
        conn.close()

        mas_currency = []
        for row in rows:
            currency = Currency(row[0], row[1], row[2], row[3], row[4], row[5])
            mas_currency.append(currency)
        return mas_currency

    # FIND by char code
    def find_by_char_code(self, char_code: str):
        """
        Ищет валюту по буквенно-цифровому коду.

        Возвращает объект Currency, если найден, иначе None.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, num_code, char_code, name, value, nominal 
            FROM currencies_const WHERE char_code=?
        """, (char_code.upper(),))

        row = cur.fetchone()
        conn.close()

        if row:
            return Currency(*row)
        return None

    # UPDATE
    def _update(self, updates: dict):
        """
        Обновляет значение валют по словарю {"USD": 92.5, "EUR": 101.2, ...}.
        """
        conn = self._connect()
        cur = conn.cursor()

        for char_code, value in updates.items():
            cur.execute("UPDATE currencies SET value=? WHERE char_code=?", (value, char_code.upper()))

        conn.commit()
        conn.close()

    def update_from_api(self):
        """
        Получает все валюты через API и обновляет их значения в базе данных.
        Если валюты нет в базе — добавляет новую запись.

        Возвращает:
            True, если обновление прошло успешно, иначе False.
        """
        try:
            currencies_data = get_all_currencies_data()  # Список словарей с валютами

            conn = self._connect()
            cur = conn.cursor()

            for data in currencies_data:
                char_code = data['char_code'].upper()
                num_code = data['num_code']
                name = data['name']
                value = data['value']
                nominal = data['nominal']

                # Проверяем, есть ли валюта в базе
                cur.execute("SELECT id FROM currencies WHERE char_code=?", (char_code,))
                row = cur.fetchone()

                if row:
                    # обновляем
                    cur.execute("""
                        UPDATE currencies
                        SET num_code=?, name=?, value=?, nominal=?
                        WHERE char_code=?
                    """, (num_code, name, value, nominal, char_code))
                else:
                    # создаем новую валюту
                    cur.execute("""
                        INSERT INTO currencies (num_code, char_code, name, value, nominal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (num_code, char_code, name, value, nominal))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении валют из API: {e}")
            return False

    # DELETE
    def _delete(self, currency_id: int):
        """Удаляет валюту из базы по её id."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM currencies WHERE id=?", (currency_id,))
        conn.commit()
        conn.close()
