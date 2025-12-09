import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.author import Author
from models.app import App
from models.user import User
from models.currency import Currency
from models.subscription import UserCurrency
from datetime import datetime


class TestAuthor(unittest.TestCase):
    """Тестирование класса Author"""

    def test_author_creation(self):
        """Проверка создания объекта Author"""
        author = Author("Потёмкин Платон", "P3122")
        self.assertEqual(author.name, "Потёмкин Платон")
        self.assertEqual(author.group, "P3122")

    def test_author_creation_default_group(self):
        """Проверка создания объекта Author с группой по умолчанию"""
        author = Author("Потёмкин Платон")
        self.assertEqual(author.name, "Потёмкин Платон")
        self.assertEqual(author.group, "P3122")

    def test_author_name_setter_valid(self):
        """Проверка сеттера имени с корректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        author.name = "Петр Петров"
        self.assertEqual(author.name, "Петр Петров")

    def test_author_name_setter_invalid_empty(self):
        """Проверка сеттера имени с пустой строкой"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.name = ""
        self.assertIn("Имя не может быть меньше одного символа", str(context.exception))

    def test_author_name_setter_invalid_not_string(self):
        """Проверка сеттера имени с нестроковым значением"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.name = 123
        self.assertIn("Имя не может быть меньше одного символа", str(context.exception))

    def test_author_group_setter_valid(self):
        """Проверка сеттера группы с корректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        author.group = "P3123"
        self.assertEqual(author.group, "P3123")

    def test_author_group_setter_invalid_short(self):
        """Проверка сеттера группы с некорректным значением (слишком короткая)"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.group = "P312"
        self.assertIn("Группа должна быть строкой и менее 5 символов", str(context.exception))

    def test_author_group_setter_invalid_long(self):
        """Проверка сеттера группы с некорректным значением (слишком длинная)"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.group = "P31222"
        self.assertIn("Группа должна быть строкой и менее 5 символов", str(context.exception))

    def test_author_group_setter_invalid_not_string(self):
        """Проверка сеттера группы с нестроковым значением"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.group = 3122
        self.assertIn("Группа должна быть строкой и менее 5 символов", str(context.exception))


class TestApp(unittest.TestCase):
    """Тестирование класса App"""

    def test_app_creation(self):
        """Проверка создания объекта App"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        self.assertEqual(app.name, "Test App")
        self.assertEqual(app.version, "1.0.0")
        self.assertEqual(app.author, author)

    def test_app_name_setter_valid(self):
        """Проверка сеттера названия приложения"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        app.name = "New App Name"
        self.assertEqual(app.name, "New App Name")

    def test_app_name_setter_with_spaces(self):
        """Проверка сеттера названия приложения с пробелами"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        app.name = "   App With Spaces   "
        self.assertEqual(app.name, "App With Spaces")

    def test_app_name_setter_invalid_empty(self):
        """Проверка сеттера названия приложения с пустой строкой"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.name = ""
        self.assertIn("Название приложения должно быть строкой не менее 1 символа", str(context.exception))

    def test_app_name_setter_invalid_only_spaces(self):
        """Проверка сеттера названия приложения только с пробелами"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.name = "   "
        self.assertIn("Название приложения должно быть строкой не менее 1 символа", str(context.exception))

    def test_app_name_setter_invalid_not_string(self):
        """Проверка сеттера названия приложения с нестроковым значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.name = 123
        self.assertIn("Название приложения должно быть строкой не менее 1 символа", str(context.exception))

    def test_app_version_setter_valid(self):
        """Проверка сеттера версии с корректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        app.version = "2.1.5"
        self.assertEqual(app.version, "2.1.5")

    def test_app_version_setter_invalid_not_string(self):
        """Проверка сеттера версии с нестроковым значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.version = 1.0
        self.assertIn("Версия должна быть строкой", str(context.exception))

    def test_app_version_setter_invalid_format(self):
        """Проверка сеттера версии с некорректным форматом"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.version = "1.a.0"
        self.assertIn("Версия должна быть в формате X.Y.Z", str(context.exception))

    def test_app_author_getter(self):
        """Проверка геттера автора"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        self.assertEqual(app.author, author)

    def test_app_author_setter_valid(self):
        """Проверка сеттера автора с корректным значением"""
        author1 = Author("Потёмкин Платон", "P3122")
        author2 = Author("Иван Иванов", "P3123")
        app = App("Test App", "1.0.0", author1)
        app.author = author2
        self.assertEqual(app.author, author2)

    def test_app_author_setter_invalid(self):
        """Проверка сеттера автора с некорректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.author = "Not an Author"
        self.assertIn("Автор должен быть объектом класса Author", str(context.exception))


