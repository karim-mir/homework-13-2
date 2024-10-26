import os
from typing import Dict, List

import pandas as pd

# Путь к файлу
base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, "data/transactions_excel.xlsx")


def get_financial_transactions_operations(path: str) -> List[Dict]:
    """Функция для считывания финансовых операций из Excel принимает путь к файлу Excel в качестве аргумента
    и выдает список словарей с транзакциями"""
    # Чтение Excel файла в DataFrame
    df = pd.read_excel(path)
    operations = []

    for index, row in df.iterrows():
        # Создаем словарь для каждой строки и добавляем его в список операций
        operation = {
            "id": row["id"],
            "state": row["state"],
            "date": row["date"],
            "amount": row["amount"],
            "currency_name": row["currency_name"],
            "currency_code": row["currency_code"],
            "from": row["from"],
            "to": row["to"],
            "description": row["description"],
        }
        operations.append(operation)
        # Выводим информацию о транзакции
        print(
            operation["id"],
            operation["state"],
            operation["date"],
            operation["amount"],
            operation["currency_name"],
            operation["currency_code"],
            operation["from"],
            operation["to"],
            operation["description"],
        )

    return operations


if __name__ == "__main__":
    operations = get_financial_transactions_operations(path)
