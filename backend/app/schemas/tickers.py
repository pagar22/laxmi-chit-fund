from enum import Enum
from typing import Annotated, Dict, Optional

from app.schemas.common import TimeStamp
from app.utils.validators import validate_date_path
from pydantic import BaseModel, Field, StringConstraints, validator


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


class MonthlyCandleBase(BaseModel):
    month: Annotated[str, StringConstraints(pattern=r"^(0[1-9]|1[0-2])$")]
    year: Annotated[str, StringConstraints(pattern=r"^(19\d{2}|20\d{2})$")]
    daily: Dict[str, CandleBase] = Field(default_factory=dict)
    monthly: Optional[CandleBase] = None

    @validator("daily", pre=True, allow_reuse=True)
    def validate_daily(cls, v):
        for key in v:
            validate_date_path(key)
        return v
