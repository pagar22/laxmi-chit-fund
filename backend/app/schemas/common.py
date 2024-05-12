from datetime import datetime
from datetime import timezone as tz
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class TimeStamp(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc))


class MonthlyBase(BaseModel):
    month: Annotated[str, StringConstraints(pattern=r"^(0[1-9]|1[0-2])$")]
    year: Annotated[str, StringConstraints(pattern=r"^(19\d{2}|20\d{2})$")]
