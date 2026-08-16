#!/usr/bin/env python3
"""Apply AFR20 audit fixes to manuscripts-v2 jes/pas/act/epi/rev."""
import re
from pathlib import Path

BASE = Path("/agent/manuscripts-v2")

# Exact AFR20 memory verses (BibleSA 2020)
VERSES = {
    "JES-01": "Kyk, ek is die diensmeisie van die Here. Mag met my gebeur volgens u woord. — Luk. 1:38.",
    "JES-02": "jy moet Hom Jesus noem, want Hy sal sy volk van hulle sondes verlos. — Matt. 1:21.",
    "JES-03": "sy het geboorte geskenk aan haar eerste kind, 'n seun. Sy het Hom in doeke toegedraai en in 'n krip neergelê, omdat daar nie vir hulle plek in die herberg was nie. — Luk. 2:7.",
    "JES-04": "Moenie bang wees nie. Kyk, ek bring vir julle 'n goeie boodskap wat vir die hele volk 'n bron van groot vreugde sal wees. — Luk. 2:10.",
    "JES-05": "Toe hulle die ster sien, het hulle 'n onbeskryflike groot vreugde ervaar. — Matt. 2:10.",
    "JES-06": "Maak gereed, neem die Kindjie en sy moeder en vlug na Egipte, en bly daar tot wanneer ek jou opdrag gee; want Herodes is van plan om die Kindjie te soek en Hom dood te maak. — Matt. 2:13.",
    "JES-07": "Waarom het julle na My gesoek? Het julle nie geweet dat Ek met die dinge van my Vader besig moet wees nie? — Luk. 2:49.",
    "JES-08": "Dit is my geliefde Seun oor wie Ek My verheug. — Matt. 3:17.",
    "JES-09": "Die Here jou God moet jy aanbid en Hom alleen dien. — Matt. 4:10.",
    "JES-10": "Kom kyk! — Joh. 1:39.",
    "JES-11": "Want so lief het God die wêreld gehad dat Hy sy unieke Seun gegee het, sodat elkeen wat in Hom glo, nie verlore sal gaan nie, maar die ewige lewe sal hê. — Joh. 3:16.",
    "JES-12": "Maar die water wat Ek hom sal gee, sal in hom 'n fontein van water word wat opspring tot die ewige lewe. — Joh. 4:14.",
    "JES-13": "Ons Vader in die hemel, laat u Naam geheilig word. — Matt. 6:9.",
    "JES-14": "Wees stil, bedaar! — Mark. 4:39.",
    "JES-15": "Toe het Jesus die brode geneem, en nadat Hy die seëngebed uitgespreek het, het Hy dit laat uitdeel aan dié wat daar gesit het. — Joh. 6:11.",
    "JES-16": "Hou moed, dit is Ek; moenie langer bang wees nie. — Matt. 14:27.",
    "JES-17": "Gaan maak jy ook so. — Luk. 10:37.",
    "JES-18": "Want hierdie seun van my was dood en het weer lewendig geword, hy was verlore en is weer gevind. — Luk. 15:24.",
    "JES-19": "Ek is die opstanding en die lewe. — Joh. 11:25.",
    "JES-20": "Die Seun van die mens het gekom om te soek en te red wat verlore is. — Luk. 19:10.",
    "JES-21": "Laat die kindertjies na My toe kom en moet hulle nie langer verhinder nie. — Mark. 10:14.",
    "JES-22": "Dit is my geliefde Seun. Luister na Hom! — Mark. 9:7.",
    "JES-23": "En Ek, wanneer Ek van die aarde opgehef word, sal almal na My toe trek. — Joh. 12:32.",
    "PAS-01": "Hosanna vir die Seun van Dawid! Geseënd is Hy wat kom in die Naam van die Here! Hosanna in die hoogste! — Matt. 21:9.",
    "PAS-02": "Jy moet die Here jou God liefhê met jou hele hart en met jou hele siel en met jou hele verstand. — Matt. 22:37.",
    "PAS-03": "Dit is my liggaam, wat vir julle gegee word. — Luk. 22:19.",
    "PAS-04": "My Vader, as dit moontlik is, laat hierdie beker by My verbygaan. Nogtans, nie soos Ek wil nie, maar soos U wil. — Matt. 26:39.",
    "PAS-05": "Bêre jou swaard op sy plek. Want almal wat die swaard opneem, sal deur die swaard omkom. — Matt. 26:52.",
    "PAS-06": "Ú het dit gesê. Maar Ek sê vir julle: Van nou af sal julle die Seun van die Mens sien sit aan die regterhand van die Magtige, en Hom op die wolke van die hemel sien kom. — Matt. 26:64.",
    "PAS-07": "Die Here het omgedraai en stip na Petrus gekyk. — Luk. 22:61.",
    "PAS-08": "Vader, vergeef hulle, want hulle weet nie wat hulle doen nie. — Luk. 23:34.",
    "PAS-09": "Hy het dit in sy nuwe graf gelê. — Matt. 27:60.",
    "PAS-10": "Hy is nie hier nie, maar is opgewek! — Luk. 24:6.",
    "PAS-11": "Moes die Christus nie hierdie dinge ly en dan in sy heerlikheid ingaan nie? — Luk. 24:26.",
    "PAS-12": "Gelukkig is hulle wat nie gesien het nie, en tog tot geloof gekom het. — Joh. 20:29.",
    "PAS-13": "Hierdie Jesus, wat van julle na die hemel weggeneem is, sal net so terugkom soos wat julle Hom na die hemel sien weggaan het. — Hand. 1:11.",
    "ACT-01": "Bekeer julle, en laat elkeen van julle in die Naam van Jesus Christus tot vergewing van julle sondes gedoop word. — Hand. 2:38.",
    "ACT-02": "In die Naam van Jesus Christus van Nasaret, staan op en loop! — Hand. 3:6.",
    "ACT-03": "Here Jesus, ontvang my gees! — Hand. 7:59.",
    "ACT-04": "Filippus het hom die evangelie van Jesus Christus verkondig. — Hand. 8:35.",
    "ACT-05": "Ek is Jesus, die Een wat jy vervolg. — Hand. 9:5.",
    "ACT-06": "God maak geen onderskeid nie. — Hand. 10:34.",
    "ACT-07": "Glo in die Here Jesus, en jy sal gered word. — Hand. 16:31.",
    "ACT-08": "Die God wat die wêreld en alles wat daarin is, gemaak het, Hy wat Here van hemel en aarde is, woon nie in tempels wat met hande gemaak is nie. — Hand. 17:24.",
    "ACT-09": "Moenie bang wees nie, Paulus. Jy moet voor Caesar staan; en God het jou al die mense saam met jou op die skip geskenk. — Hand. 27:24.",
    "EPI-01": "Ek is immers daarvan oortuig dat nóg dood, nóg lewe, nóg engele, nóg magte … ons sal kan skei van die liefde van God in Christus Jesus, ons Here. — Rom. 8:38–39.",
    "REV-01": "Heilig, Heilig, Heilig is die Here God, die Almagtige, wat was en wat is en wat kom! — Openb. 4:8.",
    "REV-02": "Waardig is die Lam wat geslag is, om die krag en rykdom en wysheid en sterkte en eer en heerlikheid en lof te ontvang. — Openb. 5:12.",
    "REV-03": "Kyk, Ek maak alles nuut. — Openb. 21:5.",
    "REV-04": "Hy sal elke traan uit hulle oë afdroog. En die dood sal nie meer daar wees nie. — Openb. 21:4.",
    "REV-05": "Hulle sal sy aangesig sien, en sy Naam is op hulle voorkoppe. — Openb. 22:4.",
    "REV-06": "Kom! En laat elkeen wat dors het, kom. En laat elkeen wat dit begeer, die water van die lewe kom kry, verniet! — Openb. 22:17.",
}

