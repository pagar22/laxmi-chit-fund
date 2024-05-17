from app.daos.base import BaseDAO
from app.internal.firebase import log
from app.schemas.smallcases import SmallcaseBase, SmallcaseStatisticsBase
from app.utils.dates import split_date


class SmallcaseDAO(BaseDAO):

    model = SmallcaseBase

    def __init__(self):
        super().__init__("smallcases")

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
