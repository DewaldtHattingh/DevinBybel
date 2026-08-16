#!/usr/bin/env python3
"""Add scaffold scripture_audit blocks to manuscripts that lack them."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_ROOT = ROOT / "manuscripts-v2"

DAV03_DETAILS = [
    "Saul",
    "Jesse sends David",
    "Goliath's challenge",
    "lion",
    "bear",
    "David credits God",
    "Saul's armour",
    "armour rejected",
    "staff",
    "five smooth stones",
    "shepherd's bag",
    "sling",
    "Goliath's shield bearer",
    "stone strikes forehead",
    "Goliath falls face down",
    "Goliath's sword",
    "Goliath killed/beheaded",
    "Philistines flee",
]


def split_front(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        raise ValueError("no frontmatter")
    parts = text.split("---", 2)
    return "---", parts[1], parts[2]


def details_from_must_include(data: dict) -> list[str]:
    raw = data.get("must_include") or []
    if isinstance(raw, str):
        raw = [raw]
    out: list[str] = []
    for item in raw:
        for part in re.split(r"[;•|/]", str(item)):
            part = part.strip().strip('"')
            if part:
                out.append(part)
    return out or ["(fill from passage checklist)"]


def scaffold(data: dict, story_id: str) -> dict:
    passage = data.get("primary_passage") or ""
    details = DAV03_DETAILS if story_id == "DAV-03" else details_from_must_include(data)
    return {
        "primary_passage": passage,
        "passage_read": False,
        "context_read": False,
        "required_details": details,
        "unsupported_details": [],
        "chronology_check": "pending",
        "people_check": "pending",
        "numbers_check": "pending",
        "theology_check": "pending",
        "direct_quotes_verified": False,
        "afr20_quote_check": "pending",
        "audit_status": "needs_v3_repass",
    }


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    dash, raw, body = split_front(text)
    data = yaml.safe_load(raw) or {}
    sid = str(data.get("story_id", ""))
    if isinstance(data.get("scripture_audit"), dict) and set(
        data["scripture_audit"]
    ) >= {
        "required_details",
        "audit_status",
        "passage_read",
    }:
        return False
    data["scripture_audit"] = scaffold(data, sid)
    # Keep top-level quote flag honest: structural AFR20 pass ≠ approved V3
    if data.get("afr20_quote_check") == "verified":
        data["afr20_quote_check"] = "pending"
        data["scripture_audit"]["afr20_quote_check"] = "pending"
    dumped = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    path.write_text(f"---\n{dumped}---{body}", encoding="utf-8")
    return True


def main() -> int:
    n = 0
    for path in sorted(MANUSCRIPT_ROOT.rglob("*.md")):
        if process(path):
            n += 1
            print(f"injected {path.relative_to(ROOT)}")
    print(f"{n} files updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
