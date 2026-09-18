# -*- coding: utf-8 -*-
"""从 deepseek1024 商店 API 拉取插件目录并生成内置兜底目录 market-catalog.json。
用法: python tools/update-market-catalog.py [limit]
输出: app/src/main/assets/tools/market-catalog.json
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "src" / "main" / "assets" / "tools" / "market-catalog.json"
API = "https://deepseek1024.com/api/v1/plugins?page=1&limit={limit}"
DEFAULT_LIMIT = 60


def fetch(limit):
    req = urllib.request.Request(API.format(limit=limit), headers={
        "User-Agent": "dsha-market-catalog/1.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def pick_npm(pkg):
    """优先取 verified 的 npm spec + revision；否则 None。"""
    for m in pkg.get("installMethods") or []:
        if m.get("kind") == "npm" and m.get("verification") == "verified" and m.get("spec"):
            spec = m["spec"]
            rev = (m.get("revision") or "").strip()
            if rev and "@" not in rev:
                return spec + "@" + rev
            return spec
    for m in pkg.get("installMethods") or []:
        if m.get("kind") == "npm" and m.get("spec"):
            return m["spec"]
    return None


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LIMIT
    data = fetch(limit)
    packages = data.get("packages") or data.get("items") or []
    entries = []
    for pkg in packages:
        spec = pick_npm(pkg)
        if not spec:
            continue
        desc = pkg.get("description") or {}
        entries.append({
            "name": (pkg.get("name") or spec).strip(),
            "spec": spec,
            "owner": pkg.get("owner") or "",
            "url": pkg.get("url") or "",
            "category": pkg.get("category") or "",
            "zh": (desc.get("zh") or "")[:160],
            "en": (desc.get("en") or "")[:160],
            "installs": int(pkg.get("installCount") or 0),
            "stars": int(pkg.get("stars") or 0),
        })
    entries.sort(key=lambda e: (e["installs"], e["stars"]), reverse=True)
    doc = {
        "source": "deepseek1024",
        "generatedBy": "tools/update-market-catalog.py",
        "plugins": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"market-catalog.json: {len(entries)} 个插件, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
