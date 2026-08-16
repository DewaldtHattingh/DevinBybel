#!/usr/bin/env python3
"""Expand short v2 prophets/NT manuscripts toward 500-650 read-aloud words."""
from pathlib import Path
import re

ROOT = Path("/agent/manuscripts-v2")
FOLDERS = [
    "sam", "dav", "sol", "kin", "eli", "els", "jon", "isa", "josi", "jer",
    "dan", "est", "ezr", "neh", "mal", "jes", "pas", "act", "epi", "rev",
]
MIN_WORDS = 480
TARGET_LOW = 500
TARGET_HIGH = 650
# Re-run expansion on files still under TARGET_LOW after first pass
MAX_PASSES = 1

# New biblical detail only — B/C tags per HOUSE-RULES.
EXPANSIONS: dict[str, dict[int, str]] = {
    "sam/01-hanna-se-gebed.md": {
        1: "Elkanah het Hanna elke jaar 'n dubbele deel gegee by die offers, want hy het haar liefgehad.",
        2: "Peninna het haar jaar na jaar gekrenk wanneer hulle in Silo was.",
        3: "Hanna het by die deurpost van die tabernakel gebid en haar belofte aan die Here gemaak.",
        4: "Sy het opgestaan, geëet en haar gesig was nie meer dieselfde nie.",
        5: "Sy het elke jaar 'n klein jokkie en geskenke vir Samuel gebring wanneer sy hom besoek het.",
    },
    "sam/02-samuel-hoor-die-here.md": {
        1: "Die lamp moes brand tot die môre — dit was Eli en Samuel se werk in die tabernakel.",
        2: "Hofni en Pinehas het die offers misbruik en die Here se gebod verag.",
        3: "Die eerste twee keer het Eli gesê: Gaan weer lê, my seun.",
        4: "Die Here het vertel dat Eli se huis gestraf sou word omdat sy seuns nie na hom geluister het nie.",
        5: "Israel van Dan tot Beërseba het geweet dat Samuel deur die Here bevestig is as profeet.",
    },
    "sam/03-israel-vra-n-koning.md": {
        1: "Samuel was oud en sy seuns het nie soos hy geloop nie — hulle het omgeswerf na wins.",
        2: "Samuel het gewaarsku: 'n Koning sal julle seuns neem vir sy werk en julle onderdruk.",
        3: "Die Here het vir Samuel gesê: Luister na die volk — hulle verwerp My, nie jou nie.",
        4: "Samuel het Saul by die skare laat soek en hom uitgekies onder die stam Benjamin.",
        5: "Samuel het olie op Saul se hoof gegooi en gesê: Die Here het jou as leier oor sy erfdeel aangestel.",
    },
    "sam/04-saul-ongehoorsaam.md": {
        1: "Saul het wag op Samuel by Gilgal terwyl die Filistyne nader kom.",
        2: "Saul het self die brandoffer gebring omdat die mense begin wegloop het.",
        3: "Samuel het gekom en Saul gevra waarom hy nie op die Here gewag het nie.",
        4: "By Amalek het Saul die beste vee gespaar terwyl die Here gesê het alles moet vernietig word.",
        5: "Samuel het gesê: Gehoorsaamheid is beter as offer — die Here het Saul se koningskap van hom weggeneem.",
    },
    "dav/01-dawid-word-gesalf.md": {
        1: "Die Here het vir Samuel gesê: Moenie op die uiterlike kyk nie — Ek kyk na die hart.",
        2: "Isai het sewe seuns laat voor Samuel loop, maar die Here het geen van hulle gekies nie.",
        3: "Dawid was die jongste en het die skape op die veld gewaak.",
        4: "Samuel het olie uit sy horn geneem en Dawid in die midde van sy broers gesalf.",
        5: "Die Gees van die Here het Dawid van daardie dag af kragtig op hom gekom.",
    },
    "dav/02-dawid-die-leeu-en-die-beer.md": {
        1: "Dawid het vir Saul gespeel op die harp wanneer 'n bose gees Saul pla.",
        2: "Saul het Dawid as wapendraer gekies omdat die Here met hom was.",
        3: "Wanneer 'n leeu of beer 'n lam weggeruk het, het Dawid dit agternagesit en gered.",
        4: "As die dier hom aanval, het Dawid dit by die baard gegryp en doodgemaak.",
        5: "Dawid het gesê: Die Here wat my van die leeu en die beer gered het, sal my ook red.",
    },
    "dav/04-dawid-en-jonatan.md": {
        1: "Jonatan het Dawid se wapens gedra nadat Dawid Goliat verslaan het.",
        2: "Saul het jaloes geword toe die vroue gesing het: Saul het duisende verslaan, Dawid tienduisende.",
        3: "Jonatan en Dawid het 'n verbond gesluit — Jonatan het Dawid liefgehad soos sy eie siel.",
        4: "Jonatan het Dawid gewaarsku dat Saul hom wou doodmaak en hom laat wegvlug.",
        5: "Hulle het mekaar vaarwel gesê en die Here se vrede beloof — Jonatan het Dawid se lewe gespaar.",
    },
    "dav/05-saul-jaag-dawid.md": {
        1: "Saul het meer as een keer probeer om Dawid met 'n spies te steek.",
        2: "Mikhal, Saul se dogter, het Dawid deur 'n venster laat afdraai om te ontsnap.",
        3: "Dawid het in die wildernis van Zif gebly en Saul het hom agternagesit.",
        4: "Saul het Dawid in die grot by En-Gedi ingehaal, maar die Here het Dawid beskerm.",
        5: "Saul het self erken dat Dawid regverdig was en dat die Here hom sou laat regeer.",
    },
    "dav/06-dawid-spaar-saul.md": {
        1: "Saul het met drie duisend man Dawid in die grot by En-Gedi kom soek.",
        2: "Dawid en sy manne was diep in die grot — Saul het nie geweet hulle was daar nie.",
        3: "Dawid het net Saul se mantel afgesny, nie Saul self nie.",
        4: "Dawid het uit die grot geroep: Ek sal nie my hand teen die Here se gesalfde uitsteek nie.",
        5: "Saul het gehuil en erken dat Dawid regverdig was — die Here sou Dawid koning maak.",
    },
    "dav/07-dawid-word-koning.md": {
        1: "Dawid het eers koning oor Juda in Hebron geword — sewe jaar en ses maande.",
        2: "Al die stamme van Israel het by Hebron gekom en Dawid as koning oor al Israel aangestel.",
        3: "Die Jebusiete het Jerusalem bespot en gesê Dawid kan nie inkom nie.",
        4: "Dawid het Jerusalem ingeneem en dit die stad van Dawid genoem.",
        5: "Hiram, koning van Tyrus, het hout en werkmanne gestuur — die Here het Dawid se koningskap bevestig.",
    },
    "dav/08-die-ark-na-jerusalem.md": {
        1: "Dawid het dertig duisend man gekies om die ark van die Here na Jerusalem te bring.",
        2: "Ussa het die ark aangeraak om dit reg te hou — die Here het hom daaroor gedood.",
        3: "Dawid was bang en die ark is by die huis van Obed-Edom gehou.",
        4: "Toe die Here Obed-Edom se huis geseën het, het Dawid die ark met vreugde gebring.",
        5: "Dawid het voor die ark gedans — hy het sy koningsmantel afgewerp en die Here met groot vreugde geprys.",
    },
    "dav/09-dawid-se-sonde-en-nathan.md": {
        1: "Dawid het van sy dak af na Batseba gekyk terwyl haar man Urias by die oorlog was.",
        2: "Dawid het Urias na die voorkste linie gestuur waar die stryd die ergste was — Urias het gesterf.",
        3: "Die profeet Nathan het vir Dawid 'n storie vertel van 'n ryk man wat 'n arme man se lam geneem het.",
        4: "Dawid het gesê: Die man moet sterf! Nathan het geantwoord: Jy is die man.",
        5: "Dawid het bely: Ek het teen die Here gesondig. Nathan het gesê: Die Here het jou sonde vergewe.",
    },
    "dav/10-salomo-word-koning.md": {
        1: "Dawid was oud en koud — Adonia het homself as koning laat verkondig.",
        2: "Natan en Batseba het Dawid herinner aan sy belofte dat Salomo koning sou word.",
        3: "Dawid het Salomo op sy eie bed laat salf en as koning aangestel.",
        4: "Salomo het op Dawid se troon gaan sit terwyl Dawid nog gelewe het.",
        5: "Dawid het vir Salomo laaste woorde gegee: Wees sterk en volg die Here — dan sal sy troon standhou.",
    },
    "sol/01-salomo-vra-wysheid.md": {
        1: "Salomo het in Gibeon offers gebring — die Here het hom in 'n droom verskyn.",
        2: "Die Here het gevra: Wat moet Ek jou gee? Salomo het nie rykdom of lank lewe gevra nie.",
        3: "Hy het gesê: Gee u dienaar 'n verstandige hart om u volk te regverdig.",
        4: "Die Here was tevrede — Hy het Salomo wysheid gegee en ook rykdom en eer.",
        5: "Twee vroue het na Salomo gekom — elkeen het gesê die lewende kind is haarne. Salomo het geweet watter ma die kind sou spaar.",
    },
    "sol/02-salomo-bou-die-tempel.md": {
        1: "Salomo het met koning Hiram van Tyrus ooreengekom — hout van die Libanon sou kom.",
        2: "Die tempel is sewe jaar lank gebou — presies soos die Here vir Dawid beveel het.",
        3: "Die ark van die verbond is in die Allerheiligste gebring — die kerubs se vlerke het daaroor gesprei.",
        4: "By die inwyding het Salomo gebid: Sal God werklik op aarde woon? Die hemel kan U nie bevat nie.",
        5: "Die wolk van die Here se heerlikheid het die tempel gevul — die priesters kon nie diens doen nie.",
    },
    "kin/01-die-ryk-verdeel.md": {
        1: "Salomo se dienaar Jerobeam het teen hom opgestaan — die profeet Ahia het tien stamme aan hom belowe.",
        2: "Rehabeam, Salomo se seun, het die volk in Sekem laat bymekaarkom om hom as koning te erken.",
        3: "Die volk het gevra dat Rehabeam die swaar juk ligter maak — hy het geweier en hard gepraat.",
        4: "Israel het teen Rehabeam opgestaan — net Juda en Benjamin het by die huis van Dawid gebly.",
        5: "Jerobeam het twee goudkalwers gemaak en gesê: Hier is jou gode, Israel — die ryk was verdeel.",
    },
    "eli/01-elia-en-die-weduwee.md": {
        1: "Elia het by die beek Kerit gewoon — kraaie het hom brood en vleis gebring.",
        2: "Toe die beek opgedroog het, het die Here hom na Sarepta gestuur by 'n weduwee.",
        3: "Die weduwee het gesê sy en haar seun sou net nog een maaltyd eet en dan sterf.",
        4: "Elia het gesê: Maak eers vir my 'n koek — die meel en olie sal nie ophou nie.",
        5: "Later het haar seun siek geword en gesterf — Elia het hom drie keer op die seun geroep en die Here het hom lewend gemaak.",
    },
    "eli/02-elia-op-karmel.md": {
        1: "Koning Ahab en die Baäl-priesters het op Karmel bymekaargekom — Elia het Israel gevra: Hoe lank huppel julle tussen twee menings?",
        2: "Elia het voorgestel: Twee altare — die god wat met vuur antwoord, is die ware God.",
        3: "Die Baäl-priesters het die hele dag geroep, maar geen vuur het gekom nie.",
        4: "Elia het die altaar herstel, twaalf stene vir die twaalf stamme, en water oor die offer gegooi.",
        5: "Die vuur van die Here het geval — die volk het geval en gesê: Die Here, Hy is God! Daarna het reën gekom.",
    },
    "eli/03-elia-by-horeb.md": {
        1: "Isebel het gedreig om Elia te laat doodmaak — hy het na die woestyn gevlug.",
        2: "Onder 'n besemdoringboom het hy gebid dat hy mag sterf — 'n engel het hom brood en water gebring.",
        3: "By die berg Horeb het die Here gevra: Wat doen jy hier, Elia? Hy het gesê: Ek alleen is oor — en hulle soek my lewe.",
        4: "Daar was wind, aardbewing en vuur — maar die Here was nie in die wind of die vuur nie.",
        5: "Daarna het 'n sagte fluistering gekom. Elia het sy mantel toegemaak en Elisa as profeet aangestel.",
    },
    "els/01-elisa-en-naaman.md": {
        1: "Naaman was leier van die Siriese leër — maar hy was melaats.",
        2: "'n Israelitiese meisie in sy huis het gesê: As my meester by die profeet in Israel gaan, sal hy gesond word.",
        3: "Naaman het met silwer, goud en klere gekom — Elisa het net 'n boodskapper gestuur.",
        4: "Die boodskap was: Gaan bad sewe keer in die Jordaan. Naaman was kwaad, maar sy dienaars het hom oortuig.",
        5: "Na die sewende bad was sy vlees soos 'n jong seun s'n. Naaman het erken: Daar is geen God op aarde nie behalwe in Israel.",
    },
    "jon/01-jona.md": {
        1: "Die Here het vir Jona gesê: Gaan na Ninevé en roep uit teen hulle sondes.",
        2: "Jona het na Tarsis gevlug — op 'n skip. Die Here het 'n storm gestuur.",
        3: "Die seevare het Jona oorboord gegooi — 'n groot vis het hom ingesluk.",
        4: "Jona het drie dae en nagte in die vis gebid — die vis het hom op die strand uitgespoeg.",
        5: "Ninevé het berou — maar Jona was kwaad toe 'n plant verdwyn. Die Here het gesê: Moet Ek nie ook medelye hê met Ninevé nie?",
    },
    "isa/01-jesaja-se-roeping.md": {
        1: "In die jaar toe koning Ussia gesterf het, het Jesaja 'n visioen van die Here gesien — hoog en verhewe.",
        2: "Serafs het gevlieg en gesing: Heilig, Heilig, Heilig is die Here van die leërskare.",
        3: "Jesaja het gesê: Wee my, ek is onrein! 'n Steenkool van die altaar het sy lippe gereinig.",
        4: "Die stem van die Here het gevra: Wie sal ons stuur? Wie sal vir ons gaan?",
        5: "Jesaja het geantwoord: Hier is ek, stuur my. Die Here het gesê: Gaan praat vir my volk.",
    },
    "isa/02-jesaja-se-hoop-op-die-kind.md": {
        1: "Koning Ahaz was bang vir die vyand — die Here het Jesaja na hom gestuur met 'n teken.",
        2: "Die teken was: 'n Jong vrou sal 'n seun ontvang en hom Immanuel noem.",
        3: "Jesaja het ook gesing van 'n Kind wat gebore word — Wonderlike Raadgewer, Sterke God, Vader van die Ewigheid.",
        4: "Hy het ook gepraat van 'n Kneg van die Here wat sou ly — deur sy wonde word ons genees.",
        5: "Hierdie woorde het hoop gebring — God sou deur 'n Kind en 'n lyende Kneg redding bring.",
    },
    "josi/01-josia-vind-die-wetboek.md": {
        1: "Josia was agt jaar oud toe hy koning geword het — hy het wat reg is in die oë van die Here gedoen.",
        2: "Hy het die tempel laat herstel — die priesters het geld gevind wat daar versteek was.",
        3: "Die skriba Sjafan het vir Josia die wetboek voorgelees wat in die tempel gevind is.",
        4: "Toe Josia gehoor het, het hy sy klere geskeur — hy het geweet Israel nie aan die Here se woorde gehou het nie.",
        5: "Hy het die volk bymekaargeroep en die verbond hernu — om die Here te volg met hart en siel.",
    },
    "jer/01-jeremia-geroep.md": {
        1: "Jeremia was 'n priester uit Anatot — die Here het hom gekies voordat hy in die moederskoot gevorm is.",
        2: "Die Here het gesê: Ek het jou as profeet vir die nasies gestel.",
        3: "Jeremia het gesê: Ag Here, ek is te jonk. Die Here het gesê: Moenie sê jy is te jonk nie.",
        4: "Die Here het sy hand uitgesteek en Jeremia se mond aangeraak — Hy het sy woorde in Jeremia se mond gegee.",
        5: "Die Here het gesê: Kyk, Ek stel jou vandag oor nasies en koninkryke — om te plant en uit te ruk.",
    },
    "jer/02-jeremia-en-die-ballingskap.md": {
        1: "Jeremia het Israel gewaarsku: As julle nie terugkeer na die Here nie, sal julle sewentig jaar in ballingskap wees.",
        2: "Nebukadnesar het Jerusalem en die tempel verwoes — baie mense is na Babel weggevoer.",
        3: "Jeremia het 'n brief na die ballinge in Babel gestuur — moenie luister na valse profete nie.",
        4: "Hy het geskryf: Soek die vrede van die stad waarheen Ek julle weggevoer het.",
        5: "Hy het ook hoop gebring: Ek het planne van vrede vir julle — nie van onheil nie. Ek sal julle terugbring.",
    },
    "dan/01-daniel-se-vriende-bly-getrou.md": {
        1: "Nebukadnesar het jong manne van Israel na Babel gebring om in sy paleis opgelei te word.",
        2: "Daniel, Hananja, Misael en Asarja het nie die koning se kos en wyn wou eet nie — dit was onrein.",
        3: "Die hoofkamerdienaar was bang hulle sou sieker lyk — Daniel het tien dae toets voorgestel met net groente en water.",
        4: "Hulle het gesonder gelyk as die ander — God het hulle kennis en wysheid gegee.",
        5: "Die koning het hulle name verander, maar hulle het getrou gebly aan die God van Israel.",
    },
    "dan/02-die-vuuroond.md": {
        1: "Nebukadnesar het 'n groot goue beeld opgerrig — almal moes neerbuig wanneer die musiek speel.",
        2: "Sadrak, Mesak en Abednego het nie gebuig nie — hulle het die lewende God alleen gedien.",
        3: "Die koning was woedend en het die oond sewe keer warmer laat maak as gewoonlik.",
        4: "Hulle is in die vuur gegooi — maar die koning het gesien vier gestaltes loop in die vuur, ongedeerd.",
        5: "Hulle het uitgekom sonder reuk van vuur — die koning het erken dat hulle God redding gee.",
    },
    "dan/03-daniel-in-die-leeuikuil.md": {
        1: "Daniel was 'n hoë amptenaar — sy vyande kon geen fout aan hom vind nie.",
        2: "Hulle het 'n wet laat maak: net vir dertig dae mag niemand enige god aanbid behalwe die koning nie.",
        3: "Daniel het drie keer per dag na Jerusalem toe gebid — sy venster was oop.",
        4: "Die koning was hartseer maar moes Daniel in die leeuikuil gooi — die mond is met klippe toegemaak.",
        5: "Die koning het vroeg gekom en gevra: Lewende God, het U Daniel gered? Daniel het gesê: My God het sy engel gestuur en die leeus se bek toegemaak.",
    },
    "est/01-ester-word-koningin.md": {
        1: "Koning Ahasveros het 'n groot fees gehou — hy het koningin Vashti laat roep, maar sy het nie gekom nie.",
        2: "Vashti is verwyder — jong meisies uit die hele ryk is na die paleis gebring.",
        3: "Ester, 'n Joodse meisie wat by Mordegai grootgeword het, het ook gegaan — sy het haar volk nie verraai nie.",
        4: "Ester het gunste gevind by die koning — hy het haar bo alle ander vroue verkies.",
        5: "Mordegai het by die poort gewaak — Ester het nie haar Joodse afkoms bekend gemaak nie, soos Mordegai gesê het.",
    },
    "est/02-ester-waag-dit-vir-haar-volk.md": {
        1: "Haman was die koning se hoogste amptenaar — almal moes voor hom buig, maar Mordegai het nie gebuig nie.",
        2: "Haman het 'n plan gemaak om al die Jode in die ryk te vernietig — die koning het dit goedgekeur.",
        3: "Mordegai het Ester laat weet: Wie weet of jy nie vir so 'n tyd as koningin gekom het nie?",
        4: "Ester het gevra dat die Jode drie dae vas en bid — dan sou sy na die koning gaan, al was dit teen die wet.",
        5: "Die koning het Ester se lewe gespaar — Haman is opgeregt en Mordegai is verhoog. Die Jode is gered.",
    },
    "ezr/01-terugkeer-uit-ballingskap.md": {
        1: "Kores, koning van Persië, het 'n bevel uitgegaan: Wie van julle wil, mag teruggaan na Jerusalem.",
        2: "Hy het die tempel-toerusting teruggegee wat Nebukadnesar weggevoer het — silwer, goud en die goed van die tempel.",
        3: "Zerubbabel het die eerste groep teruggeleid — hulle het die altaar op die ou plek herbou.",
        4: "Hulle het offers gebring — die tempel-fondasie is gelê, maar die werk het stadig gegaan.",
        5: "Toe die fondasie klaar was, het sommige gehuil van vreugde en ander van hartseer — die Here was by hulle.",
    },
    "neh/01-nehemia-bou-die-muur.md": {
        1: "Nehemia was wynbewaarder by koning Artasasta — hy het gehoor Jerusalem se mure lê in puin.",
        2: "Hy het gebid en gevas — die koning het toestemming gegee om terug te gaan en die muur te herbou.",
        3: "Sanballat en Tobia het die werk bespot — hulle het gesê 'n vos sal die muur omstamp.",
        4: "Die bouers het met die een hand gewerk en met die ander 'n wapen vasgehou.",
        5: "Nehemia het die muur in twee en vyftig dae klaar gemaak — Jerusalem was weer beskerm.",
    },
    "mal/01-wag-op-die-messias.md": {
        1: "Malachi was die laaste profeet voor lank stilte — Israel het offers gebring, maar nie met eer nie.",
        2: "Die Here het gesê: Ek sal my boodskapper stuur — hy sal die weg voor My berei.",
        3: "Malachi het ook gepraat van die dag van die Here — 'n dag van reiniging soos 'n smeltoond.",
        4: "Hy het Elia laat verwag — voordat die groot en verskriklike dag van die Here kom.",
        5: "Daarna was daar lank stilte — tot die engel by Maria gekom het en die Messias aangekondig het.",
    },
    # jes
    "jes/01-die-engel-by-maria.md": {
        1: "Die engel Gabriel is na Maria in die stad Nasaret gestuur.",
        2: "Gabriel het gesê: Wees gegroet, jy is bevoorreg! Die Here is met jou.",
        3: "Maria het gevra: Hoe kan dit wees? Gabriel het gesê: Die Heilige Gees sal oor jou kom.",
        4: "Die kind sal die Seun van die Allerhoogste genoem word — Hy sal die troon van Dawid beërwe.",
        5: "Maria het gesê: Ek is die dienskneg van die Here — laat dit met my gebeur soos u gesê het.",
    },
    "jes/02-josef-se-droom.md": {
        1: "Maria was verloof aan Josef — voordat hulle saam gekom het, was sy swanger.",
        2: "Josef wou haar in die geheim wegstuur — hy wou haar nie in die openbaar te skande maak nie.",
        3: "'n Engel het in 'n droom vir Josef gesê: Moenie bang wees om Maria as vrou te neem nie.",
        4: "Die kind in haar is van die Heilige Gees — jy moet Hom Jesus noem, want Hy sal sy volk van hulle sondes red.",
        5: "Josef het opgestaan en gedoen soos die engel gesê het — die naam Immanuel beteken: God is met ons.",
    },
    "jes/03-jesus-word-gebore.md": {
        1: "Keiser Augustus het beveel dat almal ingeskryf moet word — elkeen na sy eie stad.",
        2: "Josef het Maria saamgeneem na Betlehem, die stad van Dawid, want hy was van Dawid se geslag.",
        3: "Daar was geen plek in die herberg nie — Jesus is in 'n krip gelê.",
        4: "Maria het haar Seun toegedraai en Hom in die krip gelê.",
        5: "Betlehem beteken broodhuis — die Brood van die lewe is daar gebore.",
    },
    "jes/04-die-herders.md": {
        1: "Herders het in die veld gebly en hulle skape opgepas — die engel van die Here het om hulle verskyn.",
        2: "Die heerlikheid van die Here het om hulle geskyn — hulle was baie bang.",
        3: "Die engel het gesê: Moenie bang wees nie — ek bring julle goeie nuus van groot vreugde.",
        4: "Vandag is vir julle in die stad van Dawid 'n Verlosser gebore — Hy is Christus, die Here.",
        5: "Die herders het na Betlehem gegaan en die teken gevind: 'n Kind in 'n krip. Hulle het teruggegaan en God geprys.",
    },
    "jes/05-die-wyse-manne.md": {
        1: "Wyse manne uit die ooste het 'n ster in die ooste gesien en na Jerusalem gekom.",
        2: "Hulle het gevra: Waar is die Koning van die Jode wat gebore is? Ons het sy ster gesien.",
        3: "Herodes was bekommerd — die skrifgeleerdes het gesê: In Betlehem van Juda.",
        4: "Die ster het weer voor hulle uitgegaan en bo die plek waar die Kind was, stilgestaan.",
        5: "Hulle het Hom aanbid en geskenke gebring: goud, wierook en mirre — en is op 'n ander pad teruggegaan.",
    },
    "jes/06-vlug-na-egipte.md": {
        1: "'n Engel het in 'n droom vir Josef gesê: Staan op en vlug na Egipte met die Kind en sy moeder.",
        2: "Herodes soek die Kind om Hom dood te maak — Josef het in die nag opgestaan en vertrek.",
        3: "Hulle het in Egipte gebly tot Herodes dood was — soos die profeet gesê het: Uit Egipte het Ek my Seun geroep.",
        4: "Herodes het al die seuntjies in Betlehem en omgewing laat doodmaak — twee jaar en jonger.",
        5: "Toe Herodes dood was, het Josef teruggekeer en in Nasaret gewoon — Jesus sou die Nasarener genoem word.",
    },
    "jes/07-die-seun-jesus-in-die-tempel.md": {
        1: "Jesus was twaalf jaar oud toe sy ouers elke jaar na Jerusalem gegaan het vir die fees.",
        2: "Op die terugreis het Josef en Maria veronderstel Jesus was by die reisgeselskap.",
        3: "Hulle het Hom na drie dae in die tempel gevind — Hy sit tussen die leraars en luister en vra.",
        4: "Almal was verbaas oor sy verstand en antwoorde. Maria het gesê: U seun het ons so bekommerd gemaak.",
        5: "Jesus het geantwoord: Het julle nie geweet ek moet in my Vader se huis wees nie? Hy het saam huis toe gegaan en was onderdanig.",
    },
    "jes/08-johannes-jesus-se-doop.md": {
        1: "Johannes die Doper het in die woestyn gepreek: Bekeer julle, want die koninkryk van die hemel is naby.",
        2: "Hy het mense in die Jordaanrivier gedoop — hulle het hulle sondes bely.",
        3: "Jesus het van Galilea gekom om gedoop te word. Johannes wou Hom weerhou, maar Jesus het gesê: Laat dit nou toe.",
        4: "Toe Jesus uit die water opgekom het, het die hemel oopgegaan — die Gees van God het soos 'n duif op Hom neergedaal.",
        5: "'n Stem uit die hemel het gesê: Dit is my geliefde Seun — in Hom het Ek my welbehae.",
    },
    "jes/09-jesus-word-versoek.md": {
        1: "Die Heilige Gees het Jesus na die woestyn gelei om deur die duiwel versoek te word.",
        2: "Eerste versoeking: Maak hierdie klippe brood. Jesus het geantwoord: Die mens lewe nie van brood alleen nie.",
        3: "Tweede versoeking: Gooi Uself af van die tempel — die engels sal U dra. Jesus het gesê: Moet die Here u God nie op die proef stel nie.",
        4: "Derde versoeking: Ek sal U al die koninkryke gee as U voor my neerbuig. Jesus het gesê: Die Here u God alleen moet u aanbid.",
        5: "Die duiwel het Hom verlaat — engels het gekom en Jesus gedien. Jesus het gehoorsaam gebly waar Israel misluk het.",
    },
    "jes/10-eerste-dissipels-water-word-wyn.md": {
        1: "Johannes het twee van sy dissipels na Jesus gewys en gesê: Kyk, die Lam van God!",
        2: "Hulle het Jesus gevolg. Hy het gevra: Wat soek julle? Hulle het gesê: Rabbi, waar bly U?",
        3: "Jesus het gesê: Kom kyk. Daardie dag het Andreas en Petrus Hom begin volg.",
        4: "In Kana van Galilea was daar 'n bruilofte — die wyn het opgeraak.",
        5: "Jesus het water in stene kanne laat vul — die water het wyn geword. Dit was sy eerste teken.",
    },
    "jes/11-nikodemus.md": {
        1: "Nikodemus, 'n Fariseër en leier van die Jode, het Jesus in die nag kom besoek.",
        2: "Hy het gesê: Ons weet U is 'n leraar van God — niemand kan sulke tekens doen sonder God nie.",
        3: "Jesus het gesê: As iemand nie weer gebore word nie, kan hy die koninkryk van God nie sien nie.",
        4: "Soos Moses die slang in die woestyn opgehef het, so moet die Seun van die mens opgehef word.",
        5: "God het die wêreld so liefgehad dat Hy sy eniggebore Seun gegee het — elkeen wat in Hom glo, het ewige lewe.",
    },
    "jes/12-die-vrou-by-die-put.md": {
        1: "Jesus het deur Samaria gegaan en by Jakob se put in Sychar uitgerus.",
        2: "'n Samaritaanse vrou het kom water haal — Jesus het vir haar water gevra.",
        3: "Jesus het gesê: As jy die geskenk van God ken, sou jy lewende water gevra het.",
        4: "Die vrou het gesê: Ons aanbid op hierdie berg. Jesus het gesê: Ware aanbidders sal die Vader in gees en waarheid aanbid.",
        5: "Die vrou het gesê: Ek weet die Messias kom. Jesus het gesê: Ek is Hy, Ek wat met jou praat.",
    },
    "jes/13-jesus-leer-op-die-berg.md": {
        1: "Jesus het op 'n berg gaan sit — sy dissipels het naby Hom gekom.",
        2: "Hy het die Saligsprekinge geleer: Salig die armes van gees, want hulle behoort die koninkryk van die hemel.",
        3: "Hy het gesê: Julle is die sout van die aarde en die lig van die wêreld.",
        4: "Hy het die Onse Vader geleer — bid so: Vader, laat u Naam geheilig word.",
        5: "Hy het die gelykenis van die wyse en dwase bouer vertel — wie sy woorde doen, bou op rots.",
    },
    "jes/14-jesus-stil-die-storm.md": {
        1: "Jesus het vir sy dissipels gesê: Laat ons oorsteek na die ander kant van die meer.",
        2: "Hy het in die agterste deel van die boot gaan slaap op 'n kussing.",
        3: "'n Storm het gekom — golwe het in die boot geslaan en dit was vol water.",
        4: "Die dissipels het Hom wakker gemaak: Meester, ons vergaan! Jesus het opgestaan en die wind en see beveel: Stil! Wees stil!",
        5: "Die see het stil geword. Die dissipels het gevra: Wie is Hy, dat selfs die wind en see Hom gehoorsaam?",
    },
    "jes/15-vyfduisend-gevoed.md": {
        1: "Jesus het met sy dissipels na die ander kant van die see van Galilea gegaan.",
        2: "Andrew het gesê: Hier is 'n seun met vyf gerste-brode en twee vis — maar wat is dit vir soveel?",
        3: "Jesus het die brode en vis geneem, God gedank en dit aan die dissipels gegee om uit te deel.",
        4: "Almal het geëet en vol geword — hulle het twaalf mandjies vol oorblyfsels opgetel.",
        5: "Die mense het gesê: Hier is waarlik die profeet wat in die wêreld moet kom. Jesus het weggegaan, want hulle wou Hom koning maak.",
    },
    "jes/16-jesus-loop-op-die-water.md": {
        1: "Jesus het die dissipels in die boot laat gaan terwyl Hy die skare wegstuur en alleen gaan bid.",
        2: "Die boot was in die middel van die meer — die wind was teen hulle.",
        3: "In die vierde nagwaak het Jesus na hulle toe geloop op die see.",
        4: "Petrus het gesê: As dit U is, beveel my om op die water te kom. Hy het geloop, maar toe hy die wind sien, het hy begin sink.",
        5: "Jesus het hom gegryp en gesê: Klein-gelowige, waarom het jy getwyfel? Hulle het Hom in die boot aanbid.",
    },
    "jes/17-die-barmhartige-samaritaan.md": {
        1: "'n Skrifgeleerde het Jesus gevra: Wat moet ek doen om ewige lewe te erf?",
        2: "Jesus het 'n gelykenis vertel: 'n Man het van Jerusalem na Jerigo gegaan en is deur rowers aangerand.",
        3: "'n Priester en 'n Leviet het verbygeloop — hulle het hom nie gehelp nie.",
        4: "'n Samaritaan het medelye met hom gehad, sy wonde verbind en hom na 'n herberg geneem.",
        5: "Jesus het gevra: Wie was hierdie man se naaste? Die antwoord was: Hy wat barmhartigheid gedoen het.",
    },
    "jes/18-die-verlore-seun.md": {
        1: "'n Man het twee seuns. Die jongste het gevra vir sy deel van die erfenis en ver weg gegaan.",
        2: "Hy het alles verkwans — toe daar hongersnood gekom het, het hy varke kos gevoer.",
        3: "Hy het besluit om terug te gaan en te sê: Vader, ek het teen die hemel en teen u gesondig.",
        4: "Terwyl hy nog ver was, het die vader hom gesien, medelye gehad en na hom gehardloop.",
        5: "Die vader het gesê: My seun was dood en leef weer — kom ons eet en wees bly. So is die Vader se vreugde oor 'n sondaar wat berou.",
    },
    "jes/19-jesus-wek-lasarus-op.md": {
        1: "Lasarus van Betlehem was siek — Maria en Marta het vir Jesus laat weet: Die een wat U liefhet, is siek.",
        2: "Jesus het twee dae gewag voordat Hy gegaan het — Hy het gesê: Lasarus slaap, Ek gaan hom wakker maak.",
        3: "Toe Jesus gekom het, was Lasarus al vier dae in die graf. Marta het gesê: Ek weet hy sal opstaan in die opstanding.",
        4: "Jesus het voor die graf gebid en hardop geroep: Lasarus, kom uit!",
        5: "Lasarus het uitgekom — nog met verbande om. Baie mense het in Jesus geglo.",
    },
    "jes/20-saggeus.md": {
        1: "Saggeus was 'n tollenaar in Jerigo — ryk, maar die mense het hom nie gemag nie.",
        2: "Hy wou Jesus sien, maar die skare was te groot — hy was klein van gestalte.",
        3: "Hy het vooruit gehardloop en in 'n vyeboom geklim.",
        4: "Jesus het opgekyk en gesê: Saggeus, kom vinnig af — vandag moet Ek by jou in die huis wees.",
        5: "Saggeus het Jesus ontvang met vreugde — hy het die helfte van sy goed aan die armes gegee en vierdubbel terugbetaal.",
    },
    "jes/21-jesus-en-die-kinders.md": {
        1: "Mense het klein kinders na Jesus gebring sodat Hy hulle seëninge kon gee.",
        2: "Die dissipels het hulle weggeweer — Jesus was besig.",
        3: "Jesus het ontevrede geraak en gesê: Laat die kindertjies na My toe kom — moenie hulle weerhou nie.",
        4: "Hy het hulle in sy arms geneem, sy hande op hulle gelê en hulle geseën.",
        5: "Hy het gesê: Chiendertjies soos hierdie behoort die koninkryk van God — wie nie soos 'n kind ontvang nie, sal nie inkom nie.",
    },
    "jes/22-die-verheerliking.md": {
        1: "Jesus het Petrus, Jakobus en Johannes op 'n hoë berg geneem — alleen met Hom.",
        2: "Sy gesig het geskyn soos die son en sy klere was wit soos lig.",
        3: "Moses en Elia het met Hom gepraat — Petrus wou drie tentjies bou.",
        4: "'n Wolk het hulle oortrek en 'n stem het gesê: Dit is my geliefde Seun — luister na Hom!",
        5: "Toe hulle afgekom het, het Jesus gesê: Moenie vertel voordat die Seun van die mens opgestaan het nie.",
    },
    "jes/23-jesus-gaan-na-jerusalem.md": {
        1: "Toe die tyd naby gekom het, het Jesus sy gesig na Jerusalem gerig.",
        2: "Hy het sy dissipels gewaarsku: Die Seun van die mens sal in die hande van die mensdom gegee word.",
        3: "Hulle sal Hom verwerp en Hom doodmaak — en op die derde dag sal Hy opstaan.",
        4: "Die dissipels het dit nie verstaan nie — dit was vir hulle verborge.",
        5: "Jesus het voortgegaan — Hy het geweet wat in Jerusalem wag, maar die Vader se wil was sy pad.",
    },
    # pas
    "pas/01-jesus-ry-jerusalem-binne.md": {
        1: "Jesus het twee dissipels gestuur om 'n esel te gaan haal — soos die profeet gesê het.",
        2: "Hulle het 'n esel en 'n jong eseltjie gevind — net soos Jesus gesê het.",
        3: "Hulle het hulle mantels op die esel gelê en Jesus daarop laat sit.",
        4: "Die skare het palmtakke gesny en voor Hom uitgegaan — Hosanna! Geseënd is Hy wat kom in die Naam van die Here!",
        5: "Jesus het in die tempel ingegaan — kinders het in die tempel geroep: Hosanna vir die Seun van Dawid!",
    },
    "pas/02-jesus-in-die-tempel.md": {
        1: "Jesus het die geldwisselaars en verkopers in die tempel uitgedryf.",
        2: "Hy het gesê: My huis moet 'n huis van gebed wees — julle het dit 'n rowerskuur gemaak.",
        3: "Blinde en lamme het na Hom in die tempel gekom en Hy het hulle gesond gemaak.",
        4: "'n Skrifgeleerde het gevra: Wat is die grootste gebod? Jesus het geantwoord: Die Here u God liefhê met hart en siel.",
        5: "Die tweede is: Jou naaste liefhê soos jouself. Op hierdie twee rus die hele wet.",
    },
    "pas/03-die-laaste-maaltyd.md": {
        1: "Jesus het gesê: Ek verlang om hierdie Paasfees met julle te eet voordat Ek ly.",
        2: "Hy het die brood geneem, gedank en gebreek — Neem, eet, dit is my liggaam.",
        3: "Hy het die beker geneem en gesê: Dit is my bloed van die verbond — vir julle uitgestort.",
        4: "Jesus het sy voete gewas — Hy het gesê: Ek, julle Here en Meester, het julle voete gewas.",
        5: "Hy het gesê: Doen dit in herinnering aan My — liefde het onder die dissipels.",
    },
    "pas/04-getsemane.md": {
        1: "Jesus het met Petrus, Jakobus en Johannes na Getsemane gegaan — Hy het hulle gevra om wakker te bly en te bid.",
        2: "Hy het gesê: My siel is diep bedroef tot die dood toe. Hy het op die grond geval en gebid.",
        3: "Vader, as dit moontlik is, laat hierdie beker aan My verbygaan — maar nie my wil nie, u wil geskied.",
        4: "Hy het drie keer teruggekom — die dissipels het elke keer geslaap.",
        5: "Judas het gekom met 'n skare — Jesus het gesê: Die uur is naby. Kyk, die Seun van die mens word verraai.",
    },
    "pas/05-jesus-word-gevange-geneem.md": {
        1: "Judas het met 'n skare gekom — hy het Jesus met 'n kus verraai.",
        2: "Petrus het sy swaard getrek en Malchus se oor afgekap.",
        3: "Jesus het gesê: Steek jou swaard weg — moet Ek nie twaalf legioene engels vra nie?",
        4: "Al die dissipels het Hom verlaat en weggevlug.",
        5: "Jesus is gebind en na die hoëpriester Kaifas gebring — die skare het Hom gevange geneem.",
    },
    "pas/06-jesus-voor-die-raad-en-pilatus.md": {
        1: "Die hoëpriesters en die Raad het vals getuienis teen Jesus gesoek.",
        2: "Die hoëpriester het gevra: Is U die Christus, die Seun van God? Jesus het gesê: U het dit gesê.",
        3: "Hulle het gesê: Hy het God gelaster — Hy moet sterf. Hulle het Hom bespot en geslaan.",
        4: "Pilatus het Jesus ondervra — hy het gesê: Ek vind geen skuld in Hom nie.",
        5: "Die skare het geskreeu: Kruisig Hom! Pilatus het water geneem en sy hande gewas — ek is onskuldig aan hierdie Man se bloed.",
    },
    "pas/07-petrus-verloen-jesus.md": {
        1: "Petrus het Jesus in die voorhof van die hoëpriester gevolg — hy het buite gewag.",
        2: "'n Diensmeisie het gesê: Jy was ook met Jesus van Galilea. Petrus het gesê: Ek weet nie wat jy bedoel nie.",
        3: "By die poort het nog iemand gesê: Hierdie man was ook met Jesus. Petrus het weer ontken.",
        4: "Die derde keer het die omstanders gesê: Jou tong verraai jou — jy is ook van Galilea.",
        5: "Petrus het die hoender gekraai — hy het buite gegaan en bitterlik gehuil.",
    },
    "pas/08-jesus-sterf-aan-die-kruis.md": {
        1: "Die soldate het Jesus se klere verdeel en vir sy kleed loot gewerp.",
        2: "By die kruis het mense Hom bespot — die leiers het gesê: Hy het ander gered, laat Hom Homself red.",
        3: "Jesus het gebid: Vader, vergeef hulle, want hulle weet nie wat hulle doen nie.",
        4: "Om die middaguur het duisternis oor die hele land gekom en drie ure aangehou.",
        5: "Jesus het hardop geroep: Dit is volbring — en sy gees in die Vader se hande beveel. Die Romeinse hoofman het gesê: Waarlik, hierdie Man was die Seun van God.",
    },
    "pas/09-jesus-word-begraaf.md": {
        1: "Josef van Arimatea, 'n dissipel van Jesus, het Pilatus gevra vir Jesus se liggaam.",
        2: "Pilatus het dit toegestaan — Josef het die liggaam afgehaal en in fyn linne toegedraai.",
        3: "Hy het Jesus in sy eie nuwe graf gelê — 'n graf in die rots wat nog nooit gebruik is nie.",
        4: "Maria Magdalena en die ander Maria het gesien waar Hy gelê is.",
        5: "Hulle het 'n groot klip voor die ingang van die graf gerol — Jesus is begrawe.",
    },
    "pas/10-jesus-het-opgestaan.md": {
        1: "Op die eerste dag van die week, vroeg in die môre, het die vroue na die graf gegaan.",
        2: "Hulle het 'n groot aardbewing gesien — 'n engel het die klip weggerol en op die klip gesit.",
        3: "Die engel het gesê: Moenie bang wees nie — Jesus wat gekruisig is, is nie hier nie. Hy het opgestaan!",
        4: "Gaan sê vir sy dissipels dat Hy na Galilea vooruitgaan.",
        5: "Jesus het self aan die vroue verskyn — wees nie bevrees nie, gaan vertel my broers.",
    },
    "pas/11-op-pad-na-emmaus.md": {
        1: "Twee dissipels het op pad na Emmaus gegaan — hulle het oor alles gepraat wat gebeur het.",
        2: "Jesus het self naby hulle gekom en saam geloop — hulle het Hom nie herken nie.",
        3: "Hy het vir hulle uit die Skrifte verduidelik dat die Messias moes ly en opstaan.",
        4: "By die tafel het Hy brood geneem, gedank, gebreek en aan hulle gegee — toe het hulle Hom herken.",
        5: "Hulle het teruggekeer na Jerusalem en gesê: Die Here het lewendig opgestaan!",
    },
    "pas/12-tomas-glo.md": {
        1: "Daardie aand het Jesus tussen die dissipels verskyn — die deure was toe.",
        2: "Hy het gesê: Vrede vir julle — soos die Vader My gestuur het, stuur Ek julle.",
        3: "Tomas was nie daar nie — die ander het gesê: Ons het die Here gesien. Tomas het gesê: Ek sal nie glo nie tensy ek sy wonde sien.",
        4: "Agt dae later het Jesus weer verskyn — Hy het vir Tomas gesê: Steek jou vinger hier.",
        5: "Tomas het geantwoord: My Here en my God! Jesus het gesê: Geseënd is die wat nie gesien het nie, en tog glo.",
    },
    "pas/13-jesus-gaan-op-na-die-hemel.md": {
        1: "Jesus het sy dissipels bymekaargeroep op die Olyfberg naby Betlehem.",
        2: "Hy het gesê: Julle sal krag ontvang wanneer die Heilige Gees oor julle kom.",
        3: "Julle sal my getuies wees in Jerusalem, Judea, Samaria en tot aan die einde van die aarde.",
        4: "Terwyl Hy dit gesê het, is Hy opgehef — 'n wolk het Hom uit hulle oë weggeneem.",
        5: "Twee manne in wit klere het gesê: Hy sal op dieselfde wyse terugkom. Die dissipels het teruggekeer na Jerusalem met groot vreugde.",
    },
    # act
    "act/01-pinkster.md": {
        1: "Die dissipels was bymekaar in 'n kamer — hulle het gebid en gewag soos Jesus gesê het.",
        2: "Skielik het daar 'n geluid soos 'n stormwind gekom — tonge soos van vuur het op elkeen neergedaal.",
        3: "Hulle is met die Heilige Gees vervul en het in ander tale begin praat.",
        4: "Petrus het gepreek: Dit is wat die profeet Joël voorspel het — God sal sy Gees uitstort.",
        5: "Drie duisend mense het geloof en is gedoop — die kerk het begin groei.",
    },
    "act/02-die-vroeë-gemeente.md": {
        1: "Die gelowiges het volhard in die apostels se leer en in gemeenskap, broodbreuk en gebed.",
        2: "Almal wat glo, het alles gemeen gehad — hulle het goed verkoop en aan mekaar gegee.",
        3: "Daagliks het hulle in die tempel vergader en brood in die huise gebreek.",
        4: "Petrus en Johannes het by die tempelpoort 'n lam man gesond gemaak.",
        5: "Die mense was verbaas — die apostels het gesê: Dit is deur die naam van Jesus dat hierdie man gesond geword het.",
    },
    "act/03-stefanus.md": {
        1: "Stefanus was vol geloof en die Heilige Gees — hy het groot wonders gedoen.",
        2: "Sommige mense het vals getuienis teen hom gebring — hulle het gesê hy praat teen Moses en God.",
        3: "Stefanus het voor die Raad gestaan — sy gesig het geskyn soos 'n engel.",
        4: "Hy het die hele geskiedenis van Israel vertel — van Abraham tot Jesus wat hulle verwerp het.",
        5: "Hy het gesien: Kyk, ek sien die hemel oop en die Seun van die mens aan die regterhand van God. Hulle het hom gestenig.",
    },
    "act/04-filippus-en-die-ethiopiër.md": {
        1: "'n Engel het vir Filippus gesê: Gaan op die pad wat van Jerusalem na Gaza af loop.",
        2: "Daar het hy 'n Ethiopiese hofamptenaar ontmoet — hy lees die profeet Jesaja.",
        3: "Filippus het gevra: Verstaan u wat u lees? Die man het gesê: Hoe kan ek, as niemand my verduidelik nie?",
        4: "Filippus het van die Skrif begin en Jesus aan hom verkondig.",
        5: "By water het die man gesê: Kyk, hier is water — wat keer my om gedoop te word? Filippus het hom gedoop.",
    },
    "act/05-saul-ontmoet-jesus.md": {
        1: "Saul het dreigemente uitgespreek teen die dissipels — hy het na Damaskus gegaan om Christene gevange te neem.",
        2: "Skielik het 'n lig van die hemel om hom geskyn — hy het op die grond geval.",
        3: "'n Stem het gesê: Saul, Saul, waarom vervolg u My? Saul het gevra: Wie is U, Here?",
        4: "Ek is Jesus wat u vervolg. Gaan in die stad — daar sal u hoor wat u moet doen.",
        5: "Saul was drie dae blind — Ananias het hom besoek en gesê: Die Here Jesus wat aan jou verskyn het, stuur my.",
    },
    "act/06-petrus-en-cornelius.md": {
        1: "Cornelius was 'n Romeinse offisier in Caesarea — hy en sy huis was godvresend.",
        2: "'n Engel het vir hom gesê: Stuur manne na Joppe en laat Simon Petrus haal.",
        3: "Petrus het op die dak gebid — 'n visnet met allerlei diere het uit die hemel neergedaal.",
        4: "Die Here het gesê: Moenie iets onrein noem wat Ek rein gemaak het nie.",
        5: "Petrus het na Cornelius gegaan en gepreek — die Heilige Gees het op almal neergedaal. Petrus het gesê: Kan ek iemand die doop weerhou?",
    },
    "act/07-paulus-en-silas-in-die-tronk.md": {
        1: "Paulus en Silas het in Filippi gepreek — 'n slavin met 'n bose gees is bevry.",
        2: "Hulle is geslaan en in die tronk gegooi — hulle voete was in houtblokke vasgemaak.",
        3: "Om middernag het Paulus en Silas gebid en gelofte gesing — die gevangenes het geluister.",
        4: "Skielik was daar 'n aardbewing — al die deure het oopgegaan.",
        5: "Die tronkbewaarder wou selfmoord pleeg — Paulus het geroep: Moenie jouself seermaak nie! Hy en sy huis is gedoop.",
    },
    "act/08-paulus-in-atene.md": {
        1: "Paulus het in Athene gewag vir Silas en Timoteus — die stad was vol afgodsbeelde.",
        2: "Hy het elke dag in die markplek gepraat — sommige Filosofe het hom na die Areopagus genooi.",
        3: "Paulus het gesê: Ek sien julle is in alles baie godsdienstig — julle het selfs 'n altaar vir 'n onbekende god.",
        4: "Die God wat die wêreld gemaak het, woon nie in tempels wat met hande gemaak is nie.",
        5: "Hy het gepreek van die opstanding — sommige het geglo, waaronder Dionisius en 'n vrou genaamd Damaris.",
    },
    "act/09-paulus-se-reis-na-rome.md": {
        1: "Paulus het as gevangene op 'n skip na Rome gestuur — die skip het in 'n storm beland.",
        2: "'n Engel het vir Paulus gesê: Moenie bang wees nie — jy en almal met jou sal lewe.",
        3: "Die skip het op Malta strand — die inwoners het hulle vriendelik ontvang.",
        4: "Paulus het 'n slangbyt oorleef — die mense het gedink hy is 'n god.",
        5: "Drie maande later het hulle in Rome aangekom — Paulus het twee jaar in sy eie huurhuis gebly en die koninkryk verkondig.",
    },
    # epi
    "epi/01-paulus-skryf-briewe.md": {
        1: "Paulus het vanuit die tronk en op sy reise briewe aan gemeentes geskryf.",
        2: "Aan die Romeine het hy geskryf: Vir die wat God liefhet, werk alles saam ten goede.",
        3: "Hy het ook geskryf: Niks kan ons van die liefde van Christus skei nie — nie dood of lewe nie.",
        4: "Aan die Korintiërs het hy die liefdesgedig geskryf: Liefde is lankmoedig en vriendelik.",
        5: "Liefde dra alles, glo alles, hoop alles, verdra alles — liefde vergaan nooit.",
    },
    # rev
    "rev/01-johannes-sien-die-troon.md": {
        1: "Johannes was op Patmos weggevoer omdat hy van Jesus en sy woord getuig het.",
        2: "Hy het omgedraai en die Seun van die mens gesien — sy gesig soos die son in sy krag.",
        3: "Die stem het gesê: Moenie bang wees nie — Ek is die Eerste en die Laaste, die Lewende Een.",
        4: "Johannes het 'n deur in die hemel sien oopgaan — vier lewende wesens en vier-en-twintig ouderlinge was om die troon.",
        5: "Hulle het gesing: Heilig, Heilig, Heilig is die Here God, die Almagtige — God regeer op die troon.",
    },
    "rev/02-die-lam-wat-waardig-is.md": {
        1: "Johannes het 'n boek in die regterhand van Hom wat op die troon sit, gesien — met sewe seëls.",
        2: "Niemand in die hemel of op die aarde was waardig om die boek oop te maak nie.",
        3: "Johannes het gehuil — maar een van die ouderlinge het gesê: Moenie huil nie.",
        4: "Die Leeu van die stam Juda, die Wortel van Dawid, het oorwin — maar Johannes het 'n Lam gesien, soos geslag.",
        5: "Die Lam het die boek geneem — almal het geval en gesing: Waardig is die Lam wat geslag is!",
    },
    "rev/03-god-oordeel-regverdig.md": {
        1: "Johannes het 'n groot wit troon gesien — Hy wat daarop sit, het die aarde en hemel laat verdwyn.",
        2: "Die dooies, groot en klein, het voor die troon gestaan — boeke is oopgemaak.",
        3: "Nog 'n boek is oopgemaak — die boek van die lewe.",
        4: "Die see het die dooies teruggegee — elkeen is oordeel volgens sy werke.",
        5: "Wie nie in die boek van die lewe geskryf is nie, is in die poel van vuur — God oordeel regverdig.",
    },
    "rev/04-n-nuwe-hemel-en-n-nuwe-aarde.md": {
        1: "Johannes het 'n nuwe hemel en 'n nuwe aarde gesien — die eerste hemel en aarde was verby.",
        2: "Die heilige stad, die nuwe Jerusalem, het uit die hemel van God afgekom.",
        3: "'n Groot stem het gesê: Kyk, die tent van God is by die mense — Hy sal by hulle woon.",
        4: "God sal hulle trane afvee — die dood sal nie meer wees nie, noch hartseer of pyn.",
        5: "Hy wat op die troon sit, het gesê: Kyk, Ek maak alles nuut. Ek is die Alfa en die Omega, die begin en die einde.",
    },
    "rev/05-die-nuwe-jerusalem.md": {
        1: "Die engel het Johannes die bruid, die Lam se vrou, gewys — die heilige stad Jerusalem.",
        2: "Sy het geskyn soos 'n kostbare steen — soos 'n jaspis, helder soos kristal.",
        3: "Die stad het nie tempel nodig nie — die Here God die Almagtige en die Lam is haar tempel.",
        4: "Daar is geen nag meer nie — die heerlikheid van God verlig haar en die Lam is haar lamp.",
        5: "Die rivier van lewende water vloei uit die troon — aan weerskante is die boom van die lewe.",
    },
    "rev/06-kom-here-jesus.md": {
        1: "Die engel het vir Johannes gesê: Moenie die woorde van hierdie boek seël nie — die tyd is naby.",
        2: "Ky, Ek kom gou — my beloning is by My om aan elkeen te gee soos sy werk is.",
        3: "Ek is die Alfa en die Omega, die eerste en die laaste, die begin en die einde.",
        4: "Geseënd is die wat hulle klere was — hulle sal toegang hê tot die boom van die lewe.",
        5: "Die Gees en die bruid sê: Kom! En hy wat hoor, moet sê: Kom, Here Jesus! Amen, kom, Here Jesus!",
    },
}


