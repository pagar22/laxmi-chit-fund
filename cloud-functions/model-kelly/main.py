from datetime import datetime

import functions_framework
import numpy as np
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from flask import Request
from pandas import DataFrame as DF
from utils.config import (
    DATE_FORMAT,
    LAXMI_API_URL,
    LAXMI_CUD_API_KEY,
    LOG,
    TickerNotFoundException,
)


@functions_framework.http
def main(request: Request):

    data = request.get_json()
    smallcase_id = data.get("smallcase_id")

    constituents = requests.get(
        f"{LAXMI_API_URL}/smallcases/{smallcase_id}/constituents/stream"
    ).json()
    LOG.info(f"{len(constituents)} constituent rebalances found")

    failed = []
    ticker_not_found = 0
    no_of_prev_quarters = 2  # Historical data for T - 2 quarters

    for quarter in constituents[no_of_prev_quarters:]:
        end_date = quarter["start_date"]
        start_date = datetime.strptime(end_date, DATE_FORMAT)
        start_date = start_date - relativedelta(months=no_of_prev_quarters * 3)
        start_date = start_date.strftime(DATE_FORMAT)
        LOG.info(f"Date range: {start_date} to {end_date}")

        df_indexes = get_indexes_df(smallcase_id, start_date, end_date)
        df_indexes["benchmark"].to_frame()

        kelly_constituents = []
        for constituent in quarter["constituents"]:
            smallcase_name = constituent["smallcase_name"]
            LOG.info(f"Calculating {smallcase_name}...")
            try:
                df, df_close = get_candles_df(smallcase_name, start_date, end_date)
                variance = get_variance(df_close)
                expected_returns = get_expected_returns(df_close, df_indexes)
                kelly = get_kelly_weightage(expected_returns, variance)
            except TickerNotFoundException:
                LOG.info("Ticker not found, using same kelly weightage")
                ticker_not_found += 1
                kelly = constituent["original_weightage"]

            kelly_constituent = {**constituent}
            kelly_constituent["kelly_weightage"] = "{:,.6f}".format(kelly)
            kelly_constituent["half_kelly_weightage"] = "{:,.6f}".format(kelly * 0.5)
            kelly_constituent["standard_deviation"] = "{:,.6f}".format(
                np.sqrt(variance)
            )
            kelly_constituents.append(kelly_constituent)

        kelly_payload = {**quarter}
        adjusted_kelly_constituents = get_adjusted_kelly_constituents(
            kelly_constituents
        )
        kelly_payload["constituents"] = adjusted_kelly_constituents

        LOG.info(kelly_payload)
        status = post_kelly_smallcase(smallcase_id, kelly_payload)
        if not status in [200, 201]:
            failed.append(quarter)

    if len(failed) == 0:
        return ("success", 200)
    else:
        LOG.debug(failed)
        return (f"smallcase_post_failed - {len(failed)}", 422)


def get_indexes_df(smallcase_id: str, start_date: str, end_date: str) -> DF:
    url = f"{LAXMI_API_URL}/smallcases/{smallcase_id}/indexes"
    params = {"start_date": start_date, "end_date": end_date}
    indexes = requests.get(url, params=params).json()

    df = pd.DataFrame.from_dict(indexes, orient="index")
    df.index = pd.to_datetime(df.index)
    return df


def get_candles_df(
    smallcase_name: str, start_date: str, end_date: str
) -> tuple[DF, DF]:
    try:
        params = {"smallcase_name": smallcase_name}
        ticker = requests.get(f"{LAXMI_API_URL}/tickers", params=params).json()
        exchange_token = ticker["exchange_token"]
    except KeyError as e:
        LOG.exception(ticker, e)
        raise TickerNotFoundException()

    url = f"{LAXMI_API_URL}/tickers/{exchange_token}/candles"
    params = {"start_date": start_date, "end_date": end_date}
    candles = requests.get(url, params=params).json()

    df = pd.DataFrame.from_dict(candles, orient="index")
    df.index = pd.to_datetime(df.index)
    df_close = df["close"].to_frame()
    return df, df_close


def get_variance(candles: DF):
    candles = candles.sort_index()
    returns = candles["close"].pct_change().dropna()
    return np.var(returns)


def get_expected_returns(candles: DF, indexes: DF):
    candles["smallcase_returns"] = candles["close"].pct_change()
    candles["benchmark_returns"] = indexes["benchmark"].pct_change()
    candles = candles.dropna()

    covariance = np.cov(candles["smallcase_returns"], candles["benchmark_returns"])[
        0, 1
    ]
    market_variance = np.var(candles["benchmark_returns"])
    beta = covariance / market_variance
    # 10 year averages
    risk_free_rate = 0.06
    expected_market_return = 0.12

    expected_return = risk_free_rate + beta * (expected_market_return - risk_free_rate)
    return expected_return / 252


def get_kelly_weightage(expected_return: float, variance: float):
    annual_risk_free_rate = 0.068
    adjusted_risk_free_rate = (1 + annual_risk_free_rate) ** (1 / 252) - 1

    kelly_weightage = (expected_return - adjusted_risk_free_rate) / variance
    return kelly_weightage


def get_adjusted_kelly_constituents(constituents: list):
    total_kelly_weight = sum(float(c["kelly_weightage"]) for c in constituents)
    for c in constituents:
        c["adjusted_kelly_weightage"] = "{:,.6f}".format(
            (float(c["kelly_weightage"]) / total_kelly_weight)
        )
    return constituents


def post_kelly_smallcase(smallcase_id: str, payload: dict):
    url = f"{LAXMI_API_URL}/smallcases/{smallcase_id}/constituents"
    headers = {"X-CUD-Api-Key": LAXMI_CUD_API_KEY}
    resp = requests.post(url, headers=headers, json=payload)
    LOG.debug(resp.status_code, resp.json())
    return resp.status_code
