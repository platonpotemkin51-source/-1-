class User:
    __users_storage = {}  # {id: User_object}
    __email_to_id = {}
    __next_id = 0

    def __init__(self, user_id: int, name: str, email: str, password: str):
        self.__id = user_id
        self.__name = name
        self.__email = email
        self.__password = password  # В реальном приложении храните хэш!

    # === СВОЙСТВА ДЛЯ ДОСТУПА К ДАННЫМ ===
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    # @property
    # def password(self):
    #     return self.__password

    def check_password(self, password: str) -> bool:
        return self.__password == password

    # === СТАТИЧЕСКИЕ МЕТОДЫ ДЛЯ РАБОТЫ С ХРАНИЛИЩЕМ ===
    @classmethod
    def __generate_id(cls) -> int:
        """Генерирует следующий ID"""
        current_id = cls.__next_id
        cls.__next_id += 1
        return current_id

    @classmethod
    def create_user(cls, name: str, email: str, password: str):
        """Создает и сохраняет нового пользователя"""
        if email in cls.__email_to_id:
            raise ValueError("Пользователь с таким email уже существует")

        user_id = cls.__generate_id()
        user = cls(user_id, name, email, password)

        # Сохраняем в двух индексах для быстрого поиска
        cls.__users_storage[user_id] = user
        cls.__email_to_id[email] = user_id

        return user

    @classmethod
    def find_by_id(cls, user_id: int):
        """Находит пользователя по ID"""
        return cls.__users_storage.get(user_id)

    @classmethod
    def find_by_email(cls, email: str):
        """Находит пользователя по email"""
        user_id = cls.__email_to_id.get(email)
        if user_id is not None:
            return cls.__users_storage.get(user_id)
        return None

    @classmethod
    def authenticate(cls, email: str, password: str):
        """Проверяет email и пароль, возвращает пользователя если верно"""
        print(f"=== AUTHENTICATE ===")
        user = cls.find_by_email(email)

        if user is not None:
            print(f"Проверяем пароль для пользователя: {user.email}")
            password_match = user.check_password(password)
            print(f"Пароль совпадает: {password_match}")

            if password_match:
                print("++++ Успешная аутентификация")
                return user
            else:
                print("---- Неправильный пароль")
                return None
        else:
            print("---- Пользователь не найден")
            return None

    @classmethod
    def user_exists(cls, email: str) -> bool:
        """Проверяет существует ли пользователь"""
        return email in cls.__email_to_id

    # @classmethod
    # def delete_user(cls, user_id: int) -> bool:
    #     """Удаляет пользователя по ID"""
    #     user = cls.find_by_id(user_id)
    #     if user:
    #         # Удаляем из обоих индексов
    #         del cls.__users_storage[user_id]
    #         del cls.__email_to_id[user.email]
    #         return True
    #     return False