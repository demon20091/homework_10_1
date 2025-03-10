from datetime import datetime
from typing import Union

from src.masks import get_masks_card_number, get_mask_account


def mask_account_card(type_and_number: Union[str]) -> Union[str]:
    '''функция, которая умеет обрабатывать информацию как о картах, так и о счетах.'''

    parts = type_and_number.split()
    only_type = ' '.join(parts[:-1])
    only_number = parts[-1]
    if len(only_number) > 16: # ещё лучше - if only_type.lower().startswith('счет')
        return f"{only_type} {get_mask_account(only_number)}"
    else:
        return f"{only_type} {get_masks_card_number(only_number)}"


def get_date(user_date: Union[str]) -> Union[str]:
    '''Функция, которая принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").'''

    date_format = datetime.strptime(user_date, "%Y-%m-%dT%H:%M:%S.%f")
    new_date = date_format.strftime("%d.%m.%Y")

    return new_date


print(mask_account_card("Visa Platinum 1234567891234567"))
print(mask_account_card("Счет 34565789789456132465"))
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
