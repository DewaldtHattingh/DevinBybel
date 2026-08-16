#!/usr/bin/env python3
"""Generate v2 manuscripts for jes/pas/act/epi/rev from v1 drafts."""

import re
from pathlib import Path

ROOT = Path("/agent")
V1_04 = ROOT / "manuscripts/volume-04"
V1_05 = ROOT / "manuscripts/volume-05"
OUT = ROOT / "manuscripts-v2"

STORIES = [
    # jes
    {"id": "JES-01", "folder": "jes", "num": "01", "slug": "die-engel-by-maria", "title": "Die engel by Maria",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 1:26–38",
     "must_include": ["Gabriel", "Jesus", "Seun van die Allerhoogste", "laat dit so wees"],
     "theology": "God word mens", "v1": V1_04 / "01-die-engel-by-maria.md",
     "prev": "MAL-01", "next": "JES-02"},
    {"id": "JES-02", "folder": "jes", "num": "02", "slug": "josef-se-droom", "title": "Josef se droom",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 1:18–25",
     "must_include": ["engel", "Jesus red", "Immanuel"],
     "theology": "Josef gehoorsaam", "v1": V1_04 / "02-josef-se-droom.md",
     "prev": "JES-01", "next": "JES-03"},
    {"id": "JES-03", "folder": "jes", "num": "03", "slug": "jesus-word-gebore", "title": "Jesus word gebore",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 2:1–7",
     "must_include": ["sensus", "Betlehem", "krip"],
     "theology": "Nederige geboorte", "v1": V1_04 / "03-jesus-word-gebore.md",
     "prev": "JES-02", "next": "JES-04"},
    {"id": "JES-04", "folder": "jes", "num": "04", "slug": "die-herders", "title": "Die herders",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 2:8–20",
     "must_include": ["heerlikheid", "goeie nuus", "teken"],
     "theology": "Goeie nuus vir almal", "v1": V1_04 / "04-die-herders.md",
     "prev": "JES-03", "next": "JES-05"},
    {"id": "JES-05", "folder": "jes", "num": "05", "slug": "die-wyse-manne", "title": "Die wyse manne",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 2:1–12",
     "must_include": ["ster", "Herodes", "geskenke", "aanbidding"],
     "theology": "Heidene soek die Koning", "v1": V1_04 / "05-die-wyse-manne.md",
     "prev": "JES-04", "next": "JES-06"},
    {"id": "JES-06", "folder": "jes", "num": "06", "slug": "vlug-na-egipte", "title": "Vlug na Egipte",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 2:13–23",
     "must_include": ["droom", "Egipte", "Herodes se geweld", "Nasaret"],
     "theology": "God beskerm die Kind", "v1": V1_04 / "06-vlug-na-egipte-terugkeer.md",
     "prev": "JES-05", "next": "JES-07"},
    {"id": "JES-07", "folder": "jes", "num": "07", "slug": "die-seun-jesus-in-die-tempel", "title": "Die seun Jesus in die tempel",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 2:41–52",
     "must_include": ["twaalf", "My Vader se huis"],
     "theology": "Jesus ken sy Vader", "v1": V1_04 / "07-die-seun-jesus-in-die-tempel.md",
     "prev": "JES-06", "next": "JES-08"},
    {"id": "JES-08", "folder": "jes", "num": "08", "slug": "johannes-jesus-se-doop", "title": "Johannes; Jesus se doop",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 3",
     "must_include": ["bekeer", "doop", "Gees", "stem uit hemel"],
     "theology": "Vader bevestig die Seun", "v1": V1_04 / "08-johannes-die-doper-jesus-se-doop.md",
     "prev": "JES-07", "next": "JES-09"},
    {"id": "JES-09", "folder": "jes", "num": "09", "slug": "jesus-word-versoek", "title": "Jesus word versoek",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 4:1–11",
     "must_include": ["drie versoekings", "Skrif-antwoorde"],
     "theology": "Jesus gehoorsaam waar Israel/Adam misluk", "v1": V1_04 / "09-jesus-word-versook.md",
     "prev": "JES-08", "next": "JES-10"},
    {"id": "JES-10", "folder": "jes", "num": "10", "slug": "eerste-dissipels-water-word-wyn", "title": "Eerste dissipels; water word wyn",
     "section": "Jesus — geboorte en bediening", "passage": "Joh. 1–2",
     "must_include": ["Volg My", "Kana"],
     "theology": "Jesus se heerlikheid begin", "v1": V1_04 / "10-jesus-roept-dissipels-water-word-wyn.md",
     "prev": "JES-09", "next": "JES-11"},
    {"id": "JES-11", "folder": "jes", "num": "11", "slug": "nikodemus", "title": "Nikodemus",
     "section": "Jesus — geboorte en bediening", "passage": "Joh. 3",
     "must_include": ["nag", "nuut gebore", "slang", "God so lief"],
     "theology": "Nuwe lewe; kruis vooruit", "v1": V1_04 / "11-nikodemus.md",
     "prev": "JES-10", "next": "JES-12"},
    {"id": "JES-12", "folder": "jes", "num": "12", "slug": "die-vrou-by-die-put", "title": "Die vrou by die put",
     "section": "Jesus — geboorte en bediening", "passage": "Joh. 4",
     "must_include": ["lewende water", "ware aanbidding", "Messias"],
     "theology": "Jesus vir buitestaanders", "v1": V1_04 / "12-die-vrou-by-die-put.md",
     "prev": "JES-11", "next": "JES-13"},
    {"id": "JES-13", "folder": "jes", "num": "13", "slug": "jesus-leer-op-die-berg", "title": "Jesus leer op die berg",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 5–7 (gekies)",
     "must_include": ["Saligsprekinge", "Ons Vader", "wyse/dwase bouer"],
     "theology": "Koninkryk se etos", "v1": V1_04 / "13-jesus-leer-op-die-berg.md",
     "prev": "JES-12", "next": "JES-14"},
    {"id": "JES-14", "folder": "jes", "num": "14", "slug": "jesus-stil-die-storm", "title": "Jesus stil die storm",
     "section": "Jesus — geboorte en bediening", "passage": "Mark. 4:35–41",
     "must_include": ["boot", "slaap", "Stil maar!", "Wie is Hy?"],
     "theology": "Jesus heers oor skepping", "v1": V1_04 / "14-jesus-stil-die-storm.md",
     "prev": "JES-13", "next": "JES-15"},
    {"id": "JES-15", "folder": "jes", "num": "15", "slug": "vyfduisend-gevoed", "title": "Vyfduisend gevoed",
     "section": "Jesus — geboorte en bediening", "passage": "Joh. 6:1–15",
     "must_include": ["brood/visse", "seën", "twaalf mandjies"],
     "theology": "Jesus voorsien", "v1": V1_04 / "15-vyfduisend-word-gevoed.md",
     "prev": "JES-14", "next": "JES-16"},
    {"id": "JES-16", "folder": "jes", "num": "16", "slug": "jesus-loop-op-die-water", "title": "Jesus loop op die water",
     "section": "Jesus — geboorte en bediening", "passage": "Matt. 14:22–33",
     "must_include": ["nag", "Dit is Ek", "Petrus sink", "red"],
     "theology": "Jesus red; aanbidding", "v1": V1_04 / "16-jesus-loop-op-die-water.md",
     "prev": "JES-15", "next": "JES-17"},
    {"id": "JES-17", "folder": "jes", "num": "17", "slug": "die-barmhartige-samaritaan", "title": "Die barmhartige Samaritaan",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 10:25–37",
     "must_include": ["naaste", "priester/Leviet", "Samaritaan"],
     "theology": "Wie is my naaste?", "v1": V1_04 / "17-die-barmhartige-samaritaan.md",
     "prev": "JES-16", "next": "JES-18"},
    {"id": "JES-18", "folder": "jes", "num": "18", "slug": "die-verlore-seun", "title": "Die verlore seun",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 15:11–32",
     "must_include": ["ver land", "terugkeer", "vader hardloop", "ouer broer"],
     "theology": "Vader se genade", "v1": V1_04 / "18-die-verlore-seun.md",
     "prev": "JES-17", "next": "JES-19"},
    {"id": "JES-19", "folder": "jes", "num": "19", "slug": "jesus-wek-lasarus-op", "title": "Jesus wek Lasarus op",
     "section": "Jesus — geboorte en bediening", "passage": "Joh. 11",
     "must_include": ["Ek is die opstanding", "ween", "Kom uit!"],
     "theology": "Jesus het mag oor dood", "v1": V1_04 / "19-jesus-wek-lasarus-op.md",
     "prev": "JES-18", "next": "JES-20"},
    {"id": "JES-20", "folder": "jes", "num": "20", "slug": "saggeus", "title": "Saggeus",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 19:1–10",
     "must_include": ["boom", "vandag redding", "viervoudig"],
     "theology": "Soek en red wat verlore is", "v1": V1_04 / "20-saggeus.md",
     "prev": "JES-19", "next": "JES-21"},
    {"id": "JES-21", "folder": "jes", "num": "21", "slug": "jesus-en-die-kinders", "title": "Jesus en die kinders",
     "section": "Jesus — geboorte en bediening", "passage": "Mark. 10:13–16",
     "must_include": ["dissipels verhinder", "Jesus ontvang", "soos kind"],
     "theology": "Koninkryk vir kinders", "v1": V1_04 / "21-jesus-en-die-kinders.md",
     "prev": "JES-20", "next": "JES-22"},
    {"id": "JES-22", "folder": "jes", "num": "22", "slug": "die-verheerliking", "title": "Die verheerliking",
     "section": "Jesus — geboorte en bediening", "passage": "Mark. 9:2–9",
     "must_include": ["berg", "Moses/Elia", "stem"],
     "theology": "Luister na Hom", "v1": V1_04 / "22-die-verheerliking.md",
     "prev": "JES-21", "next": "JES-23"},
    {"id": "JES-23", "folder": "jes", "num": "23", "slug": "jesus-gaan-na-jerusalem", "title": "Jesus gaan na Jerusalem",
     "section": "Jesus — geboorte en bediening", "passage": "Luk. 9:51; 18:31–34",
     "must_include": ["gesig gerig", "lyde voorspel"],
     "theology": "Pad na die kruis", "v1": V1_04 / "23-jesus-gaan-na-jerusalem.md",
     "prev": "JES-22", "next": "PAS-01"},
    # pas
    {"id": "PAS-01", "folder": "pas", "num": "01", "slug": "jesus-ry-jerusalem-binne", "title": "Jesus ry Jerusalem binne",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Matt. 21:1–11",
     "must_include": ["donkie", "Hosanna", "Seun van Dawid"],
     "theology": "Koning kom nederig", "v1": V1_05 / "01-jesus-ry-jerusalem-binne.md",
     "prev": "JES-23", "next": "PAS-02"},
    {"id": "PAS-02", "folder": "pas", "num": "02", "slug": "jesus-in-die-tempel", "title": "Jesus in die tempel",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Matt. 21:12–16; 22:34–40",
     "must_include": ["reiniging", "grootste gebooie"],
     "theology": "Huis van gebed; liefde", "v1": V1_05 / "02-jesus-in-die-tempel.md",
     "prev": "PAS-01", "next": "PAS-03"},
    {"id": "PAS-03", "folder": "pas", "num": "03", "slug": "die-laaste-maaltyd", "title": "Die laaste maaltyd",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Luk. 22; Joh. 13",
     "must_include": ["brood/beker", "verraad", "voete was"],
     "theology": "Nuwe verbond", "v1": V1_05 / "03-die-laaste-maaltyd.md",
     "prev": "PAS-02", "next": "PAS-04"},
    {"id": "PAS-04", "folder": "pas", "num": "04", "slug": "getsemane", "title": "Getsemane",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Matt. 26:36–46",
     "must_include": ["waak", "nie My wil nie", "dissipels slaap"],
     "theology": "Gehoorsaamheid in angs", "v1": V1_05 / "04-getsemane.md",
     "prev": "PAS-03", "next": "PAS-05"},
    {"id": "PAS-05", "folder": "pas", "num": "05", "slug": "jesus-word-gevange-geneem", "title": "Jesus word gevange geneem",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Matt. 26:47–56",
     "must_include": ["kus", "arrestasie", "swaard", "dissipels vlug"],
     "theology": "Hy gee Homself oor", "v1": V1_05 / "05-jesus-word-gevange-geneem.md",
     "prev": "PAS-04", "next": "PAS-06"},
    {"id": "PAS-06", "folder": "pas", "num": "06", "slug": "jesus-voor-die-raad-en-pilatus", "title": "Jesus voor die Raad en Pilatus",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Matt. 26–27",
     "must_include": ["vals getuies", "Barabbas", "skare"],
     "theology": "Onskuldige veroordeel", "v1": V1_05 / "06-jesus-voor-die-raad-en-pilatus.md",
     "prev": "PAS-05", "next": "PAS-07"},
    {"id": "PAS-07", "folder": "pas", "num": "07", "slug": "petrus-verloen-jesus", "title": "Petrus verloën Jesus",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Luk. 22:54–62",
     "must_include": ["drie keer", "haan", "Jesus kyk", "Petrus ween"],
     "theology": "Mislukking; later herstel", "v1": V1_05 / "07-petrus-verloen-jesus.md",
     "prev": "PAS-06", "next": "PAS-08"},
    {"id": "PAS-08", "folder": "pas", "num": "08", "slug": "jesus-sterf-aan-die-kruis", "title": "Jesus sterf aan die kruis",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Luk. 23; Joh. 19",
     "must_include": ["kruis", "vergewe", "Dit is volbring", "duisternis"],
     "theology": "Plaasvervangende dood", "v1": V1_05 / "08-jesus-sterf-aan-die-kruis.md",
     "prev": "PAS-07", "next": "PAS-09"},
    {"id": "PAS-09", "folder": "pas", "num": "09", "slug": "jesus-word-begraaf", "title": "Jesus word begrawe",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Matt. 27:57–66",
     "must_include": ["Josef", "graf", "klip", "wag"],
     "theology": "Ware dood", "v1": V1_05 / "09-jesus-word-begraaf.md",
     "prev": "PAS-08", "next": "PAS-10"},
    {"id": "PAS-10", "folder": "pas", "num": "10", "slug": "jesus-het-opgestaan", "title": "Jesus het opgestaan",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Luk. 24; Joh. 20:1–18",
     "must_include": ["leë graf", "engele", "Maria"],
     "theology": "Hy leef", "v1": V1_05 / "10-jesus-het-opgestaan.md",
     "prev": "PAS-09", "next": "PAS-11"},
    {"id": "PAS-11", "folder": "pas", "num": "11", "slug": "op-pad-na-emmaus", "title": "Op pad na Emmaus",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Luk. 24:13–35",
     "must_include": ["Skrifte", "brood breek", "herken"],
     "theology": "Skrif wys na Hom", "v1": V1_05 / "11-op-pad-na-emmaus.md",
     "prev": "PAS-10", "next": "PAS-12"},
    {"id": "PAS-12", "folder": "pas", "num": "12", "slug": "tomas-glo", "title": "Tomas glo",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Joh. 20:19–29",
     "must_include": ["vrede", "wonde", "My Here", "salig sonder sien"],
     "theology": "Geloof", "v1": V1_05 / "12-tomas-en-die-ander-dissipels.md",
     "prev": "PAS-11", "next": "PAS-13"},
    {"id": "PAS-13", "folder": "pas", "num": "13", "slug": "jesus-gaan-op-na-die-hemel", "title": "Jesus gaan op na die hemel",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 1:1–11",
     "must_include": ["belofte van Gees", "wolk", "sal terugkom"],
     "theology": "Hy kom weer", "v1": V1_05 / "13-jesus-gaan-op-na-die-hemel.md",
     "prev": "PAS-12", "next": "ACT-01"},
    # act
    {"id": "ACT-01", "folder": "act", "num": "01", "slug": "pinkster", "title": "Pinkster",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 2",
     "must_include": ["wind/vuur", "tale", "Petrus", "~3000"],
     "theology": "Gees gegee", "v1": V1_05 / "14-pinkster.md",
     "prev": "PAS-13", "next": "ACT-02"},
    {"id": "ACT-02", "folder": "act", "num": "02", "slug": "die-vroeë-gemeente", "title": "Die vroeë gemeente",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 2:42–47; 3",
     "must_include": ["leer", "gemeenskap", "kreupel loop"],
     "theology": "Nuwe lewe saam", "v1": V1_05 / "15-die-vroeë-gemeente.md",
     "prev": "ACT-01", "next": "ACT-03"},
    {"id": "ACT-03", "folder": "act", "num": "03", "slug": "stefanus", "title": "Stefanus",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 6–7",
     "must_include": ["getuienis", "steniging", "Saul stem saam"],
     "theology": "Getrou tot die dood", "v1": V1_05 / "16-stefanus.md",
     "prev": "ACT-02", "next": "ACT-04"},
    {"id": "ACT-04", "folder": "act", "num": "04", "slug": "filippus-en-die-ethiopiër", "title": "Filippus en die Ethiopiër",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 8:26–40",
     "must_include": ["Jesaja", "Jesus", "doop"],
     "theology": "Evangelie gaan uit", "v1": V1_05 / "17-filippus-en-die-ethiopiër.md",
     "prev": "ACT-03", "next": "ACT-05"},
    {"id": "ACT-05", "folder": "act", "num": "05", "slug": "saul-ontmoet-jesus", "title": "Saul ontmoet Jesus",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 9",
     "must_include": ["lig", "Waarom vervolg jy My?", "Ananias"],
     "theology": "Vyand word dienaar", "v1": V1_05 / "18-saul-ontmoet-jesus.md",
     "prev": "ACT-04", "next": "ACT-06"},
    {"id": "ACT-06", "folder": "act", "num": "06", "slug": "petrus-en-cornelius", "title": "Petrus en Cornelius",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 10",
     "must_include": ["doek-visioen", "heidene", "Gees val"],
     "theology": "Geen partydigheid", "v1": V1_05 / "19-petrus-en-cornelius.md",
     "prev": "ACT-05", "next": "ACT-07"},
    {"id": "ACT-07", "folder": "act", "num": "07", "slug": "paulus-en-silas-in-die-tronk", "title": "Paulus en Silas in die tronk",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 16",
     "must_include": ["Filippi", "liedere", "aardbewing", "cipier"],
     "theology": "God oop tronkdeure", "v1": V1_05 / "20-paulus-en-silas-in-die-tronk.md",
     "prev": "ACT-06", "next": "ACT-08"},
    {"id": "ACT-08", "folder": "act", "num": "08", "slug": "paulus-in-atene", "title": "Paulus in Atene",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 17",
     "must_include": ["Onbekende god", "opstanding"],
     "theology": "Evangelie vir filosowe", "v1": V1_05 / "21-paulus-in-atene.md",
     "prev": "ACT-07", "next": "ACT-09"},
    {"id": "ACT-09", "folder": "act", "num": "09", "slug": "paulus-se-reis-na-rome", "title": "Paulus se reis na Rome",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Hand. 27–28",
     "must_include": ["storm", "skipbreuk", "huisgevangenis"],
     "theology": "Evangelie tot die einde van die aarde", "v1": V1_05 / "22-paulus-se-reis-na-rome.md",
     "prev": "ACT-08", "next": "EPI-01"},
    # epi
    {"id": "EPI-01", "folder": "epi", "num": "01", "slug": "paulus-skryf-briewe", "title": "Paulus skryf briewe",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Rom. 8; 1 Kor. 13 (gekies)",
     "must_include": ["niks skei van liefde", "liefde beskryf"],
     "theology": "Briewe bou die kerk", "v1": V1_05 / "23-paulus-skryf-briewe.md",
     "prev": "ACT-09", "next": "REV-01"},
    # rev
    {"id": "REV-01", "folder": "rev", "num": "01", "slug": "johannes-sien-die-troon", "title": "Johannes sien die troon",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Op. 1; 4",
     "must_include": ["Patmos", "Seun van Mens (ingetoë)", "heilig heilig"],
     "theology": "Aanbidding", "v1": V1_05 / "24-johannes-se-visioen-van-die-troon.md",
     "prev": "EPI-01", "next": "REV-02"},
    {"id": "REV-02", "folder": "rev", "num": "02", "slug": "die-lam-wat-waardig-is", "title": "Die Lam wat waardig is",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Op. 5",
     "must_include": ["seël", "Leeu/Lam", "nuwe lied"],
     "theology": "Lam is waardig", "v1": V1_05 / "25-die-lam-wat-waardig-is.md",
     "prev": "REV-01", "next": "REV-03"},
    {"id": "REV-03", "folder": "rev", "num": "03", "slug": "god-oordeel-regverdig", "title": "God oordeel regverdig",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Op. 20:11–15",
     "must_include": ["groot wit troon", "boeke"],
     "theology": "Oordeel is ernstig", "v1": V1_05 / "26-god-oordeel-regverdig.md",
     "prev": "REV-02", "next": "REV-04"},
    {"id": "REV-04", "folder": "rev", "num": "04", "slug": "n-nuwe-hemel-en-n-nuwe-aarde", "title": "'n Nuwe hemel en aarde",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Op. 21:1–7",
     "must_include": ["God by mense", "trane afvee", "alles nuut"],
     "theology": "Hoop se einde", "v1": V1_05 / "27-n-nuwe-hemel-en-n-nuwe-aarde.md",
     "prev": "REV-03", "next": "REV-05"},
    {"id": "REV-05", "folder": "rev", "num": "05", "slug": "die-nuwe-jerusalem", "title": "Die nuwe Jerusalem",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Op. 21–22:5",
     "must_include": ["stad", "rivier", "lewensboom", "sy aangesig"],
     "theology": "God by sy volk vir altyd", "v1": V1_05 / "28-die-nuwe-jerusalem.md",
     "prev": "REV-04", "next": "REV-06"},
    {"id": "REV-06", "folder": "rev", "num": "06", "slug": "kom-here-jesus", "title": "Kom, Here Jesus",
     "section": "Lyde, opstanding, kerk, Openbaring", "passage": "Op. 22:6–21",
     "must_include": ["Gees en bruid sê kom", "genade"],
     "theology": "Maranata", "v1": V1_05 / "29-kom-here-jesus.md",
     "prev": "REV-05", "next": None},
]


