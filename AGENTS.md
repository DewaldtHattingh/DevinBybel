# Agent instructions — Devin se Bedtyd-Bybel

Biblical accuracy is the highest priority. Read `.cursor/rules/biblical-accuracy.mdc` and `.cursor/rules/writing-style.mdc` before any manuscript edit.

## Pipeline

`Bible source → coverage matrix → manuscript → automated audit → Scripture audit → approved manuscript → image spec → images → Word/PDF`

Do **not** rewrite stories in bulk until `python3 scripts/validate_manuscripts.py` is green for the files you touch, and `--approved` is reserved for stories that have a real passage re-audit.

## Canonical paths

- Stories: `manuscripts-v2/`
- Matrix: `docs/COVERAGE-MATRIX.md`
- Rules: `docs/HOUSE-RULES.md`
- Validator: `scripts/validate_manuscripts.py`
- AFR20 protocol: `docs/AFR20-AUDIT-PROTOCOL.md`
- Local Bible text (if legally permitted): `reference/` — **do not commit** unlicensed full AFR20

## After editing a story

1. Second PASSAGE AUDIT against the full assigned AFR20 passage.  
2. Update `scripture_audit`.  
3. Run `python3 scripts/validate_manuscripts.py --path <file>`.
