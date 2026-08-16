#!/usr/bin/env python3
"""Trim redundant filler from v2 gospels manuscripts to hit ~500-650 words."""

import re
from pathlib import Path

ROOT = Path("/agent/manuscripts-v2")
FOLDERS = ["jes", "pas", "act", "epi", "rev"]

# Generic volume-05 filler lines to remove entirely
FILLER_PATTERNS = [
    r"\nDit was lank, lank gelede — maar hierdie storie is nog steeds vir ons vanaand\.\n",
    r"\nDie mense het geluister en onthou\. Dit was 'n dag wat hulle nooit sou vergeet nie\.\n",
    r"\nEn weet jy wat toe gebeur het\? Die Here was naby — selfs toe dit moeilik gelyk het\.\n",
    r"\nDie dissipels het gekyk en geluister\. Alles het presies so gebeur soos God belowe het\.\n",
    r"\nDie Here was by hulle — selfs toe die pad swaar was\. En ons weet: God vergeet sy kinders nooit\.\n",
    r"\n\nOns kan vanaand rustig wees, want God se storie eindig altyd in sy goeie hande\.\n",
    r"\nOns kan nou rustig wees\. Die storie is vertel, en die Here bly by ons — vanaand, môre, en altyd\.\n",
]


def trim_page_bridges(body: str) -> str:
    """Remove trailing single-paragraph bridges before --- page breaks."""
    pages = re.split(r"(---\n)", body)
    out = []
    for i, chunk in enumerate(pages):
        if chunk == "---\n":
            out.append(chunk)
            continue
        # Within a page section, if last non-empty block is a single short paragraph
        # after a blank line and the page has 3+ paragraphs, drop the last one
        parts = chunk.rstrip().split("\n\n")
        if len(parts) >= 3:
            last = parts[-1].strip()
            # Bridge paragraphs: no markdown headers, no beeldnota, relatively short
            if (
                last
                and not last.startswith("#")
                and not last.startswith(">")
                and not last.startswith("!")
                and not last.startswith("**Een dag")
                and len(last.split()) < 25
                and not last.startswith("En weet jy")
            ):
                parts = parts[:-1]
        out.append("\n\n".join(parts))
        if chunk.endswith("\n") and not out[-1].endswith("\n"):
            out[-1] += "\n"
    return "".join(out)


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    fm_end = text.find("---", 3) + 3
    front = text[: fm_end + 1]
    body = text[fm_end + 1 :]

    for pat in FILLER_PATTERNS:
        body = re.sub(pat, "\n", body)

    body = trim_page_bridges(body)
    # Collapse triple+ newlines
    body = re.sub(r"\n{3,}", "\n\n", body)

    new_text = front + body
    path.write_text(new_text, encoding="utf-8")
    words = len(re.findall(r"\b\w+\b", body))
    return words


def main():
    for folder in FOLDERS:
        for p in sorted((ROOT / folder).glob("*.md")):
            w = process_file(p)
            flag = " !" if w > 660 or w < 490 else ""
            print(f"{w:4d} {p.name}{flag}")


if __name__ == "__main__":
    main()
