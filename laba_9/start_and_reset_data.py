import os
from controllers.databasecontroller import DatabaseController
from utils.currencies_api import get_all_currencies_data

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
    {"name": "Старожилов Аркадий", "email": "star_ar@mail.com"},
    {"name": "Лукьянов Александр", "email": "lukaki@mail.com"},
    {"name": "Аветисян Владислав", "email": "avet@mail.com"},
    {"name": "Пузиков Ярослав", "email": "yarei@mail.com"},
    {"name": "Потёмкин Платон", "email": "spbsvu3skype2@mail.com"}
]


# ------------------------------
# MAIN
# ------------------------------

def main_2():
    if os.path.exists("database.db"):
        os.remove("database.db")

    db_controller = DatabaseController("database.db")

    db_controller.insert_users(test_users)
    db_controller.insert_currencies(get_all_currencies_data())
    db_controller.insert_currencies_const(get_all_currencies_data())
    db_controller.insert_subscriptions(test_user_subscriptions)
    # db_controller.insert_all_currencies(get_all_currencies_data())

    print("🎉 database.db полностью заполнена!")


if __name__ == "__main_2__":
    main_2()