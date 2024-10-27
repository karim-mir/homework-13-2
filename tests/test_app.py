import unittest
import os
from unittest.mock import patch
from flask import json
from dotenv import load_dotenv
from src.app import app
from src.views import get_stock_data, get_currency_data

# Загружаем переменные окружения перед запуском тестов
load_dotenv()

class TestApp(unittest.TestCase):
    """Тестовый класс для проверки функций в приложении Flask."""

    def setUp(self):
        """Настройка тестов."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """Тестирование корневого маршрута."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Welcome to the Financial API!")

    @patch.dict(os.environ, {"CURRENCY_API_URL": "https://api.example.com", "CURRENCY_API_KEY": "mock_currency_key"})
    @patch("src.views.get_currency_data")
    def test_currency_success(self, mock_get_currency_data):
        """Тестирование успешного получения данных о валюте."""
        mock_get_currency_data.return_value = [
            {"currency": "USD", "rate": 1.0},
            {"currency": "EUR", "rate": 0.85}
        ]

        response = self.app.get("/currency")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn({"currency": "USD", "rate": 1.0}, data)
        self.assertIn({"currency": "EUR", "rate": 0.85}, data)

    @patch("src.views.get_currency_data")
    def test_currency_error(self, mock_get_currency_data):
        """Тестирование обработки ошибок при получении данных о валюте."""
        # Здесь вызываем исключение, которое приложение ожидает от функции
        mock_get_currency_data.side_effect = Exception("CURRENCY_API_URL is not set in the environment variables.")

        response = self.app.get("/currency")
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Failed to fetch currency data: CURRENCY_API_URL is not set in the environment variables.")

    @patch.dict(os.environ, {"STOCK_API_KEY": "mock_stock_key"})
    @patch("src.views.get_stock_data")
    def test_stock_success(self, mock_get_stock_data):
        """Тестирование успешного получения данных о запасах."""
        # Устанавливаем ожидаемое значение
        mock_get_stock_data.return_value = {"symbol": "AAPL", "price": 231.41}
        response = self.app.get("/stock/AAPL")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {"symbol": "AAPL", "price": 231.41})

    @patch("src.views.get_stock_data")
    def test_stock_error(self, mock_get_stock_data):
        """Тестирование обработки ошибок при получении данных о запасах."""
        # Здесь вызываем исключение, которое ваше приложение ожидает от функции
        mock_get_stock_data.side_effect = ValueError("STOCK_API_KEY is not set in the environment variables.")

        response = self.app.get("/stock/INVALID")
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Failed to fetch stock data: STOCK_API_KEY is not set in the environment variables.")

if __name__ == "__main__":
    unittest.main()
