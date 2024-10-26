import re
from typing import Dict, List


def filter_by_transactions(transactions: List[Dict[str, any]], search_term: str) -> List[Dict[str, any]]:
    """
    Фильтрует список банковских операций по заданной строке поиска.

    :param transactions: Список словарей, каждый из которых содержит данные о банковской операции.
    :param search_term: Строка для поиска в описаниях операций.
    :return: Список словарей, в которых описание содержит строку поиска.
    """
    if not isinstance(transactions, list):
        raise ValueError("transactions должна быть списка словарей")

    # Компилируем регулярное выражение для поиска, игнорируя регистр
    pattern = re.compile(search_term, re.IGNORECASE)

    # Фильтруем транзакции, оставляя только те, у которых описание соответствует паттерну
    filtered_transactions = [
        transaction
        for transaction in transactions
        if isinstance(transaction, dict) and pattern.search(transaction.get("description", ""))
    ]

    return filtered_transactions


# Пример использования функции
transactions = [
    {"id": 1, "description": "Покупка продуктов", "amount": 150},
    {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
    {"id": 3, "description": "Покупка электроники", "amount": 300},
]

# Фильтруем транзакции, ищем 'покупка'
try:
    result = filter_by_transactions(transactions, "покупка")
    print(result)
except ValueError as e:
    print(f"Ошибка: {e}")
