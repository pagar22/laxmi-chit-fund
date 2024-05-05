from datetime import datetime
from datetime import timezone as tz

from pydantic import BaseModel, Field


class TimeStamp(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc))
