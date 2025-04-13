from unittest.mock import mock_open, patch

import pytest

from src.utils import converted_transactions, transaction_amount


@patch("builtins.open", new_callable=mock_open, read_data='[{"amount": 100, "currency": "USD"}]')
def test_valid_file(mock_file):
    """ Тест на корректный файл с транзакциями. """
    transactions = converted_transactions("data/operations.json")
    assert transactions == [{"amount": 100, "currency": "USD"}]


@patch("builtins.open", new_callable=mock_open, read_data='')
def test_empty_file(mock_file):
    """ Тест на пустой файл. """
    transactions = converted_transactions("data/operations.json")
    assert transactions == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_file):
    """ Тест на случай, если файл не найден. """
    transactions = converted_transactions("data/operations.json")
    assert transactions == []


@pytest.fixture
def some_transaction_rub():
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }


def test_transaction_amount_rub(some_transaction_rub):
    """ Тест на получение суммы в рублях, если транзакция в рублях. """
    assert transaction_amount(some_transaction_rub) == "\nТранзакция ID: 939719570, сумма: 9824.07 RUB"


@pytest.fixture
def some_transaction_usd():
    return {
        "id": 939719840,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "1500.6",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }


@patch("src.utils.convert_curr")
def test_transaction_amount_non_rub_success(mock_convert_curr, some_transaction_usd):
    """ Тест на получение суммы в рублях, если транзакция в иностранной валюте и запрос успешный. """
    mock_convert_curr.return_value = 158388.33
    result = transaction_amount(some_transaction_usd)
    assert result == "\nТранзакция ID: 939719840, сумма: 158388.33 RUB"
    mock_convert_curr.assert_called_once_with("USD", "RUB", "1500.6")


@patch("src.utils.convert_curr")
def test_transaction_amount_non_rub_fail(mock_convert_curr, some_transaction_usd):
    """ Тест на получение суммы в рублях, если транзакция в иностранной валюте и запрос провален. """
    mock_convert_curr.return_value = -1
    result = transaction_amount(some_transaction_usd)
    assert result == "\nТранзакция ID: 939719840, сумма: 1500.6 USD"
