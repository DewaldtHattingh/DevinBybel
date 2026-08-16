#!/usr/bin/env python3
"""Remove near-duplicate trailing sentences from expanded narrative paragraphs."""
import re
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("exp", Path(__file__).parent / "expand-volume-02.py")
exp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp)


def sentence_overlap(s1, s2):
    w1 = set(re.findall(r"\w+", s1.lower()))
    w2 = set(re.findall(r"\w+", s2.lower()))
    if not w1 or not w2:
        return 0
    return len(w1 & w2) / min(len(w1), len(w2))


def trim_paragraph(para):
    para_sents = re.split(r"(?<=[.!?…])\s+", para.strip())
    changed = True
    while changed and len(para_sents) > 1:
        changed = False
        tail = para_sents[-1]
        for prev in para_sents[:-1]:
            if sentence_overlap(tail, prev) >= 0.78:
                para_sents.pop()
                changed = True
                break
    return " ".join(para_sents)


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out = []
    current_page = None
    narrative_buf = []

    def flush():
        nonlocal narrative_buf
        if narrative_buf:
            out.append(trim_paragraph(" ".join(narrative_buf)))
            narrative_buf = []

    for line in lines:
        if line.startswith("## Bladsy"):
            flush()
            m = re.search(r"Bladsy (\d+)", line)
            current_page = int(m.group(1)) if m else None
            out.append(line)
            continue
        if line.startswith("## "):
            flush()
            current_page = None
            out.append(line)
            continue
        if line.strip() == "---":
            flush()
            out.append(line)
            continue
        s = line.strip()
        if (
            current_page
            and current_page <= 5
            and s
            and not s.startswith("!")
            and not s.startswith(">")
            and not s.startswith("#")
        ):
            narrative_buf.append(s)
            continue
        flush()
        out.append(line)
    flush()
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    base = Path("/agent/manuscripts/volume-02")
    for path in sorted(base.glob("*.md")):
        process_file(path)
    print("Trimmed duplicates in", len(list(base.glob("*.md"))), "files")


if __name__ == "__main__":
    main()
