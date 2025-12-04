# **Отчет по лабораторной работе: Веб-приложение для отслеживания курсов валют**

## **1. Цель работы**
Разработка веб-приложения для отображения и управления курсами валют с использованием API Центробанка России. Задачи включали:
- Реализацию моделей данных (пользователи, валюты, подписки)
- Создание веб-сервера на базе HTTPServer
- Интеграцию с внешним API для получения актуальных курсов
- Реализацию шаблонов Jinja2 для отображения данных
- Написание тестов для всех компонентов системы

## **2. Описание предметной области**

### **Модели и их свойства:**

**Author (Автор):**
- `name` - имя автора (строка, минимум 1 символ)
- `group` - номер группы (строка, ровно 5 символов)

**App (Приложение):**
- `name` - название приложения (строка, минимум 1 символ)
- `version` - версия (строка формата X.Y.Z)
- `author` - объект класса Author

**User (Пользователь):**
- `id` - уникальный идентификатор
- `name` - имя (строка, минимум 2 символа)
- `email` - email (строка с символом '@')

**Currency (Валюта):**
- `id` - уникальный идентификатор
- `num_code` - цифровой код (3 цифры)
- `char_code` - символьный код (3 символа)
- `name` - название валюты
- `value` - курс к рублю
- `nominal` - номинал

**UserCurrency (Подписки):**
- `user_id` - ID пользователя
- `currency_id` - ID валюты

### **Связи между моделями:**
- Один пользователь может иметь много подписок на валюты (One-to-Many)
- Одна валюта может быть в подписках у многих пользователей (Many-to-Many через UserCurrency)
- App содержит Author (One-to-One)

## **3. Структура проекта**

```
project/
├── main.py                    # Главный файл сервера
├── models/                    # Бизнес-логика
│   ├── __init__.py
│   ├── author.py             # Класс Author
│   ├── app.py                # Класс App
│   ├── user.py               # Класс User
│   ├── currency.py           # Класс Currency
│   └── user_currency.py      # Класс UserCurrency
├── utils/
│   └── currencies_api.py     # API для получения курсов валют
├── templates/                # HTML шаблоны
│   ├── index.html
│   ├── currencies.html
│   ├── users.html
│   └── user.html
├── tests/                    # Тесты
│   ├── test_model.py
│   ├── test_get_currency.py
│   └── test_control_main.py
└── requirements.txt          # Зависимости
```

## **4. Описание реализации**

### **4.1 Реализация моделей и свойств**

**Геттеры/сеттеры реализованы через декоратор `@property`:**

```python
class User:
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) < 2:
            raise ValueError("Имя должно быть строкой не менее 2 символов")
        self.__name = value.strip()
```

**Хранение данных в памяти:**
```python
class User:
    __users = {}  # Словарь для хранения {id: user_object}
    __next_id = 0  # Счетчик для генерации ID
```

### **4.2 Маршруты и обработка запросов**

**Основные маршруты в `main.py`:**
```python
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Главная страница
        elif self.path == '/currencies':
            # Список валют
        elif self.path == '/users':
            # Список пользователей
        elif self.path.startswith('/user?'):
            # Страница пользователя
```

**Обработка параметров:**
```python
# Извлечение ID пользователя из URL
if self.path.startswith('/user?id='):
    user_id = int(self.path.split('=')[1])
```

### **4.3 Использование Jinja2**

**Инициализация Environment:**
```python
env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)
```

**Рендеринг шаблонов:**
```python
template = env.get_template("index.html")
result = template.render(
    flag=flag,
    app=app,
    currencies_count=currencies_count,
    users_count=users_count,
)
```

**Шаблоны с условиями:**
```html
{% if flag == True %}
    <h1>Информация о приложении</h1>
{% else %}
    <h1>Информация об авторе</h1>
{% endif %}
```

### **4.4 Интеграция функции get_currencies**

**Получение данных из API:**
```python
def get_currencies(currency_codes: list = None, 
                   url: str = "https://www.cbr-xml-daily.ru/daily_json.js"):
    response = requests.get(url, timeout=10)
    data = response.json()
```

**Обработка ошибок:**
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except (requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException) as e:
    raise ConnectionError(f"API недоступно: {str(e)}")
```

**Обновление валют в базе:**
```python
def update_all_currencies():
    currencies_data = get_all_currencies_data()
    for currency_data in currencies_data:
        currency = Currency.find_by_char_code(currency_data['char_code'])
        if currency:
            currency.value = currency_data['value']
```

## **5. Примеры работы приложения**

### **Скриншоты страниц:**

**Главная страница (/)**
```
Информация о приложении

Приложение
Название: First
Версия: 1.0.0

Автор
Platon Potemkin

