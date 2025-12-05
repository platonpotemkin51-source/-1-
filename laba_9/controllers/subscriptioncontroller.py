from controllers.subscriptioncrud import SubscriptionCRUD
from controllers.usercrud import UserCRUD
from controllers.currencycrud import CurrencyRatesCRUD


class SubscriptionController:
    """
    Контроллер для управления подписками пользователей на валюты.

    Атрибуты:
        sub_crud (SubscriptionCRUD): CRUD для работы с подписками.
        user_crud (UserCRUD): CRUD для работы с пользователями.
        curr_crud (CurrencyRatesCRUD): CRUD для работы с валютами.

    Методы:
        list_subscriptions() -> dict:
            Возвращает словарь, где ключи — объекты пользователей,
            а значения — список объектов валют, на которые они подписаны.

        subscribe_user_to_currency(user_id: int, currency_id: int):
            Подписывает пользователя на валюту.

        unsubscribe_user_from_currency(user_id: int, currency_id: int):
            Отписывает пользователя от валюты.

    Формат возвращаемых данных:

        Пример list_subscriptions():
        {
            User(id=1, name="Иван Иванов", email="ivan@example.com"): [
                Currency(num_code="840", char_code="USD", name="US Dollar", value=92.5, nominal=1),
                Currency(num_code="978", char_code="EUR", name="Euro", value=101.2, nominal=1)
            ],
            User(id=2, name="Мария Петрова", email="maria@example.com"): [
                Currency(num_code="643", char_code="RUB", name="Russian Ruble", value=1.0, nominal=1)
            ]
        }

    Примеры использования:
        >>> controller = SubscriptionController()
        >>> subscriptions = controller.list_subscriptions()
        >>> for user, currencies in subscriptions.items():
        ...     print(user.name, [c.char_code for c in currencies])
        Иван Иванов ['USD', 'EUR']
        Мария Петрова ['RUB']

        >>> controller.subscribe_user_to_currency(user_id=1, currency_id=3)
        >>> controller.unsubscribe_user_from_currency(user_id=2, currency_id=1)
    """

    def __init__(self):
        self.sub_crud = SubscriptionCRUD()
        self.user_crud = UserCRUD()
        self.curr_crud = CurrencyRatesCRUD()

    def list_subscriptions(self):
        """
        Возвращает все подписки пользователей на валюты.

        :return: dict, где ключи — объекты пользователей (User),
                 а значения — список объектов валют (Currency)
        """
        result = {}
        users = self.user_crud.read_all()
        for user in users:
            currencies_data = self.sub_crud.get_user_subscriptions(user.id)
            currencies = []
            for c in currencies_data:
                # c = (id, char_code, name, value)
                currency_obj = self.curr_crud.find_by_char_code(c[1])
                if currency_obj:
                    currencies.append(currency_obj)
            result[user] = currencies
        return result

    def subscribe_user_to_currency(self, user_id: int, currency_id: int):
        """
        Подписывает пользователя на валюту.

        :param user_id: int, ID пользователя
        :param currency_id: int, ID валюты
        """
        self.sub_crud.subscribe(user_id, currency_id)

    def unsubscribe_user_from_currency(self, user_id: int, currency_id: int):
        """
        Отписывает пользователя от валюты.

        :param user_id: int, ID пользователя
        :param currency_id: int, ID валюты
        """
        self.sub_crud.unsubscribe(user_id, currency_id)
