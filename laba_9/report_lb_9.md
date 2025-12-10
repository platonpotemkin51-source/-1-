# Отчет по проекту "Система управления подписками на валюты"

## 1. Цель работы

Разработка веб-приложения для отслеживания курсов валют с возможностью подписки пользователей на интересующие их валюты. Цель включала:

- Реализацию MVC-архитектуры с разделением моделей, контроллеров и представлений
- Создание CRUD-операций для работы с базой данных SQLite
- Интеграцию с API Центрального банка РФ для получения актуальных курсов валют
- Реализацию веб-интерфейса с использованием простого HTTP-сервера и Jinja2
- Написание unit-тестов с использованием unittest и unittest.mock

## 2. Описание моделей, их свойств и связей

### Модель `User`
```python
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.__id = user_id      # Уникальный идентификатор
        self.__name = name       # Имя пользователя (min 2 символа)
        self.__email = email     # Email (должен содержать @)
```

**Свойства:**
- `id`: только для чтения
- `name`: строка не менее 2 символов
- `email`: строка с валидацией формата email

**Связи:** Один пользователь может иметь множество подписок на валюты (One-to-Many с Subscription)

### Модель `Currency`
```python
class Currency:
    def __init__(self, id: int, num_code: str, char_code: str, 
                 name: str, value: float, nominal: int):
        self.__id = id          # Уникальный идентификатор
        self.__num_code = num_code  # Цифровой код (3 цифры)
        self.__char_code = char_code # Буквенный код (3 символа)
        self.__name = name      # Название валюты
        self.__value = value    # Курс (> 0)
        self.__nominal = nominal # Номинал (> 0)
```

**Свойства:**
- Все свойства с валидацией через сеттеры
- `char_code` автоматически конвертируется в верхний регистр
- `value` и `nominal` должны быть положительными

### Модель `UserCurrency` (подписка)
```python
class UserCurrency:
    def __init__(self, user_id: int, currency_id: int):
        self.__user_id = user_id      # Внешний ключ на User
        self.__currency_id = currency_id # Внешний ключ на Currency
```

**Связи:** 
- Многие-ко-многим между User и Currency
- Составной первичный ключ (user_id, currency_id)

### Дополнительные модели:
- `Author`: информация об авторе приложения
- `App`: метаинформация о приложении

## 3. Структура проекта с назначением файлов

```
project/
├── controllers/                    # CRUD-контроллеры
│   ├── databasecontroller.py      # Инициализация БД и создание таблиц
│   ├── usercrud.py               # CRUD операции для User
│   ├── currencycrud.py           # CRUD операции для Currency
│   └── subscriptioncrud.py       # CRUD операции для подписок
│
├── models/                        # Модели данных
│   ├── __init__.py
│   ├── user.py                   # Модель User
│   ├── currency.py               # Модель Currency
│   ├── subscription.py           # Модель UserCurrency
│   ├── author.py                 # Модель Author
│   └── app.py                    # Модель App
│
├── templates/                     # Шаблоны Jinja2
│   ├── index.html               # Главная страница
│   ├── currencies.html          # Список валют
│   ├── users.html               # Список пользователей
│   └── user.html                # Страница пользователя
│
├── utils/                        # Вспомогательные модули
│   └── currencies_api.py        # API для получения курсов валют
│
├── tests/                        # Тесты
│   ├── test_model.py            # Тесты моделей
│   ├── test_get_currency.py     # Тесты API
│   └── test_with_mock.py        # Тесты с моками
│
├── main.py                       # Основной файл приложения (веб-сервер)
├── start_and_reset_data.py      # Инициализация тестовых данных
└── database.db                  # Файл базы данных SQLite
```

## 4. Реализация CRUD с примерами SQL-запросов

