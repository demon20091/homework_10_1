from typing import Union


def get_masks_card_number(cart_number: Union[str]) -> str:
    """функция получения данных карты и маскировки"""
    return f"{cart_number[:4]} {cart_number[4:6]}** **** {cart_number[-4:]}"


def get_mask_account(account_number: Union[str]) -> str:
    """функция, присваиваивающая номер счета и маскирующая его"""
    return f"**{account_number[-4:]}"
