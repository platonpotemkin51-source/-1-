from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape

from controllers.currencycrud import CurrencyRatesCRUD
from controllers.usercrud import UserCRUD
from controllers.subscriptioncrud import SubscriptionCRUD

from models.app import App
from models.author import Author

from start_and_reset_data import main_2
import urllib.parse

from utils.currencies_api import *


env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

# --- Контроллеры ---
user_crud = UserCRUD()
currency_crud = CurrencyRatesCRUD()
sub_crud = SubscriptionCRUD()


author = Author("Platon Potemkin", "P3122")
app = App("First", "1.0.0", author)


# -------------------------------
#        Route Handlers
# -------------------------------

def index_handler(query):
    currencies_count = len(currency_crud._read())
    users_count = len(user_crud.read_all())

    template = env.get_template("index.html")
    return template.render(
        flag=True,
        app=app,
        currencies_count=currencies_count,
        users_count=users_count
    )

def author_handler(query):
    currencies_count = len(currency_crud._read())
    users_count = len(user_crud.read_all())

    template = env.get_template("index.html")
    return template.render(
        flag=False,
        app=app,
        currencies_count=currencies_count,
        users_count=users_count
    )

def currencies_handler(query):
    currencies = currency_crud._read()
    template = env.get_template("currencies.html")
    return template.render(
        currencies=currencies,
        currencies_count=len(currencies)
    )

def users_handler(query):
    users = user_crud.read_all()
    template = env.get_template("users.html")
    return template.render(
        users=users,
        users_count=len(users)
    )

def currency_update_handler(query):
    currency_crud.update_from_api()
    return redirect("/currencies")

def currency_delete_handler(query):
    if "id" not in query:
        return error_page("Не указан id валюты")

    currency_id = int(query["id"])
    currency_crud._delete(currency_id)

    return redirect("/currencies")

def currency_show_handler(query):
    currencies = currency_crud._read()
    print("==== Currencies ====")
    for c in currencies:
        print(c)
        print('Валюта:', c.name , 'стоит', c.value,'рублей' )
    return redirect("/currencies")

def user_page_handler(query):
    if "id" not in query:
        return error_page("Не указан id пользователя")

    user_id = int(query["id"])
    user = user_crud.read_by_id(user_id)

    if not user:
        return error_page("Пользователь не найден")

    currencies = sub_crud.get_user_subscriptions(user_id)
    sub_string = ", ".join([c.char_code for c in currencies])

    template = env.get_template("user.html")
    return template.render(
        user=user,
        sub=sub_string,
        currencies=currencies
    )

def currency_reset_handler(query):
    main_2()
    return redirect("/currencies")

def subscribe_handler(query, method="GET"):
    """
    Обработчик подписки, работающий с GET и POST
    """
    if "user_id" not in query or "char_code" not in query:
        return error_page("Не хватает параметров user_id или char_code")

    user_id = int(query["user_id"])
    char_code = query["char_code"].upper()

    print(f"[{method}] Подписка: user_id={user_id}, char_code={char_code}")

    cur = currency_crud.find_by_char_code(char_code)
    if not cur:
        return error_page(f"Валюта {char_code} не найдена")

    sub_crud.subscribe(user_id, cur.id)
    return redirect(f"/user?id={user_id}")


# -------------------------------
#       Match Routes
# -------------------------------

ROUTES_GET = {
    "/": index_handler,
    "/author": author_handler,
    "/currencies": currencies_handler,
    "/users": users_handler,
    # "/currency/add": currency_add_handler,
    "/currency/update": currency_update_handler,
    "/currency/delete": currency_delete_handler,
    "/user": user_page_handler,
    "/currency/show": currency_show_handler,
    "/currency/reset": currency_reset_handler,
    "/subscribe": lambda q: subscribe_handler(q, "GET")
}
ROUTES_POST = {
    "/subscribe": lambda q: subscribe_handler(q, "POST"),
}



# -------------------------------
#     HTTP & Routing Engine
# -------------------------------

def redirect(url):
    return ("REDIRECT", url)


def error_page(message):
    return f"<h1>Ошибка</h1><p>{message}</p>"


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # parse path & params
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        query = {k: v[0] for k, v in query.items()}

        # find route
        handler = ROUTES_GET.get(path, None)

        if not handler:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        result = handler(query)

        # redirect
        if isinstance(result, tuple) and result[0] == "REDIRECT":
            self.send_response(302)
            self.send_header("Location", result[1])
            self.end_headers()
            return

        # normal response
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        query = urllib.parse.parse_qs(body)
        query = {k: v[0] for k, v in query.items()}

        handler = ROUTES_POST.get(path, None)

        if not handler:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        result = handler(query)

        if isinstance(result, tuple) and result[0] == "REDIRECT":
            self.send_response(302)
            self.send_header("Location", result[1])
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))


# -------------------------------
#       RUN SERVER
# -------------------------------

if __name__ == "__main__":
    httpd = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
    print("Server is running on http://localhost:8080")
    httpd.serve_forever()
