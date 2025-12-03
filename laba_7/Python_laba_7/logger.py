import functools
import logging
import sys
from typing import Any, Callable, Optional


def logger(func: Optional[Callable] = None,
           *,
           handle: Any = sys.stdout) -> Callable:
    """
    Параметризуемый декоратор для логирования вызовов функций.

    Args:
        func: Декорируемая функция (используется при вызове без скобок)
        handle: Объект для логирования (sys.stdout, файл, StringIO или logging.Logger)

    Returns:
        Декорированная функция
    """

    def decorator(original_func: Callable) -> Callable:
        print(f"decorated func: {func}, {handle}")

        @functools.wraps(original_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Определяем способ логирования
            is_logger = isinstance(handle, logging.Logger)

            # Формируем информацию о вызове
            func_name = original_func.__name__
            args_repr = [repr(arg) for arg in args]
            kwargs_repr = [
                f"{key}={repr(value)}" for key, value in kwargs.items()
            ]
            signature = ", ".join(args_repr + kwargs_repr)

            # Логируем начало вызова
            start_message = f"Calling {func_name}({signature})"

            if is_logger:
                handle.info(start_message)
            else:
                handle.write(f"[INFO] {start_message}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()

            try:
                # Выполняем функцию
                result = original_func(*args, **kwargs)

                # Логируем успешное завершение
                success_message = f"{func_name} returned {repr(result)}"

                if is_logger:
                    handle.info(success_message)
                else:
                    handle.write(f"[INFO] {success_message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()

                return result

            except ValueError as e:
                # Для квадратного уравнения: дискриминант < 0
                error_message = f"{func_name} raised ValueError: {str(e)}"

                if is_logger:
                    if "Дискриминант отрицательный" in str(e):
                        handle.warning(
                            error_message
                        )  # WARNING для отрицательного дискриминанта
                    elif "Оба коэффициента" in str(e):
                        handle.critical(
                            error_message
                        )  # CRITICAL для полностью невозможной ситуации
                    else:
                        handle.error(error_message)
                else:
                    if "Дискриминант отрицательный" in str(e):
                        handle.write(f"[WARNING] {error_message}\n")
                    elif "Оба коэффициента" in str(e):
                        handle.write(f"[CRITICAL] {error_message}\n")
                    else:
                        handle.write(f"[ERROR] {error_message}\n")

                    if hasattr(handle, 'flush'):
                        handle.flush()

                raise

            except Exception as e:
                # Логируем ошибку
                error_message = f"{func_name} raised {type(e).__name__}: {str(e)}"

                if is_logger:
                    handle.error(error_message)
                else:
                    handle.write(f"[ERROR] {error_message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()

                # Повторно выбрасываем исключение
                raise

        return wrapper

    # Обработка случаев @logger, @logger(), @logger(handle=...)
    if func is None:
        # Был вызван как @logger() или @logger(handle=...)
        return decorator
    else:
        # Был вызван как @logger (без скобок)
        return decorator(func)
