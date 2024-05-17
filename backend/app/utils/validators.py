from datetime import datetime

from fastapi import HTTPException, Query

DATE_FORMAT = "%Y-%m-%d"


def _format_date(date: str, format: str = DATE_FORMAT) -> str:
    """
    - Parameters: date (str) in the format YYYY-MM-DD
    - Returns: 0-padded date string of type YYYY-MM-DD
    """
    return datetime.strptime(date, DATE_FORMAT).strftime(format)


def _validate_date(date: str):
    """
    Tests if the given date (str) is in the format YYYY-MM-DD. Raises ValueError if not.
    - Parameters: date (str)
    - Returns: None
    """
    try:
        datetime.strptime(date, DATE_FORMAT)
    except:
        raise ValueError(f"Invalid date format {date}")


def datestr(date: str = Query(..., description="YYYY-MM-DD")) -> str:
    """
    - Parameters: FastAPI query param date (str) in the format YYYY-MM-DD
    - Returns: 0-padded date string of type YYYY-MM-DD
    """
    try:
        _validate_date(date)
        return _format_date(date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def getdate(date: str) -> tuple[str, str, str]:
    """
    - Parameters: date (str) in the format YYYY-MM-DD
    - Returns: tuple of strings (year, month, day)
    """
    y, m, d = date.split("-")
    return y, m, d
