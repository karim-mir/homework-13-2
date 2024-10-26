import functools


def log(filename):
    """
    Декоратор для логирования вызовов функции.

    Параметры:
    filename (str): Имя файла, в который будут записываться логи вызовов функции.

    Возвращает:
    function: Обернутая функция с добавленным функционалом логирования.

    Логирование включает:
    - Запись имени функции, переданных аргументов и возвращаемого значения при успешном выполнении.
    - Запись информации об ошибке, если возникает исключение, включая имя функции и переданные аргументы.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                with open(filename, "a") as file:
                    file.write(f"Запуск функции: {func.__name__} с аргументами: {args}, {kwargs}\n")
                    file.write(f"Функция: {func.__name__} вернула: {result}\n")
                return result
            except Exception as e:
                with open(filename, "a") as file:
                    file.write(f"Ошибка в функции: {func.__name__} с аргументами: {args}, {kwargs}\n")
                raise e

        return wrapper

    return decorator
