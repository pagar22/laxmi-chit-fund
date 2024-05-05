from enum import Enum
from typing import Optional

from app.schemas.common import TimeStamp


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
    upstox_instrument_key: Optional[str] = None
