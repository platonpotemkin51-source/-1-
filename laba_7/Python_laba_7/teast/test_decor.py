import unittest
import io
import math
import logging
from typing import Any, Callable, Optional
import functools
from logger import logger
from func import get_currencies, solve_quadratic


class TestLoggerDecorator(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

    def test_successful_call_logs_correctly(self):
        """Тест: успешный вызов → логи INFO с аргументами и результатом"""

        @logger(handle=self.stream)
        def square(x):
            return x * x

        result = square(5)

        logs = self.stream.getvalue()
        self.assertEqual(result, 25)
        self.assertIn("[INFO] Calling square(5)", logs)
        self.assertIn("[INFO] square returned 25", logs)

    def test_value_warning_negative_discriminant(self):
        """Тест: solve_quadratic с D < 0 → [WARNING] и проброс исключения"""

        @logger(handle=self.stream)
        def test_func():
            return solve_quadratic(1, 0, 1)  # x² + 1 = 0 → D = -4

        with self.assertRaises(ValueError) as cm:
            test_func()

        self.assertIn("Дискриминант отрицательный", str(cm.exception))

        logs = self.stream.getvalue()
        self.assertIn("[WARNING]", logs)
        self.assertIn("Дискриминант отрицательный", logs)

    def test_value_critical_a_zero_b_zero(self):
        """Тест: a=0, b=0 → [CRITICAL] и проброс исключения"""

        @logger(handle=self.stream)
        def test_func():
            return solve_quadratic(0, 0, 5)

        with self.assertRaises(ValueError) as cm:
            test_func()

        self.assertIn("Оба коэффициента a и b равны нулю", str(cm.exception))

        logs = self.stream.getvalue()
        self.assertIn("[CRITICAL]", logs)
        self.assertIn("Оба коэффициента", logs)

    def test_general_exception_logs_error(self):
        """Тест: произвольное исключение → [ERROR] и проброс"""

        @logger(handle=self.stream)
        def faulty_func():
            return solve_quadratic("abc", 1, 2)

        with self.assertRaises(TypeError) as context:
            faulty_func()

        self.assertIn("Коэффициент 'a' должен быть числом",
                      str(context.exception))

        logs = self.stream.getvalue()
        self.assertIn("[ERROR]", logs)
        self.assertIn("Коэффициент 'a' должен быть числом", logs)


# --- Пример из (6.3) ---
class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

        # Поддельная функция вместо get_currencies, чтобы не зависеть от сети
        @logger(handle=self.stream)
        def wrapped():
            raise ConnectionError("Failed to connect to currency API")

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
