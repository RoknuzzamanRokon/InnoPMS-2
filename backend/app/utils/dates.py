from collections.abc import Iterator
from datetime import date, timedelta


def iter_dates(start_date: date, end_date: date) -> Iterator[date]:
    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += timedelta(days=1)
