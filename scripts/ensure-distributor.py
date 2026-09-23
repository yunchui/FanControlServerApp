#!/usr/bin/env python3
"""Ensure a fnOS FPK manifest file carries distributor=yunchui (our fork identity).
Usage: ensure-distributor.py <manifest-path>
Replaces or appends distributor / distributor_url. Leaves other lines untouched.
"""

import re
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: ensure-distributor.py <manifest>")
        return 2
    path = sys.argv[1]
    url = "https://github.com/yunchui/FanControlServerApp"
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    if re.search(r"^distributor\s*=", txt, re.M):
        txt = re.sub(r"^distributor\s*=.*$", "distributor           = yunchui", txt, flags=re.M)
        txt = re.sub(r"^distributor_url\s*=.*$", "distributor_url       = " + url, txt, flags=re.M)
    else:
        block = "\ndistributor           = yunchui\ndistributor_url       = " + url
        if re.search(r"^maintainer_url\s*=", txt, re.M):
            txt = re.sub(r"(^maintainer_url\s*=.*$)", r"\1" + block, txt, count=1, flags=re.M)
        else:
            txt = txt.rstrip("\n") + "\n" + block.lstrip("\n") + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
