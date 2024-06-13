import calendar
from datetime import datetime

import functions_framework
import requests
from flask import Request
from schemas import CandlestickRequest


def get_last_day_of_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def format_date_path(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


@functions_framework.http
def main(request: Request):
    try:
        payload = CandlestickRequest(**request.get_json())
    except Exception as e:
        print(e)
        return ("bad request", 400)

    # LAXMI_URL = "https://laxmi-chit-fund-xgqm3fv7ua-ew.a.run.app"
    LAXMI_URL = "http://localhost:2000"
    UPSTOX_URL = "https://api.upstox.com/v2"

    year, month, day = payload.date.split("-")
    last_day = get_last_day_of_month(int(year), int(month))
    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{last_day}"

    params = {"smallcase_name": payload.smallcase_name}
    resp = requests.get(f"{LAXMI_URL}/tickers/", params=params)

    if resp.status_code == 200:

        ticker = resp.json()
        exchange_token = ticker["exchange_token"]
        instrument_key = ticker["upstox_instrument_key"]

        resp = requests.get(
            f"{UPSTOX_URL}/historical-candle/{instrument_key}/day/{end_date}/{start_date}"
        )
        if resp.status_code == 200:
            candles = resp.json()["data"]["candles"]
            if len(candles) > 0:
                candles_request = {"month": month, "year": year}
                # Daily candles
                daily = {}
                for candle in candles:
                    timestamp = format_date_path(datetime.fromisoformat(candle[0]))
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
            resp = requests.post(
                f"{LAXMI_URL}/tickers/{exchange_token}/candles?date={payload.date}",
                json=candles_request,
            )
            print(resp.json())
        else:
            print(resp.json())
            return ("candlesticks not found, upstox failure", 404)

    elif resp.status_code == 404:
        # invoke instrument scraper
        return ("ticker not found, internal failure", 404)

    # 1. get instrument using smallcase name
    # 2. if instrument, get candlesticks -> post candlesticks to be
    # 3. if no instrument, return logger warning to invoke instrument scraper first

    # instrument scraper
    # 1. Map smallcase name to instrument using csv
    # 2. Ideally ask for user confirmation before posting instrument to be
    # 3. Post instrument to be

    return "OK"