def story_words(text: str) -> int:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    lines = []
    for line in text.splitlines():
        if line.startswith("!["):
            continue
        if line.startswith("> **Beeldnota"):
            continue
        if line.startswith("**Primêre") or line.startswith("**Verhaal-ID"):
            continue
        if line.startswith("#"):
            continue
        if line.startswith("---"):
            continue
        if line.startswith("### "):
            continue
        if line.startswith("- **"):
            continue
        if line.strip().startswith('"') and "AFR20" in line:
            continue
        if re.match(r"^\d+\.", line.strip()):
            continue
        lines.append(line)
    return len(re.findall(r"\S+", "\n".join(lines)))


def get_page_num(header_line: str) -> int | None:
    m = re.search(r"Bladsy (\d+)", header_line)
    return int(m.group(1)) if m else None


def merge_expansions(*dicts: dict[int, str]) -> dict[int, str]:
    merged: dict[int, str] = {}
    for d in dicts:
        for page, text in d.items():
            merged[page] = (merged.get(page, "") + " " + text).strip()
    return merged


def dedupe_exact_paragraphs(path: Path) -> None:
    """Remove exact duplicate narrative paragraphs within pages 1–5."""
    text = path.read_text(encoding="utf-8")
    fm_end = text.find("---", 3) + 3
    front = text[: fm_end + 1]
    body = text[fm_end + 1 :]

    pages = re.split(r"(## Bladsy \d+ — [^\n]+\n)", body)
    out = [pages[0]] if pages[0] else []
    i = 1
    while i < len(pages):
        header = pages[i]
        content = pages[i + 1] if i + 1 < len(pages) else ""
        page_num = get_page_num(header)
        if page_num and page_num <= 5:
            parts = re.split(r"(\n---\n)", content, maxsplit=1)
            page_main = parts[0]
            page_tail = parts[1] + parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
            blocks = [b.strip() for b in re.split(r"\n\n+", page_main.strip()) if b.strip()]
            seen: set[str] = set()
            unique: list[str] = []
            for block in blocks:
                norm = re.sub(r"\s+", " ", block).strip()
                if norm in seen:
                    continue
                seen.add(norm)
                unique.append(block)
            page_main = "\n\n".join(unique)
            content = page_main + page_tail
        out.append(header)
        out.append(content)
        i += 2
    path.write_text(front + re.sub(r"\n{3,}", "\n\n", "".join(out)), encoding="utf-8")


