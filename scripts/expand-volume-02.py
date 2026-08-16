#!/usr/bin/env python3
"""Append inline story-specific sentences to reach word-count targets."""
from pathlib import Path
import re

# Each value is NEW biblical detail only — no repetition of existing narrative.
EXPANSIONS = {
    "01-moses-as-baba.md": {
        1: "Die Israeliete het in die land Gosen gewoon en vir Farao bakstene gemaak. Hulle families het groot geword — seuns en dogters, oumas en oupas.",
        2: "Die vroegste Israelitiese seuntjies is in die Nylrivier gegooi. Ouers moes bang wees, maar dogtertjies moes lewe.",
        3: "Jokebed en haar man was van die stam Levi. Hulle het gesien dat hulle seuntjie mooi was — en hom drie maande lank in die huis versteek.",
        4: "Miryam het naby die rivier gewag. Farao se dogter het diensmeisies by haar gehad toe sy die mandjie laat haal het.",
        5: "Jokebed het haar seun weer in haar arms gehou as sy opvoedster. Moses het in Farao se huis grootgeword — maar hy was ’n Israeliet.",
    },
    "02-die-brandende-bos.md": {
        1: "Hy het die Egiptenaar in die sand begrawe. Toe Farao dit gehoor het, wou hy Moses doodmaak — en Moses het weggevlug.",
        2: "Jetro was priester in Midian. Moses het by hom gewoon, met Sippra getroud, en hulle het ’n seun Gersom gekry.",
        3: "Die berg Horeb lê in die woestyn. Moses het sy skape laat wei daar naby toe hy die bos sien brand sonder om op te brand.",
        4: "Die Here het gesê: Ek het die nood van Israel in Egipte gesien en hulle gekreun gehoor. Ek het My afgebuig om hulle uit te red.",
        5: "Die Here het Moses se staf in ’n slang laat verander en weer terug in ’n staf. Aäron sou na Moses toe kom en saam met hom praat.",
    },
    "03-moses-voor-farao.md": {
        1: "Moses was tagtig jaar oud en Aäron drie jaar ouer. Hulle het die oudstes van Israel bymekaar geroep en die volk het gebid toe hulle gehoor het dat God hulle onthou het.",
        2: "Die oorsigbeamptes het vir Farao gekla dat die volk nie meer na hulle luister nie. Farao het Israel self strooi laat soek — maar steeds dieselfde hoeveelheid bakstene verlang.",
        3: "Die Here het gesê: Nou sal Ek met ’n sterk hand aan Farao wys wie Ek is. Groter tekens sou kom.",
        4: "Moses het ook sy hand in sy boesem gesteek — eers met uitslag, toe weer gesond. Nog tekens het Farao gesien, maar sy hart het verhard.",
        5: "Die Here het gesê: Ek sal my hand aan Farao en aan Egipte lê. Dan sal hulle weet dat Ek die Here is.",
    },
    "04-die-tien-plae.md": {
        1: "Aäron het sy staf oor die riviere uitgestrek. Die vis in die rivier het gesterf en die water het stank — sewe dae lank.",
        2: "Aäron het sy hand uitgestrek en paddas het oral gekom — in bedde, oonde en bakke. Farao se towenaars kon die paddas nie wegneem nie. Stof op die grond het lewendige mugge geword, en swerms vlieë het Egipte volgemaak.",
        3: "Net in Gosien, waar Israel gewoon het, was daar geen hael nie. Die sprinkane het alles oorblywende geëet wat die hael oorgelaat het.",
        4: "Moses het gesê: Laat my volk gaan om My te dien. As jy weier, sal nog een pla kom — elke eerstgeborene in Egipte sal sterf, mens en dier.",
        5: "Die negende pla se duisternis het drie dae geduur. Nou wag die volk op die Paasfees — die nag wanneer die Here sou verbygaan.",
    },
    "05-die-paasfees.md": {
        1: "Die lam moes een jaar oud wees, sonder enige gebrek. Die hele gemeenskap van Israel moes dit op dieselfde nag eet.",
        2: "Geen suurdeeg moes in hulle huise wees nie. Hulle moes haastig eet — gordels vas, skoene aan, staf in die hand.",
        3: "In Farao se huis, by die meule en in die tronk — oral waar daar geen bloed op die deur was nie, het die eerstgeborene gesterf.",
        4: "Daar was groot gegil in Egipte — geen huis sonder iemand wat dood was nie. Farao het Moses en Aäron in die nag geroep.",
        5: "Die Israeliete het ongeveer vier honderd dertig jaar in Egipte gewoon. Hulle het goud, silwer en klere van die Egiptenaars gekry en ongesuurde deeg op hulle skouers gedra.",
    },
    "06-deur-die-rooi-see.md": {
        1: "Die Here het nie Israel deur die Filistynse land gelei nie — die volk sou dalk terugkeer na Egipte. Hy het hulle deur die woestyn na die Rooi See gelei, en Josef se bene het saam gegaan.",
        2: "Farao het ses honderd uitgesoekde strydwagens geneem — elke strydwagen met sy ruiters. Die Egiptenaars het Israel ingehaal by Pi-Hahirot, tussen Migdol en die see.",
        3: "Die engel van God en die wolk het van voor Israel af na agter hulle gegaan. Die wolk het vir Israel lig gegee en vir die Egiptenaars duisternis — die hele nag het Moses sy hand oor die see uitgestrek.",
        4: "Die kinders van Israel het op droë grond deur die see gegaan. Die Egiptenaars het agterna gegaan — al hulle perde, strydwagens en ruiters. Die Here het na die Egiptenaars gekyk deur die vuursag.",
        5: "Toe die Egiptenaars probeer vlug het, het die Here hulle wielruppe laat los. Die water het teruggekeer en die strydwagens bedek. Moses en die volk het die Here se lof gesing.",
    },
    "07-brood-uit-die-hemel-water-uit-die-rots.md": {
        1: "Die volk het die vleispotte in Egipte onthou. Die Here het gesê: Elke oggend sal julle net genoeg vir daardie dag insamel.",
        2: "Die wit korrels was soos koriander-saad en het soos wafels met heuning gelyk. Elkeen moes twee tiende efa insamel — net genoeg vir daardie dag.",
        3: "Moses het ’n kruik vol manna voor die Here bewaar vir toekomstige geslagte. So het Israel veertig jaar manna geëet in die woestyn.",
        4: "Die Here het vir Moses gesê: Neem die oudstes van Israel saam en gaan na die rots by Horeb. Slaan op die rots, en water sal uitkom.",
        5: "Moses het die rots twee keer geslaan. Israel het die Here daar getoets en gevra: Is die Here onder ons of nie?",
    },
    "08-sinai-en-die-tien-gebooie.md": {
        1: "Drie maande na hulle uit Egipte getrek het, het Israel by die berg Sinai gekamp. Die Here het gesê: Julle sal my besitende volk wees — ’n koninkryk van priesters.",
        2: "Die volk moes hul klere was en vir twee dae gereed wees. Hulle moes nie naby die berg kom nie — selfs nie ’n dier laat wei teen die berg nie.",
        3: "Die gebooie dek God en ander mense — geen ander gode, geen beelde, geen vals getuienis, geen doodslag of diefstal nie. Die sabbat en ouers-eer is ook daar.",
        4: "Die berg Sinai het gerook — die Here het daarop neergedaal in vuur. Die trompet se klank het harder en harder geword.",
        5: "Moses het veertig dae en veertig nagte op die berg gebly. Die Here het die woorde op twee stene tablette geskryf — die werk van God.",
    },
    "09-die-goue-kalf.md": {
        1: "Moses het veertig dae en veertig nagte op die berg gebly. Die volk het by Aäron gekom en gode gevra wat voor hulle uit sou gaan.",
        2: "Aäron het al die goue oorskote laat bring en die goud in die vuur gegooi. Die volk het feesgehou en rondom die kalf gedans.",
        3: "Moses het gepleit: Waarom tog, Here, sal u toorn warm word? Onthou Abraham, Isak en Israel. Die Here het gesê Hy sal nie die volk verdelg nie.",
        4: "Moses het die kalf verbrand, dit tot stof vermaal en in die water gegooi. Die Leviete het aan die Here se kant gestaan.",
        5: "Moses het weer veertig dae op die berg gebly. Die Here het nuwe tablette geskryf en Homself bekendgemaak as barmhartig en genadig — maar Hy vergewe nie sonde sonder straf nie.",
    },
    "10-die-tabernakel.md": {
        1: "Die Here het presiese planne gegee vir die heilige tent — die tabernakel. Dit sou die plek wees waar Hy onder sy volk sou woon op die reis deur die woestyn.",
        2: "Kunsvlyers soos Besalel en Oholiab het die werk geleid. Almal wat ’n gewillige hart gehad het, het goud, silwer, koper, purper, fyn linne en bokhare gebring.",
        3: "Binne was die ark van die verbond met die twee stene tablette, die verzoendeksel, die goue lampstand, die altaar vir reukoffers en die altaar vir brandoffers — presies soos die Here beveel het.",
        4: "Moses het die tabernakel op die eerste dag van die eerste maand opgerig. Hy het die heilige goed binne gesit en die altaar en voorhof opgestel. Aäron en sy seuns is in hulle amp aangestel.",
        5: "Die wolk het die tent bedek en die heerlikheid van die Here het die tabernakel gevul. Bedags was die wolk bo die tabernakel. Wanneer die wolk opstyg, het Israel getrek — tot die wolk weer neergedaal het.",
    },
    "11-die-twaalf-verkenners.md": {
        1: "Die Here het een man uit elke stam gestuur. Hulle het druiwe van Eskol meegebring — so groot dat twee man dit op ’n stok moes dra.",
        2: "Hulle het gesê die land vloei oor van melk en hening, maar die mense is sterk en die stede versterk. Die volk het die hele nag gehuil.",
        3: "Kaleb het gesê: Ons moet dadelik optrek en die land inpak. Moenie bang wees vir die mense van die land nie. Die volk wou hulle met klippe gooi.",
        4: "Almal van twintig jaar en ouer sou in die woestyn sterf. Net Kaleb en Josua — en die kinders — sou die beloofde land sien.",
        5: "Die Amalekiete en Kanaäniete het hulle teruggedryf toe hulle sonder die Here probeer opgaan het. Israel sou veertig jaar swerf.",
    },
    "12-die-koper-slang.md": {
        1: "Israel het om die land Edom getrek — die lang pad deur die woestyn. Hulle het ongeduldig geword en gemurmureer teen God en teen Moses.",
        2: "Die Here het brandende slange onder die volk gestuur. Baie mense is gebyt en het gesterf. Israel het na Moses gegaan, hulle sonde bely en gevra dat die Here die slange wegneem.",
        3: "Moses het vir die volk gebid. Die Here het gesê: Maak ’n brandende slang en sit dit op ’n paal. Moses het ’n koper slang gemaak en dit in die middel van die kamp opgerig.",
        4: "Wanneer iemand gebyt is en na die koper slang op die paal gekyk het, het hy gelewe. Dit was nie die slang wat gered het nie — dit was die Here wat redding gee vir die wat na sy teken kyk.",
        5: "Israel het geleer dat kla nie die antwoord is nie. Later sou Jesus sê dat soos Moses die slang in die woestyn opgehef het, so sal die Seun van die mens opgehef word.",
    },
    "13-josua-en-die-jordaan.md": {
        1: "Die Here het vir Josua gesê: Van die woestyn tot die Groot See, en tot by die groot rivier — al die land wat Ek beloof het, sal julle beërwe.",
        2: "Die volk moes nog drie dae wag voordat hulle oorgestek het — tyd om hulleself voor te berei. Die rivier was vol, want dit was oesfeestyd.",
        3: "Die water van bo af het opgestaan soos ’n dam, en die water verder af het weggetrek na die Doodsee. Die priesters het in die middel van die rivier gestaan.",
        4: "Josua het die klippe as gedenksteen opgerig by Gilgal. Wanneer julle kinders vra wat dit beteken, vertel julle van die Jordaan wat opgedroog het.",
        5: "Toe die priesters met die ark uit die rivier gekom het, het die water weer teruggevloei. Josua het die volk laat herdenk dat die lewende God by hulle was.",
    },
    "14-jerigo.md": {
        1: "Ragab se huis was in die muur van Jerigo. Die koning het gehoor daar is spioene en Ragab gevra om hulle uit te lewer. Sy het hulle versteek.",
        2: "Sy het die spioene op die dak versteek onder vlasstengels. Sy het gesê: Ek weet die Here het julle hierdie land gegee. Sy het hulle deur die venster laat afdraai met ’n tou.",
        3: "Jerigo was dig gesluit — geen mens het in of uitgegaan nie. Sewe priesters moes voor die ark loop en hoorne blaas terwyl Israel elke dag om die stad marsjeer.",
        4: "Op die sewende dag het hulle sewe keer om die stad gegaan. By die sewende rondte het die priesters die hoorne geblaas en die volk geskreeu. Die mure het geval — plat op die grond.",
        5: "Josua het Ragab en haar familie gespaar — almal in haar huis is veilig gebly. Die rooi koord het in die venster gebly as teken. Ragab het in Israel gewoon.",
    },
    "15-debora-en-barak.md": {
        1: "Koning Jabin van Kanaän het in Hasor geregeer. Sy leier Sisera het nege honderd yster strydwagens gehad. Israel het twintig jaar lank geroep om hulp.",
        2: "Debora het onder die palmboom van Debora tussen Rama en Bet-El gesit en die volk gehelp. Sy het vir Barak gesê: Trek op na Tabor met tien duisend man uit Naftali en Sebulon.",
        3: "Barak het gesê: As jy nie saamgaan nie, gaan ek nie. Sisera het nege honderd yster strydwagens by die Kishonrivier gehad. Debora het gesê: Vandag het die Here Sisera in jou hand gegee.",
        4: "Die Here het Sisera se leër in verwarring gebring. Barak het van die berg Tabor afgejaag. Nie een man van Sisera se leër was oor nie.",
        5: "Sisera het te voet weggevlug na Jael se tent. Sy het hom melk gegee en hom laat rus — en toe hy slaap, het sy die tentpen deur sy slaap gesteek.",
    },
    "16-gideon.md": {
        1: "Die Midianiete het Israel se oes vernietig. Israel het in rotsholtes gewoon om weg te kruip. Gideon het koring dors in die wingerd — bang dat die Midianiete dit sou wegvat.",
        2: "Die engel het gesê: Gaan in jou krag en red Israel. Gideon het die altaar van Baäl afgebreek en ’n altaar vir die Here gebou. Die mense wou hom doodmaak, maar sy pa het gesê: Laat Baäl self hom straf.",
        3: "Drie en twintig duisend man het opgeroep. Die Here het gesê: Daar is te veel — Israel sal roem op hulleself. Hy het die leër laat krimp totdat net drie honderd oor was.",
        4: "Elke man het ’n fakkels in ’n klei kan gehou en ’n trompet in sy hand. Om die Midianitiese kamp het hulle die kanne gebreek, die fakkels gewys en geroep: ’n Swaard vir die Here en vir Gideon!",
        5: "Die Midianiete het in verwarring gevlug en teen mekaar geveg. Gideon het boodskappers gestuur na Efraim, Manasse, Asjer en Naftali. Israel het veertig jaar rus gehad.",
    },
    "17-simson-word-gebore.md": {
        1: "Manoah was van die stam Dan en woon in Zora. Sy vrou was onvrugbaar — sy kon nie kinders kry nie.",
        2: "Die engel het gesê die seun sal ’n Nasireër van God wees van sy moeder se skoot af — geen wyn, geen onrein kos, geen skeermes oor sy hoof.",
        3: "Toe Manoah ’n bok as offer gebring het, het die engel in die vlam opgegaan. Manoah en sy vrou het op hulle gesigte geval.",
        4: "Manoah het gesê: Ons sal sekerlik sterf — ons het God gesien. Sy vrou het gesê: As die Here ons wou doodmaak, sou Hy nie die offer aanvaar het nie.",
        5: "Die Gees van die Here het begin om hom te roer in die kamp van Dan, tussen Zora en Esjtaol. Israel het nog gely — maar die Here het reeds ’n bevryder voorberei.",
    },
    "18-simson-en-die-leeu.md": {
        1: "Die Filistyne het in Timnah gewoon — nie ver van Israel af nie. Simson se ouers het bekommerd gewonder of dit reg is om 'n vreemde vrou te neem.",
        2: "By die wingerde van Timnah het die leeu gebrul. Simson het die leeu oopgeruk met sy hande alleen, soos iemand 'n boklam sou skeur.",
        3: "Toe hy later terugkom, het bye in die leeukarkas nes gemaak. Heuning was binne — kos vir Simson en sy ouers, sonder dat hulle geweet het waar dit vandaan kom.",
        4: "Dertig metgeselle was by die feestyd. Simson bied dertig hemde en dertig pakke klere as weddenskap aan vir wie die raaisel kan raai.",
        5: "Die raaisel blyk uit die leeu-eter en die heuning-soetigheid te kom. Maar die metgeselle kan dit nie raai nie — en die stryd met die Filistyne sou begin.",
    },
    "19-simson-se-stryd-met-die-filistyne.md": {
        1: "Sy het hom aanhoudend gevra totdat hy die antwoord op die sewende dag vertel het — die leeu en die heuning.",
        2: "Hy het na Askalon gegaan — dertig manne verslaan en hulle klere geneem om die weddenskap te betaal.",
        3: "Hy het drie honderd jakkalse gevang, twee aan twee gebind, en fakkels tussen hulle sterte vasgemaak. Die vuur het die Filistyne se koringlande vernietig.",
        4: "Die Gees van die Here het weer kragtig op hom gekom. God het water uit die holte laat kom sodat hy kon drink nadat hy moeg was.",
        5: "Hy het Israel twintig jaar lank as rigter gelei. Die stryd met die Filistyne was nog nie verby nie.",
    },
    "20-simson-en-delila.md": {
        1: "Die Filistynse vyf vorste het Delila silwer gebied: Vind uit waar sy krag vandaan kom. Elke vorst het elf honderd silwerstukke beloof.",
        2: "Simson het drie keer vals antwoorde gegee — met toue, nuwe toue en die weefgetou. Elke keer het die Filistyne hom probeer vang, en elke keer het hy hulle maklik ontsnap.",
        3: "Delila het elke dag gedruk totdat Simson moeg was van haar vrae. Hy het alles vertel: hy is ’n Nasireër — ’n skeermes het nooit oor sy hoof gekom nie.",
        4: "Delila het ’n man geroep om sy sewe hare te sny terwyl hy op haar skoot slaap. Sy krag het van hom weggegaan en die Gees van die Here het van hom gewyk.",
        5: "Die Filistyne het sy oë uitgegrawe en hom na Gaza gebring. Hulle het hom met koperkettings geboei en in die tronk laat maal soos ’n os. Maar sy haar het begin teruggroei.",
    },
    "21-simson-se-laaste-gebed.md": {
        1: "Die Filistyne het hom blind en met koperkettings geboei gehou. Terwyl hy daar gemaal het, het sy haar begin teruggroei — maar niemand het dit opgemerk nie.",
        2: "Die Filistynse vorste het ’n groot offerfees vir Dagon gehou. Ons god het ons vyand in ons hand gegee, het hulle gesê. Hulle het hom tussen die twee middelste pilare van die tempel laat staan.",
        3: "Simson het vir die seun wat hom gelei het gesê: Laat my die pilare voel waarop die huis rus. Daar was drie duisend man en vrou op die dak — om Simson te sien en om Dagon te prys.",
        4: "Simson het tot die Here gebid: Versterk my net hierdie een keer, dat ek aan die Filistyne vergelding kan gee vir my twee oë. Hy het die twee middelste pilare gegryp en hulle laat wankel.",
        5: "Die tempel het op die vorste en al die mense geval. Simson het meer gedood in sy dood as in sy hele lewe. Hy is in Manoah se graf begrawe — en die tyd van die rigters het geëindig.",
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
    last_narrative_idx = None

    for line in lines:
        if line.strip() == "---" and current_page and current_page <= 5:
            if current_page in expansions and current_page not in inserted_for_page:
                if last_narrative_idx is not None:
                    out[last_narrative_idx] = (
                        out[last_narrative_idx].rstrip() + " " + expansions[current_page]
                    )
                else:
                    out.append(expansions[current_page])
                inserted_for_page.add(current_page)

        out.append(line)

        if line.startswith("## Bladsy"):
            current_page = get_page_num(line)
            last_narrative_idx = None
        elif current_page and current_page <= 5:
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("!")
                and not stripped.startswith(">")
                and not stripped.startswith("#")
                and stripped != "---"
            ):
                last_narrative_idx = len(out) - 1

    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    base = Path("/agent/manuscripts/volume-02")
    for fname, expansions in EXPANSIONS.items():
        expand_file(base / fname, expansions)
    print(f"Expanded {len(EXPANSIONS)} files")


if __name__ == "__main__":
    main()
