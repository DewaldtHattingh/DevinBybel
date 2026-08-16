#!/usr/bin/env python3
"""Remove duplicate narrative paragraphs added by expansion pass."""
import re
from pathlib import Path


def dedupe_page(body: str) -> str:
    parts = body.split("\n\n")
    kept = []
    prev_text = None
    for block in parts:
        stripped = block.strip()
        if not stripped or stripped.startswith("![") or stripped.startswith(">") or stripped == "---":
            kept.append(block)
            prev_text = None
            continue
        # narrative paragraph
        key = stripped[:30].lower()
        if prev_text and key[:20] == prev_text[:20]:
            # skip duplicate (keep first, longer version)
            continue
        kept.append(block)
        prev_text = stripped
    return "\n\n".join(kept)


def dedupe_file(path: Path):
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r"(## Bladsy \d+[^\n]*\n)", text)
    if len(chunks) < 2:
        return
    out = [chunks[0]]
    for i in range(1, len(chunks), 2):
        header = chunks[i]
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        if "Bladsy 6" in header:
            out.append(header + body)
        else:
            out.append(header + dedupe_page(body))
    path.write_text("".join(out), encoding="utf-8")


def main():
    base = Path("/agent/manuscripts/volume-04")
    for p in sorted(base.glob("*.md")):
        if p.name.startswith("_"):
            continue
        dedupe_file(p)
    print("Deduped volume-04 manuscripts")


if __name__ == "__main__":
    main()
