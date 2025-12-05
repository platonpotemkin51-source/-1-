from models.user import User
import sqlite3


class UserCRUD:
    """
    CRUD-класс для управления пользователями в базе данных SQLite.

    Атрибуты:
        db_path (str): Путь к файлу базы данных SQLite. По умолчанию "database.db".

    Методы:
        create(name: str, email: str) -> User:
            Создает нового пользователя и возвращает объект User.

        read_all() -> list[User]:
            Возвращает список всех пользователей в базе.

        read_by_id(user_id: int) -> User | None:
            Возвращает пользователя по ID или None, если не найден.

        find_by_email(email: str) -> User | None:
            Возвращает пользователя по email или None, если не найден.

        update(user_id: int, name: str = None, email: str = None):
            Обновляет имя и/или email пользователя по ID.

        delete(user_id: int):
            Удаляет пользователя по ID.

    Формат таблицы users:

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );

    Примеры использования:
        >> user_crud = UserCRUD()

        # Создание пользователя
        >> user = user_crud.create("Иван Иванов", "ivan@example.com")
        >> print(user.id, user.name, user.email)
        1 Иван Иванов ivan@example.com

        # Получение всех пользователей
        >> all_users = user_crud.read_all()
        >> [u.name for u in all_users]
        ["Иван Иванов"]

        # Поиск пользователя по ID
        >> user = user_crud.read_by_id(1)
        >> print(user.email)
        ivan@example.com

        # Поиск пользователя по email
        >> user = user_crud.find_by_email("ivan@example.com")
        >> print(user.name)
        Иван Иванов

        # Обновление пользователя
        >> user_crud.update(1, name="Иван Петров")
        >> user = user_crud.read_by_id(1)
        >> print(user.name)
        Иван Петров

        # Удаление пользователя
        >> user_crud.delete(1)
        >> user_crud.read_by_id(1)
        None
    """

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def _connect(self):
        """Создает и возвращает соединение с базой данных SQLite."""
        return sqlite3.connect(self.db_path)

    # CREATE
    def create(self, name: str, email: str) -> User:
        """Создает нового пользователя и возвращает объект User."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cur.lastrowid
        conn.close()

        return User(user_id, name, email)

    # READ all
    def read_all(self):
        """Возвращает список всех пользователей в базе в виде объектов User."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, name, email FROM users")
        rows = cur.fetchall()
        conn.close()

        return [User(*row) for row in rows]

    # READ by id
    def read_by_id(self, user_id: int):
        """Возвращает пользователя по ID или None, если не найден."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, name, email FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        conn.close()

        return User(*row) if row else None

    # READ by email
    def find_by_email(self, email: str):
        """Возвращает пользователя по email или None, если не найден."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, name, email FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        conn.close()

        return User(*row) if row else None

    # UPDATE
    def update(self, user_id: int, name: str = None, email: str = None):
        """Обновляет имя и/или email пользователя по ID."""
        conn = self._connect()
        cur = conn.cursor()

        if name:
            cur.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
        if email:
            cur.execute("UPDATE users SET email=? WHERE id=?", (email, user_id))

        conn.commit()
        conn.close()

    # DELETE
    def delete(self, user_id: int):
        """Удаляет пользователя по ID."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
