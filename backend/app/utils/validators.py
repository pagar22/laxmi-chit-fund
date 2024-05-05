from datetime import datetime


def format_date_path(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def validate_date_path(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        raise ValueError(f"Invalid date format {date}")
