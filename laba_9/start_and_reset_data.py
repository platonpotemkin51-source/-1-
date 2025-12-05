import sqlite3
from utils.currencies_api import get_all_currencies_data
import os

# ------------------------------
# ТЕ ДАННЫЕ, КОТОРЫЕ ТЫ УКАЗАЛ
# ------------------------------

test_user_subscriptions = [
    {'user_id': 1, 'currency_id': [0, 1, 2, 3, 4]},
    {'user_id': 2, 'currency_id': [1, 3]},
    {'user_id': 3, 'currency_id': [19, 3, 25, 44, 53]},
    {'user_id': 4, 'currency_id': [34, 28]},
    {'user_id': 5, 'currency_id': [0, 32, 15, 50]}
]

test_users = [
    {"name":"Старожилов Аркадий", "email":"star_ar@mail.com"},
    {"name":"Лукьянов Александр", "email":"lukaki@mail.com"},
    {"name":"Аветисян Владислав", "email":"avet@mail.com"},
    {"name":"Пузиков Ярослав", "email":"yarei@mail.com"},
    {"name":"Потёмкин Платон", "email":"spbsvu3skype2@mail.com"}
]

# ------------------------------
# 1. СОЗДАНИЕ ТАБЛИЦ
# ------------------------------

def create_tables(conn):
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
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER NOT NULL,
        currency_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, currency_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (currency_id) REFERENCES currencies(id)
    );
    """)

    conn.commit()
    print("✔ Таблицы созданы")


# ------------------------------
# 2. ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ
# ------------------------------

def insert_users(conn):
    cur = conn.cursor()

    for u in test_users:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (u["name"], u["email"])
        )

    conn.commit()
    print("✔ Пользователи добавлены")


# ------------------------------
# 3. ДОБАВЛЕНИЕ ВСЕХ ВАЛЮТ ИЗ API ЦБ
# ------------------------------

def insert_currencies(conn):
    currencies = get_all_currencies_data()  # ДОЛЖНО ВЕРНУТЬ список валют
    cur = conn.cursor()

    for c in currencies:
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
    print("✔ Валюты добавлены :", len(currencies))


# ------------------------------
# 4. СОЗДАНИЕ ПОДПИСОК
# ------------------------------

def insert_subscriptions(conn):
    cur = conn.cursor()

    for sub in test_user_subscriptions:
        user_id = sub["user_id"]

        for cid in sub["currency_id"]:
            try:
                cur.execute("""
                    INSERT INTO subscriptions (user_id, currency_id)
                    VALUES (?, ?)
                """, (user_id, cid))
            except sqlite3.IntegrityError:
                pass  # Игнорируем дубли


    conn.commit()
    print("✔ Подписки добавлены")


# ------------------------------
# MAIN
# ------------------------------

def main():
    if os.path.exists("database.db"):
        os.remove("database.db")
    conn = sqlite3.connect("database.db")

    create_tables(conn)
    insert_users(conn)
    insert_currencies(conn)
    insert_subscriptions(conn)

    conn.close()
    print("🎉 database.db полностью заполнена!")


if __name__ == "__main__":
    main()
