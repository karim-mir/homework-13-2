import csv
import os
from typing import Dict, List

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, "data/transactions.csv")


def get_financial_transactions(path: str) -> List[Dict]:
    """Функция принимает путь к файлу CSV в качестве аргумента и выдает список словарей с транзакциями"""
    transactions = []
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")  # Указываем ; как разделитель
        for row in reader:
            transactions.append(row)
            print(
                row["id"],
                row["state"],
                row["date"],
                row["amount"],
                row["currency_name"],
                row["currency_code"],
                row["from"],
                row["to"],
                row["description"],
            )
    return transactions


if __name__ == "__main__":
    transactions = get_financial_transactions(path)
    print(transactions)
