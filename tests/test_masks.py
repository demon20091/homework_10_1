import pytest

from src.masks import get_mask_account, get_masks_card_number



@pytest.mark.parametrize(
    "cart_number, masked",
    [
        ("1596837868705199", "1596 83** **** 5199"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("6831982476737658", "6831 98** **** 7658"),
        ("8990922113665229", "8990 92** **** 5229"),
        ("5999414228426353", "5999 41** **** 6353"),
    ],
)

def test_get_masks_card_number(cart_number, masked):
    """Тест на правильность маскирования номера карты."""
    assert get_masks_card_number(cart_number) == masked


@pytest.mark.parametrize(
    "account_number, masked",
    [
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
    ],
)

def test_get_mask_account(account_number, masked):
    """Тест на правильность маскирования номера счета."""
    assert get_mask_account(account_number) == masked