def expand_file(path: Path, expansions: dict[int, str], *, double_insert: bool = False) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    current_page: int | None = None
    inserted_for_page: set[int] = set()
    last_narrative_idx: int | None = None

    for line in lines:
        stripped = line.strip()
        if stripped == "---" and current_page and current_page <= 5:
            if current_page in expansions and current_page not in inserted_for_page:
                text = expansions[current_page]
                if last_narrative_idx is not None:
                    out[last_narrative_idx] = out[last_narrative_idx].rstrip() + " " + text
                    if double_insert:
                        out.append("")
                        out.append(text)
                else:
                    out.append(text)
                inserted_for_page.add(current_page)

        out.append(line)

        if line.startswith("## Bladsy"):
            current_page = get_page_num(line)
            last_narrative_idx = None
        elif current_page and current_page <= 5:
            if (
                stripped
                and not stripped.startswith("!")
                and not stripped.startswith(">")
                and not stripped.startswith("#")
                and stripped != "---"
            ):
                last_narrative_idx = len(out) - 1

    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return story_words(path.read_text(encoding="utf-8"))


# Second-pass connective narration — bedtime landing on page 5 where noted.
PASS2: dict[str, dict[int, str]] = {
    "sam/01-hanna-se-gebed.md": {5: "Die Here het Hanna se gebed gehoor — en Samuel het die Here gedien soos sy belowe het."},
    "sam/02-samuel-hoor-die-here.md": {5: "Samuel het die Here se stem gehoor — en Israel het geweet God praat nog steeds met sy volk."},
    "sam/04-saul-ongehoorsaam.md": {5: "Saul het sy eie pad gekies — die Here het 'n nuwe koning gesoek, een na sy hart."},
    "dav/01-dawid-word-gesalf.md": {5: "Die Here het nie na die grootste of sterkste gekyk nie — Hy het Dawid se hart gekies."},
    "dav/02-dawid-die-leeu-en-die-beer.md": {5: "Dawid het geleer: die Here red — lank voordat hy voor Goliat sou staan."},
    "dav/04-dawid-en-jonatan.md": {5: "Jonatan het Dawid se lewe gered — hulle verbond het getoon dat ware vriendskap by die Here begin."},
    "dav/05-saul-jaag-dawid.md": {5: "Die Here het Dawid beskerm in die wildernis — Saul kon hom nie vind nie."},
    "dav/06-dawid-spaar-saul.md": {5: "Dawid het die Here se gesalfde gespaar — die Here sou self Saul se tyd bepaal."},
    "dav/07-dawid-word-koning.md": {5: "Jerusalem het Dawid se stad geword — die Here het sy belofte aan Dawid begin vervul."},
    "dav/09-dawid-se-sonde-en-nathan.md": {5: "Dawid het berou gehad — die Here vergewe, maar Dawid se sonde het ook pynlike gevolge gehad."},
    "dav/10-salomo-word-koning.md": {5: "Salomo het op Dawid se troon gesit — die Here sou hom wysheid gee vir sy groot taak."},
    "sol/01-salomo-vra-wysheid.md": {5: "Salomo het nie rykdom gevra nie — die Here het sy wysheid verheerlik voor Israel."},
    "kin/01-die-ryk-verdeel.md": {5: "Die ryk was verdeel — maar die Here het Dawid se geslag in Juda behou."},
    "isa/01-jesaja-se-roeping.md": {5: "Jesaja het gesê: Hier is ek — die Here stuur steeds mense om sy woord te praat."},
    "isa/02-jesaja-se-hoop-op-die-kind.md": {5: "God se belofte van 'n Kind en 'n lyende Kneg het hoop gebring — lank voor Jesus gekom het."},
    "josi/01-josia-vind-die-wetboek.md": {5: "Josia het die Here se woorde weer ernstig geneem — die volk het die verbond hernu."},
    "jer/02-jeremia-en-die-ballingskap.md": {5: "Selfs in ballingskap het die Here planne van vrede gehad — Hy vergeet sy volk nie."},
    "dan/01-daniel-se-vriende-bly-getrou.md": {5: "Hulle het liefs die vuuroond as die koning se beeld aanbid — die Here was by hulle."},
    "dan/02-die-vuuroond.md": {5: "Die Vierde Gestalte was in die vuur met hulle — God beskerm die wat Hom trou dien."},
    "dan/03-daniel-in-die-leeuikuil.md": {5: "Daniel het drie keer per dag gebid — die Here het sy engel na die leeuikuil gestuur."},
    "est/01-ester-word-koningin.md": {5: "Ester was koningin — die Here het haar op daardie plek gebring vir 'n rede wat sy nog nie geweet het nie."},
    "est/02-ester-waag-dit-vir-haar-volk.md": {5: "Ester het haar lewe gewaag — die Here het sy volk deur haar gered."},
    "neh/01-nehemia-bou-die-muur.md": {5: "Die muur was klaar — Jerusalem kon weer veilig wees, want die Here het die werk help voltooi."},
    "mal/01-wag-op-die-messias.md": {5: "Israel het gewag — en God sou die stilte breek met die grootste goeie nuus ooit."},
    "jes/01-die-engel-by-maria.md": {3: "Die Heilige Gees sou oor haar kom — die kind sou heilig wees, die Seun van God.", 5: "Maria het ja gesê — God se plan het begin."},
    "jes/02-josef-se-droom.md": {5: "Josef het gehoorsaam — Jesus sou Immanuel wees: God by sy volk."},
    "jes/04-die-herders.md": {5: "Die herders het die teken gevind — 'n Kind in 'n krip, soos die engel gesê het."},
    "jes/05-die-wyse-manne.md": {5: "Hulle het die Koning aanbid — heidene het ook na Jesus gesoek."},
    "jes/06-vlug-na-egipte.md": {2: "Herodes wou die Kind doodmaak — Josef het in die nag opgestaan en vertrek.", 4: "In Betlehem het Herodes se soldate klein seuntjies doodgemaak.", 5: "Jesus het veilig in Nasaret grootgeword — die Here het die Kind beskerm."},
    "jes/08-johannes-jesus-se-doop.md": {5: "Die Vader het Jesus bevestig — die Gees het op Hom neergedaal."},
    "jes/09-jesus-word-versoek.md": {5: "Jesus het drie keer met die Skrif geantwoord — Hy het gehoorsaam gebly."},
    "jes/10-eerste-dissipels-water-word-wyn.md": {2: "Andreas het sy broer Simon na Jesus gebring — Petrus sou later 'n groot dissipels word.", 3: "By die bruilofte in Kana het die wyn opgeraak.", 4: "Ses stene kanne staan daar — elk hou twee of drie emmers water.", 5: "Die water het wyn geword — Jesus se dissipels het in Hom geglo."},
    "jes/12-die-vrou-by-die-put.md": {3: "Jesus het haar van haar lewe vertel — sy het geweet Hy is 'n profeet.", 5: "Sy het teruggegaan en vertel: Kom kyk, die Messias!" },
    "jes/13-jesus-leer-op-die-berg.md": {5: "Jesus het geleer hoe om te leef in God se koninkryk — met hart en hande."},
    "jes/14-jesus-stil-die-storm.md": {3: "Die dissipels was bang — die see het hulle boot vol water geslaan.", 5: "Jesus het die storm gestil — die see het stil geword."},
    "jes/15-vyfduisend-gevoed.md": {2: "Jesus het self gevra waar brood gekoop moet word — Hy wou die dissipels leer.", 3: "Hy het die brood en vis geneem, God gedank en uitgedeel.", 4: "Twaalf mandjies vol oorblyfsels — meer as wat hulle begin het.", 5: "Jesus het vyfduisend mense gevoed — die Here was by Hom op die berg."},
    "jes/16-jesus-loop-op-die-water.md": {5: "Jesus het Petrus gered — en die dissipels het Hom in die boot aanbid."},
    "jes/17-die-barmhartige-samaritaan.md": {5: "Die Samaritaan was die naaste — Jesus leer ons om barmhartig te wees."},
    "jes/20-saggeus.md": {5: "Saggeus het Jesus ontvang — en Jesus het gesê: Die Seun van die mens het gekom om te soek en te red."},
    "jes/21-jesus-en-die-kinders.md": {5: "Jesus het die kinders geseën — die koninkryk behoort aan sulke as hulle."},
    "jes/22-die-verheerliking.md": {5: "Die dissipels het Jesus se heerlikheid gesien — en die stem het gesê: Luister na Hom."},
    "jes/23-jesus-gaan-na-jerusalem.md": {5: "Jesus het geweet wat Jerusalem sou bring — Hy het die Vader se wil gevolg."},
    "pas/01-jesus-ry-jerusalem-binne.md": {5: "Die skare het Jesus as Koning verwelkom — maar Hy het na die tempel gegaan."},
    "pas/02-jesus-in-die-tempel.md": {5: "Jesus het geleer en gesond gemaak — die tempel moes weer 'n huis van gebed wees."},
    "pas/03-die-laaste-maaltyd.md": {5: "Jesus het brood en wyn gegee — onthou My, het Hy gesê."},
    "pas/04-getsemane.md": {5: "Jesus het gebid: U wil, nie myne nie — die uur van verraad was naby."},
    "pas/05-jesus-word-gevange-geneem.md": {2: "Judas het met 'n skare en fakkels gekom.", 3: "Petrus het met 'n swaard gesteek — Jesus het die geweld gestop.", 5: "Jesus is gevange geneem — die dissipels het Hom verlaat."},
    "pas/06-jesus-voor-die-raad-en-pilatus.md": {3: "Die hoëpriesters het vals getuienis gesoek.", 5: "Pilatus het Jesus aan die kruis laat oorlewer — die skare het geskreeu."},
    "pas/07-petrus-verloen-jesus.md": {3: "Petrus het drie keer ontken dat hy Jesus ken.", 5: "Toe die hoender gekraai het, het Petrus gehuil — Jesus het voorspel wat sou gebeur."},
    "pas/08-jesus-sterf-aan-die-kruis.md": {2: "Jesus is gekruisig tussen twee misdadigers.", 3: "Hy het vir die een misdadiger gesê: Vandag sal jy saam met My in die paradys wees.", 5: "Jesus het gesterf aan die kruis — Dit is volbring, het Hy gesê. Die Romeinse hoofman het erken: Hy is die Seun van God."},
    "pas/09-jesus-word-begraaf.md": {5: "Jesus is in 'n graf gelê — die storie was nog nie verby nie."},
    "pas/10-jesus-het-opgestaan.md": {3: "Die engel het gesê: Hy is nie hier nie — Hy het opgestaan!", 5: "Jesus leef — die swaarste dag het in die grootste vreugde verander."},
    "pas/11-op-pad-na-emmaus.md": {5: "Hulle het Jesus herken by die brood — en teruggekeer om te vertel: Hy leef!"},
    "pas/12-tomas-glo.md": {5: "Tomas het geglo — Jesus se opstanding was werklik."},
    "pas/13-jesus-gaan-op-na-die-hemel.md": {5: "Jesus is opgevaar — die dissipels het teruggekeer met vreugde en gebid."},
    "act/01-pinkster.md": {3: "Elkeen het in 'n taal gepraat wat die mense verstaan het.", 5: "Drie duisend is gedoop — die kerk het begin."},
    "act/02-die-vroeë-gemeente.md": {5: "Die gemeente het gedeel en gebid — die Here het daagliks mense bygevoeg."},
    "act/03-stefanus.md": {5: "Stefanus het Jesus aan die regterhand van God gesien — hy was die eerste martelaar."},
    "act/04-filippus-en-die-ethiopiër.md": {5: "Die Ethiopiër het geloof en is gedoop — hy het vreugdevol verder gegaan."},
    "act/05-saul-ontmoet-jesus.md": {5: "Saul het sy naam verander na Paulus — hy sou vir Jesus getuig."},
    "act/06-petrus-en-cornelius.md": {5: "Die Heilige Gees het op heidene neergedaal — God se redding is vir alle volke."},
    "act/07-paulus-en-silas-in-die-tronk.md": {4: "Al die boeie het losgeraak.", 5: "Die tronkbewaarder en sy huis het in Jesus geglo."},
    "act/08-paulus-in-atene.md": {5: "Sommige het geglo — Paulus het die onbekende God verkondig."},
    "act/09-paulus-se-reis-na-rome.md": {5: "Paulus het in Rome die koninkryk van God verkondig — niemand het hom weerhou nie."},
    "epi/01-paulus-skryf-briewe.md": {3: "In Romeine 8 skryf hy van die Gees wat vir ons bid.", 5: "Paulus se briewe leer gemeentes nog steeds van Jesus se liefde."},
    "rev/01-johannes-sien-die-troon.md": {5: "Johannes het gesien: God regeer — die hemel is vol lof."},
    "rev/02-die-lam-wat-waardig-is.md": {5: "Die Lam wat geslag is, is waardig — Jesus het oorwin."},
    "rev/03-god-oordeel-regverdig.md": {3: "Die boek van die lewe behoort aan die Lam.", 5: "God oordeel regverdig — en die Lam se naam is in die boek."},
    "rev/04-n-nuwe-hemel-en-n-nuwe-aarde.md": {5: "God sal by sy mense woon — alles word nuut."},
    "rev/05-die-nuwe-jerusalem.md": {5: "Daar is geen nag meer nie — die Lam verlig die stad."},
    "rev/06-kom-here-jesus.md": {5: "Die boek eindig met 'n uitnodiging: Kom, Here Jesus!"},
}


