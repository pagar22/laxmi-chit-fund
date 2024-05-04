from enum import Enum
from typing import Optional

from pydantic import BaseModel


class InstrumentType(Enum):
    EQUITY = "EQUITY"
    INDEX = "INDEX"


class ExchangeType(Enum):
    NSE = "NSE"
    BSE = "BSE"


class TickerBase(BaseModel):
    name: str
    ticker: str
    exchange_token: int
    exchange: ExchangeType
    instrument_type: InstrumentType
    lot_size: Optional[int] = None
    upstox_instrument_key: Optional[str] = None
