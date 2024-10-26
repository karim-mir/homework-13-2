from typing import Dict, Generator, List, Union

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {},  # Пустая транзакция
    {
        "id": 142264269,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]


def filter_by_currency(transactions: List[Dict], currency: str) -> Generator[Union[Dict, str], None, None]:
    """Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной"""
    found = False  # Флаг для отслеживания найденных транзакций
    for operation_in_transaction in transactions:
        if (
            operation_in_transaction
            and operation_in_transaction.get("operationAmount", {}).get("currency", {}).get("name") == currency
        ):
            found = True
            yield operation_in_transaction

    if not found:
        yield "Нет значений"  # Возвращаем строку, если ничего не найдено


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""
    # Проверяем, если список пустой
    if not transactions:
        yield "Нет значений"

    for transaction in transactions:
        if not transaction:  # Проверяем пустую транзакцию
            yield "Описание отсутствует"
            continue

        description = transaction.get("description")
        yield description if description else "Описание отсутствует"


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор, который выдает номера банковских карт в формате: XXXX XXXX XXXX XXXX."""
    for number in range(start, stop + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[
            8:12
        ] + " " + f"{number:016d}"[12:]
