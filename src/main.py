import os
from typing import Dict, List

from src.filter_transactions import filter_by_transactions
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.transactions_csv import get_financial_transactions
from src.transactions_xlsx import get_financial_transactions_operations
from src.utils import load_transactions

# Пути к файлам
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "data/transactions.json")
excel_path = os.path.join(base_dir, "data/transactions_excel.xlsx")
csv_path = os.path.join(base_dir, "data/transactions.csv")


def print_transactions(transactions: List[Dict[str, any]]):
    if transactions:
        print(f"Всего банковских операций в выборке: {len(transactions)}")
        for transaction in transactions:
            if isinstance(transaction, dict):
                print(
                    f"{transaction.get('date', 'Дата отсутствует')} "
                    f"{transaction.get('description', 'Описание отсутствует')}"
                )
                amount = transaction.get("amount", "Сумма отсутствует")
                currency_code = transaction.get("currency_code", "Код валюты отсутствует")
                print(f"Сумма: {amount} {currency_code}")
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


def get_transaction_choice():
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из Excel-файла")
    print("3. Получить информацию о транзакциях из CSV-файла")
    choice = input("Пользователь: ")
    return choice


def process_transactions(choice: str):
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return load_transactions(json_path)
    elif choice == "2":
        print("Для обработки выбран Excel-файл.")
        return get_financial_transactions_operations(excel_path)
    elif choice == "3":
        print("Для обработки выбран CSV-файл.")
        return get_financial_transactions(csv_path)
    else:
        print("Неверный выбор.")
        return None


def filter_transactions_by_state(transactions):
    while True:
        status = input("Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): ").upper()
        filtered_transactions = filter_by_state(transactions, status)

        if filtered_transactions:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return filtered_transactions
        else:
            print(f'Статус операции "{status}" недоступен.')


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    choice = get_transaction_choice()
    transactions = process_transactions(choice)

    if transactions is None:
        return

    filtered_transactions = filter_transactions_by_state(transactions)

    # Сортировка по дате
    sort_decision = input("Программа: Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_decision == "да":
        order = input("Программа: Отсортировать по возрастанию или по убыванию? ").strip().lower()

        # Преобразуем ввод пользователя в boolean
        if order == "возрастанию":
            reverse = False
        elif order == "убыванию":
            reverse = True
        else:
            print("Неверный ввод. Сортировка не выполнена.")
            return

        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    # Фильтрация по валюте
    currency_decision = input("Программа: Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if currency_decision == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    # Дополнительная фильтрация по описанию
    description_decision = (
        input("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    )
    if description_decision == "да":
        search_term = input("Введите слово для поиска: ")
        filtered_transactions = filter_by_transactions(filtered_transactions, search_term)

    print("Распечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":
    main()
