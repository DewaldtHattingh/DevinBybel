#!/usr/bin/env python3
"""Expand V05 manuscripts toward 500-650 word target."""
import re
from pathlib import Path

DIR = Path("/agent/manuscripts/volume-05")

# Extra paragraph per page (2-5) keyed by filename
EXTRA = {
"01-jesus-ry-jerusalem-binne.md": [
    "Die dissipels het presies gedoen wat Jesus gesê het. Hulle het die esel en die jong eseltjie by die poort gevind, net soos Hy belowe het.",
    "Dit was soos die profeet gesê het: Kyk, jou koning kom nederig, op 'n esel. Die mense het dit herken en begin juig.",
    "Kinders en grootmense het saam geloop. Sommige het palmblare van die bome afgekap en dit voor Jesus uitgesprei.",
    "Die hele stad het begin roer. Almal het gevra wie hierdie Man is — en die dissipels het geweet dit is die Here.",
],
"02-jesus-in-die-tempel.md": [
    "Die voorhof was die plek waar ook nie-Jode moes bid. Maar die handelaars het dit vol geroep en handel gemaak.",
    "Jesus het die tafels omgekeer en die duweverkopers weggejaag. Die tempel moes weer 'n huis van gebed wees, nie 'n mark nie.",
    "Blindes en lamme het na Hom gekom, en Hy het hulle gesond gemaak. Kinders het in die tempel geroep: Hosanna vir die Seun van Dawid!",
    "Die wetkenner wou weet watter gebod die belangrikste is. Jesus het oor liefde vir God en vir die naaste gepraat — die hart van al die gebooie.",
],
"03-die-laaste-maaltyd.md": [
    "By die tafel was dit stil en ernstig. Jesus het geweet dit was die laaste maaltyd voor Hy sou ly.",
    "Petrus het gesê Jesus sal nooit sy voete was nie. Maar Jesus het hom geleer dat diensbaarheid die pad van sy volk is.",
    "Die brood en die beker was simbole van Jesus se liggaam en bloed — die nuwe verbond wat God met sy volk sluit.",
    "Judas was ook aan die tafel. Jesus het gesê een van hulle sou Hom verraai, en die dissipels was hartseer.",
],
"04-getsemane.md": [
    "Jesus het Peter, Jakobus en Johannes 'n bietjie verder geneem. Hy het hulle gevra om wakker te bly en saam te bid.",
    "Hy het drie keer dieselfde gebed gebid: Nie my wil nie, maar u wil. Elke keer het die dissipels weer ingeslaap.",
    "Jesus het gesê die gees is gewillig maar die vlees is swak. Bid en waak, sodat julle nie in versoeking val nie.",
    "Die derde keer het Jesus die dissipels wakker gemaak. Die uur was naby, en Hy het die Vader se wil aanvaar.",
],
"05-jesus-word-gevange-geneem.md": [
    "Judas het 'n teken met die soldate ooreengekom — 'n soen sou wys wie Jesus is. Dit was 'n swaar verraad.",
    "Die soldate het Jesus gegryp. Een dissipels het 'n swaard getrek, maar Jesus het gesê geweld is nie die pad nie.",
    "Jesus het die gewonde man se oor aangeraak en dit heel gemaak. Hy kon engels roep, maar die Skrif moes vervul word.",
    "Toe het al die dissipels Hom verlaat en weggevlug. Jesus het alleen oorgebly — maar die Vader was by Hom.",
],
"06-jesus-voor-die-raad-en-pilatus.md": [
    "Die Raad het vals getuies gesoek, maar hul stories het nie ooreengestem nie. Hulle wou Jesus skuldig bevind.",
    "Die hoëpriester het gevra of Jesus die Christus is. Jesus het geantwoord: U sê dit — en die Raad het Hom skuldig bevind.",
    "Pilatus het Jesus gevra of Hy die Koning van die Jode is. Pilatus het gesien Jesus is onskuldig, maar die skare was luid.",
    "Pilatus het Barábas vrygelaat soos die skare gevra het. Hy het sy hande gewas en Jesus oorgelewer om gekruisig te word.",
],
"07-petrus-verloen-jesus.md": [
    "Petrus het van ver af Jesus gevolg. Hy het in die voorhof gesit by 'n vuur — maar hy was bang om herken te word.",
    "Die eerste keer het 'n dienskneg gesê Petrus was saam met Jesus. Petrus het gesê: Ek ken Hom nie.",
    "Die tweede keer het iemand anders dieselfde gesê. Weer het Petrus ontken dat hy Jesus ken.",
    "Die derde keer, terwyl die haan kraai, het Petrus weer ontken. Jesus het omgedraai en na hom gekyk — en Petrus het bitterlik geween.",
],
"08-jesus-sterf-aan-die-kruis.md": [
    "Simon van Sirene het gehelp om die kruis te dra. By Golgota is Jesus gekruisig saam met twee misdadigers.",
    "Jesus het gebid: Vader, vergeef hulle. Een misdadiger het Hom bespot; die ander het gevra dat Jesus hom onthou.",
    "Om die middaguur het duisternis gekom en drie ure aangehou. Jesus het sy gees in die Vader se hande beveel.",
    "Jesus het gesê: Dit is volbring. Die Romeinse hoofman het gesê: Waarlik, hierdie Man was die Seun van God.",
],
"09-jesus-word-begraaf.md": [
    "Josef van Arimatéa was 'n ryk man en 'n dissipels van Jesus. Hy het na Pilatus gegaan en Jesus se liggaam gevra.",
    "Hy het fyn linne geneem en Jesus daarmee toegewikkel. Saam met Nikodemus het hulle Jesus in 'n nuwe rotsgraf gelê.",
    "Maria Magdalena en die ander Maria het gesit en gekyk waar Jesus gelê is. Dit was die dag voor die sabbat.",
    "Die priesters het die graf laat verseël en soldate geplaas om dit te bewaak. Maar God se plan was nog nie verby nie.",
],
"10-jesus-het-opgestaan.md": [
    "Die vroue het vroeg na die graf gegaan met speserye. Hulle het gewonder wie die groot klip sou wegrol.",
    "Toe hulle gekom het, was die klip reeds weg. Jesus se liggaam was nie in die graf nie — en hulle was verbaas.",
    "Twee engels het gesê: Waarom soek julle die Lewende tussen die dodes? Onthou, Hy het gesê Hy sou opstaan!",
    "Petrus en Johannes het gehardloop en die leë graf gesien. Maria Magdalena het Jesus lewend ontmoet by die graf.",
],
"11-op-pad-na-emmaus.md": [
    "Die twee dissipels was hartseer. Hulle het gepraat oor alles wat met Jesus gebeur het — hoe Hy gekruisig is.",
    "Jesus het naby gekom en saam geloop, maar hulle het Hom nie herken nie. Hy het gevra waaroor hulle so praat.",
    "Hy het van Moses en al die profete verduidelik dat die Christus moes ly en dan in heerlikheid ingaan.",
    "By Emmaus het Jesus brood gebroke — en toe het hulle Hom herken. Hulle het dieselfde nag teruggehardloop om die goeie nuus te vertel.",
],
"12-tomas-en-die-ander-dissipels.md": [
    "Die dissipels was bang en het die deure gesluit. Maar Jesus het tussen hulle verskyn en gesê: Vrede vir julle!",
    "Hy het sy hande en sy sy gewys sodat hulle kon sien dit is regtig Hy. Die dissipels was bly.",
    "Tomas was nie daar nie. Later het hy gesê hy sal nie glo tensy hy die spykers in Jesus se hande sien nie.",
    "Agt dae later het Jesus weer verskyn. Tomas het geval en gesê: My Here en my God! Jesus het gesê: Glo, en gelukkig is die wat nie gesien het nie.",
],
"13-jesus-gaan-op-na-die-hemel.md": [
    "Veertig dae lank het Jesus aan sy dissipels verskyn. Hy het met hulle gepraat oor die koninkryk van God.",
    "Die dissipels het gevra of Hy nou Israel sou herstel. Jesus het gesê die Vader bepaal die tye — maar die Gees sal krag gee.",
    "Jesus is opgehef terwyl hulle kyk, en 'n wolk het Hom weggeneem. Twee engels het gesê Hy sal terugkom.",
    "Die dissipels het teruggegaan na Jerusalem — bly en wag op die belofte van die Heilige Gees.",
],
"14-pinkster.md": [
    "Al die dissipels was op een plek en het saam gewag. Jerusalem was vol mense van oral vir die fees.",
    "Skielik het wind en tongvormige vuur gekom. Hulle is met die Heilige Gees vervul en het in verskillende tale gepraat.",
    "Mense uit baie lande het gehoor en was verbaas — elkeen het die dissipels in sy eie taal verstaan.",
    "Petrus het gepreek dat Jesus opgestaan het. Ongeveer drieduisend mense het glo en laat doop daardie dag.",
],
"15-die-vroeë-gemeente.md": [
    "Die eerste gelowiges het saam geleer, gebid, brood gebreek en vir mekaar gesorg. Die Here het daagliks mense by hulle gevoeg.",
    "Petrus en Johannes het na die tempel gegaan. By die poort Pragtig het 'n man gesit wat van geboorte af lam was.",
    "Die man het geld gevra. Petrus het gesê: In die Naam van Jesus Christus, staan op en loop! En hy het opgestaan.",
    "Hy het geloop en gespring en God geprys. Die gemeente het kos gedeel en mekaar liefgehad — 'n lewe van geloof en omgee.",
],
"16-stefanus.md": [
    "Stefanus was vol geloof en die Heilige Gees. Hy het wonders gedoen en die mense van Jesus vertel.",
    "Sommige mense kon nie teen hom staan nie. Hulle het vals getuies gebring en gesê Stefanus praat teen Moses en God.",
    "Stefanus het die geskiedenis van Israel vertel en opgekyk. Hy het gesê: Ek sien die hemel oop en Jesus staan by die Vader.",
    "Die skare het hom met klippe doodgemaak. Stefanus het gebid: Here Jesus, ontvang my gees — en die Here was by hom.",
],
"17-filippus-en-die-ethiopiër.md": [
    "'n Engel het Filippus na die woestynpad gestuur. Daar het hy 'n Ethiopiese amptenaar in sy wa sien lees.",
    "Die man lees die profeet Jesaja. Filippus het gevra of hy verstaan, en die man het hom genooi om te kom sit.",
    "Filippus het verduidelik dat die teks oor Jesus gaan — die Lam wat gelei is soos 'n skaap na die slagting.",
    "By water langs die pad het die amptenaar glo en laat doop. Die goeie nuus het ver gereis na Ethiopië.",
],
"18-saul-ontmoet-jesus.md": [
    "Saulus het briewe gehad om Christene in Damaskus te arresteer. Hy was op die pad vol oortuiging.",
    "Skielik het 'n lig van die hemel om hom geskyn. 'n Stem het gesê: Saul, Saul, waarom vervolg jy My?",
    "Saulus was blind en moes na Damaskus gelei word. God het Ananias gestuur om na hom te gaan en vir hom te bid.",
    "Saulus kon weer sien, is gedoop en het dadelik begin preek: Jesus is die Seun van God! Jesus het hom heeltemal verander.",
],
"19-petrus-en-cornelius.md": [
    "Cornelius was 'n Romeinse offisier wat God gevrees het. 'n Engel het hom gesê om vir Petrus te stuur.",
    "Terselfdertyd het Petrus 'n visioen gesien: 'n doek met diere het neergedaal. 'n Stem het drie keer gesê: Wat God rein gemaak het, moenie jy onrein noem nie.",
    "Die Heilige Gees het vir Petrus gesê om saam met Cornelius se boodskappers te gaan. Petrus het nie getwyfel nie.",
    "Terwyl Petrus gepraat het, het die Gees op almal gekom. Petrus het hulle in Jesus se Naam laat doop — God wys geen voorkeur nie.",
],
"20-paulus-en-silas-in-die-tronk.md": [
    "In Filippi het Paulus en Silas by 'n rivier met vroue gepraat. Lydia het glo en laat doop — die eerste bekeerling daar.",
    "Later is hulle gearresteer en stewig in die tronk vasgebind. Dit was donker en hartseer.",
    "Om middernag het hulle gebid en lofliedere gesing. Skielik het 'n aardbewing die deure oopgemaak.",
    "Die tronkopsigter wou homself doodmaak, maar Paulus het gesê: Moenie — ons is almal hier! Hy en sy huis het glo en laat doop.",
],
"21-paulus-in-atene.md": [
    "Paulus het oral in Athene beelde van gode gesien. Hy was bekommerd dat die mense die ware God nie ken nie.",
    "Hy het in die mark gepraat, en die filosofe het hom na die Areopagus genooi om te verduidelik.",
    "Paulus het gesê hy sien 'n altaar: Aan die onbekende god. Die God wat julle sonder om Hom te ken aanbid, verkondig ek aan julle.",
    "Sommige het gespot, maar ander het glo — onder andere Dionisius en Damaris. Die goeie nuus het selfs in Athene vrug gedra.",
],
"22-paulus-se-reis-na-rome.md": [
    "Paulus was 'n gevangene op 'n skip na Rome. 'n Storm het baie dae aangehou en almal was bang.",
    "'n Engel het Paulus gesê: Moenie bang wees nie — jy en almal op die skip sal veilig wees.",
    "Die skip het gestrand, maar almal het die kus bereik. Niemand het gesterf nie, net soos die engel gesê het.",
    "In Rome het Paulus in 'n huis gebly en die koninkryk van God verkondig — sonder vrees en met hoop.",
],
"23-paulus-skryf-briewe.md": [
    "Paulus kon nie self oral gaan nie, maar sy briewe kon reis na gemeentes ver oor die wêreld.",
    "Sommige gemeentes was bang of het vergeet hoe om lief te hê. Paulus wou hulle help onthou wat waar is.",
    "Hy het geskryf: Niks kan ons van die liefde van God skei nie — nie nood, angs, vervolging of enigiets anders nie.",
    "Hy het ook beskryf wat liefde is: lankmoedig, vriendelik, nie jaloers nie — liefde vergaan nooit. Daardie woorde leef nog vandag.",
],
"24-johannes-se-visioen-van-die-troon.md": [
    "Johannes was op Patmos omdat hy van Jesus getuig het. Hy het 'n stem gehoor soos 'n trompet.",
    "Hy het Jesus gesien soos 'n Seun van die mens — helder soos die son. Jesus het gesê: Moenie bang wees nie, Ek het die dood oorwin.",
    "'n Deur in die hemel het oopgegaan. Johannes het 'n troon gesien, en iemand het daarop gesit — helder soos juwele.",
    "Vier-en-twintig ouderlinge het geval en gesing: Heilig, Heilig, Heilig is die Here God, die Almagtige! God regeer.",
],
"25-die-lam-wat-waardig-is.md": [
    "Johannes het 'n boek in God se hand gesien — diggeseël met sewe seëls. Niemand kon dit oopmaak nie, en Johannes het gehuil.",
    "'n Ouderling het gesê: Moenie huil nie — die Leeu uit Juda het oorwin. Johannes het 'n Lam gesien wat leef.",
    "Die Lam het die boek geneem. Al die hemel het geval en gesing: Waardig is U, Lam, om die boek te neem!",
    "Johannes het geweet: die Lam is Jesus. Hy alleen is waardig om die seëls oop te maak.",
],
"26-god-oordeel-regverdig.md": [
    "Johannes het 'n groot wit troon gesien. Die hemel en aarde het weggevlug voor die een wat daarop sit.",
    "Die dooies het voor die troon gestaan. Boeke is oopgemaak, ook die boek van die lewe.",
    "God oordeel regverdig volgens wat geskryf staan. Dit is ernstig — niks verkeerd bly weg nie.",
    "Maar Johannes het ook gehoor: Kyk, Ek maak alles nuut! Die oordeel is ernstig, maar God belowe ook iets nuuts.",
],
"27-n-nuwe-hemel-en-n-nuwe-aarde.md": [
    "Johannes het 'n nuwe hemel en 'n nuwe aarde gesien. Die eerste hemel en aarde was verby.",
    "Hy het die nuwe Jerusalem gesien — soos 'n bruid versier, helder met die heerligheid van God.",
    "'n Stem het gesê: Kyk, die tent van God is by die mense! Hy sal by hulle woon en hulle sal sy volk wees.",
    "God sal elke traan afvee. Die dood en hartseer sal nie meer wees nie. Hy het gesê: Ek maak alles nuut!",
],
"28-die-nuwe-jerusalem.md": [
    "'n Engel het Johannes die stad gewys — die bruid van die Lam. Die stad het geskyn met God se heerlikheid.",
    "Die Lam was die lamp van die stad. Daar was geen tempel nie, want die Here God en die Lam is die tempel.",
    "Johannes het 'n rivier van lewende water gesien en die boom van die lewe — met vrugte en helende blare.",
    "God se diensbode sal sy aangesig sien. Daar sal geen nag meer wees nie — die Here God sal op hulle skyn.",
],
"29-kom-here-jesus.md": [
    "Die engel het gesê: Hierdie woorde is getrou en waar. Jesus het belowe om gou terug te kom.",
    "Hy het gesê: Gelukkig is die wat hul klere was — sodat hulle by die boom van die lewe mag kom.",
    "Jesus het gesê: Kyk, Ek kom gou! Ek is die Alfa en die Omega, die Begin en die Einde.",
    "Die Gees en die bruid sê: Kom! Johannes het gebid: Amen, kom, Here Jesus! Die genade van die Here Jesus sal met almal wees.",
],
}


