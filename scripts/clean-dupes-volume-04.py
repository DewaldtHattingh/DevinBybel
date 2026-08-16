#!/usr/bin/env python3
"""Remove exact duplicate narrative paragraphs within each page."""
import re
from pathlib import Path


def dedupe_page_body(body: str) -> str:
    blocks = body.split("\n\n")
    seen = set()
    out = []
    for block in blocks:
        key = block.strip()
        if not key:
            continue
        if key.startswith("![") or key.startswith(">") or key == "---":
            out.append(block)
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(block)
    return "\n\n".join(out) + ("\n" if out else "")


def clean_file(path: Path):
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r"(## Bladsy \d+[^\n]*\n)", text)
    out = [chunks[0]]
    for i in range(1, len(chunks), 2):
        header = chunks[i]
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        out.append(header + dedupe_page_body(body))
    path.write_text("".join(out), encoding="utf-8")


def main():
    base = Path("/agent/manuscripts/volume-04")
    for p in sorted(base.glob("*.md")):
        clean_file(p)
    print("Cleaned duplicate paragraphs")


if __name__ == "__main__":
    main()
