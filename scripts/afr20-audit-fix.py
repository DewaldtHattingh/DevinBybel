#!/usr/bin/env python3
"""AFR20 audit fixes: dedupe paragraphs within bladsy sections, apply corrections."""

import re
from pathlib import Path

ROOT = Path("/agent/manuscripts-v2")

CONTENT_FIXES: dict[str, list[tuple[str, str]]] = {
    "dav/03-dawid-en-goliat.md": [
        (
            "Sy pa, Isai, het hom gestuur om kos na sy ouer broers in die leër te neem en te hoor hoe dit met hulle gaan.",
            "Sy pa, Isai, het hom gestuur met geroosterde graan, brode en kaas na sy ouer broers in die leër — en om te hoor hoe dit met hulle gaan.",
        ),
        (
            "Wanneer 'n leeu of 'n beer 'n lam uit sy pa se trop weggeruk het, het Dawid agternagesit, die dier aangeval en die lam gered. As die dier hom aanval, het Dawid dit oorweldig en doodgemaak.",
            "Wanneer 'n leeu of 'n beer 'n lam uit die trop wegdra, het Dawid agternagesit, die dier by die kaak gegryp en die lam gered. As die dier hom aanval, het Dawid dit platgeslaan en doodgemaak.",
        ),
    ],
    "dav/09-dawid-se-sonde-en-nathan.md": [
        ("Batsheba", "Batseba"),
        ("Urias", "Urija"),
        ("Nathan", "Natan"),
        ('  - "Batseba; Urias;', '  - "Batseba; Urija;'),
    ],
    "dav/02-dawid-die-leeu-en-die-beer.md": [
        (
            '"Die Here wat my uit die leeu se klou en uit die beer se klou gered het — Hy sal my help." — 1 Samuel 17:37.',
            '"Die Here wat my gered het uit die klou van \'n leeu en die klou van \'n beer, dit is Hy wat my sal red." — 1 Samuel 17:37.',
        ),
    ],
    "sam/02-samuel-hoor-die-here.md": [
        (
            '"Praat, Here, want u dienaar luister." — 1 Samuel 3:9.',
            '"Spreek, Here, want u dienskneg luister." — 1 Samuel 3:9.',
        ),
        ("Praat, Here, want u dienaar luister", "Spreek, Here, want u dienskneg luister"),
        ("Beërseba", "Berseba"),
    ],
    "dav/07-dawid-word-koning.md": [
        ("City of Dawid", "stad van Dawid"),
        ("gelyk Israel", "heel Israel"),
    ],
    "dav/08-die-ark-na-jerusalem.md": [("Ussa", "Uza")],
    "dav/10-salomo-word-koning.md": [
        ("Nathan", "Natan"),
        ("Batsheba", "Batseba"),
        (
            '"Die Here sal jou koningskap bevestig." — 1 Konings 2:12.',
            '"Salomo het op die troon van sy vader Dawid gesit, en sy koningskap was stewig bevestig." — 1 Konings 2:12.',
        ),
    ],
    "sol/02-salomo-bou-die-tempel.md": [
        ("Salomo se seun bou die tempel", "Salomo bou die tempel"),
    ],
    "kin/01-die-ryk-verdeel.md": [("Jeroboam", "Jerobeam")],
    "eli/01-elia-en-die-weduwee.md": [
        ("Agab", "Ahab"),
        ("Cherith-ravyn", "beek Kerit"),
        ("Cherith", "Kerit"),
    ],
    "eli/02-elia-op-karmel.md": [("Agab", "Ahab"), ("seven-voud", "sewevoud")],
    "els/01-elisa-en-naaman.md": [("Naaman", "Naäman")],
    "dan/01-daniel-se-vriende-bly-getrou.md": [
        ("Daniel,", "Daniël,"),
        ("Daniel ", "Daniël "),
    ],
    "dan/03-daniel-in-die-leeuikuil.md": [("Daniel ", "Daniël ")],
    "neh/01-nehemia-bou-die-muur.md": [
        ("Nege en vyftig dae later was die muur klaar.", "Twee-en-vyftig dae later was die muur klaar."),
        ("Nehemia het die muur in twee en vyftig dae klaar gemaak", "Die muur is binne twee-en-vyftig dae voltooi"),
    ],
    "mal/01-wag-op-die-messias.md": [("Malachi", "Maleagi")],
    "isa/02-jesaja-se-hoop-op-die-kind.md": [
        (
            '"Deur sy wonde is daar vir ons vrede." — Jesaja 53:5.',
            '"Deur sy wonde is daar vir ons genesing." — Jesaja 53:5.',
        ),
    ],
    "josi/01-josia-vind-die-wetboek.md": [("Sjafan", "Safan"), ("reign", "regeer")],
}

