from flask import Flask, jsonify, request
from datetime import datetime
import logging
from dotenv import load_dotenv
from src.views import get_currency_data, get_stock_data

load_dotenv()
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Корневой маршрут
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Financial API!"

@app.route("/currency", methods=["GET"])
def currency():
    try:
        currency_data = get_currency_data()
        return jsonify(currency_data), 200
    except Exception as e:
        logging.error("Error fetching currency data: %s", e)
        return jsonify({"error": "Failed to fetch currency data: CURRENCY_API_URL is not set in the environment variables."}), 500

@app.route("/stock/<string:symbol>", methods=["GET"])
def stock(symbol):
    try:
        stock_data = get_stock_data(symbol)
        return jsonify(stock_data), 200
    except Exception as e:
        logging.error("Error fetching stock data: %s", e)
        return jsonify({"error": "Failed to fetch stock data: " + str(e)}), 500

# Пример данных о картах
cards = [
    {"number": "1234567812345814", "expenses": [1200, 62]},
    {"number": "9876543210987512", "expenses": [7.94]}
]

# Пример транзакций
transactions = [
    {"date": "2021-12-21", "amount": 1198.23, "category": "Переводы", "description": "Перевод Кредитная карта. ТП 10.2 RUR"},
    {"date": "2021-12-20", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
]

def get_greeting(current_time):
    if current_time.hour < 6:
        return "Доброй ночи"
    elif current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"

def calculate_cashback(expenses):
    return sum(expenses) / 100  # 1 рубль на каждые 100 рублей

def get_top_transactions():
    return sorted(transactions, key=lambda x: x["amount"], reverse=True)[:5]

@app.route("/api/data", methods=["GET"])
def get_data():
    date_time_str = request.args.get("date_time")
    if not date_time_str:
        return jsonify({"error": "Date and time string is required"}), 400

    try:
        current_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

    greeting = get_greeting(current_time)

    # Получение информации по картам
    card_info = []
    for card in cards:
        last4 = card["number"][-4:]  # последние 4 цифры карты
        total_spent = sum(card["expenses"])  # Общая сумма расходов
        cashback = calculate_cashback(card["expenses"])  # Кэшбэк
        card_info.append({"last_digits": last4, "total_spent": round(total_spent, 2), "cashback": round(cashback, 2)})

    top_transactions = get_top_transactions()

    # Получение курсов валют и цен акций
    try:
        currency_rates = get_currency_data()  # Получение данных о курсах валют
        stock_prices = [
            get_stock_data("AAPL"),  # Пример получения данных по акции Apple
            get_stock_data("AMZN"),  # Пример получения данных по акции Amazon
            get_stock_data("GOOGL"),  # Пример получения данных по акции Google
            get_stock_data("MSFT"),  # Пример получения данных по акции Microsoft
            get_stock_data("TSLA"),  # Пример получения данных по акции Tesla
        ]
    except Exception as e:
        logging.error("Error fetching stock data or currency rate: %s", e)
        return jsonify({"error": "Failed to fetch stock price or currency rate: " + str(e)}), 500

    return jsonify({
        "greeting": greeting,
        "cards": card_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    })

if __name__ == "__main__":
    app.run(debug=True)
