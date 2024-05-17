from datetime import datetime

from fastapi import HTTPException, Query

DATE_FORMAT = "%Y-%m-%d"


def _format_date(date: str, format: str = DATE_FORMAT) -> str:
    """
    Tests if the given date (str) is of the format YYYY-MM-DD. Raises ValueError if not.
    - Parameters: date (str), format (str) defaulting to YYYY-MM-DD
    - Returns: 0-padded date string of type YYYY-MM-DD
    """
    try:
        return datetime.strptime(date, DATE_FORMAT).strftime(format)
    except:
        raise ValueError(f"{date} is not of the expected format YYYY-MM-DD")


def datestr(date: str = Query(..., description="YYYY-MM-DD")) -> str:
    """
    FastAPI query param validator for date strings.
    - Parameters: Date (str) in the format YYYY-MM-DD
    - Returns: 0-padded date string in the format YYYY-MM-DD
    """
    try:
        return _format_date(date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_date(date: str) -> tuple[str, str, str]:
    """
    - Parameters: date (str) in the format YYYY-MM-DD
    - Returns: tuple of strings (year, month, day)
    """
    y, m, d = date.split("-")
    return y, m, d


def get_days_between_dates(date_from: str, date_to: str) -> int:
    """
    - Parameters: date_from (str), date_to (str) in the format YYYY-MM-DD
    - Returns: Number of days between the two dates
    """
    date_from = datetime.strptime(date_from, DATE_FORMAT)
    date_to = datetime.strptime(date_to, DATE_FORMAT)
    return (date_to - date_from).days
