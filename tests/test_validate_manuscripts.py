import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_manuscripts import validate_data, parse_frontmatter, validate_file  # noqa: E402


MINIMAL_OK = """---
story_id: TST-01
title: "Toets"
primary_passage: "1 Sam 17"
afr20_quote_check: pending
scripture_audit:
  primary_passage: "1 Samuel 17"
  passage_read: false
  context_read: false
  required_details:
    - Saul
  unsupported_details: []
  chronology_check: pending
  people_check: pending
  numbers_check: pending
  theology_check: pending
  direct_quotes_verified: false
  afr20_quote_check: pending
  audit_status: needs_v3_repass
---

# Toets

## Bladsy 1 — Opening

![Beeld: opening](x-p1.png)

**Een dag, lank, lank gelede,** was daar 'n vallei.

## Bladsy 2

![Beeld: a](x-p2.png)

Teks.

## Bladsy 3

![Beeld: b](x-p3.png)

Teks.

## Bladsy 4

![Beeld: c](x-p4.png)

Teks.

## Bladsy 5

![Beeld: d](x-p5.png)

Teks.

## Bladsy 6 — Geheue

![Beeld: e](x-p6.png)

### Wie was in hierdie verhaal?

- **Saul** — koning.

### Wat leer ons?

Die oorlog behoort aan die Here.

### Vers om te onthou

“Die oorlog behoort aan die Here.” — 1 Samuel 17:47. 〔AFR20-kontrole〕

### Onthou jy?

1. Wie?
"""


def test_structural_ok():
    data, body = parse_frontmatter(MINIMAL_OK)
    assert validate_data(data, body, approved=False) == []


def test_approved_rejects_scaffold():
    data, body = parse_frontmatter(MINIMAL_OK)
    errors = validate_data(data, body, approved=True)
    assert any("approved gate" in e for e in errors)


def test_missing_audit():
    text = MINIMAL_OK.replace("scripture_audit:\n", "not_audit:\n")
    # still has keys under not_audit — strip whole block instead
    text = """---
story_id: TST-01
title: "Toets"
primary_passage: "1 Sam 17"
afr20_quote_check: pending
---

**Een dag, lank, lank gelede,** x
### Wie was in hierdie verhaal?
### Wat leer ons?
### Vers om te onthou
“x” — 1:1
### Onthou jy?
![Beeld: a](1)
![Beeld: b](2)
![Beeld: c](3)
![Beeld: d](4)
![Beeld: e](5)
![Beeld: f](6)
"""
    data, body = parse_frontmatter(text)
    errors = validate_data(data, body, approved=False)
    assert any("scripture_audit" in e for e in errors)


def test_duplicate_paragraphs():
    data, body = parse_frontmatter(MINIMAL_OK)
    repeated = (
        "Dieselfde lang sin word hier herhaal vir niks anders as lengte.\n\n"
        "Dieselfde lang sin word hier herhaal vir niks anders as lengte."
    )
    body = body + "\n\n" + repeated + "\n\n" + repeated
    errors = validate_data(data, body, approved=False)
    assert any("duplicate" in e for e in errors)


def test_approved_gold_standard():
    data, body = parse_frontmatter(MINIMAL_OK)
    data["afr20_quote_check"] = "verified"
    data["scripture_audit"].update(
        {
            "passage_read": True,
            "context_read": True,
            "chronology_check": "passed",
            "people_check": "passed",
            "numbers_check": "passed",
            "theology_check": "passed",
            "direct_quotes_verified": True,
            "afr20_quote_check": "verified",
            "audit_status": "approved",
            "unsupported_details": [],
            "required_details": ["Saul", "vyf gladde klippe"],
        }
    )
    assert validate_data(data, body, approved=True) == []


def test_validate_file_missing(tmp_path):
    p = tmp_path / "x.md"
    p.write_text("no frontmatter", encoding="utf-8")
    errors = validate_file(p, approved=False)
    assert errors
