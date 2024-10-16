import re
import unittest


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


class TestFilterTransactions(unittest.TestCase):

    def setUp(self):
        """Создаем тестовые данные для каждого теста."""
        self.transactions = [
            {"id": 1, "description": "Покупка продуктов", "amount": 150},
            {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
            {"id": 3, "description": "Покупка электроники", "amount": 300},
            {"id": 4, "description": "Обслуживание автомобиля", "amount": 200},
        ]

    def test_filter_transactions_case_insensitive(self):
        """Тестируем фильтрацию с учетом регистра."""
        result = filter_transactions(self.transactions, "покупка")
        expected_result = [
            {"id": 1, "description": "Покупка продуктов", "amount": 150},
            {"id": 3, "description": "Покупка электроники", "amount": 300},
        ]
        self.assertEqual(result, expected_result)

    def test_filter_transactions_no_matches(self):
        """Тестируем случай, если нет совпадений."""
        result = filter_transactions(self.transactions, "нет такого слова")
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_filter_transactions_partial_match(self):
        """Тестируем частичное совпадение."""
        result = filter_transactions(self.transactions, "обслуживание")
        expected_result = [
            {"id": 4, "description": "Обслуживание автомобиля", "amount": 200},
        ]
        self.assertEqual(result, expected_result)

    def test_filter_transactions_empty_string(self):
        """Тестируем случай фильтрации с пустой строкой поиска."""
        result = filter_transactions(self.transactions, "")
        expected_result = self.transactions  # Все транзакции должны быть возвращены
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
