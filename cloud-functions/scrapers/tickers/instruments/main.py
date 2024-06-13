import difflib
from io import StringIO

import functions_framework
import pandas as pd
import requests
from flask import Request
from utils.config import BUCKET, LAXMI_URL, LOG


@functions_framework.http
def main(request: Request):
    data: dict = request.get_json()
    exchange_token = data.get("exchange_token")
    smallcase_name = data.get("smallcase_name")

    if not exchange_token and not smallcase_name:
        LOG.error("Bad Request", exchange_token, smallcase_name)
        return (f"bad_request, smallcase_name or exchange_token required", 400)
    try:
        tickers = get_tickers_csv()
        if smallcase_name:
            top_match = get_row_from_smallcase_name(tickers, smallcase_name)
            ticker = parse_ticker_from_row(top_match)
            ticker["smallcase_name"] = smallcase_name
            post_ticker(ticker)

        elif exchange_token:
            LOG.warn(f"💛 POST using exchange_token is discouraged!")
            ticker_row = tickers.query(f"exchange_token == {exchange_token}")
            ticker = parse_ticker_from_row(ticker_row)
            post_ticker(ticker)
        return (f"success", 200)

    except RequestError as e:
        return (f"{e}", e.status_code)


class RequestError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def get_tickers_csv() -> pd.DataFrame:
    blob = BUCKET.blob("tickers/NSE.csv")
    csv = StringIO(blob.download_as_bytes().decode("utf-8"))
    return pd.read_csv(csv)


def get_row_from_smallcase_name(
    tickers: pd.DataFrame, smallcase_name: str
) -> pd.Series:
    def get_similarity(x):
        return difflib.SequenceMatcher(None, x, smallcase_name).ratio()

    tickers["name_lower"] = tickers["name"].str.lower()
    tickers["similarity"] = tickers["name_lower"].apply(get_similarity)
    top_match = tickers.sort_values("similarity", ascending=False).head(1)
    LOG.info(f"Choosing Top Match: {top_match}")
    return top_match


def parse_ticker_from_row(ticker_row: pd.Series) -> dict:
    rename_cols = {"tradingsymbol": "ticker", "instrument_key": "upstox_instrument_key"}
    parse_cols = [
        "exchange",
        "exchange_token",
        "name",
        "ticker",
        "instrument_type",
        "upstox_instrument_key",
        "lot_size",
    ]
    df: pd.Series = ticker_row.rename(columns=rename_cols)
    tickers = df[parse_cols].to_dict(orient="records")
    LOG.info(f"Parsed Tickers from CSV: {tickers}")
    return tickers[0]


def post_ticker(ticker: dict):
    resp = requests.post(f"{LAXMI_URL}/tickers", json=ticker)
    if resp.status_code not in [200, 201]:
        LOG.error(f"Failed to create ticker: {resp.json()}")
        raise RequestError(f"ticker_not_posted", resp.status_code)
