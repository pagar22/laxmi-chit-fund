from enum import Enum
from typing import Optional

from pydantic import BaseModel


class InstrumentType(Enum):
    EQUITY = "equity"
    INDEX = "index"


class ExchangeType(Enum):
    NSE = "nse"
    BSE = "bse"


class TickerBase(BaseModel):
    id: str
    name: str
    exchange: ExchangeType
    instrument_type: InstrumentType
    upstox_instrument_key: Optional[str]
