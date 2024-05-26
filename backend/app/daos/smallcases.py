from datetime import datetime, timedelta

from app.daos.base import BaseDAO
from app.internal.firebase import log
from app.schemas.smallcases import (
    SmallcaseBase,
    SmallcaseConstituentsBase,
    SmallcaseIndexesBase,
    SmallcaseStatisticsBase,
)
from app.utils.dates import format_date, get_date, split_date
from dateutil.relativedelta import relativedelta


class SmallcaseDAO(BaseDAO):

    model = SmallcaseBase

    def __init__(self):
        super().__init__("smallcases")

    async def __create_historical_doc(
        self, smallcase_id: str, collection_id: str, date: str, data: dict
    ):
        y, m, d = split_date(date)
        date = f"{y}-{m}"
        path = f"{smallcase_id}/{collection_id}/{date}"
        print(path)
        await self.collection_reference.document(path).set(data)

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

    async def get_indexes(self, id: str, start_date: str, end_date: str):
        indexes = {}
        start = get_date(start_date)
        end = get_date(end_date)

        earliest = await self._get_first_doc_by_id(f"/{id}/indexes")
        if earliest:
            start = max(start, get_date(f"{earliest.id}-01"))
            log.info(f"🔍 Earliest start date for indexes of {id} is {start}")

        while (start.year, start.month) <= (end.year, end.month):
            date = format_date(str(start))
            y, m, d = split_date(date)
            path = f"{id}/indexes/{y}-{m}"
            doc = await self.collection_reference.document(path).get()
            if doc.exists:
                log.info(f"🤩 Found indexes for {id} at {date}")
                indexes.update(SmallcaseIndexesBase(**doc.to_dict()).indexes)
            start += relativedelta(months=1)

        f_indexes = {k: v for k, v in indexes.items() if start_date <= k <= end_date}
        return {k: f_indexes[k] for k in sorted(f_indexes)}

    async def get_statistics(self, id: str, date: str):
        y, m, d = split_date(date)
        date = f"{y}-{m}"
        path = f"{id}/statistics/{date}"
        doc = await self.collection_reference.document(path).get()
        if doc.exists:
            log.info(f"🤩 Found statistics for {id} at {date}")
            return SmallcaseStatisticsBase(**doc.to_dict())
        return None

    async def create_constituents(self, id: str, payload: SmallcaseConstituentsBase):
        data = self._model_dump_json(payload)
        await self.__create_historical_doc(id, "constituents", payload.start_date, data)
        log.info(f"🩳 Created constituents for {id} at {payload.start_date}")

    async def create_indexes(self, id: str, payload: SmallcaseIndexesBase, date: str):
        data = self._model_dump_json(payload, exclude_none=True)
        await self.__create_historical_doc(id, "indexes", date, data)
        log.info(f"📈 Created indexes for {id} at {date}")

    async def create_statistics(
        self, id: str, payload: SmallcaseStatisticsBase, date: str
    ):
        data = self._model_dump_json(payload, exclude_none=True)
        await self.__create_historical_doc(id, "statistics", date, data)
        log.info(f"💹 Created statistics for {id} at {date}")
