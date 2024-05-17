from app.daos.base import BaseDAO
from app.schemas.tickers import CandleStickBase, TickerBase
from app.utils.dates import format_date, get_date, split_date
from dateutil.relativedelta import relativedelta


class TickerDAO(BaseDAO):

    model = TickerBase

    def __init__(self):
        super().__init__("tickers")

    async def get_candle_doc(
        self, ticker: str, year: str, month: str
    ) -> CandleStickBase:
        path = f"{ticker}/candles/{year}-{month}"
        print(path)
        doc = await self.collection_reference.document(path).get()
        return CandleStickBase(**doc.to_dict())

    async def get_candle_sticks(self, ticker: str, start_date: str, end_date: str):
        candles = {}
        start = get_date(start_date)
        end = get_date(end_date)

        while (start.year, start.month) <= (end.year, end.month):
            date = format_date(str(start))
            y, m, d = split_date(date)
            doc = await self.get_candle_doc(ticker, y, m)
            candles.update(doc.daily)
            start += relativedelta(months=1)

        f_candles = {k: v for k, v in candles.items() if start_date <= k <= end_date}
        return {k: f_candles[k] for k in sorted(f_candles)}

    async def create_candle_sticks(
        self, ticker: str, payload: CandleStickBase, date: str
    ):
        y, m, d = split_date(date)
        payload.year, payload.month = y, m
        path = f"{ticker}/candles/{y}-{m}"
        doc = self.collection_reference.document(path)
        await doc.set(self._model_dump_json(payload, exclude_none=True))
