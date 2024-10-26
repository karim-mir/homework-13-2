from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: Список словарей, который нужно фильтровать.
    :param state: Значение ключа 'state' для фильтрации. По умолчанию 'EXECUTED'.
    :return: Новый список словарей, содержащих только те, у которых ключ 'state' соответствует заданному значению.

    Пример:
    >>> filter_by_state([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}])
    [{'id': 1, 'state': 'EXECUTED'}]
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате.

    :param data: Список словарей, который нужно сортировать.
    :param reverse: Параметр для определения порядка сортировки.
                    По умолчанию True (убывание). Если False, то сортировка в порядке возрастания.
    :return: Новый список словарей, отсортированный по дате.

    Пример:
    >>> sort_by_date([{"id": 1, "date": "2022-01-01T12:00:00"}, {"id": 2, "date": "2021-01-01T12:00:00"}])
    [{'id': 1, 'date': '2022-01-01T12:00:00'}, {'id': 2, 'date': '2021-01-01T12:00:00'}]
    """
    try:
        return sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {e}")


# Примеры использования
if __name__ == "__main__":
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )

    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
