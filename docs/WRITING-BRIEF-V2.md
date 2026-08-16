# V2 writing brief (agents)

Write Afrikaans bedtime manuscripts for Devin (ages 2–8).

## Sources of truth

1. `/agent/docs/COVERAGE-MATRIX.md` — every ID, must-include, theology centre  
2. `/agent/docs/HOUSE-RULES.md` — constitutional rules  

## Output path

`/agent/manuscripts-v2/<folder>/<NN>-<slug>.md`

Folder map: gen, job, abr, jos, exo, num, deu, jsh, jdg, rut, sam, dav, sol, kin, eli, els, jon, isa, josi, jer, dan, est, ezr, neh, mal, jes, pas, act, epi, rev

Examples:
- `manuscripts-v2/gen/01-die-skepping.md` (GEN-01)
- `manuscripts-v2/job/02-satan-daag-job-uit.md` (JOB-02)
- `manuscripts-v2/exo/04-bloed-paddas-en-muggies.md` (EXO-04)

## Required structure (every file)

```markdown
---
story_id: XXX-NN
title: "…"
section: …
pages: 6
primary_passage: "…"
must_include: […]
theology_centre: "…"
continuity_from: …
continuity_to: …
afr20_quote_check: pending
---

# Title
**Primêre gedeelte:** …
**Verhaal-ID:** …

## Bladsy 1 — Opening
![Beeld: opening](../../assets/images/XXX-NN-p1.png)
> **Beeldnota:** …
**Een dag, lank, lank gelede,** …

… pages 2–5 …

## Bladsy 6 — Geheue
… Wie was / Wat leer ons / Vers 〔AFR20-kontrole〕 / Onthou jy? (3 questions)
```

## Hard rules

- ~500–650 Afrikaans words (narrative + memory)
- No invented psychology; no fake quotes
- Keep hard biblical facts in narration; Beeldnota non-graphic
- Theology from passage (never “believe in yourself”)
- Job: NOT prosperity gospel; friends corrected; Job prays for them
- Plagues: each EXO-04…07 only its assigned plagues
- Dawid & Goliat: full chain including lion/bear recollection, five stones, sword, beheading in text
- No glowing Samson in Beeldnota