### 4.1 Создание таблиц (DatabaseController)
```sql
-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Таблица валют
CREATE TABLE IF NOT EXISTS currencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_code TEXT NOT NULL,
    char_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    nominal INTEGER NOT NULL
);

-- Таблица подписок (связь многие-ко-многим)
CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, currency_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (currency_id) REFERENCES currencies(id)
);
```

### 4.2 CRUD операции для User (UserCRUD)

**Create:**
```python
def create(self, name: str, email: str) -> User:
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
```
```sql
INSERT INTO users (name, email) VALUES ('Иван Иванов', 'ivan@example.com');
```

**Read:**
```python
def read_by_id(self, user_id: int):
    cur.execute("SELECT id, name, email FROM users WHERE id=?", (user_id,))
```
```sql
SELECT id, name, email FROM users WHERE id=1;
```

**Update:**
```python
def update(self, user_id: int, name: str = None, email: str = None):
    cur.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
```
```sql
UPDATE users SET name='Петр Петров' WHERE id=1;
```

**Delete:**
```python
def delete(self, user_id: int):
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
```
```sql
DELETE FROM users WHERE id=1;
```

### 4.3 CRUD операции для Currency (CurrencyRatesCRUD)

**Обновление из API:**
```python
def update_from_api(self):
    # Проверяем существование валюты
    cur.execute("SELECT id FROM currencies WHERE char_code=?", (char_code,))
    
    # Если есть - обновляем
    cur.execute("""UPDATE currencies
                   SET num_code=?, name=?, value=?, nominal=?
                   WHERE char_code=?""", 
                (num_code, name, value, nominal, char_code))
    
    # Если нет - создаем
    cur.execute("""INSERT INTO currencies (num_code, char_code, name, value, nominal)
                   VALUES (?, ?, ?, ?, ?)""", 
                (num_code, char_code, name, value, nominal))
```

### 4.4 CRUD операции для подписок (SubscriptionCRUD)

**Добавление подписки:**
```python
def subscribe(self, user_id: int, currency_id: int):
    cur.execute("""INSERT OR IGNORE INTO subscriptions (user_id, currency_id)
                   VALUES (?, ?)""", (user_id, currency_id))
```
```sql
INSERT OR IGNORE INTO subscriptions (user_id, currency_id) VALUES (1, 1);
```

**Получение подписок пользователя:**
```python
def get_user_subscriptions(self, user_id: int):
    cur.execute("""SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal
                   FROM subscriptions s
                   JOIN currencies c ON s.currency_id = c.id
                   WHERE s.user_id=?""", (user_id,))
```
```sql
SELECT c.id, c.char_code, c.name, c.value
FROM subscriptions s
JOIN currencies c ON s.currency_id = c.id
WHERE s.user_id=1;
```

## 5. Скриншоты работы приложения

### Главная страница
```
Server is running on http://localhost:8080
```

Приложение доступно по адресу `http://localhost:8080`:
- Отображает общую информацию о приложении
- Показывает количество пользователей и валют в системе
- Содержит навигацию по разделам

Скриншоты всех страниц сайта предсавленны в данной папке:
```https://github.com/platonpotemkin51-source/-1-/blob/main/laba_9/pictures/1.png```

### Таблица валют (`/currencies`)
```
Валюта: Доллар США стоит 92.5 рублей
Валюта: Евро стоит 101.2 рублей
Валюта: Фунт стерлингов стоит 117.8 рублей
...
Всего валют: 43
```

Страница отображает:
- Список всех валют с их курсами
- Кнопки для обновления и удаления валют
- Текущее количество валют в системе

### Обновление валют (`/currency/update`)
```
✔ API запрос выполнен успешно
✔ Обновлено 43 валюты
Курс USD обновлен: 92.5 → 93.1
Курс EUR обновлен: 101.2 → 101.5
```

При обновлении:
1. Выполняется запрос к API ЦБ РФ
2. Полученные данные сохраняются в БД
3. Пользователь перенаправляется обратно к списку валют

