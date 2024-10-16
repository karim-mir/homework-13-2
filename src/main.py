import csv
import json

import pandas as pd


def load_json(file_path):
    """Загружает данные из JSON-файла."""
    with open(file_path, "r") as file:
        return json.load(file)


def load_csv(file_path):
    """Загружает данные из CSV-файла."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_xlsx(file_path):
    """Загружает данные из XLSX-файла."""
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")


def filter_transactions(transactions, status):
    """Фильтрует список транзакций по указанному статусу."""
    return [
        transaction
        for transaction in transactions
        if transaction.get("status", "").lower() == status.lower()
    ]


def main():
    """Основная функция, связывающая все функциональности."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_json(file_path)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = load_csv(file_path)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = load_xlsx(file_path)
    else:
        print("Ошибка: Неверный выбор. Пожалуйста, попробуйте еще раз.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING: "
        )
        if status.upper() in valid_statuses:
            break
        else:
            print("Статус операции ", status, "недоступен.")

    print(f"Операции отфильтрованы по статусу '{status}'")
    filtered_transactions = filter_transactions(transactions, status)

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    sort_by_date = (
        input("Отсортировать операции по дате? Да/Нет: ").strip().lower() == "да"
    )
    if sort_by_date:
        sort_order = (
            input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        )
        if sort_order == "по возрастанию":
            filtered_transactions.sort(key=lambda x: x["date"])
        elif sort_order == "по убыванию":
            filtered_transactions.sort(key=lambda x: x["date"], reverse=True)

    show_rubles_only = (
        input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower() == "да"
    )
    if show_rubles_only:
        filtered_transactions = [
            t for t in filtered_transactions if t.get("currency", "") == "RUB"
        ]

    filter_by_description = (
        input(
            "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
        )
        .strip()
        .lower()
        == "да"
    )
    if filter_by_description:
        keyword = input("Введите слово для фильтрации: ")
        filtered_transactions = [
            t
            for t in filtered_transactions
            if keyword.lower() in t.get("description", "").lower()
        ]

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        print("\n", transaction["date"], transaction["description"])
        print("Счет **", transaction["account"])
        print("Сумма: ", transaction["amount"], transaction["currency"])


if __name__ == "__main__":
    main()
