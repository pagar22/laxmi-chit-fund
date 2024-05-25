from datetime import datetime, timedelta

from app.daos.base import BaseDAO
from app.internal.firebase import log
from app.schemas.smallcases import (
    SmallcaseBase,
    SmallcaseConstituentsBase,
    SmallcaseStatisticsBase,
)
from app.utils.dates import get_date, split_date


class SmallcaseDAO(BaseDAO):

    model = SmallcaseBase

    def __init__(self):
        super().__init__("smallcases")

    async def get_constituents(self, id: str, date: str):
        ref = self.collection_reference.document(id).collection("constituents")
        query = ref.where("start_date", "<=", date).where("end_date", ">=", date)
        docs = await query.get()
        if docs:
            log.info(f"🤩 Found constituents for {id} at {date}")
            return SmallcaseConstituentsBase(**docs[0].to_dict())

        if True:
            query = ref.order_by("start_date", direction="DESCENDING").limit(1)
            docs = await query.get()
            if docs:
                constituents = SmallcaseConstituentsBase(**docs[0].to_dict())
                now = datetime.now().date()
                if now >= get_date(constituents.end_date):
                    log.info(f"🤷‍♀️ Returning latest constituents for {id} at {date}")
                    return constituents
        return None

    async def create_constituents(self, id: str, payload: SmallcaseConstituentsBase):
        y, m, d = split_date(payload.start_date)
        date = f"{y}-{m}"
        path = f"{id}/constituents/{date}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload))
        log.info(f"🩳 Created constituents for {id} at {date}")

    async def get_statistics(self, id: str, date: str):
        y, m, d = split_date(date)
        date = f"{y}-{m}"
        path = f"{id}/statistics/{date}"
        doc = await self.collection_reference.document(path).get()
        if doc.exists:
            log.info(f"🤩 Found statistics for {id} at {date}")
            return SmallcaseStatisticsBase(**doc.to_dict())
        return None

    async def create_statistics(
        self, id: str, payload: SmallcaseStatisticsBase, date: str
    ):
        y, m, d = split_date(date)
        date = f"{y}-{m}"
        path = f"{id}/statistics/{date}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload, exclude_none=True))
        log.info(f"💹 Created statistics for {id} at {date}")
