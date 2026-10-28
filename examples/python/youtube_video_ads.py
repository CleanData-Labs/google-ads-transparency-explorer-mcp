"""Get YouTube video IDs and visible text of a brand's video ads.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python youtube_video_ads.py

Cost: $0.0015 per ad + $0.001 per ad where text or a video ID is found; 5 ads = max $0.0125.
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
    "adFormat": "VIDEO",
    "maxAdsPerTarget": 5,
    "includeAdText": True
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
            continue
        video = item.get("youtubeVideoId")
        link = f"https://www.youtube.com/watch?v={video}" if video else "(no video ID found)"
        print(f"{item['creativeId']}  {link}  {item.get('adText') or ''}")


if __name__ == "__main__":
    main()
