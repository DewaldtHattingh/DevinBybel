#!/usr/bin/env python3
"""Apply word-count expansions to short v2 OT manuscripts (<450 words)."""
import re
from pathlib import Path

FOLDERS = ['exo', 'num', 'deu', 'jsh', 'jdg', 'rut', 'abr', 'jos', 'gen', 'job']

def count_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    lines = content.split('\n')
    word_count = 0
    in_beeldnota = False
    skip_sections = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'): continue
        if stripped.startswith('!['): continue
        if stripped.startswith('> **Beeldnota:**'):
            in_beeldnota = True; continue
        if in_beeldnota:
            if stripped.startswith('>') or stripped == '': continue
            in_beeldnota = False
        if 'produksie-notas' in stripped.lower() or stripped.startswith('## Produksie'):
            skip_sections = True; continue
        if skip_sections: continue
        if stripped == '---': continue
        if not stripped: continue
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'〔[^〕]+〕', '', text)
        word_count += len(text.split())
    return word_count

def append_to_page(text, page_num, addition):
    """Append sentence(s) to last narrative line on a page."""
    marker = f"## Bladsy {page_num} —"
    start = text.find(marker)
    if start < 0:
        return text, False
    next_page = re.search(r'\n## Bladsy \d+ —|\n## Bladsy 6 —', text[start + 10:])
    end = start + 10 + next_page.start() if next_page else len(text)
    section = text[start:end]
    if addition in section:
        return text, False
    # Find last non-empty narrative line before ---
    lines = section.split('\n')
    for i in range(len(lines) - 1, -1, -1):
        s = lines[i].strip()
        if s and not s.startswith('#') and not s.startswith('!') and not s.startswith('>') and s != '---':
            lines[i] = lines[i].rstrip() + ' ' + addition
            new_section = '\n'.join(lines)
            return text[:start] + new_section + text[end:], True
    return text, False

