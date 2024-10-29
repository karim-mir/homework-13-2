import os
import json
import unittest
from unittest import mock
from datetime import datetime
from src.views import (
    filter_transactions,
    calculate_expenses,
    get_currency_data,
    get_stock_data,
    generate_report,
)


class FinancialAppTestCase(unittest.TestCase):

    def setUp(self):
        self.user_settings = {"user_currencies": ["USD", "EUR"]}
        with open("user_settings.json", "w") as f:
            json.dump(self.user_settings, f)

        os.environ["CURRENCY_API_URL"] = "https://api.exchangeratesapi.io"
        os.environ["CURRENCY_API_KEY"] = "test_api_key"
        os.environ["STOCK_API_KEY"] = "test_stock_api_key"

        # Определяем транзакции здесь
        self.transactions = [
            {"date": "2020-05-01", "amount": -17319, "category": "Супермаркеты"},
            {"date": "2020-05-02", "amount": -3324, "category": "Фастфуд"},
            {"date": "2020-05-03", "amount": -2289, "category": "Топливо"},
            {"date": "2020-05-04", "amount": -1850, "category": "Развлечения"},
            {"date": "2020-05-10", "amount": 33000, "category": "Пополнение_BANK007"},
            {"date": "2020-05-15", "amount": 1242, "category": "Проценты_на_остаток"},
        ]

    def tearDown(self):
        try:
            os.remove("user_settings.json")
        except FileNotFoundError:
            pass

    def test_filter_transactions(self):
        start_date = datetime.strptime("2020-05-01", "%Y-%m-%d")
        end_date = datetime.strptime("2020-05-10", "%Y-%m-%d")
        filtered = filter_transactions(start_date, end_date)
        self.assertEqual(len(filtered), 5)  # 5 транзакций попадает в этот диапазон

    def test_calculate_expenses(self):
        result = calculate_expenses(self.transactions)
        self.assertEqual(result["total_amount"], 17319 + 3324 + 2289 + 1850)
        self.assertGreater(len(result["main"]), 0)  # Должно быть хотя бы одна категория расходов

    @mock.patch("requests.get")
    def test_get_currency_data(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85, "GBP": 0.75}}
        mock_get.return_value = mock_response

        currencies = get_currency_data()
        self.assertEqual(len(currencies), 2)  # Должны быть только USD и EUR в user_settings

    @mock.patch("requests.get")
    def test_get_stock_data_success(self, mock_get):
        symbol = "AAPL"
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Time Series (Daily)": {"2024-10-27": {"4. close": "150.00"}}}
        mock_get.return_value = mock_response

        stock_data = get_stock_data(symbol)
        self.assertEqual(stock_data[0]["stock"], "AAPL")
        self.assertEqual(stock_data[0]["price"], 150.00)

    @mock.patch("requests.get")
    def test_get_stock_data_not_found(self, mock_get):
        symbol = "AAPL"
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"Time Series (Daily)": {}}
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            get_stock_data(symbol)

        self.assertEqual(
            str(context.exception), "Ошибка парсинга JSON: Ошибка парсинга JSON: данные акций не найдены."
        )

    @mock.patch("requests.get")
    def test_generate_report(self, mock_get):
        # Имитация валютных данных
        mock_response_currency = mock.Mock()
        mock_response_currency.json.return_value = {
            "rates": {
                "USD": 1.0,
                "EUR": 0.85,
            }
        }
        mock_get.side_effect = [mock_response_currency]

        # Имитация данных акций
        symbol = "AAPL"
        mock_response_stock = mock.Mock()
        mock_response_stock.status_code = 200
        mock_response_stock.json.return_value = {"Time Series (Daily)": {"2024-10-27": {"4. close": "150.00"}}}
        mock_get.side_effect = [mock_response_currency, mock_response_stock]

        # Передаем символ акций
        report = generate_report("2024-10-01", symbol)
        self.assertIn("expenses", report)
        self.assertIn("currency_rates", report)
        self.assertIn("stock_prices", report)
        self.assertEqual(report["stock_prices"][0]["stock"], "AAPL")
        self.assertEqual(report["stock_prices"][0]["price"], 150.00)


if __name__ == "__main__":
    unittest.main()
