import os
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, "data/transactions.json")


class TestLoadTransactions(unittest.TestCase):
    """Класс для тестирования функции load_transactions."""

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "operationAmount": {"amount": "100.00"}}]')
    def test_load_transactions_single_entry(self, mock_open, mock_exists):
        """Тестирование загрузки файла с одной транзакцией."""
        mock_exists.return_value = True  # Настраиваем мок для существования файла

        # Загружаем транзакции
        result = load_transactions("data/transactions.json")

        # Вывод отладочной информации
        print("Result of loading transactions:", result)

        # Проверяем, что результат соответствует ожиданиям
        self.assertEqual(len(result), 1)  # Проверяем количество загруженных транзакций
        self.assertEqual(result[0]["id"], 1)  # Проверяем корректность id
        self.assertEqual(result[0]["operationAmount"]["amount"], "100.00")  # Проверяем корректность amount


if __name__ == "__main__":
    unittest.main()
