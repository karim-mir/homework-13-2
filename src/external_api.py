import logging
import os

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

url = "https://api.apilayer.com/currency_data/convert"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_to_rub(amount: float, currency: str) -> float:
    """
    Функция для конвертации валют в рубли.

    :param amount: Сумма, которую необходимо конвертировать.
    :param currency: Валюта, в которой указана сумма.
    :return: Конвертированная сумма в рублях.
    """
    if currency == "RUB":
        return round(amount, 2)

    if not isinstance(amount, (int, float)) or amount < 0:
        raise ValueError("Сумма должна быть положительным числом.")
    if not isinstance(currency, str):
        raise ValueError("Валюта должна быть строкой.")

    headers = {"apikey": EXCHANGE_API_KEY}
    params = {"amount": amount, "from": currency, "to": "RUB"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "result" not in data:
            logger.error("В ответе API отсутствует поле 'result'.")
            return 0.0

        return round(data["result"], 2)

    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return 0.0


if __name__ == "__main__":
    rub = convert_to_rub(100, "USD")
    print(f"Сумма в рублях: {rub}")
