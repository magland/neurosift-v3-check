# neurosift-v3-check

Checking Neurosift v3 (https://v3.neurosift.app) against v2 (https://neurosift.app), feature by feature. Each feature is one page at https://magland.github.io/neurosift-v3-check/: a short list of what to check, and the same link opened in v2 on the left and v3 on the right.

## Recording results

Each feature has an issue in this repository, linked from its page. Leave a comment every time you check a feature:

- **Pass**: comment what you checked, then close the issue.
- **Fail**: comment what differs, then add the `fail` label and leave the issue open.
- If v3 changes something that passed, reopen the issue.

The page reads the issues (closed is pass, open with `fail` is fail, open without it is not checked) and shows each feature's status, the totals, and the newest comment. It reads them without signing in, which GitHub limits to 60 requests an hour per IP address.

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

Then create its issue, which also writes the issue number into the entry (needs the `gh` CLI with write access to this repository):

```bash
python3 scripts/sync_issues.py
```

## Running locally

The page loads `features.json` with `fetch`, so it needs a web server:

```bash
python3 -m http.server 8000
```