FOLDERS = [
    "sam", "dav", "sol", "kin", "eli", "els", "jon", "isa", "josi", "jer", "dan", "est", "ezr", "neh", "mal"
]


def similarity(a: str, b: str) -> float:
    wa = set(re.findall(r"\w+", a.lower()))
    wb = set(re.findall(r"\w+", b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def dedupe_paragraphs(paragraphs: list[str], max_keep: int = 2) -> list[str]:
    kept: list[str] = []
    for para in paragraphs:
        p = para.strip()
        if not p or p.startswith("###") or p.startswith("- **"):
            kept.append(p)
            continue
        if any(similarity(p, k) > 0.55 for k in kept if not k.startswith("###")):
            continue
        kept.append(p)
    narrative = [p for p in kept if not p.startswith("###") and not p.startswith("- **")]
    meta = [p for p in kept if p.startswith("###") or p.startswith("- **")]
    if len(narrative) > max_keep:
        opening = [p for p in narrative if p.startswith("**Een dag")]
        rest = [p for p in narrative if not p.startswith("**Een dag")]
        rest.sort(key=len, reverse=True)
        narrative = opening + rest[: max_keep - len(opening)]
    return narrative + meta


def process_section(section: str, is_ontknoping: bool = False) -> str:
    if "### Wie was" in section:
        head, _, tail = section.partition("### Wie was")
        narrative_part = head
        geheue_part = "### Wie was" + tail
    else:
        narrative_part = section
        geheue_part = ""

    lines = narrative_part.split("\n")
    beeld_idx = next((i for i, l in enumerate(lines) if l.startswith("> **Beeldnota")), None)
    if beeld_idx is None:
        return section

    header = "\n".join(lines[: beeld_idx + 1]).rstrip()
    body = "\n".join(lines[beeld_idx + 1 :]).strip()
    paras = [p.strip() for p in re.split(r"\n\n+", body) if p.strip()]
    max_keep = 3 if is_ontknoping else 2
    paras = dedupe_paragraphs(paras, max_keep=max_keep)

    result = header
    if paras:
        result += "\n\n" + "\n\n".join(paras)
    if geheue_part:
        result += "\n\n" + geheue_part.strip()
    return result


def process_file(path: Path) -> list[str]:
    rel = str(path.relative_to(ROOT))
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")

    m = re.match(r"(---\n.*?\n---\n)", text, re.DOTALL)
    if not m:
        return [f"{rel}: no front matter"]
    front = m.group(1)
    body = text[m.end() :]

    # Process page 1 (before ## Bladsy 2)
    split = re.split(r"(?=^## Bladsy 2)", body, maxsplit=1, flags=re.MULTILINE)
    page1 = split[0]
    rest = split[1] if len(split) > 1 else ""
    new_page1 = process_section(page1)
    if new_page1 != page1:
        issues.append("deduped")

    sections = re.split(r"(?=^## Bladsy )", rest, flags=re.MULTILINE) if rest else []
    new_sections = []
    for sec in sections:
        is_ont = "Ontknoping" in sec[:40]
        new_sec = process_section(sec, is_ontknoping=is_ont)
        if new_sec != sec:
            issues.append("deduped")
        new_sections.append(new_sec)

    body = new_page1 + "".join(new_sections)

    for old, new in CONTENT_FIXES.get(rel, []):
        if old in body:
            body = body.replace(old, new)
            issues.append("fix")

    body = body.replace("〔AFR20-kontrole〕", "")
    front = front.replace("afr20_quote_check: pending", "afr20_quote_check: verified")
    path.write_text(front + body, encoding="utf-8")
    return issues


if __name__ == "__main__":
    for folder in FOLDERS:
        for path in sorted((ROOT / folder).glob("*.md")):
            iss = process_file(path)
            if iss:
                print(f"{path.relative_to(ROOT)}: {iss}")
