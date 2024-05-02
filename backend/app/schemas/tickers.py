from enum import Enum

from pydantic import BaseModel


class InstrumentType(Enum):
    EQUITY = "equity"
    INDEX = "index"


class ExchangeType(Enum):
    NSE = "nse"
    BSE = "bse"


class TickerBase(BaseModel):
    name: str
    ticker: str
    upstox_instrument_key: str
    instrument_type: InstrumentType
    exchange: ExchangeType