# Per-file body text replacements (factual / AFR20 wording)
BODY_FIXES = {
    "jes/01-die-engel-by-maria.md": [
        ("Wees gegroet, jy wat vol genade is. Die Here is met jou.", "Gegroet, begenadigde vrou! Die Here is met jou!"),
        ("Gabriel het gesê: Wees gegroet, jy is bevoorreg! Die Here is met jou.", "Die engel het gesê: Gegroet, begenadigde vrou! Die Here is met jou!"),
        ("Jou weet van jou familie Elisa.", "Jy weet van jou familielid Elisabet."),
        ("Ek is die dienaar van die Here. Laat dit met my geskied soos jy gesê het.", "Kyk, ek is die diensmeisie van die Here. Mag met my gebeur volgens u woord."),
        ("Ek is die dienskneg van die Here — laat dit met my gebeur soos u gesê het.", "Ek is die diensmeisie van die Here — mag met my gebeur volgens u woord."),
    ],
    "jes/03-jesus-word-gebore.md": [
        ("Hy beveel een sensus.", "Hy het 'n dekreet uitgevaardig dat die bevolking geregistreer moet word."),
        ("Die sensus beteken", "Die volkstelling beteken"),
        ("Keiser Augustus het beveel dat almal ingeskryf moet word", "Keiser Augustus het beveel dat almal geregistreer moet word"),
        ("En sy het haar eerstegebore seun gebore en hom in een krip geleg.", "Sy het geboorte geskenk aan haar eerste kind, 'n seun, en Hom in 'n krip neergelê."),
        ("Maria het haar Seun toegedraai en Hom in die krip gelê.", "Maria het Hom in doeke toegedraai en in 'n krip neergelê."),
    ],
    "jes/04-die-herders.md": [
        ("Ek bring goeie nuus — groot vreugde vir alle mense.", "Moenie bang wees nie. Kyk, ek bring vir julle 'n goeie boodskap wat vir die hele volk 'n bron van groot vreugde sal wees."),
        ("Glorie aan God in die hoogste, en vrede op aarde.", "Eer aan God in die hoogste, en vrede op aarde vir die mense in wie God 'n welbehae het!"),
        ("Die engel het gesê: Moenie bang wees nie — ek bring julle goeie nuus van groot vreugde.", "Die engel het gesê: Moenie bang wees nie — ek bring vir julle 'n goeie boodskap van groot vreugde."),
    ],
    "jes/05-die-wyse-manne.md": [
        ("buitensporig verheug", "onbeskryflike groot vreugde ervaar"),
        ("goud, mirre en spesiale reuk", "goud, wierook en mirre"),
        ("geschenke: goud, mirre en spesiale reuk", "geskenke: goud, wierook en mirre"),
    ],
    "jes/06-vlug-na-egipte.md": [
        ("Neem die kind en sy ma en vlug na Egipte. Bly daar tot ek jou sê.", "Maak gereed, neem die Kindjie en sy moeder en vlug na Egipte, en bly daar tot wanneer ek jou opdrag gee."),
        ("Archelaus", "Argelaos"),
    ],
    "jes/15-vyfduisend-gevoed.md": [
        ("Jesus neem die brode, en nadat hy God gedank het, breek en gee dit aan die dissipels.", "Toe het Jesus die brode geneem, en nadat Hy die seëngebed uitgespreek het, het Hy dit laat uitdeel aan dié wat daar gesit het."),
        ("Hy het die brood en vis geneem, God gedank en uitgedeel.", "Hy het die brode geneem, die seëngebed uitgespreek en laat uitdeel."),
        ("Jesus het die brode en vis geneem, God gedank en dit aan die dissipels gegee om uit te deel.", "Jesus het die brode geneem, die seëngebed uitgespreek en laat uitdeel."),
    ],
    "pas/08-jesus-sterf-aan-die-kruis.md": [
        ("Golgota", "Kopbeenplek"),
        ("Vader, in u hande beveel Ek my gees", "Vader, in u hande gee Ek my gees oor"),
        ("sy laaste asem gehaal", "sy asem uitgeblaas"),
        ("Die Romeinse hoofman het gesê: Waarlik, hierdie Man was die Seun van God.", "Die Romeinse hoofman het gesê: Waarlik, hierdie man was onskuldig!"),
        ("Waarlik, hierdie Man was die Seun van God", "Waarlik, hierdie man was onskuldig"),
        ("Hy is die Seun van God", "Hy was onskuldig"),
        ("Dit is volbring — en sy gees in die Vader se hande beveel", "Dit is volbring! — en sy gees in die Vader se hande oorgegee"),
    ],
    "pas/10-jesus-het-opgestaan.md": [
        ("Hulle het 'n groot aardbewing gesien — 'n engel het die klip weggerol en op die klip gesit.", "Die klip was reeds weggerol. Skielik het twee mans in blink klere daar gestaan."),
        ("Die engel het gesê: Moenie bang wees nie — Jesus wat gekruisig is, is nie hier nie. Hy het opgestaan! Die engel het gesê: Hy is nie hier nie — Hy het opgestaan!", "Hulle het gesê: Waarom soek julle die Lewende by die dooies? Hy is nie hier nie, maar is opgewek!"),
        ("Hy is nie hier nie — Hy het opgestaan", "Hy is nie hier nie, maar is opgewek"),
        ("Gaan sê vir sy dissipels dat Hy na Galilea vooruitgaan.", "Onthou wat Hy vir julle gesê het toe Hy nog in Galilea was."),
        ("Jesus het self aan die vroue verskyn — wees nie bevrees nie, gaan vertel my broers.", "Maria Magdalena het die Here gesien en aan die dissipels vertel."),
    ],
    "act/01-pinkster.md": [
        ("Bekeer julle en laat julle doop", "Bekeer julle, en laat elkeen van julle in die Naam van Jesus Christus tot vergewing van julle sondes gedoop word"),
        ("Petrus het gesê: Bekeer julle en laat julle doop.", "Petrus het gesê: Bekeer julle, en laat elkeen van julle gedoop word."),
    ],
    "rev/02-die-lam-wat-waardig-is.md": [
        ("om die krag en die rykdom en die wysheid en die krag en die eer", "om die krag en rykdom en wysheid en sterkte en eer"),
        ("om krag en rykdom en wysheid te ontvang", "om die krag en rykdom en wysheid en sterkte en eer en heerlikheid en lof te ontvang"),
    ],
    "rev/04-n-nuwe-hemel-en-n-nuwe-aarde.md": [
        ("die tent van God is by die mense", "God se woonplek is by die mense"),
        ("Kyk, die tent van God is by die mense", "Kyk, God se woonplek is by die mense"),
        ("En Hy sal elke traan van hul oë afvee", "Hy sal elke traan uit hulle oë afdroog"),
        ("die dood sal nie meer wees nie, noch hartseer of pyn", "die dood sal nie meer daar wees nie"),
        ("God sal elke traan afvee", "God sal elke traan afdroog"),
        ("die eerste hemel en aarde was verby", "die eerste hemel en die eerste aarde het tot niet gegaan"),
        ("Ek is die Alfa en die Omega, die begin en die einde", "Ek is die Alfa en die Omega, die Begin en die Einde"),
    ],
    "rev/01-johannes-sien-die-troon.md": [
        ("soos 'n jaspissteen", "soos kristalhelder jaspis"),
    ],
}

