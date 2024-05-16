from datetime import datetime

from fastapi import HTTPException, Query


def format_date_path(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def validate_date_path(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        raise ValueError(f"Invalid date format {date}")


def datestr(date: str = Query(..., description="YYYY-MM-DD")):
    try:
        validate_date_path(date)
        return date
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
