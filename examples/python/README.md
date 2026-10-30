# Python examples

Needs Python 3.10+ and an Apify API token.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
python competitor_ads.py
```

| Script | What it does | Cost |
|---|---|---|
| `competitor_ads.py` | List recent Google ads that point to a competitor's domain. | $0.0015 per ad; 10 ads = $0.015. |
| `who_advertises.py` | Find the advertiser accounts behind a brand name. | $0.002 per advertiser row; up to 5 rows = $0.01. |
| `youtube_video_ads.py` | Get YouTube video IDs and visible text of a brand's video ads. | $0.0015 per ad + $0.0003 per ad where text or a video ID is found; 5 ads = max $0.009. |
| `monitor_new_ads.py` | Monitor mode: print only ads not returned by earlier runs (run it on a schedule). | $0.0015 per new ad; already-seen ads are skipped. The first run returns up to 50 ads ($0.075). |

Every script sets `max_total_charge_usd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
