import os
import unittest
from unittest.mock import patch

from src.main import get_transaction_choice, main, print_transactions, process_transactions


class TestPrintTransactions(unittest.TestCase):
    @patch("builtins.print")
    def test_print_transactions_with_data(self, mock_print):
        transactions = [
            {"date": "2023-01-01", "description": "Purchase", "amount": 100.0, "currency_code": "USD"},
            {"date": "2023-01-02", "description": "Withdrawal", "amount": 50.0, "currency_code": "EUR"},
        ]
        print_transactions(transactions)
        # Проверяем, что первый вызов print был правильным
        mock_print.assert_any_call("Всего банковских операций в выборке: 2")
        # Проверяем, что информация о первой транзакции выведена правильно
        mock_print.assert_any_call("2023-01-01 Purchase")
        mock_print.assert_any_call("Сумма: 100.0 USD")
        # Проверяем, что информация о второй транзакции выведена правильно
        mock_print.assert_any_call("2023-01-02 Withdrawal")
        mock_print.assert_any_call("Сумма: 50.0 EUR")

        @patch("builtins.print")
        def test_print_transactions_empty(self, mock_print):
            transactions = []
            print_transactions(transactions)

            # Проверяем, что выводится правильное сообщение для пустого списка
            mock_print.assert_called_once_with(
                "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации."
            )


