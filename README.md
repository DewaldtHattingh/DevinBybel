# Devin se Bedtyd-Bybel

Afrikaans layered read-aloud story Bible for ages ~2–8.

**Mission:** Psalm 78:4 — tell the next generation the LORD’s deeds.  
**Anker:** God is getrou.

## Accuracy pipeline (do this before V3 rewrites)

Permanent Cursor rules live in [`.cursor/rules/`](.cursor/rules/).  
Validate: `python3 scripts/validate_manuscripts.py`  
Approved gate: `python3 scripts/validate_manuscripts.py --approved`  
See [`docs/CONTENT-PIPELINE.md`](docs/CONTENT-PIPELINE.md) and [`AGENTS.md`](AGENTS.md).

V2 stories now have **scaffold** `scripture_audit` blocks (`audit_status: needs_v3_repass`). Structural validation can pass; **approved** stays red until a real passage re-audit.

## Canonical manuscripts (v2)

**150 episodes** under [`manuscripts-v2/`](manuscripts-v2/), audited against **BibleSA AFR20** (full passages).

| Path | Content |
|------|---------|
| [`manuscripts-v2/`](manuscripts-v2/) | Full series |
| [`docs/STORY-INDEX-V2.md`](docs/STORY-INDEX-V2.md) | ID → file index |
| [`docs/COVERAGE-MATRIX.md`](docs/COVERAGE-MATRIX.md) | Episode map |
| [`docs/AFR20-AUDIT-PROTOCOL.md`](docs/AFR20-AUDIT-PROTOCOL.md) | How we verify against BibleSA |
| [`docs/AFR20-AUDIT-LOG.md`](docs/AFR20-AUDIT-LOG.md) | Audit batch status + sample fixes |
| [`docs/HOUSE-RULES.md`](docs/HOUSE-RULES.md) | Constitutional writing rules |

## Highlights vs old plan

- **Job** = 8 stories; **plagues** split; count = **150** from Scripture coverage  
- Factual audit: every story checked against AFR20 on BibleSA; quoted verses verified  

## Legacy

`manuscripts/volume-01` … `volume-05` — Draft v1 (127). Reference only.

## Download

`DevinBybel-full-v2.zip` at repo root (when present).

## Copyright

AFR20 © Bybelgenootskap van Suid-Afrika 2020. Private family use for Devin; check BSSA permissions before commercial distribution.
