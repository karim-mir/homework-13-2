import csv
import json
import unittest
from unittest.mock import mock_open, patch

import pandas as pd

# Здесь предполагается, что ваши функции определены в модуле my_module
# from my_module import load_json, load_csv, load_xlsx, filter_transactions


def load_json(file_path):
    """Загружает данные из JSON-файла."""
    with open(file_path, "r") as file:
        return json.load(file)


def load_csv(file_path):
    """Загружает данные из CSV-файла."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_xlsx(file_path):
    """Загружает данные из XLSX-файла."""
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")


def filter_transactions(transactions, status):
    """Фильтрует список транзакций по указанному статусу."""
    return [
        transaction
        for transaction in transactions
        if transaction.get("status", "").lower() == status.lower()
    ]


class TestBankingFunctions(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"id": 1, "status": "EXECUTED"}]',
    )
    def test_load_json(self, mock_file):
        result = load_json("fake_path.json")
        expected = [{"id": 1, "status": "EXECUTED"}]
        self.assertEqual(result, expected)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="id,description,amount\n1,Покупка,150\n2,Оплата,75\n",
    )
    def test_load_csv(self, mock_file):
        result = load_csv("fake_path.csv")
        expected = [
            {"id": "1", "description": "Покупка", "amount": "150"},
            {"id": "2", "description": "Оплата", "amount": "75"},
        ]
        self.assertEqual(result, expected)

    @patch("pandas.read_excel")
    def test_load_xlsx(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame(
            {"id": [1, 2], "status": ["EXECUTED", "PENDING"]}
        )
        result = load_xlsx("fake_path.xlsx")
        expected = [{"id": 1, "status": "EXECUTED"}, {"id": 2, "status": "PENDING"}]
        self.assertEqual(result, expected)

    def test_filter_transactions(self):
        transactions = [
            {"id": 1, "description": "Покупка продуктов", "status": "EXECUTED"},
            {"id": 2, "description": "Оплата коммунальных услуг", "status": "CANCELED"},
            {"id": 3, "description": "Покупка", "status": "EXECUTED"},
        ]
        result = filter_transactions(transactions, "EXECUTED")
        expected = [
            {"id": 1, "description": "Покупка продуктов", "status": "EXECUTED"},
            {"id": 3, "description": "Покупка", "status": "EXECUTED"},
        ]
        self.assertEqual(result, expected)

    def test_filter_transactions_no_matches(self):
        transactions = [
            {"id": 1, "description": "Покупка продуктов", "status": "EXECUTED"},
            {"id": 2, "description": "Оплата коммунальных услуг", "status": "CANCELED"},
        ]
        result = filter_transactions(transactions, "PENDING")
        expected = []
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
