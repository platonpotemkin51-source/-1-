from jinja2 import Environment, PackageLoader, select_autoescape
from models import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from utils.currencies_api import *
from controllers.currencycrud import *
from controllers.usercrud import *
from controllers.subscriptioncrud import *



current_user = None

user_crud = UserCRUD()
currency_crud = CurrencyRatesCRUD()
sub_crud = SubscriptionCRUD()



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global current_user
        author = Author("Platon Potemkin", "P3122")
        app = App("First", "1.0.0", author)

        path = self.path.split("?")[0]
        query = {}
        if "?" in self.path:
            params = self.path.split("?")[1]
            for kv in params.split("&"):
                k, v = kv.split("=")
                query[k] = v

        result = ""

        if self.path == '/':
            flag = True
            currencies_count = len(currency_crud._read())
            users_count = len(user_crud.read_all())

            template = env.get_template("index.html")
            result = template.render(
                flag=flag,
                app=app,
                currencies_count=currencies_count,
                users_count=users_count,
            )


        elif self.path == '/author':
            flag = False
            currencies_count = len(currency_crud._read())
            users_count = len(user_crud.read_all())

            template = env.get_template("index.html")
            result = template.render(
                app=app,
                currencies_count=currencies_count,
                users_count=users_count,
            )

        elif self.path == '/currencies':
            currencies= currency_crud._read()
            currencies_count = len(currencies)
            template = env.get_template("currencies.html")
            result = template.render(
                currencies=currencies,
                currencies_count=currencies_count
            )
        elif self.path == '/users':
            users = user_crud.read_all()
            users_count = len(users)
            template = env.get_template("users.html")
            result = template.render(
                users=users,
                users_count=users_count
            )

        elif self.path == '/currency/update':
            print("Успено обновились")
            currency_crud.update_from_api()
            self.send_response(302)
            self.send_header('Location', '/currencies')
            self.end_headers()
            return

        elif path == '/currency/show':
            currencies = currency_crud._read()
            print("==== Currencies ====")
            for c in currencies:
                print('ID:', c.id,'Number:', c.num_code,'Cahr:', c.char_code,'Name:', c.name,'Value:', c.value,'Nominal:', c.nominal)
            self.send_response(302)
            self.send_header('Location', '/currencies')
            self.end_headers()
            return

        for i in currency_crud._read():
            if self.path == f'/currency/delete={i.id}':
                currency_crud._delete(i.id)
                currencies = currency_crud._read()
                currencies_count = len(currencies)
                template = env.get_template("currencies.html")
                result = template.render(
                    currencies=currencies,
                    currencies_count=currencies_count
                )



        # elif self.path == '/currency/delete' and "id" in query:
        #     currency_crud._delete(int(query["id"]))
        #     self.send_response(302)
        #     self.send_header('Location', '/currencies')
        #     self.end_headers()
        #     return

        # elif self.path == '/user' and "id" in query:
        #     user_id = int(query["id"])
        #     user = user_crud.read_by_id(user_id)
        #     currencies = sub_crud.get_user_subscriptions(user_id)
        #     k=[]
        #     sub = ''
        #     for j in currencies:
        #         k.append(j.char_code)
        #         sub = ', '.join(k)
        #
        #     template = env.get_template("user.html")
        #     result = template.render(
        #         sub=sub,
        #         user=user,
        #         subscriptions=currencies
        #     )


        for i in user_crud.read_all():
            if self.path == f'/user?id={i.id}':
                user= i
                k=[]
                currencies = sub_crud.get_user_subscriptions(i.id)
                for j in currencies:
                    k.append(j.char_code)
                sub = ', '.join(k)
                template = env.get_template("user.html")
                result = template.render(
                    sub=sub,
                    user=user,
                    currencies=currencies
            )




        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))















    #
    # def do_POST(self):
    #     global current_user
    #
    #     if self.path == '/register':
    #         content_length = int(self.headers['Content-Length'])
    #         post_data = self.rfile.read(content_length)
    #         data = urllib.parse.parse_qs(post_data.decode('utf-8'))
    #
    #         email = data.get('email', [''])[0]
    #         password = data.get('password', [''])[0]
    #         name = data.get('name', [''])[0]
    #
    #         if User.user_exists(email):
    #             template = env.get_template("register.html")
    #             result = template.render(error="Пользователь с таким email уже существует")
    #         else:
    #             new_user = User.create_user(name, email, password)
    #             current_user = {
    #                 'id': new_user.id,
    #                 'name': new_user.name,
    #                 'email': new_user.email
    #             }
    #             print(f"Успешная регистрация и авторизация: {email}")
    #
    #             self.send_response(302)
    #             self.send_header('Location', '/')
    #             self.end_headers()
    #             return
    #
    #     elif self.path == '/login':
    #         content_length = int(self.headers['Content-Length'])
    #         post_data = self.rfile.read(content_length)
    #         data = urllib.parse.parse_qs(post_data.decode('utf-8'))
    #
    #         email = data.get('email', [''])[0]
    #         password = data.get('password', [''])[0]
    #
    #         user = User.authenticate(email, password)
    #
    #         if user:
    #             current_user = {
    #                 'id': user.id,
    #                 'name': user.name,
    #                 'email': user.email
    #             }
    #             print(f"Успешный вход: {email}")
    #
    #             self.send_response(302)
    #             self.send_header('Location', '/')
    #             self.end_headers()
    #             return
    #         else:
    #             template = env.get_template("login.html")
    #             result = template.render(error="Неверный email или пароль")
    #
    #     self.send_response(200)
    #     self.send_header('Content-Type', 'text/html; charset=utf-8')
    #     self.end_headers()
    #     self.wfile.write(bytes(result, "utf-8"))
    #

env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)


# В самом конце main.py
if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    httpd.serve_forever()