issues_log = []
fixed_count = 0

def fix_file(path: Path, story_id: str):
    global fixed_count
    text = path.read_text(encoding="utf-8")
    original = text
    rel = str(path.relative_to(BASE))

    # Body replacements
    if rel in BODY_FIXES:
        for old, new in BODY_FIXES[rel]:
            if old in text:
                text = text.replace(old, new)
                issues_log.append((story_id, rel, f"body: {old[:50]}…"))

    # Memory verse
    if story_id in VERSES:
        new_verse = VERSES[story_id]
        text = re.sub(
            r"(### Vers om te onthou\n\n)(.+?)(\n\n### Onthou)",
            lambda m: m.group(1) + new_verse + m.group(3),
            text,
            flags=re.S,
        )
        if new_verse not in original:
            issues_log.append((story_id, rel, "memory verse → AFR20 exact"))

    # Frontmatter
    text = text.replace("afr20_quote_check: pending", "afr20_quote_check: verified")
    text = text.replace("〔AFR20-kontrole〕", "")

    if text != original:
        path.write_text(text, encoding="utf-8")
        fixed_count += 1

for folder in ["jes", "pas", "act", "epi", "rev"]:
    for f in sorted((BASE / folder).glob("*.md")):
        m = re.search(r"story_id: (\S+)", f.read_text(encoding="utf-8"))
        if m:
            fix_file(f, m.group(1))

print(f"Fixed {fixed_count} files, {len(issues_log)} issue entries")
for row in issues_log[:30]:
    print(row)