# Per-file: page_num -> addition text (biblical/connective, B/C tags)
EXPANSIONS = {
    "exo/02-die-brandende-bos.md": {
        1: "Hy het die lyk in die sand begrawe. Toe Farao dit gehoor het, wou hy Moses doodmaak.",
        2: "Moses het met Sippra 'n seun gekry, Gersom. Veertig jaar het verbygegaan terwyl Israel in Egipte swaar gewerk het.",
        3: "Die Engel van die Here het in die bos verskyn. Moses het gewonder: Waarom brand die bos nie op nie?",
        4: "Die Here het gesê: Ek het die nood van my volk in Egipte gesien en hulle klaagte gehoor.",
        5: "Die Here het ook tekens gegee — 'n staf wat in 'n slang verander, en 'n hand wat siek en weer gesond word.",
    },
    "exo/03-moses-voor-farao.md": {
        1: "Moses en Aäron het die oudstes van Israel bymekaar geroep. Toe hulle gehoor het dat God hulle onthou het, het hulle gebuig.",
        2: "Die oorsigbeamptes het die volk geslaan omdat hulle nie klaargespeel het nie. Hulle het Moses en Aäron blameer.",
        3: "Die Here het gesê: Deur 'n sterk hand sal Ek hulle uitdryf. Groter tekens sou kom.",
        4: "Farao se towenaars het dieselfde met hulle stawwe gedoen, maar Moses se slang het hulle slange opgevreet.",
        5: "Deur my hand aan Farao en aan Egipte sal Ek my teken doen, en dan sal Israel uitgaan.",
    },
    "exo/04-bloed-paddas-en-muggies.md": {
        1: "Die Here het vir Moses gesê: Sê vir Aäron, neem jou staf en strek jou hand uit oor die riviere van Egipte.",
        2: "Die vis in die rivier het gesterf. Sewe dae lank kon die Egiptenaars nie drink nie.",
        3: "Farao het vir Moses gesê: Bid dat die paddas weggaan. Moses het gebid, maar Farao het weer hard geword.",
        4: "Aäron het sy staf geslaan op die stof van die aarde, en die stof het lewendige muggies geword.",
        5: "Drie plae was verby, maar Farao het steeds nie laat gaan nie. Die Here was by sy volk in Gosien.",
    },
    "exo/05-vliee-vee-en-sere.md": {
        1: "Die Here het gesê: As jy weier, sal Ek swerms vlieë op jou en jou dienaars en jou volk stuur.",
        2: "In Gosien, waar Israel gewoon het, was daar geen vlieë nie. Die Here het onderskeid gemaak.",
        3: "Al die vee van die Egiptenaars het gesterf, maar nie een van Israel se vee nie.",
        4: "Moses en Aäron het stof in die lug gegooi, en dit het sere geword op mense en diere.",
        5: "Ses plae was verby. Elke keer het die Here onderskeid gemaak tussen Israel en Egipte.",
    },
    "exo/06-hael-en-sprinkane.md": {
        1: "Moses het sy staf na die hemel uitgestrek. Die Here het donder en hael gestuur.",
        2: "Dit was die ergste storm wat Egipte ooit gesien het. In Gosien was daar geen hael nie.",
        3: "'n Ooswind het sprinkane gebring. Hulle het alles geëet wat die hael oorgelaat het.",
        4: "Die Here het 'n sterk westewind gebring en die sprinkane in die Rooi See gewaai.",
        5: "Agt plae was verby. Nog een groot pla sou kom — die ergste van almal.",
    },
    "exo/07-duisternis.md": {
        1: "Moses het sy hand na die hemel uitgestrek. Drie dae lank was daar duisternis oor Egipte.",
        2: "Niemand het opgestaan om te beweeg — drie dae lank. Dit was 'n swaar, voelbare duisternis.",
        3: "By Israel was daar lig in hulle wonings. Farao het vir Moses gesê: Moenie my weer sien nie.",
        4: "Nege plae was verby. Farao se hart was so hard dat hy steeds nie laat gaan nie.",
        5: "Die volk wag nou op die laaste pla. Moses en Aäron het Israel vertel wat nog sou kom.",
    },
    "exo/08-die-eerste-paasfees.md": {
        1: "Elke gesin moes 'n lam kies — een sonder gebrek, 'n mannetjie-lam, een jaar oud.",
        2: "Geen suurdeeg moes in hulle huise wees nie — vir sewe dae moes hulle net ongesuurde brood eet.",
        3: "Geen Israeliet moes uit sy huis gaan tot die môre nie.",
        4: "Moses het die volk geleer om hierdie fees elke jaar te herdenk.",
        5: "Hulle het gewag op die nag wanneer die Here deur Egipte sou gaan.",
    },
    "exo/09-die-tiende-pla.md": {
        1: "Elke eerstgeborene in Egipte sou sterf — van Farao se seun af tot die eerstgeborene van die slaaf by die meule.",
        2: "Israel het binne gebly, met bloed op hulle deure — op die deurposte en die balk bo die deur.",
        3: "In Israel se huise, waar die bloed was, het niemand gesterf nie.",
        4: "Farao het Moses en Aäron in die nag geroep: Trek uit, julle en julle skape en julle beeste.",
        5: "Die Here se oordeel was werklik — maar waar die bloed was, het Hy verbygegaan.",
    },
    "exo/10-israel-verlaat-egipte.md": {
        1: "Hulle het silwer en goud en klere gegee. Met hulle was ook 'n groot menigte gemengde volk.",
        2: "Dit was dieselfde nag as die Paasfees — die veertiende dag van die eerste maand.",
        3: "Josef se bene het saam gegaan, soos Josef gesweer het toe hy gesterf het.",
        4: "Die wolk het hulle bedags gelei, en die vuur het hulle snags lig gegee.",
        5: "Die Here lei sy volk. Hy was by hulle op elke stap van die pad.",
    },
    "exo/11-farao-verander-van-plan.md": {
        1: "Die Here het Moses laat draai en kamp maak by Pi-Hahirot, tussen Migdol en die see.",
        2: "Hy het sy strydwagens en ruiters gereed gemaak — ses honderd uitgesoekde strydwagens.",
        3: "Voor hulle was die Rooi See. Agter hulle die leër van Farao.",
        4: "Die Here sal vir julle veg, en julle moet stil wees.",
        5: "Die wolk het agter Israel gestaan. Die Egiptenaars kom nader met hulle strydwagens.",
    },
    "exo/12-deur-die-rooi-see.md": {
        1: "Die Here het 'n sterk oostewind die hele nag geblaas. Die water het teruggewyk.",
        2: "Die hele nag het die een nie nader aan die ander gekom nie.",
        3: "Water staan links en regs soos mure — 'n muur aan hulle regterkant en linkerkant.",
        4: "Die Egiptenaars het gesê: Laat ons vlug van Israel af, want die Here veg vir hulle!",
        5: "Miryam, die profetes, het 'n trommel geneem en die vroue het agter haar uitgegaan.",
    },
    "exo/13-brood-en-water-in-die-woestyn.md": {
        1: "Hulle het die vleispotte in Egipte onthou. Die Here het gesê: Ek sal brood uit die hemel laat reën.",
        2: "Elkeen moet net genoeg vir daardie dag insamel — twee liter per persoon.",
        3: "Moses het 'n kruik vol manna voor die Here bewaar vir toekomstige geslagte.",
        4: "Die Here het vir Moses gesê: Slaan op die rots by Horeb, en water sal uitkom.",
        5: "Moses het die plek Massa en Meriba genoem, want Israel het die Here daar getoets.",
    },
    "exo/14-sinai-en-die-tien-gebooie.md": {
        1: "Israel het by die berg Sinai gekamp — op die derde nuwe maand nadat hulle uit Egipte getrek het.",
        2: "Die berg Sinai het rook soos 'n oond. Die volk moes nie naby die berg kom nie.",
        3: "Ek is die Here jou God wat jou uit Egipte uitgelei het. Moenie die Naam van die Here misbruik nie.",
        4: "Hulle was bang vir die heerlikheid van die Here — die berg het gebrand met vuur.",
        5: "Die Here het die woorde op twee stene tablette geskryf — die werk van God.",
    },
    "exo/15-die-goue-kalf.md": {
        1: "Moses het veertig dae en veertig nagte op die berg gebly. Die volk het lank gewag.",
        2: "Aäron het al die goue oorskote laat bring en 'n beeld van 'n kalf gemaak.",
        3: "Moses het vir die Here gesmeek: Onthou Abraham, Isak en Israel.",
        4: "Hy het die kalf verbrand en tot stof vermaal. Drie duisend manne het gesterf.",
        5: "Die Here het nuwe tablette geskryf en sy verbond hernu.",
    },
    "exo/16-die-tabernakel.md": {
        1: "Volgens alles wat Ek jou wys — die patroon van die tent — so moet julle dit maak.",
        2: "Goud en silwer, pers en rooi en bloupurper stof, fyn linne, bokhare en akasia-hout.",
        3: "Binne was die ark van die verbond, die altaar en die lampstand van suiwer goud.",
        4: "Moses het die tabernakel opgerig op die eerste dag van die eerste maand.",
        5: "Moses kon nie ingaan nie, want die wolk en die heerligheid van die Here het die tabernakel gevul.",
    },
    "num/01-die-twaalf-verkenners.md": {
        1: "Moses het twaalf manne gestuur van die woestyn van Paran — een uit elke stam.",
        2: "Die land vloei oor van melk en heuning, maar die mense is sterk en die stede versterk.",
        3: "Kaleb en Josua het gesê: As die Here welbehae aan ons het, sal Hy ons inbring.",
        4: "Veertig dae, veertig jaar — hierdie geslag sal nie die land inkom nie.",
        5: "Hulle is teruggedryf tot by Horma. Kaleb en Josua sou wel die land sien.",
    },
    "num/02-die-koper-slang.md": {
        1: "Daar is geen brood en geen water nie, en ons haat hierdie ellendige kos — die manna.",
        2: "Baie mense van Israel het gesterf. Moses het vir die volk gebid.",
        3: "Moses het 'n slang van koper gemaak en dit op 'n paal opgerig.",
        4: "Baie mense het na die slang gekyk en lewe gekry.",
        5: "Die volk het verder getrek na Obot.",
    },
    "deu/01-moses-se-laaste-woorde.md": {
        1: "Sy oë was nie dof nie en sy krag was nie verminder nie. Hy het die wet vir Israel herhaal.",
        2: "Moses het Josua hande opgelê voor die hele gemeenskap.",
        3: "Van Nebo af kon Moses die hele beloofde land sien — maar nie daarheen gaan nie.",
        4: "Dit was die land van melk en heuning wat God aan die patriarge beloof het.",
        5: "Niemand weet waar sy graf is nie. Israel het dertig dae vir hom bewee.",
    },
    "jsh/01-josua-en-die-jordaan.md": {
        1: "Josua was Moses se dienaar. Die Here het gesê: Trek op en gaan die land in.",
        2: "Die rivier was vol — oesfeestyd — en die water het oor al sy banke geloop.",
        3: "Die water wat van bo af gekom het, het opgestaan soos 'n dam ver by die stad Adam.",
        4: "Twaalf klippe uit die middel van die Jordaan, waar die priesters se voete gestaan het.",
        5: "Israel staan nou in die beloofde land, oorkant Jerigo.",
    },
    "jsh/02-jerigo.md": {
        1: "Ragab het die spioene op die dak versteek. Haar huis was in die muur van Jerigo.",
        2: "Sy het gesê: Ek weet die Here julle hierdie land gegee het.",
        3: "Sewe priesters het sewe jubelhorens voor die ark geblaas.",
        4: "By die sewende keer het die priesters die hoorne geblaas en die volk geskreeu.",
        5: "Ragab en haar familie is in Israel laat leef.",
    },
    "jsh/03-ai-en-agan.md": {
        1: "Die Here het gesê: Moenie alles van Jerigo vir julleself neem nie — dit is gewy.",
        2: "Sowat ses en dertig manne is dood. Israel se harte het gesmelt.",
        3: "Daar is verbode goed in die kamp. Verwyder die sonde uit julle midde.",
        4: "Agan het 'n Babiloniese mantel, silwer en goud gesteel en onder sy tent versteek.",
        5: "Die tweede keer het Josua 'n hinderlaag geleg en Ai geneem.",
    },
    "jdg/01-debora-en-barak.md": {
        1: "Koning Jabin het in Hasor gewoon. Sisera het nege honderd yster strydwagens gehad.",
        2: "Debora het onder die palmboom tussen Rama en Bet-el gesit.",
        3: "Barak het van Naftali en Sebulon opgetrek met tienduisend man.",
        4: "Die Here het die strydwagens in verwarring gebring by die Kishonrivier.",
        5: "Jael was die vrou van Heber die Keniet. Sy het Sisera 'n kom melk gegee.",
    },
    "jdg/02-gideon-geroep.md": {
        1: "Die Midianiete het Israel se oes vernietig. Israel het in bergspore gewoon uit vrees.",
        2: "Gideon het die altaar van Baäl in die nag afgebreek met tien diensbode.",
        3: "Die eerste nag was die wol nat en die grond droog. Die tweede nag was dit omgekeerd.",
        4: "Twee en twintig duisend man het gekom, maar die Here het gesê: Daar is te veel.",
        5: "Gideon het Midian verslaan. Israel het veertig jaar rus gehad.",
    },
    "jdg/03-gideon-se-driehonderd.md": {
        1: "Eerst het die Here twee en twintig duisend man weggestuur. Toe nog drie honderd.",
        2: "Gideon het 'n droom gehoor: 'n broodrol het die tent omvergewerp.",
        3: "Elke man het 'n trompet, 'n leë kleipot en 'n fakkels in die pot gehad.",
        4: "Hulle het geroep: 'n Swaard vir die Here en vir Gideon!",
        5: "Die leiers Oreb en Zeeb is gevang. Israel het Midian onderworpe gemaak.",
    },
    "jdg/04-simson-word-gebore.md": {
        1: "Manoah was van die geslag van Dan. Sy vrou was onvrugbaar.",
        2: "Die seun sou 'n Nasireër wees — geen wyn, geen onrein kos, geen skeermes oor sy hoof.",
        3: "Die engel het in die vlam van die altaar opgegaan.",
        4: "Hulle het hom Simson genoem. Die Here het die seun seën.",
        5: "Die Gees van die Here het begin om hom te roer in die kamp van Dan.",
    },
    "jdg/05-simson-en-die-leeu.md": {
        1: "Simson het gesê: Kry vir my hierdie vrou. Sy ouers wou hê hy moet in Israel trou.",
        2: "Die Here het hierdie gebeurtenis beplan om die Filistyne te straf.",
        3: "Hy het die leeu se bek oopgeruk — hy het niks in sy hand gehad nie.",
        4: "Later het bye 'n kolonie in die leeu se karkas gemaak en heuning geproduseer.",
        5: "Simson se troue in Timna sou die begin wees van sy stryd met die Filistyne.",
    },
    "jdg/06-simson-se-raaisel.md": {
        1: "Simson het sewe dae lank feesgehou. Die verloorders moes dertig linnegewades gee.",
        2: "Die geheim was die leeu en die heening langs die pad — net Simson het dit geweet.",
        3: "Die Filistyne het Simson se vrou gedreig: Ons sal jou en jou pa se huis verbrand.",
        4: "Simson het na Askalon gegaan en dertig manne verslaan.",
        5: "Simson se vrou is aan sy metgesel gegee. Die konflik het erger geword.",
    },
    "jdg/07-simson-teen-die-filistyne.md": {
        1: "Simson se vrou en haar pa is verbrand. Simson was woedend.",
        2: "Hy het drie honderd jakkalse gevang en fakkels tussen hulle sterte vasgemaak.",
        3: "Drie duisend man van Juda het Simson gebind en na Lehi gebring.",
        4: "Hy het 'n kaakbeen van 'n esel gegryp en daarmee duisend man verslaan.",
        5: "God het water uit 'n holte laat kom. Simson het twintig jaar as rigter gelei.",
    },
    "jdg/08-simson-en-delila.md": {
        1: "Die vyf Filistynse vorste het Delila silwer gebied — elf honderd stukke elk.",
        2: "Simson het drie keer vals antwoorde gegee. Elke keer het hy die Filistyne ontsnap.",
        3: "'n Skeermes het nooit oor sy hoof gekom nie — hy is 'n Nasireër van God.",
        4: "Die Gees van die Here het van hom gewyk. Die Filistyne het hom na Gaza gebring.",
        5: "Sy haar het begin teruggroei. Die Here het hom nie heeltemal verlaat nie.",
    },
    "jdg/09-simson-se-laaste-gebed.md": {
        1: "Simson het in die tronk gemaal — soos 'n os by 'n molen.",
        2: "Hulle het Dagon prysgegee: Ons god het ons vy in ons hand gegee.",
        3: "Drie duisend man en vrou was op die dak om Simson te sien.",
        4: "Hy het die pilare laat wankel. Die tempel het op almal geval.",
        5: "Hy is begrawe tussen Zora en Eshtaol in Manoah se graf.",
    },
    "rut/01-rut-en-naomi.md": {
        1: "Elimelek was van Betlehem in Juda. Die hongersnood het hulle na Moab gedryf.",
        2: "Mahlon en Chilion het Moabitiese vroue getrou — Orpa en Rut.",
        3: "Naomi het gesê: Die Here se hand het teen my uitgestrek.",
        4: "Rut het gesê: Waar jy sterf, sal ek sterf. Net die dood sal ons skei.",
        5: "Hulle het in Betlehem aangekom aan die begin van die koringoogst.",
    },
    "rut/02-rut-en-boas.md": {
        1: "Rut het in die veld van Boas geval — 'n familielid van Elimelek.",
        2: "Die wet sê arm mense mag aren agter die oesers optel.",
        3: "Boas het vir Rut gesê: Die Here vergoed jou werk onder sy vleuels.",
        4: "Boas het die loskoping voltooi voor die ouens van die stad.",
        5: "Obed was die oupa van Isai — en uit daardie gesin sou Dawid kom.",
    },
    "abr/01-abram-word-geroep.md": {
        1: "Abram het in Ur in Mesopotamië gewoon. Die Here het gesê: Gaan na 'n land wat Ek jou sal wys.",
        2: "Deur jou sal alle families op aarde geseën word. Abram was sewentig jaar toe hy vertrek het.",
        3: "Die Here het aan Abram verskyn by die groot boom More en gesê: Aan jou nageslag sal Ek hierdie land gee.",
        4: "Hy het 'n altaar gebou tussen Bet-el en Ai en die Here aangeroep.",
        5: "Abram het geglo en die Here het hom gereken as regverdig.",
    },
    "abr/02-god-se-verbond-met-abram.md": {
        1: "Die Here het Abram in 'n visioen gesê: Moenie bang wees nie, Abram — Ek is jou skild.",
        2: "Abram het gesê: Ek het geen erfgenaam nie. Eliezer van Damascus sal my erf.",
        3: "Die Here het hom buite laat kyk: Tel die sterre — so talryk sal jou nageslag wees.",
        4: "Abram het geglo, en die Here het dit hom as geregtigheid gereken.",
        5: "God het die verbond bevestig — Abram sou vader van baie nasies wees.",
    },
    "abr/03-drie-besoekers-sara-lag.md": {
        1: "Drie manne het by Abraham se tent verskyn in die hitte van die dag.",
        2: "Abraham het hulle water en kos gegee — kalf, melk en botter.",
        3: "Een het gesê: Volgende jaar sal Sara 'n seun hê. Sara het agter die tentdeur geluister.",
        4: "Sara het in haar hart gelag: Kan ek nog genotskap hê, nou ek oud is?",
        5: "Die Here het gevra: Waarom het Sara gelag? Is enigiets te wonderlik vir die Here?",
    },
    "abr/04-isak-word-gebore.md": {
        1: "Die Here het Sara besoek soos Hy beloof het. Sara het swanger geword.",
        2: "Abraham was honderd jaar oud toe Isak gebore is.",
        3: "Sara het gesê: God het my laat lag. Almal wat dit hoor, sal saam met my lag.",
        4: "Op die dag Isak gespeen is, het Sara Hagar en Ismaël weggejaag.",
        5: "God het vir Hagar gesê: Ek sal Ismaël 'n groot nasie maak.",
    },
    "abr/05-abraham-en-isak-op-die-berg.md": {
        1: "God het vir Abraham gesê: Neem jou seun Isak op die berg Moria en offer hom.",
        2: "Abraham het vroeg opgestaan en hout vir die brandoffer gesny.",
        3: "Isak het gevra: Waar is die lam vir die brandoffer? Abraham het gesê: God sal voorsien.",
        4: "'n Engel het geroep: Moenie die seun seer maak nie — nou weet Ek jy vrees God.",
        5: "Abraham het 'n ram in die struik gevind en dit as offer gebring.",
    },
    "abr/06-isak-en-rebekka.md": {
        1: "Abraham het sy oudste dienaar gesweer om 'n vrou vir Isak uit sy familie te kry.",
        2: "Die dienaar het by die put van Nahor gewag met tien kamele.",
        3: "Rebekka het water gegee vir hom en al sy kamele.",
        4: "Laban en Betuel het gesê: Dit kom van die Here — neem Rebekka en gaan.",
        5: "Isak het Rebekka in sy tent ontvang en hom met haar getroud.",
    },
    "abr/08-jakob-se-droom-by-bet-el.md": {
        1: "Jakob het van Beërsheba weggetrek na Haran. Hy het by Bet-el kamp gemaak.",
        2: "Hy het 'n klip onder sy kop gesit en in die ope veld geslaap.",
        3: "Hy het gedroom van 'n ladder tussen hemel en aarde, met engele wat op en af klim.",
        4: "Die Here het gesê: Ek is met jou en sal jou terugbring na hierdie land.",
        5: "Jakob het die plek Bet-el genoem — die huis van God.",
    },
    "abr/10-jakob-word-israel.md": {
        1: "Jakob het sy gesin en vee oor die Jabbokrivier gestuur.",
        2: "Hy het alleen agtergebly en 'n man het met hom geworstel tot die dag breek.",
        3: "Die man het Jakob se heup ontwricht. Jakob het gesê: Ek laat jou nie gaan voor jy my seën nie.",
        4: "Hy het gesê: Jou naam sal nie meer Jakob wees nie, maar Israel.",
        5: "Jakob het Esau ontmoet en hulle het versoen.",
    },
    "jos/02-josef-by-potifar-en-in-die-tronk.md": {
        1: "Potifar het Josef gekoop. Die Here was met Josef en hy was suksesvol.",
        2: "Potifar se vrou het vir Josef gelieg en gesê hy het haar aangerand.",
        3: "Josef is in die tronk gegooi waar die koning se gevangenes was.",
        4: "Die tronkopsigter het alles onder Josef se sorg gegee.",
        5: "Josef het die bakker en die wynbewaarder se drome vertolk.",
    },
    "jos/05-josef-maak-homself-bekend.md": {
        1: "Josef het sy silwerbeker in Benjamin se sak laat sit.",
        2: "Juda het gesweer: Ek sal myself persoonlik verantwoordelik hou vir die seun.",
        3: "Josef kon nie meer hou nie. Hy het hardop gehuil.",
        4: "Ek is Josef, het hy gesê. Is my pa nog lewend?",
        5: "Farao het gesê: Bring julle pa en julle gesinne na Egipte.",
    },
    "job/01-job-en-sy-gesin.md": {
        1: "Job het in die land Uz gewoon — oos van Kanaän.",
        2: "Hy het brandoffers gebring vir elke kind — sewe bulle en sewe ramme.",
        3: "Hy het sewe duisend skape en drie duisend kamele gehad.",
        4: "Die Here het Job se karakter geken voordat die beproewing begin het.",
        5: "Job se getrouheid was gebaseer op sy vrees vir God, nie sy rykdom nie.",
    },
    "job/02-satan-daag-job-uit.md": {
        1: "Die seuns van God het voor die Here verskyn, en Satan was ook daar.",
        2: "Satan het gesê: Skeer 'n hand af — dan sal Job U vervloek.",
        3: "Job se vee, diensbode en kinders is op een dag vernietig.",
        4: "Job het sy kleermantel geskeur en op die grond geval om te aanbid.",
        5: "Die Here het Satan se mag beperk — Job se lewe moes gespaar word.",
    },
    "job/03-job-word-siek.md": {
        1: "Satan het Job met swere van sy voetsool tot sy kroon getref.",
        2: "Job het op 'n ashoop gesit en 'n skerf gebruik om homself te skraap.",
        3: "Job se vrou het gesê: Vloek God en sterf!",
        4: "Drie vriende — Elifaz, Bildad en Sofar — het van ver gekom.",
        5: "Hulle het sewe dae stilgesit — niemand het 'n woord gepraat nie.",
    },
    "job/04-job-se-vriende-kom.md": {
        1: "Elifaz was van Teman, Bildad van Suah, en Sofar van Naäma.",
        2: "Hulle het saam met Job getreur en sewe dae stilgesit.",
        3: "Job het eers gepraat en sy geboortedag vervloek.",
        4: "Die vriende sou later probeer verduidelik waarom Job ly.",
        5: "Maar hulle sou mis het — Job was regverdig.",
    },
    "job/05-job-en-sy-vriende-stryd.md": {
        1: "Job en sy vriende het baie rondtes van gesprek gehad.",
        2: "Elifaz het gesê: Wie ooit onskuldig perish? Die goddelose ly altyd.",
        3: "Job het geantwoord: Ek wens ek was nooit gebore nie.",
        4: "Die vriende het gedink Job se sonde is die rede vir sy lyding.",
        5: "Job het bly pleit vir regverdigheid voor God.",
    },
    "job/06-god-antwoord-job.md": {
        1: "Die Here het uit 'n stormwind gepraat — magtig en heilig.",
        2: "Waar was jy toe Ek die fondamente van die aarde gelê het?",
        3: "God het van die leeu, die bok, die arend en die behemoth gepraat.",
        4: "Job het gesê: Ek het U gehoor met die ore, maar nou sien ek U met my oë.",
        5: "Job het sy hand op sy mond gesit en erken God is groter as sy vrae.",
    },
    "job/07-job-se-vriende-word-tergewys.md": {
        1: "Die Here was toornig op Elifaz, Bildad en Sofar.",
        2: "Julle het nie reg van My gepraat nie, soos My dienaar Job nie.",
        3: "Job moes vir sy vriende bid en offer bring namens hulle.",
        4: "Job het gebid vir sy vriende, en die Here het hulle sonde vergewe.",
        5: "Die Here het Job se goed begin herstel.",
    },
    "job/08-job-word-herstel.md": {
        1: "Die Here het Job se vee verdubbel — veertien duisend skape.",
        2: "Hy het weer sewe seuns en drie dogters gekry.",
        3: "Sy dogters Jemima, Kesia en Keren-Happuk was die mooiste in die land.",
        4: "Job het honderd en veertig jaar geleef en sy kinders en kleinkinders gesien.",
        5: "Die Here het Job se laaste dae meer geseën as sy eerste.",
    },
}

