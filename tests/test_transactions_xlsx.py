import unittest
from unittest.mock import MagicMock, patch

# Импортируем тестируемую функцию
from src.transactions_xlsx import get_financial_transactions_operations


class TestFinancialTransactions(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_get_financial_transactions_operations(self, mock_read_excel):
        # Создаем фейковые данные для теста
        fake_data = [
            {
                "id": 1,
                "state": "completed",
                "date": "2023-01-01",
                "amount": 100,
                "currency_name": "USD",
                "currency_code": "USD",
                "from": "Alice",
                "to": "Bob",
                "description": "Payment for services",
            },
            {
                "id": 2,
                "state": "pending",
                "date": "2023-01-02",
                "amount": 200,
                "currency_name": "EUR",
                "currency_code": "EUR",
                "from": "Charlie",
                "to": "Dave",
                "description": "Refund",
            },
        ]

        # Настраиваем mock, чтобы он возвращал фейковые данные
        mock_read_excel.return_value = MagicMock()
        mock_read_excel.return_value.iterrows.return_value = [(i, row) for i, row in enumerate(fake_data)]

        # Вызываем функцию
        operations = get_financial_transactions_operations("fake_path")

        # Проверяем, что возвращаемые операции соответствуют фейковым данным
        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0]["id"], 1)
        self.assertEqual(operations[0]["state"], "completed")
        self.assertEqual(operations[1]["id"], 2)
        self.assertEqual(operations[1]["state"], "pending")
        self.assertEqual(operations[1]["currency_name"], "EUR")

    @patch("pandas.read_excel")
    def test_get_financial_transactions_operations_empty(self, mock_read_excel):
        # Проверяем случай с пустым файлом
        mock_read_excel.return_value = MagicMock()
        mock_read_excel.return_value.iterrows.return_value = []

        # Вызываем функцию
        operations = get_financial_transactions_operations("fake_path")

        # Проверяем, что возвращаемый список операций пуст
        self.assertEqual(operations, [])


if __name__ == "__main__":
    unittest.main()
