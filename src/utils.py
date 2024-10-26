import json
import logging
import os
from typing import Dict, List

# Создаем хэндлер
handler = logging.FileHandler("logs.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s:%(module)s:%(levelname)s:%(name)s:%(message)s")
handler.setFormatter(formatter)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, handlers=[handler])

logger = logging.getLogger()

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, "data/transactions.json")


def load_transactions(path: str) -> List[Dict]:
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях"""

    logger.info("Запуск операции...")
    # Проверяем на существование файла
    if not os.path.exists(path):
        logger.error("Файл не найден.")
        return []

    logger.info("Начало загрузки данных")

    # Открываем файл по переданному пути
    with open(path, "r", encoding="utf-8") as file:
        try:
            # Загружаем данные JSON
            data_operations = json.load(file)
            logger.info("Данные успешно загружены: %s", str(data_operations))  # Отладочный вывод
        except json.JSONDecodeError:
            logger.error("Неподдерживаемый формат данных")
            return []

    # Проверяем, является ли загруженный объект списком
    if not isinstance(data_operations, list):
        logger.error("Загруженные данные не являются списком.")
        return []

    valid_transactions = []  # Список для хранения валидных транзакций

    # Проходим по всем транзакциям в загруженных данных
    for transaction in data_operations:
        # Проверяем, что транзакция является словарем и содержит необходимые поля
        if isinstance(transaction, dict) and "id" in transaction and "operationAmount" in transaction:
            # Проверяем, что id является целым числом, а amount (из вложенного словаря) - числом
            if isinstance(transaction["id"], int):
                amount_str = transaction["operationAmount"].get("amount")
                if isinstance(amount_str, str) and amount_str.replace(".", "", 1).isdigit():
                    valid_transactions.append(transaction)  # Добавляем валидную транзакцию в список

    logger.info("Валидные транзакции загружены: %s", str(valid_transactions))
    return valid_transactions  # Возвращаем валидные транзакции


if __name__ == "__main__":
    transactions = load_transactions(path)
    print("Полученные транзакции:", transactions)  # Выводим загруженные транзакции
