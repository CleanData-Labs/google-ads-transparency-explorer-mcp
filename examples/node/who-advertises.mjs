// Find the advertiser accounts behind a brand name.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node who-advertises.mjs
//
// Cost: $0.002 per advertiser row; up to 5 rows = $0.01.
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.10.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cleandata-labs/google-ads-transparency-explorer';
const MAX_COST_USD = 0.10;

const input = {
  "queries": [
    "HelloFresh"
  ],
  "resultType": "advertisers",
  "regions": [
    "US"
  ],
  "maxAdvertisersPerQuery": 5
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

for (const item of items.filter((i) => i.type === 'advertiser')) {
  console.log(`${item.name} ${item.advertiserId} ads ~${item.approxAdCountLow}-${item.approxAdCountHigh} verified=${item.verified}`);
}
