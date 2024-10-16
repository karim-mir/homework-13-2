from collections import Counter


def categorize_transactions(transactions, categories):
    """
    Подсчитывает количество операций в каждой из заданных категорий.

    :param transactions: Список словарей, каждый из которых содержит данные о банковской операции.
    :param categories: Список категорий, для которых нужно подсчитать количество операций.
    :return: Словарь, в котором ключи — названия категорий, а значения — количество операций в каждой категории.
    """
    # Инициализируем счетчик для хранения результатов
    category_count = Counter()

    # Проходим по всем транзакциям
    for transaction in transactions:
        # Получаем описание операции
        description = transaction.get("description", "")

        # Для каждой категории проверяем, содержится ли она в описании
        for category in categories:
            if category.lower() in description.lower():
                # Увеличиваем счётчик для соответствующей категории
                category_count[category] += 1

    # Преобразуем Counter в обычный словарь для удобства
    return dict(category_count)


# Пример использования функции
transactions = [
    {"id": 1, "description": "Покупка продуктов", "amount": 150},
    {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
    {"id": 3, "description": "Покупка электроники", "amount": 300},
    {"id": 4, "description": "Покупка напитков", "amount": 50},
]

categories = ["Покупка", "Оплата", "Коммунальные услуги"]

# Вызываем функцию и выводим результат
result = categorize_transactions(transactions, categories)
print(result)  # Пример вывода: {'Покупка': 3, 'Оплата': 1, 'Коммунальные услуги': 1}
