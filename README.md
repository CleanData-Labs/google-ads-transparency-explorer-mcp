<p align="center"><img src="assets/icon.png" alt="Google Ads Transparency Scraper icon" width="96"></p>

# Google Ads Transparency Scraper (remote MCP tool)

See the ads any company runs on Google Search, YouTube, Shopping, Maps and Play, from the public Google Ads Transparency Center. Works as a remote MCP tool and through the Apify API.

It runs as an [Apify Actor](https://apify.com/cleandata-labs/google-ads-transparency-explorer) maintained by CleanData Labs, so you can use it in two ways:

1. **As a tool for your AI agent** (Claude, Cursor, VS Code / Copilot, Claude Code or any MCP client) through the hosted Apify MCP server. Nothing to install.
2. **From your own code** with the official `apify-client` for Python or JavaScript.

This repository holds the docs, ready-to-paste MCP configs and small runnable examples. The Actor itself is hosted on Apify; there is no server code to run here.

```text
https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer
```

## What it does

- **Every ad creative** for a brand name, a domain (e.g. `nike.com`), an advertiser ID (`AR...`) or a pasted Ads Transparency Center URL.
- Advertiser, domain, format (text / image / video), first and last shown dates, days shown, preview link, and the advertiser identity (country, legal name, verified status) for free.
- **Ad text and YouTube video IDs** of video ads (add-on).
- **EU reach and audience data** published under the Digital Services Act: times-shown ranges per country and platform, audience selection, topic (add-on, EU ads only).
- **Filters**: several countries at once, platform (Search, YouTube, Shopping, Maps, Play), format and date range.
- **Advertiser mode**: "who advertises for this brand or website?", one row per advertiser account.
- **Monitor mode**: return only ads not seen in earlier runs; schedule it for new-ad alerts.

## Connect it to your AI agent (MCP)

The URL above is a Streamable HTTP MCP endpoint that exposes one tool, `cleandata-labs--google-ads-transparency-explorer`, whose arguments are the [input fields](docs/input-reference.md). Two ways to authorize:

- **OAuth (recommended):** add only the URL. On first use your client opens an Apify sign-in page. A free Apify account works.
- **API token:** send the header `Authorization: Bearer <YOUR_APIFY_TOKEN>`. Get the token in [Apify Console > Settings > API & Integrations](https://console.apify.com/settings/integrations). Keep it out of git.

Ready-made config files are in [`examples/mcp/`](examples/mcp/).

### Claude (claude.ai and Claude Desktop)

Settings > Connectors > **Add custom connector**. Name: `Google Ads Transparency Scraper`, Remote MCP server URL: `https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer`. Sign in with Apify when asked.

If you prefer a local config file, Claude Desktop can run Apify's official stdio server instead (`claude_desktop_config.json`, needs Node.js 18+):

```json
{
  "mcpServers": {
    "google-ads-transparency": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "cleandata-labs/google-ads-transparency-explorer"],
      "env": { "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>" }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project). OAuth:

```json
{
  "mcpServers": {
    "google-ads-transparency": {
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer"
    }
  }
}
```

With a token instead:

```json
{
  "mcpServers": {
    "google-ads-transparency": {
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer",
      "headers": { "Authorization": "Bearer <YOUR_APIFY_TOKEN>" }
    }
  }
}
```

### VS Code (GitHub Copilot agent mode)

`.vscode/mcp.json`. OAuth:

```json
{
  "servers": {
    "google-ads-transparency": {
      "type": "http",
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer"
    }
  }
}
```

With a token, VS Code can prompt for it once and store it securely:

```json
{
  "inputs": [
    { "type": "promptString", "id": "apify-token", "description": "Apify API token", "password": true }
  ],
  "servers": {
    "google-ads-transparency": {
      "type": "http",
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer",
      "headers": { "Authorization": "Bearer ${input:apify-token}" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http google-ads-transparency "https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer"
# or with a token:
claude mcp add --transport http google-ads-transparency "https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer" --header "Authorization: Bearer $APIFY_TOKEN"
```

### Other clients and combining tools

Any client that supports remote Streamable HTTP servers can use the same URL. To load several Actors in one connection, separate them with commas, e.g. `https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer,cleandata-labs/url-to-markdown`. Already using `https://mcp.apify.com` with the default tools? Ask your agent to run `cleandata-labs/google-ads-transparency-explorer`.

### Try these prompts

- "Show me 10 recent Google ads that point to nike.com in the US, with first and last shown dates."
- "Which advertiser accounts run Google ads for HelloFresh? Include approximate ad counts and verification status."
- "Find 5 YouTube video ads from nike.com in the US and give me the YouTube links."

### Tips for agents

- Smallest useful input: `{"domains": ["nike.com"], "queries": [], "regions": ["US"], "maxAdsPerTarget": 10}` (10 ads, $0.015).
- Pass `queries: []` when you search by `domains`, `advertiserIds` or `startUrls`; otherwise the demo default `["Nike"]` also runs.
- Keep `maxAdsPerTarget` at 10-20 for a quick look; the default is 100 per target and a brand name can match up to 3 advertisers.
- Use `resultType: "advertisers"` for "who advertises for X?" questions.
- 10 ads take about 5 seconds; with `includeAdText` or `includeDetails` allow about 1 second per ad.

## Use it from code

Python (`pip install apify-client`):

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("cleandata-labs/google-ads-transparency-explorer").call(run_input={"domains": ["nike.com"], "queries": [], "regions": ["US"], "maxAdsPerTarget": 10})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item)
```

JavaScript / Node.js (`npm install apify-client`):

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('cleandata-labs/google-ads-transparency-explorer').call({"domains": ["nike.com"], "queries": [], "regions": ["US"], "maxAdsPerTarget": 10});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

Runnable examples, each with a hard cost cap (`max_total_charge_usd` / `maxTotalChargeUsd`):

- Python: [`competitor_ads.py`](examples/python/competitor_ads.py), [`who_advertises.py`](examples/python/who_advertises.py), [`youtube_video_ads.py`](examples/python/youtube_video_ads.py), [`monitor_new_ads.py`](examples/python/monitor_new_ads.py). See [`examples/python/README.md`](examples/python/README.md).
- Node.js: [`competitor-ads.mjs`](examples/node/competitor-ads.mjs), [`who-advertises.mjs`](examples/node/who-advertises.mjs). See [`examples/node/README.md`](examples/node/README.md).

```bash
export APIFY_TOKEN=...            # never commit it
cd examples/python && pip install -r requirements.txt && python competitor_ads.py
cd examples/node && npm install && node competitor-ads.mjs
```

You can also call it over plain HTTP, from Make, Zapier or n8n, or on a schedule. See the [Apify API docs](https://docs.apify.com/api/v2).

## Input and output

Full list of input fields with types and defaults: [`docs/input-reference.md`](docs/input-reference.md).

Example output row:

```json
{
  "type": "ad",
  "advertiserName": "SC DANTE INTERNATIONAL SA",
  "advertiserId": "AR09040091694841724929",
  "creativeId": "CR15732726098741428225",
  "domain": "emag.ro",
  "format": "IMAGE",
  "firstShown": "2021-10-25T07:00:00Z",
  "lastShown": "2026-10-27T19:06:16Z",
  "shownForDays": 1829,
  "adText": "Kit de îmbunătățire a luminii CORSAIR VENGEANCE 2x RGB, alb, set | eMAG",
  "youtubeVideoId": null,
  "topic": "Electronics",
  "impressionsMin": 20000,
  "impressionsMax": 25000,
  "advertiserCountry": "RO",
  "advertiserVerified": true,
  "adUrl": "https://adstransparency.google.com/advertiser/AR09040091694841724929/creative/CR15732726098741428225?region=RO"
}
```

Other row types: `advertiser` (advertisers mode: `advertiserId`, `name`, `countryCode`, `approxAdCountLow` / `approxAdCountHigh`, `legalName`, `verified`), `noResults` (free) and `error` (free). Reach and audience fields are filled only for ads shown in the EU; elsewhere they are `null`.

## Pricing

Pay per event on Apify: **$0.0015 per ad** ($1.50 per 1,000 ads). You pay Apify from your own Apify account; nothing is billed through this repository.

- Optional add-ons: full details (`includeDetails`) +$0.0015 per ad; ad text / YouTube video ID (`includeAdText`) +$0.0003 per ad, charged only when text or a video ID was actually found.
- Advertiser rows (`resultType: "advertisers"`): $0.002 per advertiser.
- Targets with no ads, blocked requests and errors are free.
- Each run also has an Actor start event ($0.001 per run). There is no separate compute or proxy fee.
- Set a *maximum cost per run* (smallest allowed: $0.10); the run stops cleanly when it is reached.

Apify's free plan includes a monthly platform credit (currently $5), which is enough to try the tool on real data. Prices can change; the [Actor page](https://apify.com/cleandata-labs/google-ads-transparency-explorer) always shows the current price.

## Good to know

- This is an independent tool by CleanData Labs. It is not affiliated with or endorsed by Google. It reads publicly available pages; use the data in line with the source site's terms and the laws that apply to you.
- The examples call the live Actor, so each run costs a little (see the cost note at the top of each script).
- Found a bug or need a field? Open an issue here or on the Actor's Issues tab on Apify.

## Links

- Apify Actor: <https://apify.com/cleandata-labs/google-ads-transparency-explorer>
- MCP endpoint: `https://mcp.apify.com?tools=cleandata-labs/google-ads-transparency-explorer`
- MCP registry name: `io.github.CleanData-Labs/google-ads-transparency-explorer` (see [`server.json`](server.json))
- Apify MCP server docs: <https://docs.apify.com/platform/integrations/mcp>

More tools from CleanData Labs:

- [Google Trends Scraper](https://github.com/CleanData-Labs/google-trends-explorer-mcp): Google Trends data for AI agents and scripts: interest over time, interest by region, related and rising queries, Trending Now and keyword suggestions.
- [URL to Markdown Converter](https://github.com/CleanData-Labs/url-to-markdown-mcp): Turn web pages and PDFs into clean, LLM-ready Markdown with metadata, token counts and optional RAG chunks.
- [Keyword Research Tool — Autocomplete & Trends](https://github.com/CleanData-Labs/seo-keyword-research-for-agents-mcp): Keyword ideas from Google Autocomplete plus Google Trends interest, direction and rising searches, returned as one compact JSON result per seed keyword with a plain-English summary.

## License

The example code and docs in this repository are released under the [MIT License](LICENSE). The hosted Actor is a paid service under [Apify's terms](https://apify.com/store-terms-and-conditions).
