import unittest
from unittest.mock import mock_open, patch

# Импортируем ваш функцию
from src.transactions_csv import get_financial_transactions


class TestGetFinancialTransactions(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="id;state;date;amount;currency_name;currency_code;from;to;description"
        "\n1;complete;2023-01-01;100;USD;USD;Alice;Bob;Payment"
        "\n2;pending;2023-02-01;200;EUR;EUR;Alice;Charlie;Transfer"
        "\n",
    )
    @patch("csv.DictReader")
    def test_get_financial_transactions(self, mock_csv_dict_reader, mock_open):
        # Настройка mock для DictReader
        mock_csv_dict_reader.return_value = [
            {
                "id": "1",
                "state": "complete",
                "date": "2023-01-01",
                "amount": "100",
                "currency_name": "USD",
                "currency_code": "USD",
                "from": "Alice",
                "to": "Bob",
                "description": "Payment",
            },
            {
                "id": "2",
                "state": "pending",
                "date": "2023-02-01",
                "amount": "200",
                "currency_name": "EUR",
                "currency_code": "EUR",
                "from": "Alice",
                "to": "Charlie",
                "description": "Transfer",
            },
        ]

        # Проверяем, что функция возвращает правильный массив транзакций
        path = "dummy_path.csv"
        transactions = get_financial_transactions(path)

        expected_transactions = [
            {
                "id": "1",
                "state": "complete",
                "date": "2023-01-01",
                "amount": "100",
                "currency_name": "USD",
                "currency_code": "USD",
                "from": "Alice",
                "to": "Bob",
                "description": "Payment",
            },
            {
                "id": "2",
                "state": "pending",
                "date": "2023-02-01",
                "amount": "200",
                "currency_name": "EUR",
                "currency_code": "EUR",
                "from": "Alice",
                "to": "Charlie",
                "description": "Transfer",
            },
        ]

        self.assertEqual(transactions, expected_transactions)

        # Проверяем, что open вызван с правильным путем
        mock_open.assert_called_once_with(path, mode="r", newline="", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
