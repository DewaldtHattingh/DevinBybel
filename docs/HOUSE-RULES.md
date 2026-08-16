# Devin se Bedtyd-Bybel — Huisreëls (grondwet)

## Mission

> “We will tell the next generation the praiseworthy deeds of the LORD, his power, and the wonders he has done.” — Psalm 78:4 〔AFR20-kontrole〕

**Afrikaans anker vir die projek:** God is getrou.

## Constitutional rules (non-negotiable)

1. **Biblical facts are fixed. Storytelling is flexible. Theology must arise from the passage. Illustrations may clarify, but never rewrite, Scripture.**
2. **We never remove a biblical fact merely because it is uncomfortable, unusual, violent or difficult for a child.** We adapt *how* it is explained and illustrated — not *whether* it happened.
3. **Do not remove the biblical event; remove unnecessary graphic detail.**
4. **Tell less per story, but tell what you choose properly.** A story = one memorable causal episode — not “the life of Moses / Dawid / Simson.”
5. **Completeness beats round numbers.** There is **no hard story-count target**. The coverage matrix decides whether we end at 127, 145, 170, or more. Never combine episodes only to hit a quota.

## Series identity

Layered Afrikaans read-aloud story Bible for ages ~2–8: simple enough for a toddler via pictures and rhythm; accurate enough that a seven- or eight-year-old still learns real names, places, causes and consequences.

## Manuscript locations

- **v2 (canonical):** `manuscripts-v2/<section>/` using matrix IDs (`GEN-01`, `JOB-02`, …)
- **v1 (legacy):** `manuscripts/volume-0X/` — reusable only; do not treat as final

## Per-story architecture

- Standard unit: **6 designed pages** (4 only for genuinely short episodes).
- Target: **~500–650 total words** (production target, not an attention-science claim).
- Rhythm: **wonder → orientation → problem → rising action → climax → peaceful landing**
- Middle may be dramatic (Red Sea, Goliath, lions, storm). **Last 30–60 seconds descend** emotionally — bedtime, not an action cartoon.

### Opening (every story)

> **Een dag, lank, lank gelede…**

Then locate people/place/situation with concrete nouns.

### Closing anchors (print on tonight’s page)

1. **Wie was in hierdie verhaal?** — 3–5 names, each with a 5–12 word role  
2. **Wat leer ons?** — one lesson from *this* passage (never generic moralism / “believe in yourself”)  
3. **Vers om te onthou** — short verse/excerpt; `〔AFR20-kontrole〕` until verified against Die Bybel 2020  
4. **Onthou jy?** — three **retrieval questions** (person / concrete detail / meaning-cause)

### Bedtime ritual (how Onthou jy? is used)

- **Onthou jy?** is **optional during tonight’s reading** if Devin is tired.
- Preferred use: ask tonight’s three questions **tomorrow evening**, *before* the next story:

> “Voor ons vanaand se storie lees — onthou jy wat gister gebeur het?”

Then: **Een dag, lank, lank gelede…**

## Drafting tags (internal only — never print in the book)

While drafting, tag every sentence:

| Tag | Meaning | Allowed? |
|-----|---------|----------|
| **B** | Explicit biblical fact | Yes — state plainly |
| **C** | Safe connective narration joining explicit facts | Yes — no hidden knowledge |
| **Q** | Direct Scripture quotation (checked against AFR20) | Yes — never invent quote text |
| *(none / other)* | Invented psychology, weekday, weather-as-fact, unspoken motives | **Challenge and usually delete** |

Examples:

- **B** — Dawid het vyf gladde klippe gekies.  
- **C** — Toe het Dawid na Goliat toe gegaan.  
- **Forbidden** — Dawid se maag het gedraai van vrees… *(unless Scripture says so)*

**Never put quotation marks around words we created.**

## Violence & hard passages

Narration keeps materially important violence/judgement/death when Scripture includes it.  
Illustration stays non-graphic for ages 2–8 (no gore, no severed-head close-ups, restrained crucifixion).

## Illustration direction (when art begins)

Warm painterly storybook realism; gouache/watercolour-like texture; historically grounded; natural proportions; clear focal action; no VeggieTales / Marvel / photorealistic Passion extremes.

**Forbidden inventions unless the passage warrants them:** glowing Samson, magical aura David, automatic halos, blond winged angels by default, old man in the clouds as God, superhero physique as default.

## Translation baseline

- Primary: **Die Bybel 2020 (AFR20)** via BibleSA chapter pages (`https://www.biblesa.co.za/bible/AFR20/…`)  
- Audit every story against the **full passage**, not only the memory verse — see [`AFR20-AUDIT-PROTOCOL.md`](AFR20-AUDIT-PROTOCOL.md)  
- Secondary clarity: *Die Bybel vir almal* / AFR83 — never silently merge editions inside quotes  
- Commercial use: check Bible Society of South Africa quotation permissions before publishing  

## Recurring footholds (only when truthful to the passage)

- Een dag, lank, lank gelede…
- En weet jy wat toe gebeur het?
- Maar die Here het hom/haar/hulle nie vergeet nie.
- Die Here was by hom/haar/hulle.

## File naming (after matrix lock)

`manuscripts/<section>/<NN>-<slug>.md`  
Story IDs come from the matrix (`GEN-01`, `EXO-12`, `JOB-06`, …), not from a forced volume quota.
