# основной модуль программы
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author
from models import User
from models import CurrencyManager
import urllib.parse

from http.server import HTTPServer, BaseHTTPRequestHandler


current_user = None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        global current_user

        if self.path == '/':
            # Главная страница - показываем валюты в зависимости от авторизации
            if current_user:
                currencies = CurrencyManager.get_subscribed_currencies(current_user['id'])
                title = "Мои подписки"
            else:
                currencies = CurrencyManager.get_all_currencies()
                title = "Все валюты"

            template = env.get_template("index.html")
            result = template.render(
                title=title,
                currencies=currencies,
                current_user=current_user,
                CurrencyManager=CurrencyManager  # ДОБАВЛЯЕМ CurrencyManager в контекст
            )

        elif self.path == '/all-currencies':
            # Страница со всеми валютами
            currencies = CurrencyManager.get_all_currencies()
            template = env.get_template("currencies.html")
            result = template.render(
                title="Все валюты",
                currencies=currencies,
                current_user=current_user,
                show_subscribe_buttons=True,
                CurrencyManager=CurrencyManager  # ДОБАВЛЯЕМ здесь тоже
            )

        elif self.path == '/my-currencies':
            # Страница с подписанными валютами
            if not current_user:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return

            currencies = CurrencyManager.get_subscribed_currencies(current_user['id'])
            template = env.get_template("currencies.html")
            result = template.render(
                title="Мои валюты",
                currencies=currencies,
                current_user=current_user,
                show_unsubscribe_buttons=True,
                CurrencyManager=CurrencyManager  # ДОБАВЛЯЕМ здесь тоже
            )

        elif self.path.startswith('/subscribe/'):
            # Подписка на валюту
            if not current_user:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return

            currency_code = self.path.split('/')[-1].upper()
            if CurrencyManager.subscribe_currency(current_user['id'], currency_code):
                print(f"Пользователь {current_user['email']} подписался на {currency_code}")

            # Возвращаем на ту же страницу, откуда пришли
            referer = self.headers.get('Referer', '/')
            self.send_response(302)
            self.send_header('Location', referer)
            self.end_headers()
            return

        elif self.path.startswith('/unsubscribe/'):
            # Отписка от валюты
            if not current_user:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return

            currency_code = self.path.split('/')[-1].upper()
            if CurrencyManager.unsubscribe_currency(current_user['id'], currency_code):
                print(f"Пользователь {current_user['email']} отписался от {currency_code}")

            # Возвращаем на ту же страницу, откуда пришли
            referer = self.headers.get('Referer', '/')
            self.send_response(302)
            self.send_header('Location', referer)
            self.end_headers()
            return

        elif self.path == '/register':
            template = env.get_template("register.html")
            result = template.render()
        elif self.path == '/login':
            template = env.get_template("login.html")
            result = template.render()
        elif self.path == '/logout':
        #    global current_user
            current_user = None
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        #result = "<html><h1>Hello, world!</h1></html>"
        self.wfile.write(bytes(result, "utf-8"))


    def do_POST(self):
        global current_user

        if self.path == '/register':
            # получаем данные
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            # преобразовываем данные
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            # распределяем данные
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]
            name = data.get('name', [''])[0]

            if User.user_exists(email):
                template = env.get_template("register.html")
                result = template.render(error="Пользователь с таким email уже существует")
            else:
                new_user = User.create_user(name, email, password)
                current_user = {
                    'id': new_user.id,
                    'name': new_user.name,
                    'email': new_user.email
                }
                print(f"Успешная регистрация и авторизация: {email}")

                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

        elif self.path == '/login':
            # получаем данные
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            # преобразовываем данные
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            # распределяем данные
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]

            user = User.authenticate(email, password)

            if user:
                current_user = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
                print(f"Успешный вход: {email}")

                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            else:
                template = env.get_template("login.html")
                result = template.render(error="Неверный email или пароль")

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))

# main_author = Author('Platon Potemkin')
# print(main_author)
# #print(main_author.name, main_author.group)
# main_author.group = "P3122"
# #print(main_author.name, main_author.group)



env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

# template = env.get_template("index.html")

# result = template.render(title="Currensies",
#                 author=main_author.name,
#                 content=f"Группа: {main_author.group}",
#                          navigation=[{"caption": "Главная",
#                                       "href":"https://itmo.ru"
#                                       },],)

httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('Server is running on http://localhost:8080')
httpd.serve_forever()