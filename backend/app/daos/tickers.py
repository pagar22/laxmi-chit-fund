from app.daos.base import BaseDAO
from app.internal.firebase import db
from app.schemas.tickers import TickerBase


class TickerDAO(BaseDAO):

    model = TickerBase

    def __init__(self):
        super().__init__("tickers")
