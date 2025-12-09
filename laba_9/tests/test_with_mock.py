import unittest
from unittest.mock import MagicMock, patch

from controllers.usercrud import UserCRUD
from controllers.currencycrud import CurrencyRatesCRUD
from models.user import User
from models.currency import Currency


# ============================================================
#                  TESTS FOR USER CRUD
# ============================================================

class TestUserCRUD(unittest.TestCase):

    def setUp(self):
        self.crud = UserCRUD("test.db")

    def test_create_user(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.lastrowid = 1
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            user = self.crud.create("Ivan", "ivan@example.com")

        mock_cursor.execute.assert_called_with(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Ivan", "ivan@example.com")
        )
        mock_conn.commit.assert_called_once()

        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Ivan")
        self.assertEqual(user.email, "ivan@example.com")

    def test_read_all_users(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchall.return_value = [
            (1, "Ivan", "ivan@example.com")
        ]
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            users = self.crud.read_all()

        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], User)
        self.assertEqual(users[0].email, "ivan@example.com")

    def test_read_by_id_found(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchone.return_value = (1, "Ivan", "ivan@example.com")
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            user = self.crud.read_by_id(1)

        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Ivan")

    def test_read_by_id_not_found(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            user = self.crud.read_by_id(999)

        self.assertIsNone(user)

    def test_delete_user(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            self.crud.delete(5)

        mock_cursor.execute.assert_called_with(
            "DELETE FROM users WHERE id=?", (5,)
        )
        mock_conn.commit.assert_called_once()


# ============================================================
#              TESTS FOR CURRENCY CRUD
# ============================================================

class TestCurrencyCRUD(unittest.TestCase):

    def setUp(self):
        self.crud = CurrencyRatesCRUD("test.db")

    def test_create_currency(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value = mock_cursor

        # Currency __init__ принимает 6 аргументов:
        # id, num_code, char_code, name, value, nominal
        currency = Currency(None, "840", "USD", "US Dollar", 92.5, 1)

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            self.crud.create(currency)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    def test_read_all_currencies(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchall.return_value = [
            (1, "840", "USD", "US Dollar", 92.5, 1)
        ]
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            currencies = self.crud._read()

        self.assertEqual(len(currencies), 1)
        self.assertIsInstance(currencies[0], Currency)
        self.assertEqual(currencies[0].char_code, "USD")

    def test_find_by_char_code(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # find_by_char_code использует Currency(*row)
        mock_cursor.fetchone.return_value = (
            1, "840", "USD", "US Dollar", 92.5, 1
        )
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            cur = self.crud.find_by_char_code("usd")

        self.assertEqual(cur.char_code, "USD")

    def test_delete_currency(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            self.crud._delete(7)

        mock_cursor.execute.assert_called_with(
            "DELETE FROM currencies WHERE id=?", (7,)
        )
        mock_conn.commit.assert_called_once()

    @patch("utils.currencies_api.get_all_currencies_data")
    def test_update_from_api(self, mock_api):
        mock_api.return_value = [{
            "num_code": "840",
            "char_code": "USD",
            "name": "US Dollar",
            "value": 100.55,
            "nominal": 1
        }]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # валюта уже есть -> UPDATE
        mock_cursor.fetchone.return_value = (1,)
        mock_conn.cursor.return_value = mock_cursor

        with patch.object(self.crud, "_connect", return_value=mock_conn):
            result = self.crud.update_from_api()

        self.assertTrue(result)
        self.assertTrue(mock_cursor.execute.called)
