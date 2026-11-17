#!/usr/bin/env python3
"""Create a GitHub issue for each feature in features.json that has none, and
write the issue number back into the feature's entry.

Run from the repository root (needs the gh CLI, signed in with write access):

    python3 scripts/sync_issues.py            # create missing issues
    python3 scripts/sync_issues.py --dry-run  # show what would be created
"""

import json
import subprocess
import sys
import time
from urllib.parse import quote

REPO = "magland/neurosift-v3-check"
SITE = "https://magland.github.io/neurosift-v3-check/"
FEATURES = "features.json"
FAIL_LABEL = ("fail", "d73a4a", "v3 differs from v2 for this feature")


def gh(*args: str) -> str:
    return subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def link(url: str) -> str:
    """The URL with characters that break Markdown links percent-encoded."""
    return quote(url, safe=":/?&=%#,.-_~+")


def issue_body(f: dict, data: dict) -> str:
    v2 = data["v2"] + f.get("v2Path", f["path"])
    v3 = data["v3"] + f.get("v3Path", f["path"])
    checks = "\n".join(f"- {c}" for c in f.get("check", []))
    return f"""Side by side: {SITE}#{f['id']}

- [Open in v2]({link(v2)})
- [Open in v3]({link(v3)})

What to check:

{checks}

How to record a check (leave a comment each time):

- **Pass**: comment what you checked, then close the issue.
- **Fail**: comment what differs, then add the `fail` label and leave the issue open.
- If v3 changes something that passed, reopen the issue.

<!-- feature-id: {f['id']} -->
"""


def main() -> None:
    dry = "--dry-run" in sys.argv
    with open(FEATURES) as fh:
        data = json.load(fh)
    missing = [f for f in data["features"] if not f.get("issue")]
    print(f"{len(missing)} feature(s) without an issue")
    if dry or not missing:
        for f in missing:
            print(f"  would create: [{f['group']}] {f['title']}")
        return
    labels = gh("label", "list", "--repo", REPO, "--json", "name", "--jq", ".[].name")
    if FAIL_LABEL[0] not in labels.split("\n"):
        gh("label", "create", FAIL_LABEL[0], "--repo", REPO,
           "--color", FAIL_LABEL[1], "--description", FAIL_LABEL[2])
    for f in missing:
        url = gh("issue", "create", "--repo", REPO,
                 "--title", f"{f['group']}: {f['title']}",
                 "--body", issue_body(f, data))
        f["issue"] = int(url.rstrip("/").split("/")[-1])
        print(f"  #{f['issue']} {f['title']}")
        # Save after each issue so an interrupted run does not create duplicates.
        with open(FEATURES, "w") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")
        time.sleep(2)  # stay clear of GitHub's limits on creating content


if __name__ == "__main__":
    main()
