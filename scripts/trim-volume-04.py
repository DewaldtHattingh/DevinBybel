#!/usr/bin/env python3
"""Trim duplicate expansion paragraphs when total word count exceeds 650."""
import re
from pathlib import Path


def wc(s):
    return len(s.split())


def trim_file(path: Path, max_total: int = 650):
    text = path.read_text(encoding="utf-8")
    prod = ""
    if "## Produksie-notas" in text:
        text, prod = text.split("## Produksie-notas", 1)
        prod = "## Produksie-notas" + prod

    chunks = re.split(r"(## Bladsy \d+[^\n]*\n)", text)
    out = [chunks[0]]
    for i in range(1, len(chunks), 2):
        header = chunks[i]
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        if "Bladsy 6" in header:
            out.append(header + body)
            continue
        blocks = body.split("\n\n")
        new_blocks = []
        narrative_idxs = []
        for j, block in enumerate(blocks):
            s = block.strip()
            if not s or s.startswith("![") or s.startswith(">") or s == "---":
                new_blocks.append(block)
            else:
                narrative_idxs.append(j)
                new_blocks.append(block)
        # If two consecutive narrative blocks, drop shorter
        if len(narrative_idxs) >= 2:
            texts = [blocks[i].strip() for i in narrative_idxs]
            # pairwise from end: drop shorter of last two narratives if similar start
            for a, b in zip(narrative_idxs[:-1], narrative_idxs[1:]):
                t1, t2 = blocks[a].strip(), blocks[b].strip()
                if t1[:18] == t2[:18] or (wc(t1) < 60 and wc(t2) < 60):
                    drop = b if wc(t2) <= wc(t1) else a
                    blocks[drop] = ""
            new_blocks = [b for b in blocks if b.strip()]
        out.append(header + "\n\n".join(new_blocks))
    path.write_text("".join(out) + prod, encoding="utf-8")


def main():
    base = Path("/agent/manuscripts/volume-04")
    for p in sorted(base.glob("*.md")):
        trim_file(p)
    print("Trimmed all files")


if __name__ == "__main__":
    main()
