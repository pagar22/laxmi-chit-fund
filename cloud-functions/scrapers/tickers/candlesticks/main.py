from datetime import datetime

import functions_framework
import requests
from flask import Request
from utils.config import LAXMI_URL, LOG, UPSTOX_URL
from utils.dates import format_date, get_last_day_of_month
from utils.schemas import CandlestickRequest, RequestError


@functions_framework.http
def main(request: Request):
    LOG.info("😶‍🌫️ Candlesticks CF invoked...")
    try:
        payload = CandlestickRequest(**request.get_json())
    except Exception as e:
        LOG.error(f"Bad request payload, {e}")
        return (f"bad_request, {e}", 400)

    year, month, day = payload.date.split("-")
    try:
        ticker = get_ticker_by_smallcase_name(payload.smallcase_name)
        exchange_token = ticker["exchange_token"]
        instrument_key = ticker["upstox_instrument_key"]

        candles = get_upstox_candles(instrument_key, year, month)
        candles_request = parse_upstox_candles(candles, year, month)
        post_ticker_candles(exchange_token, payload.date, candles_request)
        return ("success", 200)
    except RequestError as e:
        return (str(e), e.status_code)


def get_ticker_by_smallcase_name(smallcase_name: str):
    params = {"smallcase_name": smallcase_name}
    resp = requests.get(f"{LAXMI_URL}/tickers/", params=params)
    if resp.status_code not in [200, 201]:
        LOG.error(f"Failed to GET ticker from BE, {resp.json()}")
        raise RequestError("ticker_not_found", 404)
    return resp.json()


def post_ticker_candles(exchange_token: str, date: str, candles: dict):
    url = f"{LAXMI_URL}/tickers/{exchange_token}/candles?date={date}"
    resp = requests.post(url, json=candles)
    if resp.status_code not in [200, 201]:
        LOG.error(f"Failed to POST candlesticks to BE, {resp.json()}")
        raise RequestError("candlesticks_not_posted", resp.status_code)


def get_upstox_candles(instrument_key: str, year: str, month: str):
    last_day = get_last_day_of_month(int(year), int(month))
    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{last_day}"
    path = f"{instrument_key}/day/{end_date}/{start_date}"
    resp = requests.get(f"{UPSTOX_URL}/historical-candle/{path}")
    if resp.status_code not in [200, 201]:
        LOG.error(f"Failed to GET candlesticks from upstox, {resp.json()}")
        raise RequestError("candlesticks_not_found", 404)
    return resp.json()["data"]["candles"]


def parse_upstox_candles(candles: list, year: str, month: str):
    if len(candles) > 0:
        candles_request = {"month": month, "year": year}
        # Daily candles
        daily = {}
        for candle in candles:
            timestamp = format_date(datetime.fromisoformat(candle[0]))
            daily[timestamp] = {
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5],
                "open_interest": candle[6],
            }
        candles_request["daily"] = daily

        # Monthly candle
        monthly_high = max(entry["high"] for entry in daily.values())
        monthly_low = min(entry["low"] for entry in daily.values())
        monthly_volume = sum(entry["volume"] for entry in daily.values())
        monthly_open = candles[-1][1]
        monthly_close = candles[0][4]
        candles_request["monthly"] = {
            "open": monthly_open,
            "high": monthly_high,
            "low": monthly_low,
            "close": monthly_close,
            "volume": monthly_volume,
        }
        return candles_request
