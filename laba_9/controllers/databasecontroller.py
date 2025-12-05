import sqlite3

class DatabaseController:
    """
    Класс для управления подключением к базе данных SQLite и создания таблиц.

    Атрибуты:
        db_path (str): Путь к файлу базы данных SQLite. По умолчанию "database.db".

    Методы:
        _connect() -> sqlite3.Connection:
            Возвращает соединение с базой данных.
        _create_tables():
            Создает таблицы users, currencies и subscriptions, если их нет.

    Формат таблиц в базе данных:

        Таблица users:
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        Пример строки:
            (1, "Иван Иванов", "ivan@example.com")

        Таблица currencies:
            CREATE TABLE currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                nominal INTEGER NOT NULL
            );
        Пример строки:
            (1, "840", "USD", "US Dollar", 92.5, 1)

        Таблица subscriptions:
            CREATE TABLE subscriptions (
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, currency_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (currency_id) REFERENCES currencies(id)
            );
        Пример строки:
            (1, 1)  # Пользователь с id=1 подписан на валюту с id=1

    Примеры использования:
        >> db = DatabaseController()
        >> conn = db._connect()
        >> cur = conn.cursor()
        >> cur.execute("SELECT * FROM users")
        >> users = cur.fetchall()
        >> print(users)
        [(1, "Иван Иванов", "ivan@example.com")]
    """

    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        """Создает и возвращает соединение с базой данных SQLite."""
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """Создает таблицы users, currencies и subscriptions, если их нет."""
        conn = self._connect()
        cur = conn.cursor()

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT NOT NULL,
            char_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            value REAL NOT NULL,
            nominal INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER NOT NULL,
            currency_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, currency_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (currency_id) REFERENCES currencies(id)
        );
        """)

        conn.commit()
        conn.close()
