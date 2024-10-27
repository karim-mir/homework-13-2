import os
import json
import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.views import (
    filter_transactions,
    calculate_expenses,
    get_currency_data,
    get_stock_data,
    generate_report
)

# Пример транзакций для тестирования
transactions = [
    {"date": "2020-05-01", "amount": -17319, "category": "Супермаркеты"},
    {"date": "2020-05-02", "amount": -3324, "category": "Фастфуд"},
    {"date": "2020-05-03", "amount": -2289, "category": "Топливо"},
    {"date": "2020-05-04", "amount": -1850, "category": "Развлечения"},
    {"date": "2020-05-10", "amount": 33000, "category": "Пополнение_BANK007"},
    {"date": "2020-05-15", "amount": 1242, "category": "Проценты_на_остаток"},
]

class TestViews(unittest.TestCase):
    """Тестовый класс для проверки функций во views модуля."""

    @patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
    @patch("os.getenv", side_effect=lambda x: {"CURRENCY_API_URL": "https://api.example.com",
                                                "CURRENCY_API_KEY": "test-key",
                                                "STOCK_API_KEY": "test-stock-key"}.get(x))
    def test_get_currency_data(self, mock_getenv, mock_open):
        """Тестирование функции get_currency_data.

        Проверяет, что функция корректно извлекает данные о валютах и возвращает их
        в правильном формате. Использует мокированные данные для эмуляции API.
        """
        with patch("requests.get") as mock_requests:
            mock_requests.return_value.json.return_value = {
                "rates": {
                    "USD": 1.0,
                    "EUR": 0.85,
                    "GBP": 0.75
                }
            }
            currency_data = get_currency_data()
            self.assertEqual(len(currency_data), 2)
            self.assertIn({"currency": "USD", "rate": 1.0}, currency_data)
            self.assertIn({"currency": "EUR", "rate": 0.85}, currency_data)

    @patch("requests.get")
    @patch("os.getenv", side_effect=lambda key: {
        "CURRENCY_API_URL": "https://api.example.com",
        "CURRENCY_API_KEY": "test-key",
        "STOCK_API_KEY": "test-stock-key"
    }.get(key))
    def test_get_stock_data(self, mock_getenv, mock_requests):
        """Тестирование функции get_stock_data."""

        # Верная структура ответа для успешного запроса
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            "Time Series (Daily)": {
                "2023-10-01": {
                    "1. open": "145.30",
                    "2. high": "147.25",
                    "3. low": "144.20",
                    "4. close": "150.00"
                }
            }
        }

        stock_data = get_stock_data("AAPL")
        self.assertEqual(stock_data, [{'stock': 'AAPL', 'price': 150.00}])  # Проверяем стандартный формат

        # Проверка на неверный символ
        mock_requests.return_value.status_code = 404
        mock_requests.return_value.json.return_value = {"Error Message": "Invalid Symbol"}

        with self.assertRaises(ValueError) as context:
            get_stock_data("INVALID")

        self.assertEqual(str(context.exception), "Ошибка API: 404 - Invalid Symbol")  # Проверка текста ошибки

        # Проверка на случай, если API возвращает некорректный JSON
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.side_effect = ValueError("Invalid JSON")

        with self.assertRaises(ValueError) as context:
            get_stock_data("AAPL")

        self.assertEqual(str(context.exception), "Ошибка парсинга JSON: Invalid JSON")  # Проверка текста ошибки


    def test_filter_transactions(self):
        """Тестирование функции filter_transactions.

        Проверяет, что функция правильно фильтрует транзакции по заданному диапазону дат.
        """
        start_date = datetime.strptime("2020-05-01", "%Y-%m-%d")
        end_date = datetime.strptime("2020-05-03", "%Y-%m-%d")
        result = filter_transactions(start_date, end_date)
        self.assertEqual(len(result), 3)

    def test_calculate_expenses(self):
        """Тестирование функции calculate_expenses.

        Проверяет, что функция правильно рассчитывает общие расходы
        и возвращает ожидаемую структуру данных.
        """
        expenses = calculate_expenses(transactions)
        self.assertEqual(expenses["total_amount"], 24782)  # Обновите значение здесь
        self.assertEqual(len(expenses["main"]), 5)  # Проверьте на количество основных категорий
        self.assertIn({"category": "Супермаркеты", "amount": 17319}, expenses["main"])

    @patch("src.views.get_currency_data", return_value=[])
    @patch("src.views.get_stock_data", return_value={})
    def test_generate_report(self, mock_get_currency_data, mock_get_stock_data):
        """Тестирование функции generate_report.

        Проверяет, что функция генерирует отчет с ожидаемыми данными,
        включая расходы, курсы валют и цены акций.
        """
        report = generate_report("2020-05-01")
        self.assertIn("expenses", report)
        self.assertIn("currency_rates", report)
        self.assertIn("stock_prices", report)

if __name__ == "__main__":
    unittest.main()
