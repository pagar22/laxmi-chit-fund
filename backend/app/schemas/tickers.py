from enum import Enum
from typing import Dict, Optional

from app.schemas.common import MonthlyBase, TimeStamp
from app.utils.validators import _validate_date
from pydantic import BaseModel, Field, field_validator


class InstrumentType(Enum):
    EQUITY = "EQUITY"
    INDEX = "INDEX"


class ExchangeType(Enum):
    NSE = "NSE"
    BSE = "BSE"


class TickerBase(TimeStamp):
    name: str
    ticker: str
    exchange_token: int
    exchange: ExchangeType
    instrument_type: InstrumentType
    lot_size: Optional[int] = None
    smallcase_name: Optional[str] = None
    upstox_instrument_key: Optional[str] = None


class CandleBase(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: Optional[int] = None
    open_interest: Optional[int] = None


class CandleStickBase(MonthlyBase):
    daily: Dict[str, CandleBase] = Field(default_factory=dict)
    monthly: Optional[CandleBase] = None

    @field_validator("daily")
    def validate_daily(cls, v):
        for key in v:
            _validate_date(key)
        return v
