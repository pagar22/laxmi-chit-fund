from datetime import datetime

from app.daos.base import BaseDAO
from app.schemas.tickers import CandleBase, CandleStickBase, TickerBase
from app.utils.validators import _format_date, get_date
from dateutil.relativedelta import relativedelta


class TickerDAO(BaseDAO):

    model = TickerBase

    def __init__(self):
        super().__init__("tickers")

    async def get_candle_doc(
        self, ticker: str, year: str, month: str
    ) -> CandleStickBase:
        path = f"{ticker}/candles/{year}-{month}"
        doc = await self.collection_reference.document(path).get()
        return CandleStickBase(**doc.to_dict())

    async def get_candle_sticks(self, ticker: str, start_date: str, end_date: str):
        DATE_FORMAT = "%Y-%m"
        candles = {}
        start = _format_date(start_date, DATE_FORMAT)
        end = _format_date(end_date, DATE_FORMAT)

        while start <= end:
            y, m = start.split("-")
            doc = await self.get_candle_doc(ticker, y, m)
            candles.update(doc.daily)
            if int(m) < 12:
                m = str(int(m) + 1)
            else:
                m = "01"
                y = str(int(y) + 1)
            start = _format_date(f"{y}-{m}-{'01'}", DATE_FORMAT)

        f_candles = {k: v for k, v in candles.items() if start_date <= k <= end_date}
        return {k: f_candles[k] for k in sorted(f_candles)}

    async def create_candle_sticks(
        self, ticker: str, payload: CandleStickBase, date: str
    ):
        y, m, d = get_date(date)
        payload.year, payload.month = y, m
        path = f"{ticker}/candles/{y}-{m}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload, exclude_none=True))