def main():
    base = Path("/agent/manuscripts-v2")
    expanded_count = 0
    results = []
    for folder in FOLDERS:
        for path in sorted((base / folder).glob("*.md")):
            rel = f"{folder}/{path.name}"
            before = count_words(path)
            if before >= 450 and rel not in EXPANSIONS:
                continue
            text = path.read_text(encoding="utf-8")
            changed = False
            if rel in EXPANSIONS:
                for page, addition in EXPANSIONS[rel].items():
                    text, did = append_to_page(text, page, addition)
                    changed = changed or did
            if changed:
                path.write_text(text, encoding="utf-8")
            after = count_words(path)
            if after > before:
                expanded_count += 1
                results.append((before, after, rel))
    print(f"Expanded {expanded_count} files:")
    for b, a, r in sorted(results, key=lambda x: x[2]):
        print(f"  {b:4d} -> {a:4d}  {r}")
    shorts = []
    for folder in FOLDERS:
        for path in sorted((base / folder).glob("*.md")):
            wc = count_words(path)
            if wc < 450:
                shorts.append((wc, f"{folder}/{path.name}"))
    print(f"\nStill <450: {len(shorts)}")
    for wc, r in sorted(shorts):
        print(f"  {wc:4d}  {r}")

if __name__ == "__main__":
    main()
