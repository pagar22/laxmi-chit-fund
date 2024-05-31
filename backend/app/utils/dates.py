from datetime import date, datetime

from fastapi import HTTPException, Query

DATE_FORMAT = "%Y-%m-%d"


def datestr(date: str = Query(..., description="YYYY-MM-DD")) -> str:
    """
    FastAPI query param validator for date strings.
    - Parameters: Date (str) in the format YYYY-MM-DD
    - Returns: 0-padded date string in the format YYYY-MM-DD
    """
    try:
        return format_date(date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def format_date(date: str) -> str:
    """
    Tests if the given date (str) is in the format YYYY-MM-DD. Raises ValueError if not.
    - Parameters: date (str), format (str) defaulting to YYYY-MM-DD
    - Returns: 0-padded date string of type YYYY-MM-DD
    """
    try:
        return datetime.strptime(date, DATE_FORMAT).strftime(DATE_FORMAT)
    except:
        raise ValueError(f"{date} is not of the expected format YYYY-MM-DD")


def get_date(date: str) -> date:
    """
    - Parameters: date (str) in the format YYYY-MM-DD
    - Returns: date object as YYYY-MM-DD
    """
    return datetime.strptime(date, DATE_FORMAT).date()


def split_date(date: str) -> tuple[str, str, str]:
    """
    - Parameters: date (str) in the format YYYY-MM-DD
    - Returns: tuple of strings (year, month, day)
    """
    y, m, d = date.split("-")
    return y, m, d


def validate_date_range(start_date: str, end_date: str, max_days: int) -> None:
    """
    FastAPI validator to validate the date range between start_date and end_date.
    Raises HTTP 400 for invalid date ranges.

    Parameters:
    - start_date (str), end_date (str) in the format YYYY-MM-DD
    - max_years (int): Maximum number of years allowed in the date range
    - buffer_days (int): Number of days to add to max_years to account for leap years or other
    - Returns: None
    """
    days = _get_days_between_dates(start_date, end_date)
    if days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")
    elif days > max_days:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot fetch data for more than {365 // days} year(s)",
        )


def _get_days_between_dates(date_from: str, date_to: str) -> int:
    """
    - Parameters: date_from (str), date_to (str) in the format YYYY-MM-DD
    - Returns: Number of days between the two dates
    """
    date_from = datetime.strptime(date_from, DATE_FORMAT)
    date_to = datetime.strptime(date_to, DATE_FORMAT)
    return (date_to - date_from).days
