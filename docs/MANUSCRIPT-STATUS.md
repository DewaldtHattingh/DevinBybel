# Manuscript status

## Canonical: v2 — COMPLETE

- **Location:** `manuscripts-v2/`
- **Count:** 150 episodes (matches locked coverage matrix IDs)
- **Index:** [`STORY-INDEX-V2.md`](STORY-INDEX-V2.md)

## Legacy: Draft v1

- **Location:** `manuscripts/volume-01` … `volume-05`
- **Count:** 127 (old hard-cap plan)
- **Use:** reference / comparison only

## Accuracy pipeline (2026-08-16)

- Cursor rules: `.cursor/rules/biblical-accuracy.mdc`, `writing-style.mdc`
- Validator: `scripts/validate_manuscripts.py` — **150/150 structural**; **0/150 `--approved`** (intentional)
- Each v2 file has scaffold `scripture_audit` with `audit_status: needs_v3_repass`
- Next: V3 systematic re-audit (read full AFR20 passage → fill checklist → `--approved`)

## Still open (production)

1. AFR20 word-for-word verse verification (`〔AFR20-kontrole〕`)
2. Illustration pass from Beeldnotas
3. Word/PDF layout
4. Optional read-aloud timing with Devin
