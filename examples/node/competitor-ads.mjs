// List recent Google ads that point to a competitor's domain.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node competitor-ads.mjs
//
// Cost: $0.0015 per ad; 10 ads = $0.015.
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.10.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cleandata-labs/google-ads-transparency-explorer';
const MAX_COST_USD = 0.10;

const input = {
  "queries": [],
  "domains": [
    "nike.com"
  ],
  "regions": [
    "US"
  ],
  "maxAdsPerTarget": 10
};

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
  process.exit(1);
}

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(input, { maxTotalChargeUsd: MAX_COST_USD });
console.error(`Run ${run.id} finished: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const item of items.filter((i) => i.type === 'ad')) {
  console.log(`${item.format.padEnd(6)} ${item.advertiserName} ${item.firstShown?.slice(0, 10)} -> ${item.lastShown?.slice(0, 10)} ${item.adUrl}`);
}
