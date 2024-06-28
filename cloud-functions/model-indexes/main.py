from io import StringIO

import functions_framework
import pandas as pd
import requests
from flask import Request
from utils.config import LAXMI_API_URL, LAXMI_CUD_API_KEY, LOG, bucket


@functions_framework.http
def main(request: Request):
    data: dict = request.get_json()
    smallcase_id = data.get("smallcase_id")

    indexes: pd.DataFrame = get_smallcase_indexes()
    smallcase_col = indexes.columns[1]
    benchmark_col = indexes.columns[2]

    monthly = indexes.groupby([pd.Grouper(freq="ME")])

    failed = []
    for name, group in monthly:
        start_date = group.index.min().strftime("%Y-%m-%d")
        end_date = group.index.max().strftime("%Y-%m-%d")

        indexes = {}
        for date, row in group.iterrows():
            date_str = date.strftime("%Y-%m-%d")
            indexes[date_str] = {
                "smallcase": row["smallcase"],
                "benchmark": row["benchmark"],
            }

        payload = {"start_date": start_date, "end_date": end_date, "indexes": indexes}
        status = post_indexes(smallcase_id, payload)
        if status not in [200, 201]:
            LOG.exception(f"Internal POST failed {date}")
            failed += name

    if failed:
        return (f"indexes_post_failed - {len(failed)}", 422)
    return ("success", 200)


def get_smallcase_indexes(smallcase_id: str) -> pd.DataFrame:
    blob = bucket.blob(f"smallcases/{smallcase_id}/timeline.xlsx")
    excel = StringIO(blob.download_as_bytes().decode("utf-8"))
    df = pd.read_excel(excel, sheet_name="Historical Index Values")
    df["Date"] = pd.to_datetime(df["Date"])
    df.fillna(False)
    df.replace("-", pd.NA, inplace=True)
    df.fillna(method="ffill", inplace=True)
    return df


def post_indexes(smallcase_id: str, payload: dict):
    url = f"{LAXMI_API_URL}/smallcases/{smallcase_id}/indexes"
    headers = {"X-CUD-Api-Key": LAXMI_CUD_API_KEY}
    resp = requests.post(url, headers=headers, json=payload)
    LOG.debug(resp.json())
    return resp.status_code