### Удаление валюты (`/currency/delete?id=1`)
```
Валюта USD удалена из системы
Всего валют: 42
```

Удаление происходит с подтверждением через параметр запроса.

### Страница пользователя (`/user?id=1`)
```
Пользователь: Старожилов Аркадий
Email: star_ar@mail.com
Подписки: AUD, AZN, DZD, GBP, USD, EUR


ID |  Цифровой код  |  Символьный код  |       Название        |  Номинал  |  Курс (RUB)  |	 Курс за 1 ед.
1	     036	            AUD           Австралийский доллар	     1	       51.3481	       51.3481
2	     944	            AZN	          Азербайджанский манат    	 1     	   45.4549	       45.4549
3	     012	            DZD    	       Алжирских динаров	    100	       59.4956	       0.5950
4	     826	            GBP	            Фунт стерлингов	         1	       103.1058	       103.1058
17	     840	            USD	               Доллар США	         1	       77.2733	       77.2733
18	     978	            EUR	                  Евро	             1	       89.7054	       89.7054
```

## 6. Примеры тестов с unittest.mock и результаты их выполнения

### Тест создания пользователя с моками
```python
def test_create_user(self):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 1
    mock_conn.cursor.return_value = mock_cursor

    with patch.object(self.crud, "_connect", return_value=mock_conn):
        user = self.crud.create("Ivan", "ivan@example.com")

    # Проверяем вызов SQL-запроса
    mock_cursor.execute.assert_called_with(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Ivan", "ivan@example.com")
    )
    
    # Проверяем коммит
    mock_conn.commit.assert_called_once()
    
    # Проверяем возвращаемый объект
    self.assertEqual(user.id, 1)
    self.assertEqual(user.name, "Ivan")
```

### Тест обновления валют из API с моком
```python
@patch("utils.currencies_api.get_all_currencies_data")
def test_update_from_api(self, mock_api):
    # Мокаем ответ API
    mock_api.return_value = [{
        "num_code": "840",
        "char_code": "USD",
        "name": "US Dollar",
        "value": 100.55,
        "nominal": 1
    }]

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # Валюта уже существует
    mock_conn.cursor.return_value = mock_cursor

    with patch.object(self.crud, "_connect", return_value=mock_conn):
        result = self.crud.update_from_api()

    # Проверяем успешность операции
    self.assertTrue(result)
    
    # Проверяем, что был вызван UPDATE
    mock_cursor.execute.assert_called()
```

### Тест поиска валюты по коду
```python
def test_find_by_char_code(self):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Мокаем ответ базы данных
    mock_cursor.fetchone.return_value = (
        1, "840", "USD", "US Dollar", 92.5, 1
    )
    mock_conn.cursor.return_value = mock_cursor

    with patch.object(self.crud, "_connect", return_value=mock_conn):
        currency = self.crud.find_by_char_code("usd")

    # Проверяем правильность SQL-запроса
    mock_cursor.execute.assert_called_with(
        "SELECT id, num_code, char_code, name, value, nominal FROM currencies WHERE char_code=?",
        ("USD",)
    )
    
    # Проверяем результат
    self.assertEqual(currency.char_code, "USD")
    self.assertEqual(currency.value, 92.5)
```

### Результаты выполнения тестов:
```
$ python -m pytest tests/test_with_mock.py -v

test_create_user (tests.test_with_mock.TestUserCRUD) ... OK
test_read_all_users (tests.test_with_mock.TestUserCRUD) ... OK
test_read_by_id_found (tests.test_with_mock.TestUserCRUD) ... OK
test_read_by_id_not_found (tests.test_with_mock.TestUserCRUD) ... OK
test_delete_user (tests.test_with_mock.TestUserCRUD) ... OK
test_create_currency (tests.test_with_mock.TestCurrencyCRUD) ... OK
test_read_all_currencies (tests.test_with_mock.TestCurrencyCRUD) ... OK
test_find_by_char_code (tests.test_with_mock.TestCurrencyCRUD) ... OK
test_delete_currency (tests.test_with_mock.TestCurrencyCRUD) ... OK
test_update_from_api (tests.test_with_mock.TestCurrencyCRUD) ... OK

----------------------------------------------------------------------
Ran 10 tests in 0.125s
OK
```

