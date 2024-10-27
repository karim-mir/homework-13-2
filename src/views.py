import os
import json
import requests
from pathlib import Path
from datetime import datetime
from collections import defaultdict

settings_path = os.getenv("SETTINGS_PATH")

# Получаем путь к файлу user_settings.json относительно текущего файла views.py
settings_path = Path(__file__).parent.parent / "user_settings.json"

# Проверка, существует ли файл
if not settings_path.exists():
    raise FileNotFoundError(f"Файл настроек не найден: {settings_path}")

# Загружаем настройки
with open(settings_path, "r") as f:
    user_settings = json.load(f)

# Пример транзакций
transactions = [
    {"date": "2020-05-01", "amount": -17319, "category": "Супермаркеты"},
    {"date": "2020-05-02", "amount": -3324, "category": "Фастфуд"},
    {"date": "2020-05-03", "amount": -2289, "category": "Топливо"},
    {"date": "2020-05-04", "amount": -1850, "category": "Развлечения"},
    {"date": "2020-05-10", "amount": 33000, "category": "Пополнение_BANK007"},
    {"date": "2020-05-15", "amount": 1242, "category": "Проценты_на_остаток"},
]


def filter_transactions(start_date, end_date):
    """Фильтрует транзакции по заданному диапазону дат."""
    return [
        t for t in transactions
        if start_date <= datetime.strptime(t['date'], '%Y-%m-%d') <= end_date
    ]


def calculate_expenses(transactions):
    """Расчет общей суммы расходов и расходов по категориям."""
    total_expenses = -sum(t['amount'] for t in transactions if t['amount'] < 0)
    category_totals = defaultdict(float)

    for t in transactions:
        if t['amount'] < 0:
            category_totals[t['category']] += -t['amount']  # Суммируем только расходы

    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    main_expenses = sorted_categories[:6]
    other_expenses = sum(amount for category, amount in sorted_categories[6:])

    return {
        "total_amount": total_expenses,
        "main": [{"category": category, "amount": amount} for category, amount in main_expenses] +
                [{"category": "Остальное", "amount": other_expenses}]
    }


def get_currency_data():
    """Получает данные о валютных курсах из API."""
    url = f"{os.getenv('CURRENCY_API_URL')}/latest"
    headers = {
        "apikey": os.getenv("CURRENCY_API_KEY"),
    }
    response = requests.get(url, headers=headers).json()
    return [{"currency": currency, "rate": rate} for currency, rate in response.get("rates", {}).items() if
            currency in user_settings["user_currencies"]]


def get_stock_data(symbol):
    """Получает данные о ценах на акции из API."""
    api_key = os.getenv('STOCK_API_KEY')

    url = f"{os.getenv('CURRENCY_API_URL')}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Ошибка API: {response.status_code} - {response.json().get('Error Message', 'Неизвестная ошибка')}")

    try:
        stock_data = response.json().get("Time Series (Daily)", {})
    except ValueError as e:
        raise ValueError(f"Ошибка парсинга JSON: {str(e)}")

    if not stock_data:
        raise ValueError("Ошибка при получении данных акций.")

    latest_date = next(iter(stock_data))
    return [{'stock': symbol, 'price': float(stock_data[latest_date]["4. close"])}]


def generate_report(date_str):
    """Генерирует отчет на основе входной даты."""
    current_date = datetime.strptime(date_str, '%Y-%m-%d')
    start_date = current_date.replace(day=1)
    end_date = current_date

    filtered_transactions = filter_transactions(start_date, end_date)

    expenses = calculate_expenses(filtered_transactions)

    response_data = {
        "expenses": expenses,
        "currency_rates": get_currency_data(),
        "stock_prices": get_stock_data(),
    }

    return response_data
