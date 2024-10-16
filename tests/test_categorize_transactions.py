import unittest
from collections import Counter


def categorize_transactions(transactions, categories):
    """Подсчитывает количество операций в каждой из заданных категориях."""
    category_count = Counter()

    for transaction in transactions:
        description = transaction.get("description", "")
        for category in categories:
            if category.lower() in description.lower():
                category_count[category] += 1

    # Инициализируем нули для категорий, если они не встречаются в счетчике
    for category in categories:
        if category not in category_count:
            category_count[category] = 0

    return dict(category_count)


class TestCategorizeTransactions(unittest.TestCase):

    def setUp(self):
        """Создаем тестовые данные для каждого теста."""
        self.transactions = [
            {"id": 1, "description": "Покупка продуктов", "amount": 150},
            {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
            {"id": 3, "description": "Покупка электроники", "amount": 300},
            {"id": 4, "description": "Покупка напитков", "amount": 50},
        ]
        self.categories = ["Покупка", "Оплата", "Коммунальные услуги"]

    def test_categorize_transactions_correct_count(self):
        """Тестируем подсчет транзакций для заданных категорий."""
        result = categorize_transactions(self.transactions, self.categories)
        expected_result = {"Покупка": 3, "Оплата": 1, "Коммунальные услуги": 0}
        self.assertEqual(result, expected_result)

    def test_categorize_transactions_no_matches(self):
        """Тестируем случай, если нет совпадений с категориями."""
        result = categorize_transactions(self.transactions, ["Нет таких категорий"])
        expected_result = {"Нет таких категорий": 0}
        self.assertEqual(result, expected_result)

    def test_categorize_transactions_empty_transactions(self):
        """Тестируем случай с пустым списком транзакций."""
        result = categorize_transactions([], self.categories)
        expected_result = {"Покупка": 0, "Оплата": 0, "Коммунальные услуги": 0}
        self.assertEqual(result, expected_result)

    def test_categorize_transactions_case_insensitivity(self):
        """Тестируем фильтрацию с учетом регистра."""
        result = categorize_transactions(self.transactions, ["покупка", "оплата"])
        expected_result = {"покупка": 3, "оплата": 1}
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