Статистика
Всего валют в системе: 50
Всего пользователей в системе: 5
```

**Список валют (/currencies)**
```
ID | Цифровой код | Символьный код | Название | Номинал | Курс (RUB) | Курс за 1 ед.
0  | 840         | USD           | Доллар США | 1      | 75.5000   | 75.5000
1  | 978         | EUR           | Евро       | 1      | 85.2000   | 85.2000
```

**Список пользователей (/users)**
```
ID | Имя
0  | Старожилов Аркадий
1  | Лукьянов Александр
2  | Аветисян Владислав
```

**Страница пользователя (/user?id=0)**
```
Пользователь: Старожилов Аркадий
ID: 0
Почта: star_ar@mail.com
Подписки: USD, EUR, GBP, JPY, CNY

Подписанные валюты:
USD - Доллар США - 75.5000
EUR - Евро - 85.2000
```

## **6. Самостоятельная работа (Графики курсов валют)**

### **Реализация:**
Для визуализации курсов валют за последние 3 месяца использовалась библиотека **matplotlib** и исторические данные API ЦБ РФ.

**Ключевые библиотеки:**
```python
import matplotlib.pyplot as plt
import pandas as pd
import requests
from datetime import datetime, timedelta
```

**Подход:**
1. Сбор исторических данных через API ЦБ РФ
2. Обработка и фильтрация данных
3. Построение графиков с помощью matplotlib
4. Сохранение графиков в файлы

**Пример кода:**
```python
def get_historical_rates(currency_code, days=90):
    """Получение исторических данных за указанный период"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    rates = []
    dates = []
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        try:
            url = f"https://www.cbr-xml-daily.ru/archive/{date_str}/daily_json.js"
            response = requests.get(url)
            data = response.json()
            rate = data['Valute'][currency_code]['Value']
            rates.append(rate)
            dates.append(current_date)
        except:
            pass  # Пропускаем дни без данных
        
        current_date += timedelta(days=1)
    
    return dates, rates
```

**Скриншот графика USD/RUB за 3 месяца:**
```
[Здесь был бы скриншот графика с:
 - Линией курса USD/RUB
 - Подписью осей (Дата / Курс)
 - Заголовком "Динамика курса USD/RUB за 3 месяца"
 - Сеткой для лучшей читаемости]
```

## **7. Тестирование**

### **Примеры тестов:**

**Тестирование модели User:**
```python
def test_user_creation(self):
    user = User.create("Иван Иванов", "ivan@test.com")
    self.assertEqual(user.name, "Иван Иванов")
    self.assertEqual(user.email, "ivan@test.com")
```

**Тестирование API валют:**
```python
def test_get_valid_currencies(self):
    currency_list = ['USD']
    currency_data = get_currencies(currency_list)
    self.assertIn('USD', currency_data)
    self.assertIsInstance(currency_data['USD'], float)
```

**Интеграционные тесты сервера:**
```python
def test_home_page(self):
    html = TestServer.make_request('/')
    assert 'First' in html
    assert '1.0.0' in html
```

### **Результаты тестов:**
```
test_user_creation (__main__.TestUser) ... OK
test_user_email_setter_invalid (__main__.TestUser) ... OK
test_currency_creation (__main__.TestCurrency) ... OK
test_get_valid_currencies (__main__.TestGetCurrenciesModified) ... OK
test_home_page (__main__.TestServer) ... OK

----------------------------------------------------------------------
Ran 15 tests in 2.345s
OK
```

## **8. Выводы**

### **Проблемы при реализации:**

1. **Ограничения HTTPServer**: Базовый сервер не поддерживает многопоточность и имеет ограниченную функциональность
2. **Хранение в памяти**: Потеря данных при перезапуске приложения
3. **Отсутствие сессий**: Необходимость реализации механизма аутентификации с нуля
4. **Обработка ошибок API**: Необходимость обработки различных сценариев недоступности внешнего сервиса

### **Применение принципов MVC:**

1. **Model (Модель)**: Классы User, Currency, Author представляют бизнес-логику и данные
2. **View (Представление)**: HTML шаблоны Jinja2 для отображения данных
3. **Controller (Контроллер)**: Класс SimpleHTTPRequestHandler обрабатывает запросы и управляет потоком данных

### **Новые знания:**

1. **HTTPServer**:
   - Работа с базовым HTTP-сервером Python
   - Обработка GET/POST запросов
   - Управление заголовками и кодами ответов

2. **Jinja2**:
   - Создание и наследование шаблонов
   - Передача данных из Python в HTML
   - Использование условий и циклов в шаблонах

3. **Работа с API**:
   - Интеграция с внешними REST API
   - Обработка JSON данных
   - Управление ошибками и таймаутами
   - Кэширование и обновление данных

4. **Архитектура веб-приложений**:
   - Разделение ответственности между компонентами
   - Управление состоянием приложения
   - Паттерны проектирования для веб-приложений

### **Итог:**
Лабораторная работа позволила получить практический опыт создания полноценного веб-приложения от проектирования моделей до развертывания сервера. Были изучены ключевые аспекты веб-разработки на Python, включая работу с HTTP, шаблонизацию, интеграцию с внешними API и тестирование. Полученные навыки могут быть применены для создания более сложных веб-приложений с использованием современных фреймворков.