def yaml_list(items):
    return "[" + ", ".join(f'"{x}"' for x in items) + "]"


def extract_body(v1_text: str) -> str:
    """Extract narrative body from v1, stripping frontmatter and produksie-notas."""
    if v1_text.startswith("---"):
        end = v1_text.find("---", 3)
        body = v1_text[end + 3 :].lstrip("\n")
    else:
        body = v1_text
    # Remove produksie-notas section
    body = re.sub(r"\n---\n\n## Produksie-notas[\s\S]*$", "\n", body)
    return body.strip() + "\n"


def transform_body(body: str, old_id: str, new_id: str, title: str) -> str:
    """Replace v1 IDs and fix title for PAS-12."""
    body = body.replace(old_id, new_id)
    # Fix PAS-12 title in heading
    if new_id == "PAS-12":
        body = re.sub(r"# Tomas en die ander dissipels", f"# {title}", body)
    return body


def build_frontmatter(s: dict) -> str:
    next_val = s["next"] if s["next"] else "null"
    return f"""---
story_id: {s['id']}
title: "{s['title']}"
section: {s['section']}
pages: 6
primary_passage: "{s['passage']}"
must_include: {yaml_list(s['must_include'])}
theology_centre: "{s['theology']}"
continuity_from: {s['prev']}
continuity_to: {next_val}
afr20_quote_check: pending
---"""


def main():
    written = []
    for s in STORIES:
        v1_path = s["v1"]
        if not v1_path.exists():
            raise FileNotFoundError(f"Missing v1: {v1_path}")
        v1_text = v1_path.read_text(encoding="utf-8")
        # Detect old story id from v1
        m = re.search(r"story_id:\s*(\S+)", v1_text)
        old_id = m.group(1) if m else "UNKNOWN"
        body = extract_body(v1_text)
        body = transform_body(body, old_id, s["id"], s["title"])
        out_path = OUT / s["folder"] / f"{s['num']}-{s['slug']}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        content = build_frontmatter(s) + "\n\n" + body
        out_path.write_text(content, encoding="utf-8")
        written.append(str(out_path.relative_to(ROOT)))
        print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"\nTotal: {len(written)} files")
    return written


if __name__ == "__main__":
    main()
