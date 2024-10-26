import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_numbers():
    return [
        7000792289606361,  # Input value for the first test
        0,  # Input value for the second test (for empty check)
        700079228960636100,  # Input value for the third test
    ]


@pytest.fixture
def expected_results():
    return [
        "7000 79** **** 6361",  # Expected result for the first test
        ValueError,  # Expected exception for the second test
        ValueError,  # Expected exception for the third test
    ]


def test_get_mask_card_number(card_numbers, expected_results):
    for card_number, expected in zip(card_numbers, expected_results):
        if expected is ValueError:
            with pytest.raises(ValueError):
                get_mask_card_number(card_number)
        else:
            result = get_mask_card_number(card_number)
            assert result == expected


@pytest.fixture
def account_numbers():
    return [
        73654108430135874305,  # Input value for the first test
        0,  # Input value for the second test (for empty check)
        700079228960636100,  # Input value for the third test
    ]


@pytest.fixture
def expected_results_account():
    return [
        "7365 41** **** 4305",  # Expected result for the first test (updated)
        ValueError,  # Expected exception for the second test
        ValueError,  # Expected exception for the third test
    ]


def test_get_mask_account_number(account_numbers, expected_results_account):
    for account_number, expected in zip(account_numbers, expected_results_account):
        if expected is ValueError:
            with pytest.raises(ValueError):
                get_mask_account(account_number)
        else:
            result = get_mask_account(account_number)
            assert result == expected
