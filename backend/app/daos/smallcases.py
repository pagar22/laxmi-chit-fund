from app.daos.base import BaseDAO
from app.schemas.smallcases import SmallcaseBase, SmallcaseStatisticsBase


class SmallcaseDAO(BaseDAO):

    model = SmallcaseBase

    def __init__(self):
        super().__init__("smallcases")

    async def create_statistics(self, id: str, payload: SmallcaseStatisticsBase):
        path = f"{id}/statistics/{payload.year}-{payload.month}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload, exclude_none=True))