PASS2 = {
"01-jesus-ry-jerusalem-binne.md": (
    "Die mense het van oral gekom om Jesus te sien. Jerusalem was vol vir die fees, en almal het gewag om te hoor wat Hy sou doen.",
    "Dit was 'n dag van groot vreugde. En tog het Jesus geweet dat swaar dae voorlê — maar vandag het die mense Hom as Koning verwelkom.",
),
"02-jesus-in-die-tempel.md": (
    "Jesus het die tempel binnegegaan — God se huis in Jerusalem. Dit was die plek waar mense Hom moes aanbid.",
    "Jesus het geleer dat liefde vir God en vir mense die hart van alles is. Dit is 'n les wat ons nog vandag kan onthou.",
),
"03-die-laaste-maaltyd.md": (
    "Die kamer was reggemaak vir die Paasfeesmaaltyd. Dit was 'n spesiale aand — die laaste wat Jesus met sy dissipels sou eet.",
    "Ná die maaltyd het hulle gesing en na die olyfberg gegaan. Die nag was swaar, maar Jesus het sy vriende liefgehad tot die einde.",
),
"04-getsemane.md": (
    "Getsemane was 'n tuin op die olyfberg — 'n stille plek waar Jesus kon bid. Die dissipels het saam met Hom gekom.",
    "Jesus het opgestaan, gereed om die Vader se wil te doen. Die dissipels het saam gegaan — al was hulle nog nie wakker genoeg nie.",
),
"05-jesus-word-gevange-geneem.md": (
    "Judas het 'n groot menigte saamgebring — met fakkels en wapens. Die nag was donker en stil.",
    "Jesus het Homself oorgegee. Die Skrif moes vervul word — en die Vader was steeds by Hom in die donker nag.",
),
"06-jesus-voor-die-raad-en-pilatus.md": (
    "Jesus is eers na die hoëpriester gebring, en daarna na Pilatus. Dit was 'n lang, swaar nag.",
    "Pilatus het Jesus oorgelewer. Die pad na Golgota lê voor — maar God se plan was nog nie verby nie.",
),
"07-petrus-verloen-jesus.md": (
    "Petrus het Jesus van ver af gevolg. Hy wou naby wees — maar hy was ook bang.",
    "Petrus het geween omdat hy Jesus drie keer verloën het. Maar die Here het hom aangekyk — en daar was nog hoop vir Petrus.",
),
"08-jesus-sterf-aan-die-kruis.md": (
    "Golgota was buite Jerusalem — die plek van die kruis. Mense het van ver af gestaan en gekyk.",
    "Dit was die swaarste dag — maar ook die dag waarop Jesus vir ons gesterf het. Sy liefde het geen einde nie.",
),
"09-jesus-word-begraaf.md": (
    "Die sabbat het stil verbygegaan. Jesus se vriende was hartseer en bang — hulle het nie geweet wat sou kom nie.",
    "Die graf was verseël en bewaak. Alles het klaar gelyk — maar God se storie was nog nie verby nie.",
),
"10-jesus-het-opgestaan.md": (
    "Die eerste dag van die week het aangebreek. Die vroue het vroeg opgestaan — hulle wou Jesus se liggaam bestyf.",
    "Jesus leef! Die graf is leeg en die engels het die goeie nuus vertel. Dit was die grootste dag in die geskiedenis.",
),
"11-op-pad-na-emmaus.md": (
    "Emmaus was 'n dorpie 'n entjie van Jerusalem af. Die twee dissipels het geloop en gepraat oor alles wat gebeur het.",
    "Hulle het teruggehardloop om te vertel: Die Here het opgestaan! Hul harte het gebrand terwyl Jesus met hulle gepraat het.",
),
"12-tomas-en-die-ander-dissipels.md": (
    "Die dissipels was bang na Jesus se dood. Hulle het die deure gesluit — maar Jesus het deur die vrees heen gekom.",
    "Tomas het eindelik geglo. En Jesus het gesê: Gelukkig is julle wat nie gesien het nie en tog glo — soos ons vandag.",
),
"13-jesus-gaan-op-na-die-hemel.md": (
    "Die Olyfberg was die plek waar Jesus vir die laaste keer met sy dissipels was. Hulle het saam gestaan en gekyk.",
    "Jesus is op, maar Hy sal terugkom. Die dissipels het teruggegaan — bly en vol hoop op die Gees wat sou kom.",
),
"14-pinkster.md": (
    "Die dissipels het gewag soos Jesus gesê het. Hulle was bymekaar en het gebid — en toe het die Gees gekom.",
    "Drieduisend mense het daardie dag glo. Die kerk het begin groei — en die goeie nuus het verder versprei.",
),
"15-die-vroeë-gemeente.md": (
    "Die eerste gelowiges het saam geleef soos 'n familie. Hulle het geleer, gebid en vir mekaar gesorg.",
    "Die Here het daagliks mense by die gemeente gevoeg. Dit was 'n lewe van geloof, wonder en omgee vir mekaar.",
),
"16-stefanus.md": (
    "Stefanus was die eerste wat vir Jesus gesterf het omdat hy getuig het. Hy het nie opgehou praat nie.",
    "Stefanus het Jesus in die hemel gesien. Die Here was by hom — selfs in die laaste oomblik.",
),
"17-filippus-en-die-ethiopiër.md": (
    "Die woestynpad was stil en warm. Filippus het geluister toe die engel gepraat het — en hy het gegaan.",
    "Die doop was 'n nuwe begin vir die amptenaar. Die goeie nuus het ver gereis — verder as enigiemand gedink het.",
),
"18-saul-ontmoet-jesus.md": (
    "Saulus het gedink hy doen wat reg is. Maar Jesus het hom op die pad gestop — met 'n lig en 'n stem.",
    "Saulus het 'n nuwe naam gekry: Paulus. Hy het Jesus begin preek — die een wat hy vroeër vervolg het.",
),
"19-petrus-en-cornelius.md": (
    "Petrus het geleer dat God se plan groter is as wat hy gedink het. Die evangelie is vir alle volke.",
    "Cornelius en sy huis het die Gees ontvang. God wys geen voorkeur nie — Sy liefde is vir almal.",
),
"20-paulus-en-silas-in-die-tronk.md": (
    "Filippi was 'n Romeinse kolonie. Paulus en Silas het daar gepraat en mense tot Jesus gelei.",
    "Selfs in die donker tronk het hulle God geprys. En God het die tronkopsigter en sy huis gered.",
),
"21-paulus-in-atene.md": (
    "Athene was beroemd vir sy filosofe en sy baie gode. Paulus het die ware God verkondig.",
    "Nie almal het geglo nie — maar sommige het. Die goeie nuus vind altyd mense wat luister.",
),
"22-paulus-se-reis-na-rome.md": (
    "Die see was gevaarlik en die storm het lank aangehou. Maar God het 'n engel gestuur om Paulus te vertroos.",
    "In Rome het Paulus die koninkryk verkondig — tot aan die einde van die aarde, soos Jesus gesê het.",
),
"23-paulus-skryf-briewe.md": (
    "Paulus se briewe het gemeentes ver oor die wêreld bereik — Korinte, Rome, Efese en meer.",
    "Daardie woorde help ons nog vandag om God se liefde te onthou en mekaar reg te liefhê.",
),
"24-johannes-se-visioen-van-die-troon.md": (
    "Patmos was 'n eiland waar Johannes verban was. Maar God het hom 'n groot visioen gegee.",
    "Johannes het gesien: God regeer. Die hemel is vol lof — rustig, groot en veilig.",
),
"25-die-lam-wat-waardig-is.md": (
    "Johannes het gehuil omdat niemand die boek kon oopmaak nie. Maar die Lam was daar — Jesus, wat oorwin het.",
    "Die hele hemel het gesing. Jesus is waardig — en Hy alleen kan die plan van God voltooi.",
),
"26-god-oordeel-regverdig.md": (
    "Johannes se visioen was ernstig — maar ook eerlik. God maak reg wat verkeerd is.",
    "En dan kom die belofte: Ek maak alles nuut. Die storie eindig nie in vrees nie — maar in hoop.",
),
"27-n-nuwe-hemel-en-n-nuwe-aarde.md": (
    "God belowe 'n nuwe wêreld — sonder trane, sonder dood, sonder hartseer. Hy sal by sy mense woon.",
    "Dit is die tuiste wat God van die begin af belowe het. Alles sal nuut wees — en veilig, en vol liefde.",
),
"28-die-nuwe-jerusalem.md": (
    "Die stad het geskyn soos 'n juweel. Daar is geen nag meer nie — die Lam is die lig.",
    "God se volk sal sy aangesig sien. Dit is die belofte wat vir altyd staan.",
),
"29-kom-here-jesus.md": (
    "Johannes het die laaste woorde van die Bybel opgeteken. Dit is 'n uitnodiging — Kom! — en 'n gebed: Kom, Here Jesus!",
    "So eindig ons reis deur die Bybel — met hoop, genade en die belofte dat Jesus terugkom. Slap rustig. Die Here is by jou.",
),
}


