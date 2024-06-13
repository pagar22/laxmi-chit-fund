from datetime import datetime

from pydantic import BaseModel, field_validator

DATE_FORMAT = "%Y-%m-%d"


def format_date(date: str) -> str:
    try:
        return datetime.strptime(date, DATE_FORMAT).strftime(DATE_FORMAT)
    except:
        raise ValueError(f"{date} is not of the expected format YYYY-MM-DD")


class CandlestickRequest(BaseModel):
    date: str
    smallcase_name: str

    @field_validator("date")
    def validate_dates(cls, v):
        format_date(v)
        return v
