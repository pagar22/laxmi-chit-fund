from pydantic import BaseModel, field_validator
from utils.dates import validate_date


class CandlestickRequest(BaseModel):
    date: str
    smallcase_name: str

    @field_validator("date")
    def validate_dates(cls, v):
        validate_date(v)
        return v


class RequestError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
