# neurosift-features

A list of what Neurosift does, with an example of each, shown side by side in Neurosift v2 (https://neurosift.app) and v3 (https://v3.neurosift.app). The purpose is to go through the list by hand and check that v3 does everything v2 does.

Each feature is one page: a short list of what to check, and the same link opened in v2 on the left and v3 on the right.

## Adding a feature

Add an entry to `features.json`:

```json
{
  "id": "psth",
  "group": "Views",
  "title": "PSTH",
  "path": "/nwb?url=...&tab=view:PSTH|/intervals/trials",
  "check": ["Choosing units", "Align to a column, group by a category"]
}
```

`path` is opened on both sites. v3 reads v2 links, so one path usually serves both; set `v2Path` or `v3Path` to use a different link on one side.

## Running locally

The page loads `features.json` with `fetch`, so it needs a web server:

```bash
python3 -m http.server 8000
```
