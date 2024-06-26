from datetime import date, datetime

from fastapi import HTTPException

DATE_PATH_FORMAT = "%Y-%m"
DATE_VALIDATION_FORMAT = "%Y-%m-%d"


def datestr(date: str, full_path: bool = False) -> str:
    """
    FastAPI query param validator for date strings.
    Tests if the given date (str) is in the format YYYY-MM-DD. Raises ValueError if not.
    - Parameters: date (str), full_path (bool) default is False
    - Returns: 0-padded date string of type YYYY-MM-DD if full_path is True, else YYYY-MM
    """
    try:
        path_format = DATE_VALIDATION_FORMAT if full_path else DATE_PATH_FORMAT
        return datetime.strptime(date, DATE_VALIDATION_FORMAT).strftime(path_format)
    except:
        error = f"{date} is not of the expected format YYYY-MM-DD"
        raise HTTPException(status_code=400, detail=error)


def dateparse(date: str) -> date:
    """
    - Parameters: date (str) in the format YYYY-MM-DD
    - Returns: date object as YYYY-MM-DD
    """
    return datetime.strptime(date, DATE_VALIDATION_FORMAT).date()


def validate_date_range(start_date: str, end_date: str, max_days: int) -> None:
    """
    FastAPI validator to validate the date range between start_date and end_date.
    Raises HTTP 400 for invalid date ranges.

    Parameters:
    - start_date (str), end_date (str) in the format YYYY-MM-DD
    - max_years (int): Maximum number of years allowed in the date range
    - Returns: None
    """
    max_days += 10  # Add 10 day buffer (leap years)

    end_date = dateparse(end_date)
    start_date = dateparse(start_date)
    days = (end_date - start_date).days
    if days < 0:
        raise HTTPException(status_code=400, detail="Invalid date range")
    elif days > max_days:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot fetch data for more than {max_days // 365} year(s)",
        )
