def mask_account_card(card_details: str) -> str:
    """Принимает строку с типом карты/счета и номером, возвращает замаскированный номер."""
    if not card_details:
        raise ValueError("Введены пустые данные")

    parts = card_details.split()
    if len(parts) < 2:
        raise ValueError("Введены некорректные данные")

    last_part = parts[-1]
    card_or_account_type = " ".join(parts[:-1])

    # Проверяем, состоит ли номер из цифр
    if not last_part.isdigit():
        raise ValueError("Номер карты или счета должен состоять только из цифр")

    if card_or_account_type.lower().startswith("счет"):
        if len(last_part) == 20:  # Длина номера счета
            masked_number = f"{last_part[:4]} {last_part[4:6]}** **** {last_part[-4:]}"
        else:
            raise ValueError("Введен некорректный номер счета")
    else:
        if len(last_part) in {16, 19}:  # Длина номера карты может быть 16 или 19
            masked_number = f"{last_part[:4]} {last_part[4:6]}** **** {last_part[-4:]}"
        else:
            raise ValueError("Введен некорректный номер карты")

    return f"{card_or_account_type} {masked_number}"


print(mask_account_card("Visa Platinum 7000792289606361"))


def get_data(date: str) -> str:
    """Заменяем знак "-" в строке с датой на "." и форматируем дату."""
    if not date:
        raise ValueError("Date string is empty")

    if "T" not in date:
        raise ValueError("Incomplete date format")

    date_part = date.split("T")[0]  # берем только часть до T
    parts = date_part.split("-")

    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError("Invalid date format")

    formatted_date = f"{parts[2]}.{parts[1]}.{parts[0]}"
    return formatted_date


print(get_data("2024-03-11T02:26:18.671407"))