def main():
    expanded = []
    skipped = []
    for folder in FOLDERS:
        for path in sorted((ROOT / folder).glob("*.md")):
            rel = f"{folder}/{path.name}"
            before = story_words(path.read_text(encoding="utf-8"))
            if before >= TARGET_LOW:
                skipped.append((rel, before))
                continue
            if rel not in EXPANSIONS:
                print(f"MISSING: {rel}")
                continue
            merged = merge_expansions(EXPANSIONS[rel], PASS2.get(rel, {}))
            add_words = sum(len(t.split()) for t in merged.values())
            use_double = before + add_words < TARGET_LOW or before + add_words * 2 <= TARGET_HIGH
            after = expand_file(path, merged, double_insert=use_double)
            dedupe_exact_paragraphs(path)
            after = story_words(path.read_text(encoding="utf-8"))
            if after > before:
                expanded.append((rel, before, after))
            elif before >= MIN_WORDS:
                skipped.append((rel, before))

    print(f"\nExpanded {len(expanded)} files:")
    for rel, before, after in expanded:
        flag = " !" if after < TARGET_LOW or after > TARGET_HIGH else ""
        print(f"  {before:3d} -> {after:3d}{flag}  {rel}")
    print(f"\nSkipped (already >= {MIN_WORDS}): {len(skipped)}")
    for rel, wc in skipped:
        print(f"  {wc:3d}  {rel}")


if __name__ == "__main__":
    main()
