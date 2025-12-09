import sqlite3


class DatabaseController:
    """
    Класс для управления подключением к базе данных SQLite и создания таблиц.

    Атрибуты:
        db_path (str): Путь к файлу базы данных SQLite. По умолчанию "database.db".

    Методы:
        connect() -> sqlite3.Connection:
            Возвращает соединение с базой данных.
        create_tables():
            Создает таблицы users, currencies и subscriptions, если их нет.
        insert_users(users_data):
            Добавляет тестовых пользователей в базу данных.
        insert_currencies(currencies_data):
            Добавляет валюты из API ЦБ в базу данных.
        insert_subscriptions(subscriptions_data):
            Добавляет подписки пользователей на валюты.
        insert_all_currencies(currencies_data):
            Добавляет только коды валют в таблицу all_currencies.

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

        Таблица all_currencies:
            CREATE TABLE all_currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                char_code TEXT NOT NULL UNIQUE
            );

    Примеры использования:
        >> db = DatabaseController()
        >> db.insert_users(test_users)
        >> conn = db.connect()
        >> cur = conn.cursor()
        >> cur.execute("SELECT * FROM users")
        >> users = cur.fetchall()
        >> print(users)
        [(1, "Иван Иванов", "ivan@example.com")]
    """

    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.create_tables()

    def connect(self):
        """Создает и возвращает соединение с базой данных SQLite."""
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        """Создает таблицы users, currencies, subscriptions и all_currencies, если их нет."""
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                nominal INTEGER NOT NULL
            );
            """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS currencies_const (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        num_code TEXT NOT NULL,
                        char_code TEXT NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        value REAL NOT NULL,
                        nominal INTEGER NOT NULL
                    );
                    """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, currency_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (currency_id) REFERENCES currencies(id)
            );
            """)

        # cur.execute("""
        #         CREATE TABLE IF NOT EXISTS all_currencies (
        #             id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             char_code TEXT NOT NULL UNIQUE
        #         );
        #         """)

        conn.commit()
        conn.close()
        print("✔ Таблицы созданы")

    def insert_users(self, users_data):
        """Добавляет пользователей в базу данных."""
        conn = self.connect()
        cur = conn.cursor()

        for u in users_data:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (u["name"], u["email"])
            )

        conn.commit()
        conn.close()
        print("✔ Пользователи добавлены")

    def insert_currencies_const(self, currencies_data):
        """Добавляет валюты из API ЦБ в базу данных."""
        conn = self.connect()
        cur = conn.cursor()

        for c in currencies_data:
            cur.execute("""
                            INSERT INTO currencies_const (num_code, char_code, name, value, nominal)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                c["num_code"],
                c["char_code"],
                c["name"],
                c["value"],
                c["nominal"]
            ))

        conn.commit()
        conn.close()
        print("✔ Валюты добавлены:", len(currencies_data))

    def insert_currencies(self, currencies_data):
        """Добавляет валюты из API ЦБ в базу данных."""
        conn = self.connect()
        cur = conn.cursor()

        for c in currencies_data:
            cur.execute("""
                INSERT INTO currencies (num_code, char_code, name, value, nominal)
                VALUES (?, ?, ?, ?, ?)
            """, (
                c["num_code"],
                c["char_code"],
                c["name"],
                c["value"],
                c["nominal"]
            ))

        conn.commit()
        conn.close()
        print("✔ Валюты добавлены:", len(currencies_data))

    def insert_subscriptions(self, subscriptions_data):
        """Добавляет подписки пользователей на валюты."""
        conn = self.connect()
        cur = conn.cursor()

        for sub in subscriptions_data:
            user_id = sub["user_id"]

            for cur_id in sub["currency_id"]:
                try:
                    cur.execute("""
                        INSERT INTO subscriptions (user_id, currency_id)
                        VALUES (?, ?)
                    """, (user_id, cur_id))
                except sqlite3.IntegrityError:
                    pass  # Игнорируем дубли

        conn.commit()
        conn.close()
        print("✔ Подписки добавлены")





































