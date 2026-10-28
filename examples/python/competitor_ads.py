"""List recent Google ads that point to a competitor's domain.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python competitor_ads.py

Cost: $0.0015 per ad; 10 ads = $0.015.
The run is capped with max_total_charge_usd, so it cannot cost more than $0.10.
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "cleandata-labs/google-ads-transparency-explorer"
MAX_COST_USD = Decimal("0.10")

RUN_INPUT = {
    "queries": [],
    "domains": [
        "nike.com"
    ],
    "regions": [
        "US"
    ],
    "maxAdsPerTarget": 10
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
        if item.get("type") != "ad":
            print("Row:", item.get("type"), item.get("error") or item.get("message") or "")
            continue
        print(f"{item['format']:<6} {item['advertiserName'][:30]:<30} "
              f"{(item.get('firstShown') or '')[:10]} -> {(item.get('lastShown') or '')[:10]}  {item['adUrl']}")


if __name__ == "__main__":
    main()
