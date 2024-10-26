import unittest

from src.filter_transactions import filter_by_transactions


class TestFilterTransactions(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового набора транзакций перед каждым тестом."""
        self.transactions = [
            {"id": 1, "description": "Покупка продуктов", "amount": 150},
            {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
            {"id": 3, "description": "Покупка электроники", "amount": 300},
            {"id": 4, "description": "Продажа мебели", "amount": 500},
        ]

    def test_filter_transactions_case_insensitive(self):
        """Тестирует фильтрацию транзакций с учетом регистра (без учета регистра).
        Проверяет, что оба варианта совпадений 'покупка' возвращают правильные результаты.
        """
        result = filter_by_transactions(self.transactions, "покупка")
        self.assertEqual(len(result), 2)  # Ожидаем 2 совпадения
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[1]["id"], 3)

    def test_filter_transactions_no_results(self):
        """Тестирует фильтрацию транзакций, когда нет совпадений.
        Проверяет, что фильтрация по строке, которой нет в описаниях, возвращает пустой список.
        """
        result = filter_by_transactions(self.transactions, "нет запросов")
        self.assertEqual(len(result), 0)  # Ожидаем 0 совпадений

    def test_filter_transactions_partial_match(self):
        """Тестирует фильтрацию транзакций с частичным совпадением.
        Проверяет, что фильтрация по части описания возвращает только те транзакции, которые соответствуют.
        """
        result = filter_by_transactions(self.transactions, "Коммунальных")
        self.assertEqual(len(result), 1)  # Ожидаем 1 совпадение
        self.assertEqual(result[0]["id"], 2)

    def test_filter_transactions_invalid_type(self):
        """Тестирует поведение функции при предоставлении неверного типа данных.
        Проверяет, что функция генерирует ValueError, когда передан неверный тип данных.
        """
        with self.assertRaises(ValueError) as context:
            filter_by_transactions("это не список", "покупка")
        self.assertEqual(str(context.exception), "transactions должна быть списка словарей")

    def test_filter_transactions_empty_list(self):
        """Тестирует фильтрацию пустого списка транзакций.
        Проверяет, что функция возвращает пустой список, когда входной список пуст.
        """
        result = filter_by_transactions([], "покупка")
        self.assertEqual(len(result), 0)  # Ожидаем 0 совпадений

    def test_filter_transactions_with_non_dict_elements(self):
        """Тестирует фильтрацию списка транзакций, содержащего не-словари.
        Проверяет, что функция игнорирует неправильные элементы и возвращает те, что являются словарями.
        """
        mixed_transactions = [
            {"id": 1, "description": "Покупка продуктов", "amount": 150},
            "Неправильный элемент",
            {"id": 2, "description": "Оплата коммунальных услуг", "amount": 75},
        ]
        result = filter_by_transactions(mixed_transactions, "покупка")
        self.assertEqual(len(result), 1)  # Ожидаем 1 совпадение (с словарем)
        self.assertEqual(result[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