class TestUser(unittest.TestCase):
    """Тестирование класса User"""

    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User(0, "Иван Иванов", "ivan@test.com")

    def test_user_creation(self):
        """Проверка создания объекта User"""
        self.assertEqual(self.user.id, 0)
        self.assertEqual(self.user.name, "Иван Иванов")
        self.assertEqual(self.user.email, "ivan@test.com")

    def test_user_name_getter(self):
        """Проверка геттера имени"""
        self.assertEqual(self.user.name, "Иван Иванов")

    def test_user_name_setter_valid(self):
        """Проверка сеттера имени пользователя"""
        self.user.name = "Петр Петров"
        self.assertEqual(self.user.name, "Петр Петров")

    def test_user_name_setter_invalid_short(self):
        """Проверка сеттера имени с слишком коротким значением"""
        with self.assertRaises(ValueError) as context:
            self.user.name = "Я"  # 1 символ
        self.assertIn("Имя должно быть строкой не менее 2 символов", str(context.exception))

    def test_user_name_setter_invalid_empty(self):
        """Проверка сеттера имени с пустой строкой"""
        with self.assertRaises(ValueError) as context:
            self.user.name = ""
        self.assertIn("Имя должно быть строкой не менее 2 символов", str(context.exception))

    def test_user_name_setter_invalid_not_string(self):
        """Проверка сеттера имени с нестроковым значением"""
        with self.assertRaises(ValueError) as context:
            self.user.name = 123
        self.assertIn("Имя должно быть строкой не менее 2 символов", str(context.exception))

    def test_user_email_setter_valid(self):
        """Проверка сеттера email"""
        self.user.email = "new@test.com"
        self.assertEqual(self.user.email, "new@test.com")

    def test_user_email_setter_valid_with_subdomain(self):
        """Проверка сеттера email с поддоменом"""
        self.user.email = "user@sub.domain.com"
        self.assertEqual(self.user.email, "user@sub.domain.com")

    def test_user_email_setter_invalid_no_at(self):
        """Проверка сеттера email без символа @"""
        with self.assertRaises(ValueError) as context:
            self.user.email = "not-an-email"
        self.assertIn("Email должен быть корректной электронной почтой", str(context.exception))

    def test_user_email_setter_invalid_not_string(self):
        """Проверка сеттера email с нестроковым значением"""
        with self.assertRaises(ValueError) as context:
            self.user.email = 123
        self.assertIn("Email должен быть корректной электронной почтой", str(context.exception))

    def test_user_email_setter_invalid_empty(self):
        """Проверка сеттера email с пустой строкой"""
        with self.assertRaises(ValueError) as context:
            self.user.email = ""
        self.assertIn("Email должен быть корректной электронной почтой", str(context.exception))


