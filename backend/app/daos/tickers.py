from typing import Optional

from app.daos.base import BaseDAO
from app.schemas.tickers import CandleStickBase, TickerBase
from app.utils.dates import dateparse, datestr
from dateutil.relativedelta import relativedelta


class TickerDAO(BaseDAO):

    model = TickerBase

    def __init__(self):
        super().__init__("tickers")

    async def get_by_smallcase_name(self, smallcase_name: str) -> Optional[TickerBase]:
        query = self.collection_reference.where("smallcase_name", "==", smallcase_name)
        docs = await query.get()
        if len(docs):
            return self.model(**docs[0].to_dict())

    async def get_candle_doc(
        self, exchange_token: str, date: str
    ) -> Optional[CandleStickBase]:
        path = f"{exchange_token}/candles/{date}"
        doc = await self.collection_reference.document(path).get()
        return CandleStickBase(**doc.to_dict()) if doc.exists else None

    async def get_candle_sticks(
        self, exchange_token: str, start_date: str, end_date: str
    ):
        candles = {}
        end = dateparse(end_date)
        start = dateparse(start_date)

        while (start.year, start.month) <= (end.year, end.month):
            date = datestr(str(start))
            doc = await self.get_candle_doc(exchange_token, date)
            if doc:
                candles.update(doc.daily)
            start += relativedelta(months=1)

        f_candles = {k: v for k, v in candles.items() if start_date <= k <= end_date}
        return {k: f_candles[k] for k in sorted(f_candles)}

    async def create_candle_sticks(
        self, exchange_token: str, payload: CandleStickBase, date: str
    ):
        data = self._model_dump_json(payload, exclude_none=True)
        await self._create_nested_hist_doc(exchange_token, "candles", date, data)
