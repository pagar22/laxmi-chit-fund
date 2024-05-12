from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from app.schemas.common import MonthlyBase, TimeStamp
from pydantic import BaseModel, StringConstraints


class RebalanceFrequency(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"


class Volatility(Enum):
    LOW = "Low Volatility"
    MEDIUM = "Medium Volatility"
    HIGH = "High Volatility"


class CAGRBase(BaseModel):
    value: float
    duration: str


class BenchmarkBase(BaseModel):
    id: str
    index: str
    details: str


class MethodologyBase(BaseModel):
    key: str
    details: str


class SmallcaseBase(TimeStamp):
    id: str
    name: str
    slug: str
    description: str
    volatility: Volatility
    popularity_rank: Optional[int]
    rebalance_timeline_sheet: Optional[str]

    contains_etf: bool
    contains_stock: bool
    constituent_count: int

    cagr: CAGRBase
    benchmark: BenchmarkBase
    methodology: list[MethodologyBase]

    launch_date: datetime
    inception_date: datetime
    last_rebalance_date: datetime
    next_rebalance_date: datetime

    investment_strategies: list[str]
    rebalance_frequency: RebalanceFrequency


class SmallcaseStatisticsBase(MonthlyBase):
    investor_count: Optional[int]
    subscriber_count: Optional[int]

    monthly_cagr: float
    quarterly_cagr: float
    one_year_cagr: Optional[float]
    three_year_cagr: Optional[float]
    five_year_cagr: Optional[float]

    dividend_yield: float
    dividend_yield_differential: float

    pe: float
    pb: float
    risk: float
    beta: Optional[float]
    sharpe_ratio: Optional[float]

    market_category: str
    large_cap_percentage: float
    mid_cap_percentage: float
    small_cap_percentage: float
