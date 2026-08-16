# Story template (v3 pipeline)

Copy this structure. `scripture_audit` is **internal** — do not print it in the book.

```markdown
---
story_id: DAV-03
title: "Dawid en Goliat"
section: dav
pages: 6
primary_passage: "1 Sam. 17"
must_include:
  - "…"
deferred_to: []
continuity_from: DAV-02
continuity_to: DAV-04
theology_centre: "Die oorlog behoort aan die Here"
violence_note: "onthoofing in teks; beeld nie-grafies"
afr20_quote_check: AFR20_QUOTE_CHECK_REQUIRED
scripture_audit:
  primary_passage: "1 Samuel 17"
  passage_read: false
  context_read: false
  required_details:
    - Saul
    - Jesse sends David
    - Goliath's challenge
    - lion
    - bear
    - David credits God
    - Saul's armour
    - armour rejected
    - staff
    - five smooth stones
    - shepherd's bag
    - sling
    - Goliath's shield bearer
    - stone strikes forehead
    - Goliath falls face down
    - Goliath's sword
    - Goliath killed/beheaded
    - Philistines flee
  unsupported_details: []
  chronology_check: pending
  people_check: pending
  numbers_check: pending
  theology_check: pending
  direct_quotes_verified: false
  afr20_quote_check: pending
  audit_status: needs_v3_repass
---

# Titel

**Primêre gedeelte:** …  
**Verhaal-ID:** …

## Bladsy 1 — Opening
![Beeld: opening](../../assets/images/ID-p1.png)
> **Beeldnota:** …

**Een dag, lank, lank gelede,** …

… pages 2–5 …

## Bladsy 6 — Geheue
### Wie was in hierdie verhaal?
### Wat leer ons?
### Vers om te onthou
“…” — 1 Samuel 17:47 (AFR20). 〔AFR20-kontrole〕
### Onthou jy?
```

After editing: `python3 scripts/validate_manuscripts.py --path <file>`  
Approved only when: `python3 scripts/validate_manuscripts.py --approved --path <file>`
