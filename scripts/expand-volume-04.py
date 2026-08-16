#!/usr/bin/env python3
"""Append story-specific expansion paragraphs to reach word-count targets."""
from pathlib import Path
import re

EXPANSIONS = {
    "01-die-engel-by-maria.md": {
        1: "Maria woon met haar familie in Nazaret. Josef is beloof aan haar. Sy werk en bid soos ander meisies in die dorp — totdat die hemel naby kom.",
        2: "Gabriel bring nie net nuus nie — hy bring die naam Jesus. Die kind sal die Seun van die Allerhoogste wees. Maria luister met stilte.",
        3: "Maria vra met eerlike hart. Gabriel antwoord met God se krag. Niks is te moeilik vir die Here nie.",
        4: "Maria se ja is klein maar groot. God begin sy plan met een dienaar wat luister en vertrou.",
        5: "Die dorp weet nog niks. Maar in Maria groei God se belofte. Josef sal ook een boodskap kry.",
    },
    "02-josef-se-droom.md": {
        1: "Josef werk met hout. Hy probeer om reg te leef. Die nuus van Maria se swangerskap maak hom stil en bekommerd.",
        2: "In die droom die engel noem Josef seun van Dawid. God herinner hom van die koningsbelofte aan sy familie.",
        3: "Jesus — die Here sal verlos. Die naam dra die werk wat God sal doen vir sy volk.",
        4: "Immanuel beteken God is met ons. Nie ver weg nie — naby in die kind.",
        5: "Josef word beskermer van die beloofde Koning. Binnekort kom die sensus na Bethlehem.",
    },
    "14-jesus-stil-die-storm.md": {
        1: "Petrus en die ander dissipels roei. Die oever is nog ver. Die lug word donker. Dan kom die wind.",
        2: "Hulle gooi water uit die boot. Golwe klim hoog. Die wind skree. Nog steeds Jesus slaap op die kussing.",
        3: "Jesus staan regop in die boot. Met sy woord die wind gaan weg. Die golwe word plat. Die dissipels is stil van wonder.",
        4: "Die dissipels ken die see — maar hulle ken nie hierdie mag nie. Net God se Seun kan wind en water beveel.",
        5: "Hulle kom veilig by die oever. Die dissipels praat stil oor wat hulle gesien het. Jesus is groter as die storm.",
    },
    "20-saggeus.md": {
        1: "Jerigo is een ou stad met palmbome. Jesus gaan deur met dissipels. Saggeus klouter hoog in die boom om te sien.",
        2: "Die menigte staan stil. Jesus roep Saggeus by sy naam. Saggeus kom gou af — vol vreugde.",
        3: "By die tafel praat Saggeus met oop hart. Mense buite murmure. Binne Saggeus beloof om terug te gee.",
        4: "Saggeus is ook een seun van Abraham. Vandag kom redding — nie môr nie.",
        5: "Mense in Jerigo sien dat Saggeus verander. Hy gee en gee terug. Jesus soek so mense.",
    },
    "21-jesus-en-die-kinders.md": {
        1: "Klein hande wys na Jesus. Ouers hurk met hulle kinders. Sommige kinders is stil — Jesus glimlag na hulle.",
        2: "Die dissipels wys met arms weg. Hulle dink Jesus moet net met groot mense praat.",
        3: "Jesus roep die dissipels naby. Hy sê dit duidelik: laat die kinders kom. Moenie weerhou nie.",
        4: "Elke kind kry een oomblik met Jesus. Hande op hoof. Seen. Jesus is nie te besig vir klein mense nie.",
        5: "Die kinders speel weg. Die ouers dank Jesus. Die dissipels leer: kinders behoort by God se koninkryk.",
    },
    "03-jesus-word-gebore.md": {
        1: "Die sensus beteken dat elke familie moet gaan waar hulle voorvaders gewoon het. Josef se familie kom van Bethlehem, die stad van koning Dawid. Die pad van Nazaret na Bethlehem is lank vir een swanger vrou.",
        2: "Hulle stap dag na dag. Maria is moeg. Josef soek een herberg — een plek waar mense kan slaap en waar kos beskikbaar is. Maar elke deurgang is vol. Elke kamer is beset.",
        3: "Uiteindelik kry hulle een stal waar die diere bly. Daar is een krip — een voerbak waar die diere eet. Dit is nie mooi nie, maar dit is veilig. Die nag val. Bethlehem rus.",
        4: "Die kind is klein en stil. Maria en Josef kyk na hom. Geen paleis. Geen goue bed. Maar God se belofte is hier — in Bethlehem, soos die profete gesê het.",
        5: "Die sterre skyn buite. In Rome weet niemand van hierdie nag nie. Maar God weet. Die Verlosser is gebore. Binnekort sal herders en wyse manne ook kom.",
    },
    "04-die-herders.md": {
        1: "Die herders sit by hulle skape. Hulle praat sag. Hulle luister vir enige gevaar in die nag. Dit is gewone werk — maar hierdie nag is anders.",
        2: "Die engel sê die Verlosser is gebore — Christus, die Here. Nie net vir Judea nie. Goeie nuus vir alle mense. Die herders se harte word vol van wonder.",
        3: "Dan kom baie engels. Hulle prys God in die hoogste. Hulle sê: vrede op aarde. Die hemel is vol lig — groot lig, wyd lig, nie om bang te maak nie.",
        4: "Die herders laat hulle skape en gaan na Bethlehem. Hulle soek een baba in een krip. Hulle vind Maria, Josef en die kind. Alles is presies soos die engel gesê het.",
        5: "Die herders vertel in Bethlehem wat hulle gesien het. Mense luister en wonder. Maria onthou alles. Die herders gaan terug en loof God. Die goeie nuus is vir alle mense.",
    },
    "05-die-wyse-manne.md": {
        1: "Die wyse manne ken die sterre. Hulle volg die ster oos na weste. Hulle bring geskenke. Hulle soek die koning van die Judeërs — nie om te veg nie, om te aanbid.",
        2: "In Jerusalem vra hulle waar die koning is. Herodes is bang. Hy roep die geleerdes. Hulle lees: Bethlehem. Herodes sê vir die wyse manne: gaan soek en kom terug.",
        3: "Herodes wil Jesus vind — maar nie om te aanbid nie. Die wyse manne gaan. Die ster gaan voor hulle uit. Hulle is vol vreugde. Bethlehem wag klein en stil.",
        4: "Hulle vind die kind by Maria. Hulle val neer en aanbid. Goud, mirre en spesiale reuk. Die koning is hier — nie in Herodes se paleis nie, in een huis.",
        5: "God waarsku hulle in een droom: moenie teruggaan na Herodes nie. Hulle neem een ander pad. God beskerm Jesus. Die ster het gelei — en God lei nog steeds.",
    },
    "06-vlug-na-egipte-terugkeer.md": {
        1: "Josef droom weer. Die engel sê: vlug na Egipte. Herodes soek die kind om hom dood te maak. Josef ontwaak vinnig. Daar is geen tyd om wag.",
        2: "Josef neem Maria en Jesus. Hulle gaan na Egipte — ver weg van Herodes. Hulle bly daar tot God sê hulle kan teruggaan. God gee hulle veiligheid.",
        3: "Herodes is woedend. Hy stuur soldate na Bethlehem. Hy laat jong seuns in die omtrek doodmaak. Dit is baie erg. Maar Jesus is veilig in Egipte.",
        4: "Na een tyd sterf Herodes. Die engel sê: gaan terug na Israel. Josef is bang vir Archelaus in Judea. God waarsku weer: gaan na Galilea, na Nazaret.",
        5: "Jesus groei op in Nazaret. So word die profeet se woord waar: hy sal Nazarener genoem word. Die Here was by hulle op elke stap van die pad.",
    },
    "07-die-seun-jesus-in-die-tempel.md": {
        1: "Jesus groei op in Nazaret. Josef werk. Maria sorg vir die huis. Elke jaar gaan hulle na Jerusalem vir die Paasfees. Dit is een groot feest vir God se volk.",
        2: "Toe Jesus twaalf is, gaan hulle weer. Na die feest vertrek die groep na huis. Josef en Maria dink Jesus is saam. Drie dae soek hulle hom in die menigte.",
        3: "Hulle vind Jesus in die tempel. Hy sit by die geleerdes. Hy luister. Hy vra vrae. Almal wonder oor sy antwoorde. Jesus is jong — maar sy wysheid is groot.",
        4: "Maria sê: Kind, ons was bekommerd. Jesus sê: Moet ek nie in die huis van my Vader wees nie? God is sy Vader. Jesus gaan huis met hulle en is onderdanig.",
        5: "In Nazaret groei Jesus verder. Hy word sterker en wiser. God se genade is op hom. Jesus leer en groei — en hy eer sy ouers elke dag.",
    },
    "08-johannes-die-doper-jesus-se-doop.md": {
        1: "By die Jordaanrivier kom Johannes die Doper. Hy roep: keer om! Berei die weg vir die Here. Die koninkryk van die hemel is naby. Mense kom van ver om te luister.",
        2: "Jesus kom van Galilea. Hy wil deur Johannes gedoop word. Johannes sê: ek het meer nodig dat jy my doop. Jesus sê: laat dit geskied. Dit is reg so.",
        3: "Johannes doop Jesus in die rivier. Jesus stap in die water. Toe hy uitkom, die hemel gaan oop. Die Heilige Gees daal neer soos een duif op Jesus.",
        4: "Uit die hemel kom een stem: Dit is my geliefde Seun. In hom het ek my welbehae gevonden. God self maak bekend wie Jesus is. Die Gees is op hom.",
        5: "Jesus stap verder. Johannes bly roep mense om te keer om. God het gesproken by die rivier. Jesus is gereed vir sy werk in die wêreld.",
    },
    "09-jesus-word-versook.md": {
        1: "Na die doop gaan Jesus in die woestyn. Die Heilige Gees lei hom daar. Veertig dae sonder kos. Jesus is honger. Die woestyn is groot en stil.",
        2: "Die versoeker sê: maak klippe brood. Jesus antwoord met die Skrif: die mens lewe van God se woord. Jesus weier. Hy vertrou God meer as kos.",
        3: "Die versoeker wys die hoë tempel. Val af — God sal opvang. Jesus antwoord: jy moet die Here aanbid en hom alleen dien. Jesus weier weer.",
        4: "Die versoeker wys alle koninkryke. Buig en aanbid my. Jesus sê: Weg van my, Satan! Aanbid die Here alleen. Die derde versoeking faal ook.",
        5: "Die versoeker vertrek. Engels kom en dien Jesus. Jesus wen deur God se woord te vertrou. Hy is gereed om mense te dien — nie om kwaad te doen nie.",
    },
    "10-jesus-roept-dissipels-water-word-wyn.md": {
        1: "Jesus roep mense om hom te volg. Twee manne volg Johannes. Johannes wys: Kyk, die Lam van God. Hulle gaan na Jesus. Jesus sê: Kom en sien.",
        2: "Andreas bring Simon. Jesus noem hom Petrus. Filippus bring Natanael. Natanael vra: Kan iets goed uit Nazaret kom? Filippus sê: Kom en sien. Mense begin volg.",
        3: "In Kana is een bruiloft. Die wyn is op. Maria sê vir Jesus: hulle het geen wyn nie. Jesus sê vir die dienaars: doen wat hy vir jou sê.",
        4: "Ses waterkruiken word vol water. Die dienaars skink. Die water is wyn — goeie wyn. Die bruiloftmeester is verbaas. Jesus openbaar sy glorie.",
        5: "Dit is die eerste wonder in Kana. Die dissipels glo in hom. Jesus roep en wys: kom en sien — en sy glorie word sigbaar.",
    },
    "11-nikodemus.md": {
        1: "Nikodemus is een Fariseër en lid van die Raad. Hy is geleerd. Maar iets in Jesus trek hom. Op een nag kom hy na Jesus — in die donker, stil.",
        2: "Nikodemus sê: Rabbi, ons weet jy is een leermeester van God. Jesus sê: Niemand kan die koninkryk sien sonder om opnieuw gebore te word.",
        3: "Nikodemus vra hoe een ou mens weer gebore kan word. Jesus praat van water en Gees. God gee nuwe lewe. Jesus sê: soos die slang opgehef was, so sal die Seun opgehef word.",
        4: "Jesus sê: God so liefhet die wêreld dat hy sy Seun gegee het. Wie in hom glo, het ewige lewe. God stuur nie die Seun om te veroordeel nie — maar om te red.",
        5: "Nikodemus luister. Nie alles is duidelik nog nie. Maar Jesus se woord bly: opnieuw gebore, opgehef, God so liefhet die wêreld.",
    },
    "12-die-vrou-by-die-put.md": {
        1: "Jesus kom deur Samaria. By Sikár is een put. Jesus is moeg en sit. Sy dissipels gaan kos koop. Jesus wag alleen by die put.",
        2: "Een Samaritaanse vrou kom put. Jesus vra vir water. Sy is verbaas — Jode en Samaritane praat nie gewoonlik saam nie. Jesus sê: ek kan lewende water gee.",
        3: "Die vrou vra waar. Jesus sê: wie hierdie water drink, dors weer. Maar my water word een fontein tot ewige lewe. Die vrou wil dit hê.",
        4: "Jesus praat van ware aanbidding — in gees en waarheid. Die vrou sê: die Messias kom. Jesus sê: Ek is dit — ek wat met jou praat.",
        5: "Die vrou gaan na die stad. Baie mense kom luister. Hulle sê: ons glo — Jesus is die Verlosser van die wêreld. Lewende water vir alle mense.",
    },
    "13-jesus-leer-op-die-berg.md": {
        1: "Groot menigtes volg Jesus. Hy gaan op een berg. Die dissipels sit naby. Jesus begin leer — vir alle mense wat wil luister.",
        2: "Jesus sê: Gelukkig die armes — die koninkryk behoort aan hulle. Gelukkig die sagmoediges. Gelukkig die rein van hart — hulle sal God sien. God se pad is vol genade.",
        3: "Jesus leer hoe om te bid: Ons Vader in die hemel, laat u naam geheilig word. Laat u koninkryk kom. Gee ons ons daaglikse brood. Vergewe ons soos ons vergewe.",
        4: "Jesus sê: twee bouers. Een bou op rots. Een op sand. Storm kom. Die huis op rots bly. Die huis op sand val. Wie Jesus se woorde doen, bou op rots.",
        5: "Die mense luister. Jesus leer nie om bang te maak nie — hy leer hoe om op God te bou. Bid. Wees sagmoedig. Doen wat God sê.",
    },
    "14-jesus-stil-die-storm.md": {
        1: "Aan die einde van een dag langs die see van Galilea sê Jesus: Laat ons oorsee gaan. Hulle gaan in een boot. Jesus is moeg. Die see is kalm. Die wind is stil.",
        2: "Skielik kom een groot storm. Golwe slaan in die boot. Water kom in. Die dissipels roei hard. Jesus slaap op een kussing in die agterkant. Hulle maak hom wakker.",
        3: "Jesus word wakker. Hy gebied die wind en sê vir die see: Wees stil! Wees rustig! Die wind gaan weg. Groot stilte. Die golwe word kalm. Jesus praat — die see luister.",
        4: "Jesus sê: Waarom is jy bang? Waarom geen geloof? Die dissipels vra: Wie is hierdie? Selfs wind en see gehoorsaam hom. Net God se Seun kan dit doen.",
        5: "Die boot dryf op kalm water. Die dissipels onthou. Jesus is groter as die storm. Die Here was by hulle in die boot.",
    },
    "15-vyfduisend-word-gevoed.md": {
        1: "Groot menigtes volg Jesus oor die see. Hy gaan op een berg. Byna vyfduisend man is daar, plus vroue en kinders. Jesus vra Filippus: waar koop ons brood?",
        2: "Filippus sê: tweehonderd denarius is nie genoeg nie. Een seun bring vyf brode en twee vis. Jesus sê: laat die mense sit. Hulle sit op die gras.",
        3: "Jesus neem die brode en vis. Hy bedank God. Hy breek en gee aan die dissipels. Die dissipels gee aan die mense. Almal eet. Almal word vol.",
        4: "Hulle tel twaalf mandjies vol oorblyfsels. Meer as wat hulle begin het. Die mense sê: hier is die profeet. Jesus gee nie net genoeg nie — hy gee oorvloed.",
        5: "Jesus sien dat mense hom wil dwing om koning te word. Hy gaan weg na die berg. Vyfduisend gevoed. God sorg soos in die woestyn met manna.",
    },
    "16-jesus-loop-op-die-water.md": {
        1: "Na die vyfduisend stuur Jesus dissipels in die boot. Jesus gaan bid op die berg. Dit is nag. Die boot is in die middel van die see. Wind is teen hulle.",
        2: "In die vierde wag van die nag sien hulle Jesus loop op die see. Hulle denk dit is een spook. Hulle skree. Jesus sê: Wees sterk. Dit is ek. Moenie bang wees nie.",
        3: "Petrus sê: as dit jy is, beveel dat ek na jou kom. Jesus sê: Kom. Petrus stap op die water. Dan sien hy die wind en sink. Hy roep: Here, red my!",
        4: "Jesus gryp Petrus. Hulle stap in die boot. Die wind gaan weg. Die dissipels val neer: Waarlik, jy is die Seun van God. Hulle aanbid hom.",
        5: "Die boot kom veilig by die oever. Die nag was bang — maar Jesus was daar. Op die water. In die boot. Die Seun van God.",
    },
    "17-die-barmhartige-samaritaan.md": {
        1: "Een wetkundige vra Jesus: wat moet ek doen vir ewige lewe? Jesus vra: Wat sê die wet? Liefhe God en jou naaste. Die man vra: Wie is my naaste?",
        2: "Jesus vertel: een man gaan van Jerusalem na Jericho. Rowers beseer hom en laat hom half dood. Een priester kom — gaan verby. Een Leviet kom — gaan ook verby.",
        3: "Een Samaritaan kom. Hy sien die man. Hy doet olie en wyn op die wonde. Hy bring hom na een herberg. Hy betaal — en sê hy sal meer betaal as nodig.",
        4: "Jesus vra: Wie was naaste? Die wetkundige sê: die een met barmhartigheid. Jesus sê: Gaan en doen dieselfde. Die naaste is wie help — selfs across grense.",
        5: "Jesus wys: liefde vir God en naaste gaan saam in wat jy doen. Barmhartigheid is nie net vir vriende nie. Gaan en doen dieselfde.",
    },
    "18-die-verlore-seun.md": {
        1: "Jesus vertel: een man het twee seuns. Die jonger sê: gee my my deel. Die vader gee. Die jonger gaan na een ver land met al sy geld.",
        2: "In die ver land maak hy alles op. Hongersnood kom. Hy werk vir varken. Hy is honger. Hy besef: my vader se werkers het kos — en ek sterf hier.",
        3: "Hy sê: ek gaan terug. Ek is nie waardig om seun genoem te word nie — maak me net een werker. Terwyl hy nog ver is, sy vader sien hom en hardloop.",
        4: "Die vader omhels hom. Bring beste jas, ring, feest. My seun was dood en leef weer. Die ouer broer is kwaad. Die vader sê: jou broer is terug — wees vrolik.",
        5: "Jesus wys: God is soos die vader. God verwelkom wie terugkom. Vreugde wanneer verlore gevind word — nie net wanneer iemand altyd reg bly nie.",
    },
    "19-jesus-wek-lasarus-op.md": {
        1: "In Betánia is Lasarus siek — Martha en Maria se broer. Hulle stuur vir Jesus. Jesus sê: dit lei tot God se glorie — maar hy wag twee dae nog.",
        2: "Lasarus sterf. Jesus sê: Lasarus is dood. Kom, laat ons gaan. Lasarus is vier dae in die graf. Martha sê: as jy hier was, my broer sou nie gesterf het nie.",
        3: "Jesus sê: Ek is die opstanding en die lewe. Wie in hom glo, sal lewe. Martha sê: Ja, Here, jy is die Christus. Maria kom en treur ook.",
        4: "Jesus huil met hulle. By die graf roep hy: Lasarus, kom uit! Lasarus kom uit — hande en voete omwond. Jesus sê: maak hom los.",
        5: "Lasarus leef weer. Baie glo. Jesus is opstanding en lewe — en hy huil met die wat treur. Die dood is nie die laaste woord nie.",
    },
    "20-saggeus.md": {
        1: "In Jerigo is Saggeus — rijk man en tollenaar. Baie mense haat tollenaars. Saggeus is klein. Hy kan nie deur die menigte sien nie. Hy klim in een boom.",
        2: "Jesus kom langs. Hy kyk op: Saggeus, kom gou af. Vandag moet ek by jou bly. Saggeus is verheug. Mense murmure: hy gaan by een sondaar bly.",
        3: "Saggeus sê: half my goed aan armes. As ek te veel gehef het, vier maal terug. Jesus kom om verlore te soek — en Saggeus antwoord met verandering.",
        4: "Jesus sê: Vandag is redding vir hierdie huis gekom. Die Seun van die mens soek en red verlore sondaars. Vandag — nie môr nie.",
        5: "Saggeus gee terug en gee aan armes. Jesus soek die verlore in gewone strate. Saggeus is nie dieselfde man meer nie.",
    },
    "21-jesus-en-die-kinders.md": {
        1: "Ouers bring klein kinders na Jesus. Babas en jong kinders. Hulle wil dat hy hulle sal seen — hande op hulle hoof. Die kinders is klein en vol lewe.",
        2: "Die dissipels maak die mense weg. Hulle sê: die kinders pla. Jesus is te besig. Die dissipels wys ouers en kinders weg.",
        3: "Jesus is ontsteld. Hy sê: Laat die kinders na my kom. Moenie hulle weerhou nie. Vir sulke behoort die koninkryk van God.",
        4: "Jesus neem kinders in sy arms. Hy leg hande op hulle en seen hulle. Hy sê: Wie nie die koninkryk aanneem soos een kind nie, sal nooit ingaan nie.",
        5: "Die kinders is by Jesus. Ouers is tevred. Jesus wys: kom na my — selfs die klein kinders. Oop en bereid om te ontvang, soos een kind.",
    },
    "22-die-verheerliking.md": {
        1: "Jesus neem Petrus, Jakobus en Johannes op een hoë berg. Net die vier. Hulle klim hoog. Die lug is stil. Hulle weet nie wat wag nie.",
        2: "Jesus verander. Sy klere blink — witter as enige mens kan was. Sy gesig skyn. Moses en Elia praat met Jesus. Petrus sê: dit is goed om hier te wees.",
        3: "Een wolk bedek hulle. Stem uit die wolk: Dit is my geliefde Seun. Luister na hom! Die dissipels val op hul gesig. Hulle is bang. God spreek.",
        4: "Jesus sê: Staan op. Moenie bang wees nie. Net Jesus bly — Moses en Elia weg. Jesus sê: moenie vir enigiemand sê tot die Seun opgewek is.",
        5: "Hulle gaan af van die berg. Drie dissipels sien glorie — en hoor: luister na hom. Die glorie wys wie Jesus is en wat nog kom.",
    },
    "23-jesus-gaan-na-jerusalem.md": {
        1: "Die tyd nader. Jesus stel sy gesig na Jerusalem. Vasberade. Jerusalem wag — lyding, dood en opstanding. Jesus weet wat daar kom.",
        2: "Jesus sê aan die twaalf: ons gaan op na Jerusalem. Die Seun sal oorhandig word, veroordeel, bespot, doodgemaak — en op die derde dag opgewek. Hulle verstaan nie.",
        3: "Griekse mense wil Jesus sien. Jesus sê: die tyd het gekom dat die Seun verheerlik sal word. Soos een korrel graan moet sterf om vrug te bring.",
        4: "Jesus sê: wie my liefhet, volg my. Wanneer ek opgehef word, sal alle mense tot myself getrek word. Jerusalem wag — maar Jesus gaan vir alle mense.",
        5: "Jesus gaan na Jerusalem. Lyding en opstanding wink. Die korrel sal sterf en vrug bring. Die volgende groot storie begin in Jerusalem — in Volume 5.",
    },
}