def insert_para(text: str, page_num: int, para: str) -> str:
    marker = f"## Bladsy {page_num} —"
    start = text.find(marker)
    if start == -1:
        return text
    section = text[start:]
    dash = section.find("\n\n---\n\n## Bladsy")
    if dash == -1:
        dash = section.find("\n\n---\n\n## Produksie")
    body_start = section.find("\n\n", section.find("> **Beeldnota:**")) + 2
    body = section[body_start:dash].rstrip()
    if para in body:
        return text
    new_section = section[:body_start] + body + "\n\n" + para + section[dash:]
    return text[:start] + new_section


def expand_file(path: Path, paragraphs: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for i, para in enumerate(paragraphs, start=2):
        marker = f"## Bladsy {i} —"
        start = text.find(marker)
        if start == -1:
            print(f"WARN: {marker} not found in {path.name}")
            continue
        # find next --- after this section's body
        section = text[start:]
        dash = section.find("\n\n---\n\n## Bladsy")
        if dash == -1 and i == 5:
            dash = section.find("\n\n---\n\n## Bladsy 6")
        if dash == -1:
            print(f"WARN: end of page {i} not found in {path.name}")
            continue
        body_start = section.find("\n\n", section.find("> **Beeldnota:**")) + 2
        body = section[body_start:dash].rstrip()
        if para in body:
            continue
        new_section = section[:body_start] + body + "\n\n" + para + section[dash:]
        text = text[:start] + new_section
    path.write_text(text, encoding="utf-8")


for fname, paras in EXTRA.items():
    expand_file(DIR / fname, paras)
    print(f"expanded {fname}")

for fname, (p1, p5) in PASS2.items():
    path = DIR / fname
    text = path.read_text(encoding="utf-8")
    text = insert_para(text, 1, p1)
    text = insert_para(text, 5, p5)
    path.write_text(text, encoding="utf-8")
    print(f"pass2 {fname}")