import calendar
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


def get_last_day_of_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def validate_date(date: str) -> str:
    try:
        return datetime.strptime(date, DATE_FORMAT).strftime(DATE_FORMAT)
    except:
        raise ValueError(f"{date} is not of the expected format YYYY-MM-DD")


def format_date(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)