def get_page_num(header_line: str) -> int | None:
    m = re.search(r"Bladsy (\d+)", header_line)
    return int(m.group(1)) if m else None


def expand_file(path: Path, expansions: dict[int, str]):
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    current_page = None
    inserted_for_page = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## Bladsy"):
            current_page = get_page_num(line)
        out.append(line)
        i += 1
        # After narrative block on pages 1-5, before --- separator
        if current_page and current_page <= 5 and current_page not in inserted_for_page:
            if line.strip() == "---" and current_page in expansions:
                # Insert before the --- we just appended - need different logic
                pass
        # Detect end of page narrative: next line is --- after content
        if line.strip() == "---" and current_page and current_page <= 5:
            if current_page in expansions and current_page not in inserted_for_page:
                # Remove the --- we added, insert expansion, re-add ---
                out.pop()  # remove ---
                out.append("")
                out.append(expansions[current_page])
                out.append("")
                out.append("---")
                inserted_for_page.add(current_page)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    base = Path("/agent/manuscripts/volume-04")
    targets = [
        "01-die-engel-by-maria.md",
        "02-josef-se-droom.md",
        "06-vlug-na-egipte-terugkeer.md",
        "14-jesus-stil-die-storm.md",
        "20-saggeus.md",
        "21-jesus-en-die-kinders.md",
    ]
    for fname in targets:
        if fname in EXPANSIONS:
            expand_file(base / fname, EXPANSIONS[fname])
    print("Expanded", len([f for f in targets if f in EXPANSIONS]), "files")


if __name__ == "__main__":
    main()
