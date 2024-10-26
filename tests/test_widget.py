import pytest

from src.widget import get_data, mask_account_card


# Юнит-тесты для mask_account_card
@pytest.mark.parametrize(
    "input_card_info, expected_output",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Master Card 7000792289606361", "Master Card 7000 79** **** 6361"),
        ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
        ("Счет 12345678901234567890", "Счет 1234 56** **** 7890"),
        ("Счет 1234567890123456789", ValueError),  # Некорректный номер счета
        ("Visa Gold 700079228960", ValueError),  # Некорректный номер карты
        ("", ValueError),  # Пустая строка
    ],
)
def test_mask_account_card(input_card_info, expected_output):
    if expected_output == ValueError:
        with pytest.raises(ValueError):
            mask_account_card(input_card_info)
    else:
        result = mask_account_card(input_card_info)
        assert result == expected_output


# Юнит-тесты для get_data
@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),  # Корректная дата с временем
        ("2023-10-15T12:00:00", "15.10.2023"),  # Корректная дата без миллисекунд
        ("2024-03", ValueError),  # Неполная дата (месяц без дня)
        ("date-string", ValueError),  # Некорректная строка
        ("", ValueError),  # Пустая строка
    ],
)
def test_get_data(input_data, expected_output):
    if expected_output == ValueError:
        with pytest.raises(ValueError):
            get_data(input_data)
    else:
        result = get_data(input_data)
        assert result == expected_output
