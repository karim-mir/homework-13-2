import re


def filter_transactions(transactions, search_string):
    """
    Фильтрует список банковских операций по заданной строке поиска.

    :param transactions: Список словарей, каждый из которых содержит данные о банковской операции.
    :param search_string: Строка для поиска в описаниях операций.
    :return: Список словарей, в которых описание содержит строку поиска.
    """

    # Компилируем регулярное выражение для поиска, игнорируя регистр
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтруем транзакции, оставляя только те, у которых описание соответствует паттерну
    filtered_transactions = [
        transaction
        for transaction in transactions
        if pattern.search(transaction.get("description", ""))
    ]

    return filtered_transactions


# Пример использования функции
transactions = [
    {"id": 1, "description": "Покупка продуктов", "amount": 150},
    {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
    {"id": 3, "description": "Покупка электроники", "amount": 300},
]

# Фильтруем транзакции, ищем 'покупка'
result = filter_transactions(transactions, "покупка")
print(
    result
)
