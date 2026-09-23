#!/usr/bin/env python3
"""Read the latest FanControlServer release and print url-variant FPK info as JSON.
Usage: read-release.py [version]
Env: GH_TOKEN. Picks the *-url.fpk asset (url variant).
"""

import json
import os
import sys
import urllib.request


def api(url):
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {os.environ.get('GH_TOKEN','')}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "fcs-sync"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pick(rel):
    for a in rel.get("assets", []):
        n = a["name"]
        if n.startswith("FanControlServer-") and n.endswith("-linux-amd64-url.fpk"):
            return a
    return None


def main() -> int:
    base = "https://api.github.com/repos/yunchui/FanControlServerApp"
    if len(sys.argv) >= 2:
        ver = sys.argv[1].lstrip("v")
        rel = api(f"{base}/releases/tags/v{ver}")
        if not rel or "tag_name" not in rel:
            print(f"ERROR: release v{ver} 不存在", file=sys.stderr); return 1
    else:
        rel = api(f"{base}/releases/latest")
    asset = pick(rel)
    if not asset:
        print("ERROR: release 无 *-url.fpk 资产", file=sys.stderr); return 1
    digest = asset.get("digest", "").replace("sha256:", "").rstrip()
    if not digest or len(digest) != 64:
        print("ERROR: sha256 无效或缺失", file=sys.stderr); return 1
    info = {"version": rel["tag_name"].lstrip("v"), "url": asset["browser_download_url"],
            "sha256": digest, "size": asset["size"], "published": rel.get("published_at") or ""}
    with open("/tmp/fcs_release.json", "w", encoding="utf-8") as f:
        json.dump(info, f)
    print("detected:", json.dumps(info))
    return 0


if __name__ == "__main__":
    sys.exit(main())
