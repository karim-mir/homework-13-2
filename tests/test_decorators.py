import os

import pytest

from src.decorators import log


# Удаление файла журнала после выполнения теста
@pytest.fixture
def clean_up():
    """Фикстура для удаления файла журнала после выполнения тестов.

    Эта фикстура используется для обеспечения чистоты перед тестами.
    Перед выполнением теста ничего не делает, но после выполнения
    теста проверяет, существует ли файл `test_log.txt` и
    удаляет его, если он существует.
    """
    yield
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")


@log("test_log.txt")
def divide(x, y):
    """Выполняет деление двух чисел.

    Параметры:
        x (float): Числитель.
        y (float): Знаменатель.

    Возвращает:
        float: Результат деления.

    Исключения:
        ZeroDivisionError: Если y равно нулю.
    """
    return x / y


def test_log_written_to_file(clean_up):
    """Тестирует сохранение логов после успешного выполнения функции.

    Убедитесь, что лог-файл создается, и логи корректно
    записываются при успешном вызове функции divide.
    """
    divide(10, 2)

    # Подождите некоторое время или проверяйте существование файла
    assert os.path.exists("test_log.txt"), "Файл журнала не создан."

    with open("test_log.txt", "r") as file:
        logs = file.readlines()

    assert any(
        "Запуск функции: divide с аргументами: (10, 2), {}" in log for log in logs
    ), "Логи выполнения не найдены."
    assert any("Функция: divide вернула: 5.0" in log for log in logs), "Логи результата не найдены."


def test_log_error(clean_up):
    """Тестирует логирование ошибок при возникновении исключения.

    Проверяет, что функция divide выбрасывает исключение
    ZeroDivisionError и что соответствующая запись логируется
    в файл.
    """
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open("test_log.txt", "r") as file:
        logs = file.readlines()

    assert any("Ошибка в функции: divide с аргументами: (10, 0), {}" in log for log in logs)
