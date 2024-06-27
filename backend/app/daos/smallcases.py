from datetime import datetime

from app.daos.base import BaseDAO
from app.internal.config import IS_EMULATOR_CONNECTED
from app.internal.firebase import log
from app.schemas.smallcases import (
    SmallcaseBase,
    SmallcaseConstituentsBase,
    SmallcaseIndexesBase,
    SmallcaseStatisticsBase,
)
from app.utils.dates import dateparse, datestr
from dateutil.relativedelta import relativedelta
from google.cloud.firestore_v1.base_query import FieldFilter


class SmallcaseDAO(BaseDAO):

    model = SmallcaseBase

    def __init__(self):
        super().__init__("smallcases")

    async def get_constituents(self, id: str, date: str, latest: bool = False):
        ref = self.collection_reference.document(id).collection("constituents")
        if latest:
            query = ref.order_by("start_date", direction="DESCENDING").limit(1)
            docs = await query.get()
            if docs:
                constituents = SmallcaseConstituentsBase(**docs[0].to_dict())
                now = datetime.now().date()
                if now >= dateparse(constituents.end_date):
                    log.info(f"🤷‍♀️ Returning latest constituents for {id} at {date}")
                    return constituents
        else:
            if not IS_EMULATOR_CONNECTED:
                end_filter = FieldFilter("end_date", ">=", date)
                start_filter = FieldFilter("start_date", "<=", date)
                query = ref.where(filter=start_filter).where(filter=end_filter).limit(1)
                docs = await query.get()
            else:
                start_filter = FieldFilter("start_date", "<=", date)
                filtered_docs = await ref.where(filter=start_filter).get()
                docs = [doc for doc in filtered_docs if doc.get("end_date") >= date]

            if docs:
                log.info(f"🥧 Fetched constituents for {id} at {date}")
                return SmallcaseConstituentsBase(**docs[0].to_dict())

    async def get_constituents_stream(self, id: str):
        ref = self.collection_reference.document(id).collection("constituents")
        max_quarters = 4 * 8  # 8 years max
        query = ref.order_by("start_date", direction="DESCENDING").limit(max_quarters)
        docs = await query.get()
        return [SmallcaseConstituentsBase(**doc.to_dict()) for doc in docs]

    async def get_indexes(self, id: str, start_date: str, end_date: str):
        indexes = {}
        end = dateparse(end_date)
        start = dateparse(start_date)

        earliest = await self._get_first_doc_by_id(f"/{id}/indexes")
        if earliest:
            start = max(start, dateparse(f"{earliest.id}-01"))
            log.info(f"⏰ Using start date {start} for indexes of {id}")

        while (start.year, start.month) <= (end.year, end.month):
            date = datestr(str(start))
            path = f"{id}/indexes/{date}"
            doc = await self.collection_reference.document(path).get()
            if doc.exists:
                indexes.update(SmallcaseIndexesBase(**doc.to_dict()).indexes)
            start += relativedelta(months=1)

        log.info(f"📈 Fetched {len(indexes)} indexes for {id}")
        r_indexes = {k: v for k, v in indexes.items() if start_date <= k <= end_date}
        return {k: r_indexes[k] for k in sorted(r_indexes)}

    async def get_statistics(self, id: str, date: str):
        path = f"{id}/statistics/{date}"
        doc = await self.collection_reference.document(path).get()
        if doc.exists:
            log.info(f"🤩 Found statistics for {id} at {date}")
            return SmallcaseStatisticsBase(**doc.to_dict())
        return None

    async def create_constituents(self, id: str, payload: SmallcaseConstituentsBase):
        date = payload.start_date
        data = self._model_dump_json(payload)
        await self._create_nested_hist_doc(id, "constituents", date, data)

    async def create_indexes(self, id: str, payload: SmallcaseIndexesBase, date: str):
        data = self._model_dump_json(payload, exclude_none=True)
        await self._create_nested_hist_doc(id, "indexes", date, data)

    async def create_statistics(
        self, id: str, payload: SmallcaseStatisticsBase, date: str
    ):
        data = self._model_dump_json(payload, exclude_none=True)
        await self._create_nested_hist_doc(id, "statistics", date, data)
