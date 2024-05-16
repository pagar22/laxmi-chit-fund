from app.daos.base import BaseDAO
from app.internal.firebase import log
from app.schemas.smallcases import SmallcaseBase, SmallcaseStatisticsBase


class SmallcaseDAO(BaseDAO):

    model = SmallcaseBase

    def __init__(self):
        super().__init__("smallcases")

    async def create_statistics(self, id: str, payload: SmallcaseStatisticsBase):
        date = f"{payload.year}-{payload.month}"
        path = f"{id}/statistics/{date}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload, exclude_none=True))
        log.info(f"💹 Created statistics for {id} at {date}")

    async def get_statistics(self, id: str, date: str):
        y, m, d = date.split("-")
        log.info(f"{y}-{m}-{d}")
        log.info(f"📊 Fetching statistics for {id}")
