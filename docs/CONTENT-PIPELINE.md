# Content pipeline

```text
Bible source (AFR20 / BibleSA or licensed local copy)
        ↓
Coverage matrix          docs/COVERAGE-MATRIX.md
        ↓
Manuscript               manuscripts-v2/<section>/<nn>-<slug>.md
        ↓
Automated audit          scripts/validate_manuscripts.py
        ↓
Scripture audit          scripture_audit: in YAML (not printed)
        ↓
Approved manuscript      --approved gate
        ↓
Image specification      Beeldnota + later image metadata
        ↓
Images                   assets/images/
        ↓
Word / PDF               (layout later)
```

## Automated reject conditions

`python3 scripts/validate_manuscripts.py` fails if any of:

- required frontmatter missing (`story_id`, `title`, `primary_passage`, `afr20_quote_check`)
- `scripture_audit` missing or incomplete
- opening line missing
- closing anchors missing
- consecutive duplicate paragraphs (padding)
- quoted verse without reference
- `afr20_quote_check` not in `pending` | `verified` | `AFR20_QUOTE_CHECK_REQUIRED`

`--approved` additionally requires:

- `scripture_audit.passage_read: true`
- `scripture_audit.context_read: true`
- `scripture_audit.chronology_check: passed`
- `scripture_audit.people_check: passed`
- `scripture_audit.numbers_check: passed`
- `scripture_audit.theology_check: passed`
- `scripture_audit.unsupported_details: []`
- `scripture_audit.direct_quotes_verified: true`
- `afr20_quote_check: verified`
- `scripture_audit.audit_status: approved`

V2 manuscripts currently have **scaffold** audits (`audit_status: needs_v3_repass`) so the structural validator can run, while `--approved` stays red until a real V3 passage re-audit.

## Local Bible reference

If legally permissible, place AFR20 chapter files under `reference/afr20/` for offline checks.  
**Do not** commit unlicensed full-Bible dumps. **Do not** instruct models to paste long AFR20 passages into stories.
