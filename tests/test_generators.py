import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions, transactions


@pytest.mark.parametrize(
    "currency, expected",
    [
        (
            "USD",
            [
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
                    "id": 142264269,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
            ],
        ),
        (
            "EUR",
            [
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                }
            ],
        ),
        ("GBP", ["Нет значений"]),  # Проверяем, что GBP нет
    ],
)
def test_filter_by_currency(currency, expected):
    result = list(filter_by_currency(transactions, currency))
    assert result == expected


@pytest.fixture
def dir_transaction():
    return [
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
            "id": 142264269,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
            "description": None,  # Описание отсутствует
            "from": "Некоторый источник",
            "to": "Некоторое назначение",
        },
    ]


@pytest.fixture
def expected():
    return ["Перевод организации", "Перевод со счета на счет", "Описание отсутствует"]


def test_transaction_descriptions(dir_transaction, expected):
    descriptions = list(transaction_descriptions(dir_transaction))
    assert descriptions == expected


@pytest.fixture
def card_number_test_data():
    return {
        "start": 1,
        "stop": 5,
        "expected": [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ],
    }


@pytest.fixture
def empty_card_number_test_data():
    return {
        "start": 6,
        "stop": 5,  # Пустой диапазон, старт больше конца
        "expected": [],  # Ожидаемое значение пустой коллекции
    }


# Тест функции генератора
def test_card_number_generator(card_number_test_data):
    start = card_number_test_data["start"]
    stop = card_number_test_data["stop"]
    expected = card_number_test_data["expected"]

    # Генерация номеров карт с помощью генератора
    result = list(card_number_generator(start, stop))

    # Проверка соответствия с ожидаемым значением
    assert result == expected


# Тест пустого диапазона генератора
def test_empty_card_number_generator(empty_card_number_test_data):
    start = empty_card_number_test_data["start"]
    stop = empty_card_number_test_data["stop"]
    expected = empty_card_number_test_data["expected"]

    # Генерация номеров карт с помощью генератора
    result = list(card_number_generator(start, stop))

    # Проверка соответствия с ожидаемым значением
    assert result == expected
