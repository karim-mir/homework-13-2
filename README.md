
# Банковские транзакции

Этот модуль предоставляет функции для загрузки, фильтрации и категоризации банковских транзакций. Он включает в себя операции с различными форматами данных (JSON, CSV, XLSX) и позволяет фильтровать и группировать транзакции по статусам и категориям.

## Функции

### *filter_transactions(transactions, status)*

Функция фильтрует список транзакций по заданному статусу.

Параметры:
- *transactions (list)*: Список транзакций, где каждая транзакция представлена как словарь.
- *status (str)*: Статус транзакции для фильтрации (например, *"EXECUTED", "CANCELED", "PENDING"*).

Возвращает:
- *(list)*: Список транзакций, соответствующих заданному статусу.

Пример использования:
```
transactions = [
{"id": 1, "description": "Покупка продуктов", "status": "EXECUTED"},
{"id": 2, "description": "Оплата коммунальных услуг", "status": "CANCELED"},
]

filtered = filter_transactions(transactions, "EXECUTED")
print(filtered) # [{'id': 1, 'description': 'Покупка продуктов', 'status': 'EXECUTED'}]
```

### *categorize_transactions(transactions, categories)*

Функция подсчитывает количество операций для каждой из заданных категорий.

Параметры:
- *transactions (list)*: Список транзакций, где каждая транзакция представлена как словарь.
- *categories (list)*: Список категорий для подсчета транзакций.<br><br><strong>Возвращает:
- *(dict)*: Словарь с категориями в качестве ключей и количеством транзакций в каждой категории в качестве значений.

Пример использования:

```commandline
transactions = [
{"id": 1, "description": "Покупка продуктов", "amount": 150},
{"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
]

categories = ["Покупка", "Оплата"]
result = categorize_transactions(transactions, categories)
print(result) # {'Покупка': 1, 'Оплата': 1}
```

## Тестирование  

Функции *filter_transactions* и *categorize_transactions* имеют тесты, написанные с использованием библиотеки *unittest*.

### Запуск тестов
1. Убедитесь, что у вас установлены необходимые зависимости, такие как *pandas*
2. Сохраните тесты в файл, например, *test_banking.py*
3. Выполните команду в командной строке:
```commandline
python -m unittest test_banking.py
```
### Пример тестов<br><br>Пример теста для функции *filter_transactions*

```commandline
def test_filter_transactions(self):
transactions = [
{"id": 1, "description": "Покупка продуктов", "status": "EXECUTED"},
{"id": 2, "description": "Оплата коммунальных услуг", "status": "CANCELED"},
]
result = filter_transactions(transactions, "EXECUTED")
expected = [
{"id": 1, "description": "Покупка продуктов", "status": "EXECUTED"}
]
self.assertEqual(result, expected)
```
## Заключение
Этот модуль может помочь в управлении банковскими транзакциями, предоставляя простые в использовании функции для фильтрации и категоризации.