class TestGetTransactionChoice(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1"])  # Имитация ввода пользователя
    def test_get_transaction_choice(self, mock_input, mock_print):
        choice = get_transaction_choice()

        # Проверка, что функция возвращает правильный выбор
        self.assertEqual(choice, "1")

        # Проверка, что выводится правильный текст
        mock_print.assert_any_call("Выберите необходимый пункт меню:")
        mock_print.assert_any_call("1. Получить информацию о транзакциях из JSON-файла")
        mock_print.assert_any_call("2. Получить информацию о транзакциях из Excel-файла")
        mock_print.assert_any_call("3. Получить информацию о транзакциях из CSV-файла")

    @patch("builtins.print")
    @patch("src.main.load_transactions")
    def test_process_transactions_json(self, mock_load_transactions, mock_print):
        # Устанавливаем ожидаемое возвратное значение
        mock_load_transactions.return_value = [{"date": "2023-01-01", "amount": 100.0}]

        # Формируем путь к файлу transactions.json так же, как это сделано в функции
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.normpath(os.path.join(base_dir, "src", "data", "transactions.json"))

        # Вызов функции, которую мы тестируем
        result = process_transactions("1")

        # Проверяем, что функция была вызвана с правильным аргументом
        actual_path = mock_load_transactions.call_args[0][0]
        self.assertEqual(os.path.normpath(actual_path), json_path, "Пути не совпадают!")

        # Проверка вывода
        mock_print.assert_called_once_with("Для обработки выбран JSON-файл.")

        # Проверка возвращаемого результата
        self.assertEqual(result, [{"date": "2023-01-01", "amount": 100.0}])

    @patch("builtins.print")
    @patch("src.main.get_financial_transactions_operations")
    def test_process_transactions_xlsx(self, mock_load_transactions, mock_print):
        # Устанавливаем ожидаемое возвратное значение
        mock_load_transactions.return_value = [{"date": "2023-01-01", "amount": 100.0}]

        # Формируем путь к файлу transactions.xlsx так же, как это сделано в функции
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xlsx_path = os.path.normpath(os.path.join(base_dir, "src", "data", "transactions_excel.xlsx"))

        # Вызов функции, которую мы тестируем
        result = process_transactions("2")

        # Проверяем, что функция была вызвана с правильным аргументом
        actual_path = mock_load_transactions.call_args[0][0]
        self.assertEqual(os.path.normpath(actual_path), xlsx_path, "Пути не совпадают!")

        # Проверка вывода
        mock_print.assert_called_once_with("Для обработки выбран Excel-файл.")

        # Проверка возвращаемого результата
        self.assertEqual(result, [{"date": "2023-01-01", "amount": 100.0}])

    @patch("builtins.print")
    @patch("src.main.get_financial_transactions")
    def test_process_transactions_csv(self, mock_load_transactions, mock_print):
        # Устанавливаем ожидаемое возвратное значение
        mock_load_transactions.return_value = [{"date": "2023-01-01", "amount": 100.0}]

        # Формируем путь к файлу transactions.json так же, как это сделано в функции
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.normpath(os.path.join(base_dir, "src", "data", "transactions.csv"))

        # Вызов функции, которую мы тестируем
        result = process_transactions("3")

        # Проверяем, что функция была вызвана с правильным аргументом
        actual_path = mock_load_transactions.call_args[0][0]
        self.assertEqual(os.path.normpath(actual_path), csv_path, "Пути не совпадают!")

        # Проверка вывода
        mock_print.assert_called_once_with("Для обработки выбран CSV-файл.")

        # Проверка возвращаемого результата
        self.assertEqual(result, [{"date": "2023-01-01", "amount": 100.0}])


class TestMainFunction(unittest.TestCase):

    @patch(
        "builtins.input",
        side_effect=[
            "1",  # Выбор транзакции
            "да",  # Сортировать по дате
            "возрастанию",  # Порядок сортировки
            "да",  # Фильтровать по рублевым транзакциям
            "да",  # Дополнительная фильтрация
            "тест",  # Слово для поиска в описании
        ],
    )
    @patch("src.main.process_transactions")
    @patch("src.main.filter_transactions_by_state")
    @patch("src.main.sort_by_date")
    @patch("src.main.filter_by_currency")
    @patch("src.main.filter_by_transactions")
    @patch("src.main.print_transactions")
    def test_main_successful_flow(
        self,
        mock_print_transactions,
        mock_filter_by_transactions,
        mock_filter_by_currency,
        mock_sort_by_date,
        mock_filter_transactions_by_state,
        mock_process_transactions,
        mock_input,
    ):

        # Настроим ожидания
        mock_process_transactions.return_value = [{"id": 1, "description": "тест транзакция", "currency": "RUB"}]
        mock_filter_transactions_by_state.return_value = [
            {"id": 1, "description": "тест транзакция", "currency": "RUB"}
        ]
        mock_sort_by_date.return_value = [{"id": 1, "description": "тест транзакция", "currency": "RUB"}]
        mock_filter_by_currency.return_value = [{"id": 1, "description": "тест транзакция", "currency": "RUB"}]
        mock_filter_by_transactions.return_value = [{"id": 1, "description": "тест транзакция", "currency": "RUB"}]

        # Вызов функции main
        main()

        # Проверяем вызовы
        mock_process_transactions.assert_called_once_with("1")
        mock_filter_transactions_by_state.assert_called_once()
        mock_sort_by_date.assert_called_once_with(mock_filter_transactions_by_state.return_value, False)
        mock_filter_by_currency.assert_called_once_with(mock_sort_by_date.return_value, "RUB")
        mock_filter_by_transactions.assert_called_once_with(mock_filter_by_currency.return_value, "тест")
        mock_print_transactions.assert_called_once_with(mock_filter_by_transactions.return_value)

    @patch(
        "builtins.input",
        side_effect=[
            "1",  # Выбор транзакции
            "нет",  # Не сортировать по дате
            "нет",  # Не фильтровать по рублевым транзакциям
            "нет",  # Не проводить дополнительную фильтрацию
        ],
    )
    @patch("src.main.process_transactions")
    @patch("src.main.filter_transactions_by_state")
    @patch("src.main.print_transactions")
    def test_main_without_sorting_and_filtering(
        self, mock_print_transactions, mock_filter_transactions_by_state, mock_process_transactions, mock_input
    ):

        # Настроим ожидания
        mock_process_transactions.return_value = [{"id": 2, "description": "другая транзакция", "currency": "USD"}]
        mock_filter_transactions_by_state.return_value = [
            {"id": 2, "description": "другая транзакция", "currency": "USD"}
        ]

        # Вызов функции main
        main()

        # Проверяем вызовы
        mock_process_transactions.assert_called_once_with("1")
        mock_filter_transactions_by_state.assert_called_once()
        mock_print_transactions.assert_called_once_with(mock_filter_transactions_by_state.return_value)


if __name__ == "__main__":
    unittest.main()