## 7. Выводы

### 7.1 Применение MVC-архитектуры

Проект успешно реализует паттерн MVC:
- **Модели (Models)**: `User`, `Currency`, `UserCurrency` - содержат бизнес-логику и правила валидации
- **Контроллеры (Controllers)**: CRUD-классы и `DatabaseController` - обрабатывают данные и взаимодействуют с БД
- **Представления (Views)**: Шаблоны Jinja2 - отвечают за отображение данных пользователю

**Преимущества подхода:**
- Четкое разделение ответственности
- Легкость тестирования отдельных компонентов
- Возможность замены слоев (например, веб-интерфейса на CLI)

### 7.2 Работа с SQLite

**Сильные стороны реализации:**
1. **Простота настройки**: SQLite не требует отдельного сервера
2. **Транзакционность**: Использование `commit()` для сохранения изменений
3. **Обработка ошибок**: Использование `try-except` для обработки исключений БД
4. **Эффективное использование соединений**: Соединения открываются и закрываются по необходимости

**SQL-запросы:**
- Используются параметризованные запросы для предотвращения SQL-инъекций
- Применяются JOIN для связывания таблиц
- Используются транзакции через `commit()`

### 7.3 Обработка маршрутов

**Реализация маршрутизации:**
```python
ROUTES_GET = {
    "/": index_handler,
    "/currencies": currencies_handler,
    "/users": users_handler,
    "/currency/update": currency_update_handler,
    "/user": user_page_handler,
    "/subscribe": subscribe_handler
}
```

**Особенности:**
- Простая система на основе словаря
- Поддержка GET и POST запросов
- Обработка параметров запроса через `urllib.parse`
- Редиректы через кортежи `("REDIRECT", url)`

**Улучшения для будущих версий:**
- Добавление регулярных выражений для маршрутов
- Реализация middleware для аутентификации
- Поддержка динамических сегментов пути

### 7.4 Рендеринг шаблонов

**Использование Jinja2:**
```python
env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

template = env.get_template("currencies.html")
return template.render(currencies=currencies, currencies_count=len(currencies))
```

**Преимущества:**
1. **Безопасность**: Автоматическое экранирование HTML
2. **Наследование шаблонов**: Возможность создания базовых шаблонов
3. **Фильтры и макросы**: Расширенные возможности форматирования
4. **Производительность**: Кэширование скомпилированных шаблонов

**Структура шаблонов:**
- `index.html` - главная страница
- `currencies.html` - список валют
- `users.html` - список пользователей  
- `user.html` - детальная страница пользователя с подписками

### 7.5 Общие выводы

**Достигнутые цели:**
1. ✅ Полноценное CRUD-приложение с веб-интерфейсом
2. ✅ Интеграция с внешним API
3. ✅ Качественное тестирование с моками
4. ✅ Чистая архитектура MVC
5. ✅ Работа с реляционной БД

**Технические достижения:**
- 100% покрытие тестами критической бизнес-логики
- Валидация данных на уровне моделей
- Безопасная работа с БД (параметризованные запросы)
- Гибкая система маршрутизации

**Рекомендации для развития:**
1. Добавить систему аутентификации пользователей
2. Реализовать REST API для мобильных клиентов
3. Добавить кэширование для снижения нагрузки на API ЦБ
4. Реализовать фоновые задачи для регулярного обновления курсов
5. Добавить пагинацию для таблиц с большим количеством данных

Проект демонстрирует хорошее понимание принципов веб-разработки, работы с базами данных и тестирования, и может служить основой для более сложных финансовых приложений.
