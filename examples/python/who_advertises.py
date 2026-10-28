"""Find the advertiser accounts behind a brand name.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python who_advertises.py

Cost: $0.002 per advertiser row; up to 5 rows = $0.01.
The run is capped with max_total_charge_usd, so it cannot cost more than $0.10.
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "cleandata-labs/google-ads-transparency-explorer"
MAX_COST_USD = Decimal("0.10")

RUN_INPUT = {
    "queries": [
        "HelloFresh"
    ],
    "resultType": "advertisers",
    "regions": [
        "US"
    ],
    "maxAdvertisersPerQuery": 5
}


def run_actor(run_input: dict) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first "
                 "(Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=MAX_COST_USD)
    if run is None:
        sys.exit("The run could not be started.")
    print(f"Run {run.id} finished: {run.status}", file=sys.stderr)
    return list(client.dataset(run.default_dataset_id).iterate_items())


def main() -> None:
    items = run_actor(RUN_INPUT)
    for item in items:
        if item.get("type") != "advertiser":
            continue
        low, high = item.get("approxAdCountLow"), item.get("approxAdCountHigh")
        print(f"{item['name']:<40} {item['advertiserId']}  ads ~{low}-{high}  "
              f"country={item.get('countryCode')} verified={item.get('verified')}")


if __name__ == "__main__":
    main()
