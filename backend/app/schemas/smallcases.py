from datetime import datetime
from enum import Enum
from typing import Optional

from app.schemas.common import MonthlyBase
from app.utils.dates import format_date
from pydantic import BaseModel, field_validator


class RebalanceFrequency(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class Volatility(Enum):
    LOW = "Low Volatility"
    MEDIUM = "Medium Volatility"
    HIGH = "High Volatility"


class GrowthBase(BaseModel):
    cagr: float
    returns: float
    duration: str


class BenchmarkBase(BaseModel):
    id: str
    index: str
    details: str


class MethodologyBase(BaseModel):
    key: str
    details: str


class SmallcaseBase(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    volatility: Volatility
    pfp_url: Optional[str] = None
    popularity_rank: Optional[int] = None
    rebalance_timeline_sheet: Optional[str] = None

    contains_etf: bool
    contains_stock: bool
    constituent_count: int

    benchmark: BenchmarkBase
    growth_since_launch: GrowthBase
    methodologies: list[MethodologyBase]

    launch_date: datetime
    inception_date: datetime
    last_rebalance_date: datetime
    next_rebalance_date: datetime

    investment_strategies: list[str]
    rebalance_frequency: RebalanceFrequency


# Constituents
class ConstituentBase(BaseModel):
    smallcase_name: str
    original_weightage: float
    # has_no_candles: Optional[bool] = False
    kelly_weightage: Optional[float] = None
    standard_deviation: Optional[float] = None


class SmallcaseConstituentsBase(BaseModel):
    start_date: str
    end_date: str
    constituents: list[ConstituentBase]
    average_standard_deviation: Optional[float] = None

    @field_validator("start_date", "end_date")
    def validate_dates(cls, v):
        format_date(v)
        return v


# Statistics
class ReturnsBase(BaseModel):
    monthly: float
    quarterly: float
    half_year: float
    one_year: float
    three_year: Optional[float] = None
    five_year: Optional[float] = None


class CAGRBase(BaseModel):
    one_year: float
    three_year: Optional[float] = None
    five_year: Optional[float] = None


class RatioBase(BaseModel):
    dividend_yield: Optional[float] = None
    dividend_yield_differential: Optional[float] = None

    risk: Optional[float] = None
    pe: Optional[float] = None
    pb: Optional[float] = None
    beta: Optional[float] = None
    sharpe: Optional[float] = None


class WeightageBase(BaseModel):
    large_cap: float
    mid_cap: float
    small_cap: float
    market_category: Optional[str] = None


class SmallcaseStatisticsBase(MonthlyBase):
    min_sip_amount: int
    investor_count: Optional[int] = None
    subscriber_count: Optional[int] = None

    cagr: CAGRBase
    returns: ReturnsBase
    ratios: RatioBase

    weightage: WeightageBase
