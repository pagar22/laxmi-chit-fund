import re

import functions_framework
import requests
from flask import Request
from utils.config import LAXMI_API_URL, LAXMI_CUD_API_KEY, SMALLCASE_API_URL, log


@functions_framework.http
def main(request: Request):
    data = request.get_json()
    smallcase_id = data.get("smallcase_id")
    resp = requests.get(f"{SMALLCASE_API_URL}/smallcases/smallcase?scid={smallcase_id}")
    if resp.status_code not in [200, 201]:
        return ("smallcase_not_found_external_api", resp.status_code)
    try:
        smallcase = get_smallcase(smallcase_id)
        payload = parse_smallcase(smallcase_id, smallcase)
        post_smallcase(payload)
        return ("success", 200)
    except RequestException as e:
        return (str(e), e.status_code)


class RequestException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


def get_smallcase(smallcase_id: str):
    resp = requests.get(f"{SMALLCASE_API_URL}/smallcases/smallcase?scid={smallcase_id}")
    if resp.status_code not in [200, 201]:
        log.error(f"Smallcase external GET failed: {resp.json()}")
        raise RequestException("smallcase_not_found_external", resp.status_code)
    return resp.json()["data"]


def post_smallcase(payload: dict):
    headers = {"X-CUD-Api-Key": LAXMI_CUD_API_KEY}
    resp = requests.post(f"{LAXMI_API_URL}/smallcases/", json=payload, headers=headers)
    if resp.status_code not in [200, 201]:
        log.error(f"Smallcase BE POST failed: {resp.json()}")
        raise RequestException("smallcase_not_created", resp.status_code)


def parse_smallcase(smallcase_id: str, smallcase: dict):

    def remove_p_tag(text: str):
        return re.sub(r"</?(p|ul|li)>", "", text)

    stats = smallcase["stats"]
    methodologies = []
    for m in smallcase["methodology"]:
        methodologies.append({"key": m["key"], "details": remove_p_tag(m["content"])})
    investment_strategies = []
    for i in smallcase["info"]["investmentStrategy"]:
        investment_strategies.append(i["key"])

    payload = {
        "id": smallcase_id,
        "name": smallcase["info"]["name"],
        "slug": smallcase["info"]["slug"],
        "description": smallcase["info"]["shortDescription"],
        "volatility": stats["ratios"]["riskLabel"],
        "popularity_rank": smallcase["flags"]["popular"]["rank"],
        "contains_etf": smallcase["flags"]["containsEtf"],
        "contains_stock": smallcase["flags"]["containsStock"],
        "constituent_count": smallcase["constituentsCount"],
        "growth_since_launch": {
            "cagr": stats["ratios"]["cagr"],
            "returns": stats["returns"]["sinceInception"],
            "duration": stats["ratios"]["cagrDuration"],
        },
        "benchmark": {
            "id": smallcase["benchmark"]["id"],
            "index": smallcase["benchmark"]["index"],
            "details": smallcase["benchmark"]["msg"],
        },
        "methodologies": methodologies,
        "launch_date": smallcase["info"]["uploaded"],
        "inception_date": smallcase["info"]["created"],
        "last_rebalance_date": smallcase["info"]["lastRebalanced"],
        "next_rebalance_date": smallcase["info"]["nextUpdate"],
        "investment_strategies": investment_strategies,
        "rebalance_frequency": smallcase["info"]["rebalanceSchedule"],
    }
    return payload
