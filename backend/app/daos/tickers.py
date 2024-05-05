from app.daos.base import BaseDAO
from app.internal.firebase import db
from app.schemas.tickers import MonthlyCandleBase, TickerBase


class TickerDAO(BaseDAO):

    model = TickerBase

    def __init__(self):
        super().__init__("tickers")

    async def create_candle_sticks(self, id: str, payload: MonthlyCandleBase):
        path = f"{id}/candles/{payload.year}-{payload.month}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload))
