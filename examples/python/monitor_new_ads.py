"""Monitor mode: print only ads not returned by earlier runs (run it on a schedule).

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python monitor_new_ads.py

Cost: $0.0015 per new ad; already-seen ads are skipped. The first run returns up to 50 ads ($0.075).
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
    "maxAdsPerTarget": 50,
    "onlyNewAds": True,
    "monitorStoreName": "nike-com-us-monitor"
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
    new_ads = [i for i in items if i.get("type") == "ad"]
    print(f"{len(new_ads)} new ads since the last run")
    for item in new_ads:
        print(f"  {item['format']:<6} first shown {(item.get('firstShown') or '')[:10]}  {item['adUrl']}")


if __name__ == "__main__":
    main()
