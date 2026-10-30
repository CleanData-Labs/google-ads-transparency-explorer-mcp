# Input reference: Google Ads Transparency Scraper

Generated from the Actor's published input schema. All fields are optional unless marked required. The same fields are the arguments of the MCP tool `cleandata-labs--google-ads-transparency-explorer`.

Live version: <https://apify.com/cleandata-labs/google-ads-transparency-explorer/input-schema>

| Field | Type | Default | Description |
|---|---|---|---|
| `queries` | array | `["Nike"]` | Brand names or websites to look up, e.g. ["Nike"] or ["hellofresh.com"]. Names are matched to advertiser accounts (see maxAdvertisersPerQuery). If you omit this field the default ["Nike"] is used, so pass [] when you only use domains, advertiserIds or startUrls. |
| `domains` | array |  | Exact websites, e.g. ["nike.com"]. Returns every ad that points to the domain, from any advertiser account. The most precise way to see a competitor's ads. |
| `advertiserIds` | array |  | Advertiser IDs that start with AR, e.g. ["AR16735076323512287233"], taken from an advertiser page URL on adstransparency.google.com. |
| `startUrls` | array |  | Optional advertiser, creative or domain-search links copied from adstransparency.google.com, e.g. [{"url": "https://adstransparency.google.com/advertiser/AR16735076323512287233?region=US"}]. Filters in the URL (region, format, platform, dates) are applied. |
| `resultType` | string: `ads` / `advertisers` | `"ads"` | "ads" (default) = one row per ad creative. "advertisers" = one row per advertiser account with approximate ad count, country, legal name and verification status. Use "advertisers" to check who advertises for a brand or website. |
| `regions` | array | `["US"]` | Country codes where the ads were shown, e.g. ["US"] or ["DE","FR"] (ads shown in ANY of them). [] = anywhere. Default ["US"]. Reach and audience data exist only for EU countries. |
| `platforms` | array of `SEARCH` / `YOUTUBE` / `SHOPPING` / `MAPS` / `PLAY` |  | Optional Google surfaces: any of "SEARCH", "YOUTUBE", "SHOPPING", "MAPS", "PLAY". [] = all. Google applies this filter only to ads shown since September 2023. |
| `adFormat` | string: `ALL` / `TEXT` / `IMAGE` / `VIDEO` | `"ALL"` | Creative format: "ALL" (default), "TEXT", "IMAGE" or "VIDEO". |
| `startDate` | string |  | Optional. Only ads shown on or after this date, format YYYY-MM-DD, e.g. "2026-06-01". Google applies date filters only to about the last 12 months. |
| `endDate` | string |  | Optional. Only ads shown on or before this date, format YYYY-MM-DD. |
| `maxAdsPerTarget` | integer (min 0) | `100` | Max ads per domain / advertiser, 0 = no limit. Default 100. Each ad costs one result, so AI agents should use 10-20 for a quick look. A brand-name query can expand to several advertisers. |
| `maxAdvertisersPerQuery` | integer (min 1, max 20) | `3` | How many matching advertiser accounts to use per brand-name query, 1-20. Default 3. Exact name matches first, then by ad count. Use 1 for the main brand only. |
| `includeDetails` | boolean | `false` | true = one extra request per ad to add all A/B variations, every country with dates, Google's 'times shown' ranges (EU ads), audience selection and topic. Paid add-on per ad and slower (about 1 s per ad). Default false. |
| `includeAdText` | boolean | `false` | true = read Google's ad preview to add the visible ad text (headline, description, product title, display URL) and the YouTube video ID of video ads. Paid add-on, charged only when text or a video ID was found. Default false. |
| `includeAdvertiserInfo` | boolean | `true` | true (default, free) = add advertiser country, legal name, verification status and EU-only flag to each row. |
| `onlyNewAds` | boolean | `false` | true = monitor mode: remember creative IDs in a named key-value store and return only ads not seen in earlier runs. Combine with a schedule for new-ad alerts. Default false. |
| `monitorStoreName` | string | `"ads-transparency-monitor"` | Name of the key-value store used by monitor mode. Use a different name per monitored target. Default "ads-transparency-monitor". |
| `maxRequestsPerMinute` | integer (min 5, max 600) | `50` | Request throttle, 5-600. Default 50. Without a proxy keep it around 50. |
| `maxRetries` | integer (min 0, max 10) | `5` | Retries per request on rate limits or network errors, 0-10. Default 5. Each retry uses a fresh session (and proxy IP, if enabled). |
| `requestTimeoutSecs` | integer (min 5, max 120) | `30` | Timeout per HTTP request in seconds, 5-120. Default 30. |
| `proxyConfiguration` | object | `{"useApifyProxy": true}` | Proxy settings. Default {"useApifyProxy": true}, recommended so sessions can rotate on rate limits. Leave as is unless you have a reason to change it. |
