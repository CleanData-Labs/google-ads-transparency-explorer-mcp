# Node.js examples

Needs Node.js 18+ and an Apify API token.

```bash
npm install
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
node competitor-ads.mjs
```

| Script | What it does | Cost |
|---|---|---|
| `competitor-ads.mjs` | List recent Google ads that point to a competitor's domain. | $0.0015 per ad; 10 ads = $0.015. |
| `who-advertises.mjs` | Find the advertiser accounts behind a brand name. | $0.002 per advertiser row; up to 5 rows = $0.01. |

Every script sets `maxTotalChargeUsd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