class TestCurrency(unittest.TestCase):
    """Тестирование класса Currency"""

    def setUp(self):
        """Создание тестовой валюты"""
        self.currency = Currency(0, "840", "USD", "Доллар США", 75.50, 1)

    def test_currency_creation(self):
        """Проверка создания объекта Currency"""
        self.assertEqual(self.currency.id, 0)
        self.assertEqual(self.currency.num_code, "840")
        self.assertEqual(self.currency.char_code, "USD")
        self.assertEqual(self.currency.name, "Доллар США")
        self.assertEqual(self.currency.value, 75.50)
        self.assertEqual(self.currency.nominal, 1)

    def test_currency_id_getter(self):
        """Проверка геттера ID"""
        self.assertEqual(self.currency.id, 0)

    def test_currency_id_is_readonly(self):
        """Проверка, что ID только для чтения"""
        with self.assertRaises(AttributeError):
            self.currency.id = 1

    def test_currency_num_code_getter(self):
        """Проверка геттера цифрового кода"""
        self.assertEqual(self.currency.num_code, "840")

    def test_currency_num_code_setter_valid(self):
        """Проверка сеттера цифрового кода"""
        self.currency.num_code = "978"
        self.assertEqual(self.currency.num_code, "978")

    def test_currency_num_code_setter_invalid_short(self):
        """Проверка сеттера цифрового кода с коротким значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.num_code = "12"  # Меньше 3 символов
        self.assertIn("Цифровой код должен быть строкой из 3 цифр", str(context.exception))

    def test_currency_num_code_setter_invalid_long(self):
        """Проверка сеттера цифрового кода с длинным значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.num_code = "1234"  # Больше 3 символов
        self.assertIn("Цифровой код должен быть строкой из 3 цифр", str(context.exception))

    def test_currency_num_code_setter_invalid_not_digits(self):
        """Проверка сеттера цифрового кода с нецифровыми символами"""
        with self.assertRaises(ValueError) as context:
            self.currency.num_code = "12A"
        self.assertIn("Цифровой код должен быть строкой из 3 цифр", str(context.exception))

    def test_currency_num_code_setter_invalid_not_string(self):
        """Проверка сеттера цифрового кода с нестроковым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.num_code = 840
        self.assertIn("Цифровой код должен быть строкой из 3 цифр", str(context.exception))

    def test_currency_char_code_getter(self):
        """Проверка геттера символьного кода"""
        self.assertEqual(self.currency.char_code, "USD")

    def test_currency_char_code_setter_valid(self):
        """Проверка сеттера символьного кода"""
        self.currency.char_code = "EUR"
        self.assertEqual(self.currency.char_code, "EUR")

    def test_currency_char_code_setter_lowercase(self):
        """Проверка сеттера символьного кода в нижнем регистре"""
        self.currency.char_code = "gbp"
        self.assertEqual(self.currency.char_code, "GBP")

    def test_currency_char_code_setter_invalid_short(self):
        """Проверка сеттера символьного кода с коротким значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.char_code = "US"  # 2 символа
        self.assertIn("Символьный код должен быть строкой из 3 символов", str(context.exception))

    def test_currency_char_code_setter_invalid_long(self):
        """Проверка сеттера символьного кода с длинным значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.char_code = "USDD"  # 4 символа
        self.assertIn("Символьный код должен быть строкой из 3 символов", str(context.exception))

    def test_currency_char_code_setter_invalid_not_string(self):
        """Проверка сеттера символьного кода с нестроковым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.char_code = 840
        self.assertIn("Символьный код должен быть строкой из 3 символов", str(context.exception))

    def test_currency_name_getter(self):
        """Проверка геттера названия"""
        self.assertEqual(self.currency.name, "Доллар США")

    def test_currency_name_setter_valid(self):
        """Проверка сеттера названия"""
        self.currency.name = "Евро"
        self.assertEqual(self.currency.name, "Евро")

    def test_currency_name_setter_with_spaces(self):
        """Проверка сеттера названия с пробелами"""
        self.currency.name = "   Евро   "
        self.assertEqual(self.currency.name, "Евро")

    def test_currency_name_setter_invalid_empty(self):
        """Проверка сеттера названия с пустой строкой"""
        with self.assertRaises(ValueError) as context:
            self.currency.name = ""
        self.assertIn("Название валюты не может быть пустым", str(context.exception))

    def test_currency_name_setter_invalid_only_spaces(self):
        """Проверка сеттера названия только с пробелами"""
        with self.assertRaises(ValueError) as context:
            self.currency.name = "   "
        self.assertIn("Название валюты не может быть пустым", str(context.exception))

    def test_currency_name_setter_invalid_not_string(self):
        """Проверка сеттера названия с нестроковым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.name = 123
        self.assertIn("Название валюты не может быть пустым", str(context.exception))

    def test_currency_value_getter(self):
        """Проверка геттера курса"""
        self.assertEqual(self.currency.value, 75.50)

    def test_currency_value_setter_valid_float(self):
        """Проверка сеттера курса с float"""
        self.currency.value = 80.25
        self.assertEqual(self.currency.value, 80.25)

    def test_currency_value_setter_valid_int(self):
        """Проверка сеттера курса с int"""
        self.currency.value = 80
        self.assertEqual(self.currency.value, 80.0)

    def test_currency_value_setter_invalid_negative(self):
        """Проверка сеттера курса с отрицательным значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.value = -10
        self.assertIn("Курс должен быть положительным числом", str(context.exception))

    def test_currency_value_setter_invalid_zero(self):
        """Проверка сеттера курса с нулевым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.value = 0
        self.assertIn("Курс должен быть положительным числом", str(context.exception))

    def test_currency_value_setter_invalid_not_number(self):
        """Проверка сеттера курса с нечисловым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.value = "not a number"
        self.assertIn("Курс должен быть положительным числом", str(context.exception))

    def test_currency_nominal_getter(self):
        """Проверка геттера номинала"""
        self.assertEqual(self.currency.nominal, 1)

    def test_currency_nominal_setter_valid(self):
        """Проверка сеттера номинала"""
        self.currency.nominal = 10
        self.assertEqual(self.currency.nominal, 10)

    def test_currency_nominal_setter_invalid_negative(self):
        """Проверка сеттера номинала с отрицательным значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.nominal = -1
        self.assertIn("Номинал должен быть положительным целым числом", str(context.exception))

    def test_currency_nominal_setter_invalid_zero(self):
        """Проверка сеттера номинала с нулевым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.nominal = 0
        self.assertIn("Номинал должен быть положительным целым числом", str(context.exception))

    def test_currency_nominal_setter_invalid_float(self):
        """Проверка сеттера номинала с float"""
        with self.assertRaises(ValueError) as context:
            self.currency.nominal = 1.5
        self.assertIn("Номинал должен быть положительным целым числом", str(context.exception))

    def test_currency_nominal_setter_invalid_not_number(self):
        """Проверка сеттера номинала с нечисловым значением"""
        with self.assertRaises(ValueError) as context:
            self.currency.nominal = "ten"
        self.assertIn("Номинал должен быть положительным целым числом", str(context.exception))


class TestUserCurrency(unittest.TestCase):
    """Тестирование класса UserCurrency"""

    def setUp(self):
        """Создание тестовых объектов"""
        self.user_currency = UserCurrency(1, 5)

    def test_user_id_getter(self):
        """Проверка геттера user_id"""
        self.assertEqual(self.user_currency.user_id, 1)

    def test_currency_id_getter(self):
        """Проверка геттера currency_id"""
        self.assertEqual(self.user_currency.currency_id, 5)



if __name__ == '__main__':
    unittest.main()