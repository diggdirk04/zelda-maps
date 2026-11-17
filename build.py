true=True;false=False
import json
reuse=open('reuse.js').read()
# markers: area, x%, y%, label
G=[
{"id":"loz","t":"The Legend of Zelda","y":1986,"img":"loz.webp","w":2400,"h":776,"mk":[["mount",30,10,"Death Mountain (top band)"],["grave",12,45,"Graveyard"],["lake",42,58,"Central lake"],["woods",14,88,"Lost Woods"]],"bl":"loz","xl":true,"note":"No castle on the overworld. Death Mountain fills the top of the map, the graveyard is on the far west side, and the large lake sits near the middle. The map image credits Rick N. Bruns / NESMaps."},
{"id":"aol","t":"Zelda II: The Adventure of Link (full overworld)","y":1987,"img":"aol_full.webp","w":1600,"h":1088,"mk":[["castle",16,25,"North Castle (sleeping Zelda)"],["gerudo",19,9,"Desert (Parapa)"],["grave",30,51,"King's Tomb graveyard"],["mount",12,78,"Death Mountain maze"],["tot",48,57,"Great Palace (Triforce of Courage)"]],"bl":"aol","v":[["z2_world.webp","Labelled world map",false,"z2w"]],"xl":true,"note":"Two continents. Western Hyrule (left) has North Castle, the towns, the graveyard and the Death Mountain cave maze; Eastern Hyrule (right) holds the Great Palace, Maze Island and the later towns. The map image credits Rick N. Bruns / NESMaps."},
{"id":"alttp","t":"A Link to the Past (Light & Dark World)","y":1991,"img":"alttp_light.webp","w":1500,"h":1500,"mk":[["woods",15,15,"Lost Woods"],["tot",7,7,"Master Sword pedestal"],["mount",60,12,"Death Mountain"],["zora",93,12,"Zora's Waterfall"],["grave",55,31,"Graveyard / Sanctuary"],["kak",15,50,"Kakariko Village"],["castle",50,44,"Hyrule Castle"],["gerudo",14,83,"Desert of Mystery"],["lake",82,84,"Lake Hylia"],["eastern",88,50,"Eastern Palace"],["sanct",46,25,"Sanctuary"],["house",54,67,"Link's House"]],"note":"The template for later games: castle in the centre, Death Mountain to the north, Lost Woods northwest, Kakariko west, desert southwest, Lake Hylia southeast.","base":"Light World","bl":"light","xl":true,"v":[["alttp_dark.webp","Dark World",true,"dark"],["xa_albw_on_alttp.webp","A Link Between Worlds (Hyrule)",True,None,"light",1],["xa_eow_on_alttp.webp","Echoes of Wisdom (approx.)",True,None,"light",1],["xa_lorule_on_alttp.webp","A Link Between Worlds (Lorule)",True,None,"dark",1]]},
{"id":"oot","t":"Ocarina of Time","y":1998,"img":"oot_original.webp","w":1500,"h":1036,"mk":[["gerudo",8,9,"Desert Colossus / Haunted Wasteland"],["castle",58,25,"Hyrule Castle"],["tot",53,32,"Market / Temple of Time"],["mount",70,8,"Death Mountain Crater"],["goron",76,24,"Goron City"],["kak",75,47,"Kakariko Village"],["grave",81,41,"Graveyard"],["zora",88,57,"Zora's Domain"],["ranch",42,61,"Lon Lon Ranch"],["lake",17,82,"Lake Hylia"],["woods",65,76,"Lost Woods"],["deku",56,85,"Kokiri Forest (Deku Tree)"]],"bl":"ootbase","xl":true,"note":"The original 1998 layout, from the official foldout poster: Gerudo in the far west, Death Mountain northeast, the forest southeast and Lake Hylia southwest. The 2026 Switch 2 remake keeps the same arrangement, and its map is the first thumbnail.","base":"1998 poster","v":[["oot.webp","2026 remake",false],["oot_manual_labeled.webp","Manual atlas",false,"atlas"]]},
{"id":"la","t":"Link's Awakening (Koholint Island, Switch map)","y":1993,"img":"la.webp","w":1500,"h":857,"mk":[["mount",41,6,"Mt. Tamaranch (Wind Fish's Egg)"],["woods",15,45,"Mysterious Forest"],["grave",45,47,"Cemetery"],["castle",60,44,"Kanalet Castle"],["kak",18,66,"Mabe Village"],["lake",58,85,"Martha's Bay"],["gerudo",90,84,"Yarna Desert"]],"bl":"la","xl":true,"note":"Koholint isn't Hyrule, but it reuses the pattern: a mountain range across the north, a maze forest in the west, a castle and graveyard in the middle, a bay to the south and a desert in the southeast."},
{"id":"mm","t":"Majora's Mask (Termina)","y":2000,"img":"mm_official.webp","w":1333,"h":948,"mk":[["snow",45,15,"Snowhead"],["mount",45,22,"Snowhead mountains (Gorons)"],["castle",50,48,"Clock Town (the hub)"],["lake",16,45,"Great Bay"],["gerudo",10,53,"Pirates' Fortress"],["woods",50,67,"Southern Swamp / Woodfall"],["grave",74,46,"Ikana Canyon"],["zora",25,55,"Zora Hall, Great Bay coast (approx.)"],["ranch",37,63,"Romani Ranch (approx.)"],["goron",62,31,"Goron Village (approx.)"]],"bl":"mmbase","xl":true,"note":"Official Termina map. The same biomes as Hyrule in new places: snowy mountain to the north, sea to the west, swamp to the south and the haunted canyon to the east, with Clock Town at the centre.","base":"Official","v":[["mm.webp","Fan map (named)",false],["mm_nerrel.webp","Termina painting (Nerrel)",false,"ner"],["mm_clocktown.webp","Clock Town",false,"ct"],["mm3d.webp","Termina (3DS remake)",false,"mm3d"]]},
{"id":"oos","t":"Oracle of Seasons (Holodrum, 4 seasons + Subrosia)","y":2001,"img":"oos_summer.webp","w":1500,"h":1200,"mk":[["woods",9,28,"Lost Woods"],["deku",59,77,"Maku Tree"],["kak",47,90,"Horon Village"],["grave",7,88,"Western Coast graveyard"],["gerudo",88,82,"Samasa Desert"],["mount",83,8,"Mt. Cucco"],["goron",56,12,"Goron Mountain"]],"bl":"holo","xl":true,"note":"Holodrum is the same land in four seasons. The Maku Tree in Horon Village does the Deku Tree's job as guardian, the Lost Woods are in the west, and there's a desert in the southeast and a graveyard on the west coast. Below it lies Subrosia, a lava world reached through portals. It doesn't line up with Holodrum, so it's a separate tab. Its centre is the Subrosian market, and the Temple of Seasons is in the northeast.","extra":[["oos_gb.webp","The original Game Boy Color overview map"],["oos_subrosia_nav.webp","Subrosia's in-game overview map"]],"base":"Summer","v":[["oos_spring.webp","Spring",true,"holo"],["oos_autumn.webp","Autumn",true,"holo"],["oos_winter.webp","Winter",true,"holo"],["oos_subrosia.webp","Subrosia (underground)",false,"sub"]]},
{"id":"ooa","t":"Oracle of Ages (Labrynna, present & past)","y":2001,"img":"ooa_present.webp","w":1500,"h":1200,"mk":[["deku",60,24,"Maku Tree"],["kak",55,39,"Lynna City"],["grave",86,52,"Yoll Graveyard"],["woods",15,62,"Deku Forest"],["goron",82,10,"Rolling Ridge (Gorons)"],["mount",66,6,"Rolling Ridge peaks"],["zora",25,85,"Zora Village / Zora Seas (approx.)"]],"bl":"present","xl":true,"note":"Labrynna appears in two eras. The Maku Tree is again the guardian in the middle of the map. The Gorons are on the northeastern ridge, the graveyard is to the east and the forest is to the southwest.","base":"Present","v":[["ooa_past.webp","Past",true,"past"]]},
{"id":"fs","t":"Four Swords (Realm of Memories)","y":2002,"img":"fs.webp","w":360,"h":270,
 "mk":[["mount",28,18,"Volcano stage"],["snow",15,52,"Ice / waterfall stage"]],
 "bl":"fs","xl":true,"note":"A stage-select screen rather than an overworld. The stages still follow the familiar set: volcano, ice, forest and sky."},
{"id":"ww","t":"The Wind Waker (Great Sea)","y":2002,"img":"ww_sea.webp","w":2000,"h":945,"mk":[["castle",65.6,48.5,"Tower of the Gods (Hyrule Castle sealed below)"],["tot",65.6,54.6,"Master Sword chamber (beneath)"],["mount",79.2,20.5,"Dragon Roost Island"],["rito",81.5,26.3,"Rito Aerie (Dragon Roost)"],["deku",78.6,74.4,"Great Deku Tree (Forest Haven)"],["woods",83.5,76.4,"Forest Haven / Forbidden Woods"],["snow",62.5,76.0,"Ice Ring Isle"],["house",21.0,88.3,"Link's House (Outset Island)"]],"bl":"wwbase","xl":true,"note":"Hyrule lies under the Great Sea: on the main render you can faintly see the drowned landmass beneath the water in the middle of the chart. The old kingdom is sealed below the Tower of the Gods (square E4), and Dragon Roost (fire) and Forest Haven (forest) take over the mountain and forest roles. Ice Ring Isle and Fire Mountain sit side by side as the ice and fire islands. The island chart tab is a fan map by Zantaff; the guide chart tab lists all 49 squares.","base":"Great Sea render","v":[["ww_chart.webp","Island chart (named)",false,"chart"],["ww_guide.webp","Guide sea chart",false],["ww.webp","Decorative chart",false]]},
{"id":"fsa","t":"Four Swords Adventures","y":2004,"img":"fsa.webp","w":811,"h":597,
 "mk":[["castle",48,33,"Hyrule Castle"],["mount",46,14,"Death Mountain"],["woods",15,30,"Forest"],["gerudo",20,72,"Desert pyramid"],["snow",46,66,"Frozen Hyrule"],["kak",72,58,"Village"],["lake",77,47,"Lake Hylia (crater lake)"],["eastern",81,70,"Eastern Temple"]],
 "bl":"fsa","xl":true,"note":"An island-shaped Hyrule that you see as a whole: castle and mountains at the top, desert and ice to the south, villages to the east."},
{"id":"mc","t":"The Minish Cap","y":2004,"img":"mc_full.webp","w":1500,"h":1190,"mk":[["mount",12,25,"Mt. Crenel"],["grave",31,18,"Royal Valley"],["castle",50,13,"Hyrule Castle"],["ranch",73,52,"Lon Lon Ranch"],["lake",89,52,"Lake Hylia"],["woods",87,84,"Minish Woods"],["tot",45,7,"Elemental Sanctuary (in the castle)"]],"bl":"mc","xl":true,"note":"Full map assembled from in-game graphics. Hyrule Town sits under the castle in the centre. Mt. Crenel takes Death Mountain's place in the northwest. Lon Lon Ranch is east of town, with Lake Hylia just past it and the Minish Woods to the south.","base":"Full world","v":[["mc.webp","In-game map",false]]},
{"id":"tp","t":"Twilight Princess","y":2006,"img":"tp_hd.webp","w":1476,"h":1500,"mk":[["castle",45,28,"Hyrule Castle"],["zora",64,7,"Zora's Domain"],["mount",85,31,"Death Mountain"],["kak",87,59,"Kakariko Village"],["grave",92,51,"Graveyard"],["lake",32,42,"Lake Hylia"],["gerudo",15,47,"Gerudo Desert"],["snow",13,9,"Snowpeak"],["faron",59,67,"Faron Woods"],["tot",40,72,"Sacred Grove / Temple of Time"],["ranch",57,96,"Ordon Ranch"],["goron",79,24,"Gorons (Death Mountain)"],["sanct",50,33,"Sanctuary (Castle Town)"],["woods",51,70,"Faron Woods / Faron Mist"]],"bl":"tp","xl":true,"note":"The in-game map is labelled in Hylian script; the labelled fan map tab has the English names. Provinces run from Ordona/Faron in the south, to Eldin in the east, to Lanayru in the north and west.","base":"In-game map","v":[["tp_labeled.webp","Labelled fan map (Zantaff)",false],["tp_select.webp","Area select",false],["tp_dz.webp","Every obtainable (DarkZant)",false,"dz"]]},
{"id":"ph","t":"Phantom Hourglass (World of the Ocean King)","y":2007,"img":"ph_full.webp","w":1600,"h":1208,"mk":[["mount",41.6,91.6,"Isle of Ember (volcano)"],["goron",65.6,85.0,"Goron Island"],["snow",90.9,64.1,"Isle of Frost"],["grave",87.3,15.0,"Isle of the Dead (sages' graveyard)"]],"bl":"ph","xl":true,"note":"Four sea quadrants. The recurring biomes become islands: the volcanic Isle of Ember in the southwestern sea, Goron Island and the Isle of Frost in the southeastern sea, and the Isle of the Dead, with its sages' graveyard, in the northeastern sea. Islands were identified by shape and by the Golden Frog warp signs drawn on the chart. Chart by Zantaff.","base":"Full sea chart","v":[["ph_sea.webp","In-game sea chart",false,"sea"]]},
{"id":"st","t":"Spirit Tracks (New Hyrule)","y":2009,"img":"st_full.webp","w":1000,"h":738,"mk":[["castle",40.5,55.8,"Hyrule Castle"],["tot",49.7,51.5,"Tower of Spirits"],["snow",12.0,40.7,"Snow Realm"],["mount",79.0,19.6,"Fire Realm (Fire Temple)"],["woods",25.0,63.7,"Forest Realm"],["zora",83.0,75.9,"Ocean Realm"],["gerudo",82.0,52.8,"Sand Realm (Sand Temple)"],["goron",65,28,"Goron Village (Fire Realm, approx.)"]],"bl":"st","xl":true,"note":"New Hyrule is split into five realms around the Tower of Spirits: Snow in the northwest, Fire in the northeast, Forest in the southwest, Ocean in the southeast, and Sand in the east. Hyrule Castle stands beside the tower in the middle. Each realm stands in for a classic biome.","base":"Full rail map","v":[["st.webp","Early rail map (4 realms)",false]]},
{"id":"ss","t":"Skyward Sword (Surface & Sky)","y":2011,"img":"ss_surface.webp","w":1500,"h":836,"mk":[["gerudo",24,58,"Lanayru Desert"],["mount",54,24,"Eldin Volcano"],["castle",56,76,"Sealed Grounds (future castle site)"],["tot",58,72,"Sealed Temple"],["woods",76,58,"Faron Woods"],["faron",72,40,"Skyview / Faron"],["lake",88,88,"Lake Floria"]],"bl":"ss","xl":true,"note":"Three separate provinces float apart on the map. The Sealed Grounds sit where Hyrule Castle will later be built, with the Temple of Time beside them.","base":"Surface","v":[["ss_sky.webp","The Sky",false],["ss_hd.webp","Surface (Skyward Sword HD map)",false,"sshd"]]},
{"id":"albw","t":"A Link Between Worlds (Hyrule & Lorule)","y":2013,"img":"albw_hyrule.webp","w":2048,"h":2048,"mk":[["woods",13,14,"Lost Woods"],["mount",58,9,"Death Mountain"],["zora",88,17,"Zora's River"],["sanct",47,25,"Sanctuary"],["grave",56,28,"Graveyard"],["kak",13,51,"Kakariko Village"],["castle",50,44,"Hyrule Castle"],["eastern",86,47,"Eastern Palace"],["house",54,67,"Link's House"],["gerudo",10,85,"Desert of Mystery"],["lake",78,84,"Lake Hylia"],["tot",8,7,"Master Sword pedestal"]],"bl":"hyrule","xl":true,"note":"An almost exact remake of A Link to the Past's Hyrule. Every landmark sits in the same square. Lorule is its dark twin.","base":"Hyrule","v":[["albw_lorule.webp","Lorule",true,"lorule"],["xa_alttp_on_albw.webp","A Link to the Past (Light World)",True,None,"hyrule",1],["xa_eow_on_albw.webp","Echoes of Wisdom (approx.)",True,None,"hyrule",1],["xa_dark_on_albw.webp","A Link to the Past (Dark World)",True,None,"lorule",1]]},
{"id":"tfh","t":"Tri Force Heroes (Hytopia)","y":2015,"img":"tfh.webp","w":704,"h":407,"mk":[["castle",49,52,"Hytopia Castle"],["mount",33,30,"Volcano"],["snow",70,28,"Ice Cavern"],["gerudo",14,47,"Desert / Dunes"],["woods",38,80,"Woodlands"],["lake",67,78,"Riverside"]],"bl":"tfh","xl":true,"note":"A stage-select world, not an open overworld, but it's built from the series' standard biomes around a central castle: woods, water, volcano, ice, desert, a fortress and a sky realm above."},
{"id":"botw","t":"Breath of the Wild / Tears of the Kingdom (Surface, Sky & Depths)","y":2017,"img":"botw.webp","w":1500,"h":1200,"mk":[["castle",47.6,36.8,"Hyrule Castle"],["tot",41.4,75.4,"Great Plateau / Temple of Time"],["deku",54.1,23.3,"Great Deku Tree (Korok Forest)"],["woods",51.2,27.1,"Lost Woods"],["mount",73.7,17.6,"Death Mountain (Eldin)"],["goron",66.4,19.8,"Goron City"],["zora",83.0,44.2,"Zora's Domain"],["kak",68.4,62.3,"Kakariko Village"],["house",83.6,76.6,"Hateno Village (Link's House)"],["rito",13.6,27.3,"Rito Village"],["snow",21.0,12.5,"Hebra"],["gerudo",11.5,86.4,"Gerudo Town / Desert"],["lake",51.0,81.5,"Lake Hylia"],["faron",57.0,87.5,"Faron"],["ranch",51.15,53.4,"Ranch Ruins (Lon Lon Ranch)"]],"note":"A huge open Hyrule, shared by both games. Markers are placed from in-game coordinates: castle just north of centre, Eldin northeast, Zora's Domain east, Gerudo southwest, Hebra northwest. Use the tabs for Tears of the Kingdom's own surface, sky and Depths (all line up exactly), and the checkboxes to show shrines, towers, Korok seeds, Lightroots, dispensers and shops.","bl":"botw","xl":true,"base":"Surface","v":[["totk_surface.webp","Surface (TotK)",true,"surface"],["totk_sky.webp","Sky (TotK)",true,"sky"],["totk_depths.webp","Depths (TotK)",true,"depths"],["botw_parchment.webp","Parchment map",false]],"layers":true},
{"id":"eow","t":"Echoes of Wisdom (Hyrule + Still World)","y":2024,"img":"eow.webp","w":1500,"h":1017,"mk":[["mount",12,24,"Eldin Volcano"],["kak",18,40,"Kakariko Village"],["snow",56,8,"Hebra Mountain"],["castle",47,45,"Hyrule Castle"],["zora",82,24,"Jabul Waters"],["lake",58,72,"Lake Hylia"],["goron",14,31,"Goron City"],["eastern",66,40,"Eastern Temple"],["sanct",47,29,"Northern Sanctuary"],["grave",42,28,"Graveyard"],["ranch",28,59,"Hyrule Ranch"],["gerudo",12,80,"Gerudo Desert"],["faron",86,82,"Faron Wetlands"],["woods",34.05,26.45,"Eternal Forest"],["deku",35.5,23.5,"Deku Tree (Eternal Forest, approx.)"],["house",43.8,91.6,"Link's House (Suthorn Village)"]],"note":"A top-down Hyrule with Eldin and Kakariko flipped to the northwest, Jabul Waters and the sea in the northeast and east, Gerudo southwest and Faron southeast. Lake Hylia is southeast of Castle Town, and the Eastern Temple and the Sanctuary carry over from A Link to the Past. The Still World tab shows every rift's frozen fragment of land. It's arranged in roughly the same layout as Hyrule: Eldin northwest, Jabul Waters northeast, Gerudo southwest, Faron southeast and Hyrule Castle Town in the middle.","base":"Hyrule","bl":"eow","xl":true,"v":[["eow_still.webp","Still World (rifts)",false],["xa_alttp_on_eow.webp","A Link to the Past (approx.)",True,None,None,1],["xa_albw_on_eow.webp","A Link Between Worlds (approx.)",True,None,None,1]]},
]
import base64 as _b64
def _ff(fam,f,w,st): return "@font-face{font-family:'%s';src:url(data:font/woff;base64,%s) format('woff');font-weight:%s;font-style:%s;font-display:swap}"%(fam,_b64.b64encode(open('fonts/'+f,'rb').read()).decode(),w,st)
FONTS=_ff('Bonum','bonum-b.woff',700,'normal')+_ff('Bonum','bonum-i.woff',400,'italic')+_ff('InterZ','inter-r.woff',400,'normal')+_ff('InterZ','inter-sb.woff',600,'normal')+"\n"
LAYERDATA=open('layerdata.js').read()+open('refs.js').read()+open('totkdata.js').read()+open('xldata.js').read()+open('dungeons.js').read()+'\nconst DGPACK='+__import__('json').dumps(__import__('pack_dg').run(),separators=(',',':'))+';\n'
data="const GAMES="+json.dumps(G)+";\n"
html=r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zelda Map Comparison: Recurring Areas Across Every Mainline Game</title>
<style>
:root{--bg:#14130f;--panel:#1e1c16;--panel2:#26231b;--line:#3a3528;--ink:#ece4cf;--mute:#a89f86;--gold:#d8b45a;
--castle:#f5ecd0;--mount:#ff6a3d;--kak:#d9a066;--lake:#4fb0ff;--woods:#4fd364;--zora:#2fe0d0;--gerudo:#ffc23d;--ranch:#c58a52;--grave:#b59cff;--snow:#e8f6ff;--tot:#ffe066;--faron:#a6e34a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,system-ui,sans-serif}
header,main,footer{max-width:1280px;margin:auto;padding:0 22px}header{padding-top:36px}
h1{font-family:Cinzel,serif;font-size:clamp(26px,4vw,40px);margin:0 0 6px;color:var(--gold)}
h2{font-family:Cinzel,serif;color:var(--gold);font-size:22px;margin:0 0 6px}
.sub{color:var(--mute);max-width:860px}section{margin-top:34px}
.bar{position:sticky;top:0;z-index:5;background:#14130fee;backdrop-filter:blur(4px);padding:10px 0;border-bottom:1px solid var(--line)}
.legend{display:flex;flex-wrap:wrap;gap:7px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border:1px solid var(--line);border-radius:999px;font-size:12.5px;cursor:pointer;background:var(--panel);user-select:none}
.chip.on{border-color:var(--gold);background:#3a321f}.dot{width:10px;height:10px;border-radius:50%;flex:none;border:1px solid #0008}
.ctl{display:flex;gap:14px;align-items:center;margin-top:8px;font-size:13px;color:var(--mute);flex-wrap:wrap}
select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 6px}
.map{position:relative;width:100%;border-radius:8px;overflow:hidden;background:#000;cursor:zoom-in}
.map img{width:100%;height:auto;display:block}
.mk{position:absolute;transform:translate(-50%,-50%);width:16px;height:16px;border-radius:50%;border:2px solid #000;box-shadow:0 0 0 2px #fff9,0 2px 6px #000;transition:all .2s}
.mk .lb{position:absolute;left:14px;top:-4px;white-space:nowrap;background:#000c;color:#fff;font-size:11px;padding:1px 6px;border-radius:4px;pointer-events:none}
.hide-lb .mk .lb{display:none}.mk.dim{opacity:.12}.mk.hot{width:24px;height:24px;box-shadow:0 0 0 3px #fff,0 0 18px 6px currentColor}
.mk.hot .lb{display:block!important;font-size:12.5px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:18px;margin-top:14px}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px}
.card h3{margin:0;font-size:16px}.yr{color:var(--mute);font-size:12px;margin-bottom:8px}
.note{font-size:13px;color:#d6cdb6;margin-top:8px}
.extras{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}.extras figure{margin:0;width:calc(33% - 6px);min-width:140px;cursor:zoom-in}
.extras img{width:100%;border-radius:6px;display:block;background:#000}.extras figcaption{font-size:11.5px;color:var(--mute);margin-top:3px}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}@media(max-width:800px){.compare{grid-template-columns:1fr}}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;margin-top:12px}
table{border-collapse:collapse;width:100%;min-width:1000px;font-size:13px}
th,td{border-bottom:1px solid var(--line);padding:7px 6px;text-align:center}
thead th{background:var(--panel2);font-weight:600;font-size:11.5px;writing-mode:vertical-rl;transform:rotate(180deg);height:140px;white-space:nowrap;text-align:left}
tbody th{text-align:left;white-space:nowrap;background:var(--panel);position:sticky;left:0;font-weight:600}
td.P span,td.A span{display:inline-block;width:14px;height:14px;border-radius:50%}td.A span{border:2px solid;background:transparent!important}
tr:hover td,tr:hover th{background:#2c281f}.key{display:flex;gap:18px;color:var(--mute);font-size:13px;margin-top:8px;flex-wrap:wrap}
.areas{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px;margin-top:12px}
.area{background:var(--panel);border:1px solid var(--line);border-left:5px solid;border-radius:10px;padding:12px 14px}
.area h3{margin:0 0 4px;font-size:16px}.area p{margin:4px 0;font-size:13.5px;color:#d8d0bb}
.tip{position:fixed;pointer-events:none;background:#000d;border:1px solid var(--gold);padding:6px 10px;border-radius:6px;font-size:12.5px;max-width:280px;display:none;z-index:20}
#lightbox{position:fixed;inset:0;background:#000e;display:none;z-index:30;overflow:auto;padding:30px;cursor:zoom-out}
#lightbox .map{max-width:min(96vw,1600px);margin:auto;cursor:zoom-out}#lightbox img.solo{max-width:96vw;display:block;margin:auto}
#lbcap{color:var(--ink);text-align:center;margin-top:10px;font-size:14px}
.map img.ovl{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;pointer-events:none;transition:opacity .08s}
.map.nomk .mk{display:none}
.vctl{margin-top:8px;display:flex;flex-direction:column;gap:6px}
.vtabs{display:flex;flex-wrap:wrap;gap:5px}
.vtabs button,.peek{background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 10px;font:500 12.5px Inter,sans-serif;cursor:pointer}
.vtabs button.on{background:var(--gold);color:#1a160c;border-color:var(--gold)}
.blend{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mute);flex-wrap:wrap}
.blend input{flex:1;min-width:120px;accent-color:var(--gold)}.blend .pct{width:34px}
.peek{user-select:none;touch-action:none}
.ref{margin:6px 0 9px}.refbtns{display:flex;gap:6px;margin-top:4px;flex-wrap:wrap}
.rb{background:transparent;color:var(--gold);border:1px solid #6b5a2c;border-radius:6px;padding:2px 8px;font:500 12px Inter,sans-serif;cursor:pointer}.rb:hover{background:#3a321f}
.pin{position:absolute;transform:translate(-50%,-50%);width:12px;height:12px;border-radius:50%;background:#ff3b6b;border:2px solid #fff;box-shadow:0 0 0 2px #000a;z-index:3}
.pin span{display:none;position:absolute;left:14px;top:-5px;white-space:nowrap;background:#000d;color:#fff;font-size:11.5px;padding:1px 6px;border-radius:4px}
.pin.ap{background:transparent;border:2px dashed #ff3b6b;box-shadow:none}.pin:hover span,.pin.big span{display:block}.pin.big{width:22px;height:22px;animation:pp 1.2s infinite}.pin.big span{font-size:13px;font-weight:600}
@keyframes pp{0%{box-shadow:0 0 0 0 #ff3b6bcc}70%{box-shadow:0 0 0 18px #ff3b6b00}100%{box-shadow:0 0 0 0 #ff3b6b00}}
.lyrs{position:absolute;inset:0;pointer-events:none}.lyrs .li{position:absolute;width:18px;height:18px;transform:translate(-50%,-50%);pointer-events:auto;cursor:pointer;filter:drop-shadow(0 1px 2px #000)}
.lyrs .li-korok{width:11px;height:11px}.lyrs .li-shop,.lyrs .li-disp{width:16px;height:16px}.lyrs .li:hover{transform:translate(-50%,-50%) scale(1.8);z-index:4}
#lightbox .lyrs .li{width:24px;height:24px}#lightbox .lyrs .li-korok{width:14px;height:14px}
.lyrpanel{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:12.5px;color:var(--ink);background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:7px 10px}
.lyrpanel>span{color:var(--gold);font-weight:600}.lyrpanel label{display:flex;align-items:center;gap:4px;cursor:pointer}.lyrpanel img{width:16px;height:16px}.lyrpanel small{color:var(--mute)}
.xlpanel details{border:1px solid var(--line);border-radius:6px;padding:2px 8px;background:rgba(0,0,0,.15)}
.xlpanel summary{cursor:pointer;color:var(--gold);font-size:12px}
.xlg{display:flex;flex-wrap:wrap;gap:4px 12px;padding:5px 0}
.xlpanel .xlclr{font-size:11px;padding:2px 8px;cursor:pointer;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:5px}
.xlA{font-size:10px;color:#fff;background:#555;padding:0 3px;border-radius:3px}
.xldot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#ff4fd8;border:1.5px solid #fff;box-sizing:border-box}
.lyrs .li.xldot{width:11px;height:11px}
.lyrs .xlt{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;color:#fff;font-size:9px;text-shadow:0 0 3px #000,0 0 2px #000;pointer-events:auto;cursor:default}
.lyrs .xlt2{font-size:11px;font-weight:600;color:#ffe9a8}.lyrs .xlt3{font-size:14px;font-weight:700;color:#ffd36b;letter-spacing:.5px}
.lyrs .xlt:hover{z-index:5;background:rgba(0,0,0,.6)}
.dgbtn{margin-top:8px;font-size:12px;padding:4px 10px;border-radius:6px;border:1px solid var(--gold);background:transparent;color:var(--gold);cursor:pointer}.dgbtn:hover{background:var(--gold);color:#111}
#dungeons .dgames,#dungeons .dnames,#dungeons .dfloors{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
#dungeons button{font:inherit;font-size:13px;padding:5px 11px;border-radius:7px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}
#dungeons button small{color:var(--mute);margin-left:3px}#dungeons button.on{background:var(--gold);color:#111;border-color:var(--gold)}#dungeons button.on small{color:#333}
#dungeons .dnames button{font-size:12px;padding:4px 9px}#dungeons .dfloors button{font-size:12px;padding:3px 10px;border-radius:14px}
.dview{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:14px;align-items:start}@media(max-width:820px){.dview{grid-template-columns:1fr}}
.dmapwrap{position:relative;overflow:hidden;border-radius:10px;background:#0e0e12;border:1px solid var(--line);touch-action:none;cursor:grab;max-height:78vh}
.dmap{position:relative;transform-origin:0 0;--s:1;max-height:78vh;margin:auto}.dmap img{width:100%;height:100%;display:block;object-fit:contain;image-rendering:auto;user-select:none;-webkit-user-drag:none;pointer-events:none}
.dmk{position:absolute;inset:0}.dmkr{position:absolute;width:13px;height:13px;border-radius:50%;border:2px solid #111;box-shadow:0 0 0 1.5px #fff;transform:translate(-50%,-50%) scale(calc(1/var(--s)));cursor:pointer;transition:box-shadow .15s}
.dmkr.hl{box-shadow:0 0 0 3px #fff,0 0 12px #fff;z-index:3}.dmkr.pulse{animation:dpulse 1s 2}@keyframes dpulse{50%{box-shadow:0 0 0 8px #fff8}}
.dzoom{position:absolute;right:8px;top:8px;z-index:5;display:flex;gap:4px}.dzoom button{padding:3px 9px!important;background:#000a!important}
.dside{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px;max-height:78vh;display:flex;flex-direction:column}
.dtitle{font-weight:700;color:var(--gold);margin-bottom:6px}.dlegend{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:11.5px;color:var(--mute);margin-bottom:8px}.dlegend i,.dchecks i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px;vertical-align:middle}
.dchecks{margin:0;padding:0 0 0 2px;list-style:none;overflow:auto;font-size:12.5px}.dchecks li{padding:4px 6px;border-radius:6px;cursor:pointer}.dchecks li:hover,.dchecks li.hl{background:#ffffff14}.dchecks small{display:block;color:var(--mute);font-size:11px;margin-left:13px}
.dsrc{font-size:11.5px;color:var(--mute);margin-top:8px}
.lyrinfo{flex-basis:100%;font-size:12px;color:#d6cdb6;min-height:16px}
footer{color:var(--mute);font-size:12.5px;padding-bottom:40px;padding-top:20px}a{color:var(--gold)}
'''+open('gamepage.css').read()+FONTS+open('theme.css').read()+r'''</style></head><body>
<header><h1>Hyrule Across the Ages</h1>
<div class="sub">Every mainline <i>Legend of Zelda</i> overworld from 1986 to 2024, with its dungeons, collectibles and the places that keep coming back. Open a game to explore and track it, or scroll down to compare the maps side by side and follow <a href="#callbacks">the callbacks in Breath of the Wild and Tears of the Kingdom</a>.</div></header>
<main>
<div class="bar"><div class="legend" id="legend"></div>
<div class="ctl"><label><input type="checkbox" id="lbls" checked> Show labels</label><span id="status">Showing all areas</span></div></div>

<section><h2>Compare two maps</h2><div class="sub">Put any two games side by side. Cards with tabs have other versions of the same map. Where versions line up (light and dark worlds, seasons, eras, sky, surface and Depths), use the blend slider or hold "Hold to peek" to see one over the other. Tabs marked * have a different layout, so their markers are hidden.</div>
<div class="ctl"><select id="cmpA"></select> vs <select id="cmpB"></select></div>
<div class="compare" id="compare"></div></section>

<section id="layers"><div class="fold"><div class="foldhead"><h2>World layers: sky, below and alternate worlds</h2><button type="button" class="foldhint" aria-expanded="false">Show</button></div><div class="foldbody" hidden>
<div class="sub">Many Zelda maps have a second layer stacked on the first. This section starts with the two sky maps, then puts each game's layers side by side.</div>
<h3 style="margin:18px 0 4px">The two skies</h3><div class="compare" id="skies"></div>
<div class="tablewrap" style="margin-top:12px"><table style="min-width:700px" id="skytable"></table></div>
<h3 style="margin:22px 0 4px">Layer stacks</h3><div id="stacks"></div>
<h3 style="margin:22px 0 4px">Layer types across the series</h3><div class="tablewrap"><table style="min-width:700px" id="lt"></table></div>
</div></div></section>
<section><div class="fold"><div class="foldhead"><h2>Every map</h2><button type="button" class="foldhint" aria-expanded="false">Show</button></div><div class="foldbody" hidden><div class="sub">Every overworld map in the collection, with its versions. Each game's page has the same maps with zoom and markers.</div><div class="grid" id="maps"></div></div></div></section>

<section id="dungeons-sec"><h2>Dungeon maps</h2><div class="sub"><span id="dgcount">Hundreds of</span> dungeon, floor, area and interior maps, with chests, keys, heart pieces, Skulltulas and boss spots from the randomizer trackers. Ocarina of Time dungeons have a separate Master Quest tab. Each game opens on its own page, with zoom, search, a checklist you can tick off, and notes.</div><div id="dungeons"></div></section>
<section><h2>Which areas appear where</h2><div class="sub">Includes games without a map above. Hover a cell to see the area's name in that game.</div>
<div class="key"><span>● Present under its usual name</span><span>○ Analogue / renamed equivalent</span><span>blank = absent</span></div>
<div class="tablewrap"><table id="matrix"></table></div></section>

<section><h2>How each area changes over time</h2><div class="areas" id="areas"></div></section>
<section id="callbacks"><h2>Callbacks in Breath of the Wild &amp; Tears of the Kingdom</h2>
<div class="sub">Both games are full of nods to earlier Zelda games: place names, bridges, armor, music and characters. Many names are slightly misspelled on purpose, as if worn down by history. Click 📍 to see a place on the Breath of the Wild / Tears of the Kingdom map, or ↩ to see what it refers to on the older game's map. Pins come from in-game coordinates; where a landmark has none, the pin uses a cave or well named after it. Dashed pins are approximate. TotK reuses BotW's map, so almost every place name appears in both games.</div>
<div class="ctl" style="margin-top:10px"><input id="rq" placeholder="Search callbacks..." style="background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px 10px;min-width:220px">
<select id="rg"><option value="">Both games</option><option value="BotW">Breath of the Wild</option><option value="TotK">Tears of the Kingdom</option></select>
<select id="rk"><option value="">All types</option></select><label><input type="checkbox" id="rp"> Only with map buttons</label><button id="rall" class="peek">📍 Show all on the map</button><span id="rc"></span></div>
<div id="refs" class="areas"></div></section>

</main>
<footer>The base map images were collected from official art, guide scans and community map projects; creators are credited on the images where known. Extra layers: Breath of the Wild, Tears of the Kingdom (caves, wells, chests, bosses, place names and more), Link's Awakening and Echoes of Wisdom positions come from Zelda Dungeon's open map project (github.com/zeldadungeon/maps, no license stated, so personal use only), with its marker icons. A Link to the Past item locations come from easymac/alttp-map-tracker (MIT). Dungeon maps and their markers come from tracker packs, used as the packs drew them: The Legend of Zelda, Minish Cap, both Oracles, A Link Between Worlds and Majora's Mask (the packs above), Ocarina of Time (StripesOO7 oot-tracker, MIT), A Link to the Past (StripesOO7, MIT; pots and enemy drops left out), Twilight Princess (Kizugaya TPRAP pack, GPL-3), The Wind Waker (Mysteryem ww-poptracker, MIT) and Link's Awakening (Br00ty lasr_brooty). Remake and HD versions: Twilight Princess's 'Every obtainable' tab is stitched from DarkZant's tp-map tiles with its chests, Poe Souls, Golden Bugs, heart pieces, Howling Stones, sky characters and warp portals (no license stated, personal use); Skyward Sword HD's surface map comes from the SSHD Randomizer tracker (AGPL-3) with the Surface layers re-aligned onto it; Majora's Mask 3D's Termina map and region checks come from GonzaloJMora's mm3drTracker (MIT). Link's Awakening dungeon maps already follow the Switch remake. Randomizer-tracker packs supplied the rest, matched to these maps by image alignment: The Legend of Zelda (Br00ty/tloz_brooty), Ocarina of Time (Hamsda's EmoTracker pack, shown on the Manual atlas tab), The Minish Cap (CandyCrystal, MIT), Twilight Princess (j-imbo/tprando_jim), The Wind Waker (Vrontis's map tracker, placed by sea-chart square on the Island chart tab, so positions inside a square are approximate), Skyward Sword (robojumper's SS tracker, GPL-3) and A Link to the Past entrances (StripesOO7, MIT). Packs without a stated license are used for personal use only. Oracle of Seasons (OmegaZeron, MIT), Oracle of Ages (Dranzior/Br00ty, MIT), A Link Between Worlds (Legendgreat, GPL-3, whose 2048 px maps now replace the old 512 px ones) and Majora's Mask (G4M3RL1F3, MIT, whose Termina painting by Nerrel and Clock Town map are added as tabs) came from Archipelago PopTracker packs. Region names are placed at the middle of each tracker region. Phantom Hourglass and Spirit Tracks overworld checks and dungeon maps (every temple floor, the Temple of the Ocean King, the Tower of Spirits, islands, caves and houses) come from the Archipelago randomizers' map trackers, Phantom Hourglass by carrotinator and contributors and Spirit Tracks by DayKat, carrotinator and contributors (both MIT); the Phantom Hourglass sea chart tab is the tracker's sharper chart image, and the Spirit Tracks checks are aligned onto the rail map. Breath of the Wild Hyrule Castle room names and heights come from zeldamods/objmap (GPL-3). The sharper Breath of the Wild map you see when zoomed in is the full-size map image from MrCheeze's botw-object-map, aligned to the base map. The Zelda II palace and world maps are guide scans. Zelda II overworld, Four Swords, Four Swords Adventures and Tri Force Heroes layers, and the earlier Phantom Hourglass and Spirit Tracks layers, are hand-placed from the map images and are approximate. Tears of the Kingdom layer data (shrines, Lightroots, towers, Korok seeds, dispensers, shops) comes from Alshival's Data Service TOTK map project, CC0, credited to Phil, Aeon and SuperSpazzy's data sheet. Some are fan-made, and their creators are credited on the images. Marker positions were placed by eye on each image, so treat them as approximate.</footer>
<div class="tip" id="tip"></div><div id="lightbox" role="dialog" aria-label="Full-size map"><button class="lbx" aria-label="Close">×</button><div id="lbinner"></div><div id="lbcap"></div></div>
<script>
'''+reuse+data+LAYERDATA+r'''
let active=null;
const $=s=>document.querySelector(s);
const tip=$('#tip');function showTip(e,h){tip.innerHTML=h;tip.style.display='block';tip.style.left=Math.min(e.clientX+14,innerWidth-300)+'px';tip.style.top=(e.clientY+14)+'px'}function hideTip(){tip.style.display='none'}

const LYR=[["shrine","Shrines","shrine",["surface","sky"]],["light","Lightroots","shrine",["depths"]],["tower","Skyview Towers","tower",["surface"]],["korok","Korok seeds","korok",["surface","sky"]],["disp","Zonai dispensers","dispenser",["surface","sky","depths"]],["shop","Shops","general",["surface"]]];
function lyrPos(x,y){return [(x+5000)/100,(4000-y)/80]}
function lyrInfo(k,r){const c=`<span style="color:var(--mute)">${r[1]}, ${r[2]}, ${r[3]??''}</span>`;
 if(k==='shrine')return `<b>${r[0]}</b><br>${r[5]} · ${r[6]}<br>${c}`;
 if(k==='light')return `<b>${r[0]}</b><br>Depths, under ${r[5]}<br>${c}`;
 if(k==='tower')return `<b>${r[0]}</b><br>${c}`;
 if(k==='korok')return `<b>Korok seed</b><br>${r[0]}<br>${c}`;
 if(k==='disp')return `<b>Device Dispenser</b> · ${r[0]}<br>${r[5].join(', ')}<br>${c}`;
 if(k==='shop')return `<b>${r[0]}</b> (${r[5]}, ${r[6]})<br>${r[8].slice(0,14).join(', ')}${r[8].length>14?'…':''}<br>${c}`}
function lyrIcon(k,r){if(k==='korok')return r[4]==='sky'?'korok_sky':'korok';if(k==='shop')return r[7];return LYR.find(l=>l[0]===k)[2]}
const TL=['surface','sky','depths'];
function addLayers(g,d,ctl,getCur,V,show){
 const box=document.createElement('div');box.className='lyrs';d.appendChild(box);
 const panel=document.createElement('div');panel.className='lyrpanel';
 panel.innerHTML='<span>TotK layers:</span>'+LYR.map(l=>`<label><input type="checkbox" data-k="${l[0]}"> <img src="icons/${l[2]}.png" alt=""> ${l[1]} <small>(${TOTK[l[0]].length})</small></label>`).join('')+'<div class="lyrinfo">Hover or tap an icon for details.</div>';
 ctl.appendChild(panel);const info=panel.querySelector('.lyrinfo');
 panel.querySelectorAll('input,label').forEach(e=>e.addEventListener('click',ev=>ev.stopPropagation()));
 function render(){box.innerHTML='';const layer=V[getCur()][3];
  if(!TL.includes(layer)){const any=[...panel.querySelectorAll('input:checked')].length;info.textContent=any?'Layers show on the TotK Surface, Sky and Depths tabs.':'Hover or tap an icon for details.';return}
  const frag=document.createDocumentFragment();let n=0;
  panel.querySelectorAll('input:checked').forEach(cb=>{const k=cb.dataset.k;const L=LYR.find(l=>l[0]===k);
   TOTK[k].forEach((r,i)=>{const lay=(k==='tower'||k==='shop')?'surface':r[4];if(lay!==layer)return;
    const [x,y]=lyrPos(r[1],r[2]);if(x<0||x>100||y<0||y>100)return;
    const im=document.createElement('img');im.src='icons/'+lyrIcon(k,r)+'.png';im.className='li li-'+k;im.style.left=x+'%';im.style.top=y+'%';im.dataset.k=k;im.dataset.i=i;frag.appendChild(im);n++})});
  box.appendChild(frag);const ck=panel.querySelectorAll('input:checked').length;info.textContent=!ck?'Hover or tap an icon for details.':n?`${n} icons on this tab. Hover or tap one for details.`:'Nothing from the checked layers on this tab.'}
 box.addEventListener('mouseover',e=>{const t=e.target.closest('.li');if(!t)return;info.innerHTML=lyrInfo(t.dataset.k,TOTK[t.dataset.k][+t.dataset.i]);showTip(e,info.innerHTML)});
 box.addEventListener('mouseout',e=>{if(e.target.closest('.li'))hideTip()});
 box.addEventListener('click',e=>{const t=e.target.closest('.li');if(!t)return;e.stopPropagation();info.innerHTML=lyrInfo(t.dataset.k,TOTK[t.dataset.k][+t.dataset.i])});
 panel.querySelectorAll('input').forEach(cb=>cb.onchange=()=>{if(cb.checked&&!TL.includes(V[getCur()][3]))show(1);render()});
 return render}

const ZDW='https://www.zeldadungeon.net/wiki/';const DOTC=['#ff4fd8','#4fd1ff','#ffd34f','#7dff6b','#ff8a4f','#b48cff'];
const XTAB={botw:'BotW map',surface:'TotK Surface',sky:'TotK Sky',depths:'TotK Depths',light:'Light World',dark:'Dark World',la:'map',eow:'map',loz:'map',mc:'map',tp:'map',ss:'Surface',atlas:'Manual atlas tab',chart:'Island chart tab',holo:'Holodrum (any season)',sub:'Subrosia tab',present:'Present',past:'Past tab',hyrule:'Hyrule',lorule:'Lorule tab',ner:'Termina painting tab',ct:'Clock Town tab',aol:'map',z2w:'Labelled world map tab',ph:'map',dz:'Every obtainable tab',sshd:'Skyward Sword HD tab',mm3d:'3DS remake tab',st:'map',tfh:'map',fs:'map',fsa:'map'};
function xlInfo(c,r){const src=c.src==='alttp'?'easymac/alttp-map-tracker':c.src==='zd'?'Zelda Dungeon maps':c.src;
 return `<b>${r[3]}</b>${c.kind==='label'?'':` <span style="color:var(--mute)">· ${c.n}</span>`}${r[5]?'<br>'+r[5]:''}<br><span style="color:var(--mute)">${XTAB[r[2]]||r[2]} · ${src}</span>${r[4]?` · <a href="${ZDW}${encodeURIComponent(r[4]).replace(/%2F/g,'/')}" target="_blank" rel="noopener">wiki</a>`:''}`}
function addXL(g,d,ctl,getCur,V,show){
 const cats=XL[g.id];const box=document.createElement('div');box.className='lyrs';d.appendChild(box);
 const panel=document.createElement('div');panel.className='lyrpanel xlpanel';
 const groups=[...new Set(cats.map(c=>c.g))];
 panel.innerHTML='<span>Extra layers:</span>'+groups.map(gr=>`<details><summary>${gr} <small>(${cats.filter(c=>c.g===gr).reduce((a,c)=>a+c.it.length,0)})</small></summary><div class="xlg">`+
  cats.map((c,ci)=>c.g!==gr?'':`<label><input type="checkbox" data-c="${ci}"> ${c.i?`<img src="icons/zd/${c.i}" alt="">`:c.kind==='label'?'<b class="xlA">Aa</b>':`<i class="xldot" style="background:${DOTC[ci%DOTC.length]}"></i>`} ${c.n} <small>(${c.it.length})</small></label>`).join('')+'</div></details>').join('')+
  '<button class="xlclr">Clear</button><div class="lyrinfo">Hover or tap an icon for details. Positions from open-source map projects (see credits).</div>';
 ctl.appendChild(panel);const info=panel.querySelector('.lyrinfo');
 panel.querySelectorAll('input,label,summary,details,button').forEach(e=>e.addEventListener('click',ev=>ev.stopPropagation()));
 const tabsOf=c=>[...new Set(c.it.map(r=>r[2]))];
 function render(){box.innerHTML='';const lay=V[getCur()][3];const frag=document.createDocumentFragment();let n=0,any=0;
  panel.querySelectorAll('input:checked').forEach(cb=>{any++;const ci=+cb.dataset.c,c=cats[ci];
   c.it.forEach((r,i)=>{if(r[2]!==lay)return;let el;
    if(c.kind==='label'){el=document.createElement('span');el.className='xlt xlt'+(r[6]||1);el.textContent=r[3]}
    else if(c.kind==='dot'||!c.i){el=document.createElement('i');el.className='li xldot';el.style.background=DOTC[ci%DOTC.length]}
    else{el=document.createElement('img');el.className='li';el.src='icons/zd/'+(r[6]||c.i)}
    el.style.left=r[0]+'%';el.style.top=r[1]+'%';el.dataset.c=ci;el.dataset.i=i;frag.appendChild(el);n++})});
  box.appendChild(frag);
  if(!any)info.textContent='Hover or tap an icon for details. Positions from open-source map projects (see credits).';
  else if(n)info.textContent=`${n} extra markers on this tab. Hover or tap one for details.`;
  else{const t=[...new Set([...panel.querySelectorAll('input:checked')].flatMap(cb=>tabsOf(cats[+cb.dataset.c])))];info.textContent='Nothing from the checked layers on this tab. They show on: '+t.map(x=>XTAB[x]||x).join(', ')+'.'}}
 const at=e=>{const t=e.target.closest('[data-c]');return t&&box.contains(t)?t:null};
 box.addEventListener('mouseover',e=>{const t=at(e);if(!t)return;const c=cats[+t.dataset.c];info.innerHTML=xlInfo(c,c.it[+t.dataset.i]);showTip(e,info.innerHTML)});
 box.addEventListener('mouseout',e=>{if(at(e))hideTip()});
 box.addEventListener('click',e=>{const t=at(e);if(!t)return;e.stopPropagation();const c=cats[+t.dataset.c];info.innerHTML=xlInfo(c,c.it[+t.dataset.i])});
 panel.querySelectorAll('input').forEach(cb=>cb.onchange=()=>{if(cb.checked){const c=cats[+cb.dataset.c],t=tabsOf(c);if(!t.includes(V[getCur()][3])){const vi=V.findIndex(v=>v[3]===t[0]);if(vi>=0){show(vi);return}}}render()});
 panel.querySelector('.xlclr').onclick=e=>{e.stopPropagation();panel.querySelectorAll('input:checked').forEach(c=>c.checked=false);render()};
 return render}
function mapEl(g,big){const wrap=document.createElement('div');
 const V=[[g.img,g.base||'Map',true,g.bl]].concat((g.v||[]).filter(v=>!v[5]));let cur=0;
 const d=document.createElement('div');d.className='map';
 d.innerHTML=`<img class="baseimg" src="maps/${g.img}" alt="${g.t} map" loading="lazy" width="${g.w}" height="${g.h}"><img class="ovl" alt="" style="opacity:0">`+g.mk.map(m=>`<div class="mk" data-a="${m[0]}" style="left:${m[1]}%;top:${m[2]}%;background:${AREAS[m[0]].c};color:${AREAS[m[0]].c}"><span class="lb">${m[3]}</span></div>`).join('');
 if(!big)d.onclick=e=>{if(e.target.closest('.vctl'))return;openLB(g)};
 wrap.appendChild(d);if(V.length<2&&!g.xl)return d;
 const base=d.querySelector('.baseimg'),ovl=d.querySelector('.ovl');
 const ctl=document.createElement('div');ctl.className='vctl';
 const aligned=V.filter(x=>x[2]);
 ctl.innerHTML=(V.length<2?'':`<div class="vtabs">${V.map((x,i)=>`<button data-i="${i}" class="${i?'':'on'}">${x[1]}${x[2]?'':' <span title="Different layout, so markers are hidden">*</span>'}</button>`).join('')}</div>`)+
  (aligned.length>1?`<div class="blend"><span>Blend in</span><select>${V.map((x,i)=>x[2]?`<option value="${i}">${x[1]}</option>`:'').join('')}</select><input type="range" min="0" max="100" value="0"><span class="pct">0%</span><button class="peek" title="Hold to show the blended map at full strength">Hold to peek</button></div>`:'');
 const tabs=ctl.querySelectorAll('.vtabs button'),sel=ctl.querySelector('select'),rng=ctl.querySelector('input[type=range]'),pct=ctl.querySelector('.pct');
 let show=function(i){cur=i;const x=V[i];base.src='maps/'+x[0];tabs.forEach(t=>t.classList.toggle('on',+t.dataset.i===i));d.classList.toggle('nomk',!x[2]);
  if(sel){ctl.querySelector('.blend').style.display=x[2]?'':'none';if(+sel.value===i){const o=[...sel.options].find(o=>+o.value!==i);if(o)sel.value=o.value}setOvl()}}
 function setOvl(){if(!sel)return;ovl.src='maps/'+V[+sel.value][0];const v=V[cur][2]?+rng.value:0;ovl.style.opacity=v/100;pct.textContent=rng.value+'%'}
 tabs.forEach(t=>t.onclick=e=>{e.stopPropagation();show(+t.dataset.i)});
 if(sel){sel.value=aligned.length>1?V.indexOf(aligned[1]):0;sel.onchange=setOvl;rng.oninput=setOvl;
  const pk=ctl.querySelector('.peek');let keep=0;
  const on=e=>{e.preventDefault();keep=rng.value;rng.value=100;setOvl()},off=()=>{rng.value=keep;setOvl()};
  pk.addEventListener('pointerdown',on);pk.addEventListener('pointerup',off);pk.addEventListener('pointerleave',off);
  ctl.querySelectorAll('select,input,button').forEach(el=>el.addEventListener('click',e=>e.stopPropagation()));setOvl()}
 const RR=[];if(g.layers)RR.push(addLayers(g,d,ctl,()=>cur,V,show));if(g.xl&&XL[g.id])RR.push(addXL(g,d,ctl,()=>cur,V,i=>show(i)));const _show=show;show=function(i){_show(i);RR.forEach(f=>f())};tabs.forEach(t=>t.onclick=e=>{e.stopPropagation();show(+t.dataset.i)});
 wrap.appendChild(ctl);return wrap}
function openLB(g,img,cap){const lb=$('#lightbox'),inn=$('#lbinner');inn.innerHTML='';if(img){inn.innerHTML=`<img class="solo" src="maps/${img}">`;$('#lbcap').textContent=cap}else{inn.appendChild(mapEl(g,true));$('#lbcap').textContent=g.t+' ('+g.y+')'}lbSetup(g,img);apply()}
$('#lightbox').addEventListener('click',e=>{if(e.target.id==='lightbox'||e.target.id==='lbinner'||e.target.closest('.lbx'))lbClose()});
function card(g){const c=document.createElement('div');c.className='card';c.innerHTML=`<h3>${g.t}</h3><div class="yr">${g.y}</div>`;c.appendChild(mapEl(g));
 const n=document.createElement('div');n.className='note';n.textContent=g.note;c.appendChild(n);
 {const lk=document.createElement('div');lk.innerHTML=`<a class="gpopen" href="#/g/${g.id}">Open game page</a>`+(typeof DUNG!=='undefined'&&DUNG[g.id]?`<a class="dgbtn" style="text-decoration:none;display:inline-block" href="#/g/${g.id}/d/0">Dungeon maps (${DUNG[g.id].m.length})</a>`:'');c.appendChild(lk)}
 if(g.extra){const ex=document.createElement('div');ex.className='extras';g.extra.forEach(([f,cap])=>{const fg=document.createElement('figure');fg.innerHTML=`<img src="maps/${f}" loading="lazy"><figcaption>${cap}</figcaption>`;fg.onclick=()=>openLB(g,f,cap);ex.appendChild(fg)});c.appendChild(ex)}return c}

'''+open('lbzoom.js').read()+open('gamepage.js').read()+open('gpdual.js').read()+open('gpad.js').read()+open('gpsync.js').read()+r'''
GAMES.forEach(g=>$('#maps').appendChild(card(g)));
{const D=Object.values(DUNG);const el=$('#dgcount');if(el)el.textContent=D.reduce((a,d)=>a+d.m.length,0).toLocaleString()+' maps across '+D.length+' games:';}
document.querySelectorAll('.fold').forEach(d=>{const b=d.querySelector('.foldhint'),body=d.querySelector('.foldbody');b.onclick=()=>{const open=body.hidden;body.hidden=!open;b.textContent=open?'Hide':'Show';b.setAttribute('aria-expanded',open)}});
['#cmpA','#cmpB'].forEach((s,i)=>{const el=$(s);GAMES.forEach(g=>el.innerHTML+=`<option value="${g.id}">${g.t} (${g.y})</option>`);el.value=i?'botw':'alttp';el.onchange=drawCmp});
function drawCmp(){const c=$('#compare');c.innerHTML='';[$('#cmpA').value,$('#cmpB').value].forEach(id=>c.appendChild(card(GAMES.find(g=>g.id===id))));apply()}
const lg=$('#legend');Object.entries(AREAS).forEach(([k,a])=>{const c=document.createElement('span');c.className='chip';c.dataset.k=k;c.innerHTML=`<span class="dot" style="background:${a.c}"></span>${a.n}`;c.onclick=()=>{active=active===k?null:k;apply()};lg.appendChild(c)});
function apply(){document.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x.dataset.k===active));
 document.querySelectorAll('.mk').forEach(m=>{m.classList.toggle('dim',!!active&&m.dataset.a!==active);m.classList.toggle('hot',m.dataset.a===active)});
 $('#status').textContent=active?`Highlighting ${AREAS[active].n}: on ${GAMES.filter(g=>g.mk.some(m=>m[0]===active)).length} of ${GAMES.length} maps`:'Showing all areas';}
$('#lbls').onchange=e=>document.body.classList.toggle('hide-lb',!e.target.checked);
document.addEventListener('mouseover',e=>{const m=e.target.closest('.mk');if(m)showTip(e,m.querySelector('.lb').textContent)});document.addEventListener('mouseout',e=>{if(e.target.closest('.mk'))hideTip()});
drawCmp();

SKY.forEach(g=>$('#skies').appendChild(card(g)));
const ST=[["","Skyward Sword","Tears of the Kingdom"],["Structure","One cloud sea with scattered islands","Separate archipelagos, each above a surface region"],["Hub","Skyloft, in the centre","None. The Great Sky Island is the starting area, south of centre"],["Way down","Dive through 3 columns of light (Faron, Eldin, Lanayru)","Dive anywhere and land on the ground directly below"],["Storm zone","The Thunderhead (northwest), hiding the Isle of Songs","The Thunderhead Isles (Faron Sky), fog-covered until a quest clears it"],["Temples in the sky","Sky Keep (endgame)","The Wind and Water Temples, plus the Temple of Time on the Great Sky Island"],["Relation to the surface","The surface is cut off by the Cloud Barrier","The same footprint as the surface and the Depths"]];
$('#skytable').innerHTML=ST.map((r,i)=>'<tr>'+r.map((c,j)=>i===0?`<th style="writing-mode:horizontal-tb;transform:none;height:auto;background:var(--panel2)">${c}</th>`:(j===0?`<th>${c}</th>`:`<td style="text-align:left">${c}</td>`)).join('')+'</tr>').join('');
STACKS.forEach(([t,imgs,n])=>{const c=document.createElement('div');c.className='card';c.style.marginTop='12px';c.innerHTML=`<h3>${t}</h3><div class="note" style="margin:4px 0 8px">${n}</div><div style="display:grid;grid-template-columns:repeat(${imgs.length},1fr);gap:8px">${imgs.map(([f,cap])=>`<figure style="margin:0;cursor:zoom-in" data-f="${f}" data-c="${t}: ${cap}"><img src="maps/${f}" loading="lazy" style="width:100%;border-radius:6px;background:#000;aspect-ratio:1/1;object-fit:contain"><figcaption style="font-size:12px;color:var(--mute);text-align:center">${cap}</figcaption></figure>`).join('')}</div>`;
c.querySelectorAll('figure').forEach(fg=>fg.onclick=()=>openLB(null,fg.dataset.f,fg.dataset.c));$('#stacks').appendChild(c)});
$('#lt').innerHTML='<tr><th style="writing-mode:horizontal-tb;transform:none;height:auto;background:var(--panel2)">Layer type</th><th style="writing-mode:horizontal-tb;transform:none;height:auto;background:var(--panel2);text-align:left">Where it appears</th></tr>'+LT.map(r=>`<tr><th>${r[0]}</th><td style="text-align:left">${r[1]}</td></tr>`).join('');
apply();

(function(){const kinds=[...new Set(REFS.map(r=>r[4]))].sort();$('#rk').innerHTML+=kinds.map(k=>`<option>${k}</option>`).join('');
const tag=g=>`<span style="font-size:11px;border:1px solid var(--line);border-radius:999px;padding:1px 7px;color:var(--mute);white-space:nowrap">${g}</span>`;
const ALLG=GAMES.concat(SKY);const gname=id=>{const g=ALLG.find(x=>x.id===id);return g?g.t.replace(/ \(.*/,''):id};
function draw(){const q=$('#rq').value.toLowerCase(),gm=$('#rg').value,k=$('#rk').value,pm=$('#rp').checked;
 const rows=REFS.filter(r=>(!q||r.slice(0,5).join(' ').toLowerCase().includes(q))&&(!gm||r[3].includes(gm))&&(!k||r[4]===k)&&(!pm||r[5]||r[6]));
 const by={};rows.forEach(r=>(by[r[0]]=by[r[0]]||[]).push(r));
 $('#refs').innerHTML=Object.entries(by).map(([g,rs])=>`<div class="area" style="border-left-color:var(--gold)"><h3>${g} <span style="color:var(--mute);font-weight:400;font-size:13px">(${rs.length})</span></h3>${rs.map(r=>`<div class="ref"><div style="display:flex;gap:8px;justify-content:space-between;align-items:baseline"><span><b>${r[1]}</b>: ${r[2]}</span><span style="display:flex;gap:4px">${tag(r[4])}${tag(r[3])}</span></div>${r[5]||r[6]?`<div class="refbtns">${r[5]?`<button class="rb" data-i="${REFS.indexOf(r)}" data-m="now">📍 On the BotW/TotK map</button>`:''}${r[6]?`<button class="rb" data-i="${REFS.indexOf(r)}" data-m="then">↩ Original in ${gname(r[6][0])}</button>`:''}</div>`:''}</div>`).join('')}</div>`).join('')||'<p class="sub">No matches.</p>';
 $('#rc').textContent=`${rows.length} callbacks across ${Object.keys(by).length} games`;
 $('#refs').querySelectorAll('.rb').forEach(bt=>bt.onclick=()=>showRef(REFS[+bt.dataset.i],bt.dataset.m))}
['#rq','#rg','#rk','#rp'].forEach(s=>$(s).addEventListener('input',draw));draw();
$('#rall').onclick=()=>{const g=GAMES.find(x=>x.id==='botw');openLB(g);const m=$('#lbinner .map');m.classList.add('nomk');
 REFS.filter(r=>r[5]).forEach(r=>addPin(m,r[5][0],r[5][1],r[1]+(r[7]?' (approx.)':''),false,r[7]));$('#lbcap').textContent=`Every pinned callback place (${REFS.filter(r=>r[5]).length}) on the Breath of the Wild / Tears of the Kingdom map. Hover a pin for its name.`};
function addPin(m,x,y,label,big,ap){const p=document.createElement('div');p.className='pin'+(big?' big':'')+(ap?' ap':'');p.style.left=x+'%';p.style.top=y+'%';p.innerHTML=`<span>${label}</span>`;m.appendChild(p);return p}
function showRef(r,mode){if(mode==='now'){const g=GAMES.find(x=>x.id==='botw');openLB(g);const m=$('#lbinner .map');m.classList.add('nomk');const p=addPin(m,r[5][0],r[5][1],r[1]+(r[7]?' (approximate)':''),true,r[7]);
  $('#lbcap').textContent=`${r[1]}: named after ${r[2]} (${r[0]}).`+(r[7]?' This pin is approximate: it is placed from a nearby mapped spot and the wiki description.':'');setTimeout(()=>LBZ&&LBZ.focus(r[5][0],r[5][1],3),80)}
 else{const g=ALLG.find(x=>x.id===r[6][0]);openLB(g);const m=$('#lbinner .map');
  m.querySelectorAll('.mk').forEach(e=>{const hit=e.dataset.a===r[6][1];e.classList.toggle('hot',hit);e.classList.toggle('dim',!hit)});
  const h=m.querySelector('.mk.hot');$('#lbcap').textContent=`${g.t}: ${h?h.querySelector('.lb').textContent:''}, the original of "${r[1]}" in BotW/TotK.`;if(h)setTimeout(()=>LBZ&&LBZ.focus(parseFloat(h.style.left),parseFloat(h.style.top),2.5),80)}}
})();
// matrix
const order=["loz","aol","alttp","la","oot","mm","oos","ooa","fs","ww","fsa","mc","tp","ph","st","ss","albw","tfh","botw","totk","eow"];
let h='<thead><tr><th style="writing-mode:horizontal-tb;transform:none;height:auto">Area</th>'+order.map(g=>`<th>${SHORT[g]}</th>`).join('')+'</tr></thead><tbody>';
Object.entries(AREAS).forEach(([k,a])=>{h+=`<tr><th><span class="dot" style="display:inline-block;background:${a.c};margin-right:6px"></span>${a.n}</th>`;
order.forEach(g=>{const v=M[g][k];if(!v){h+='<td></td>';return}const[t,name]=v.split('|');h+=`<td class="${t}" data-l="${SHORT[g]}: ${name||a.n}${t==='A'?' (analogue)':''}"><span style="${t==='P'?'background:':'border-color:'}${a.c}"></span></td>`});h+='</tr>'});
h+='<tr><th>Areas present</th>'+order.map(g=>`<td><b>${Object.keys(M[g]).length}</b></td>`).join('')+'</tr></tbody>';
const tb=$('#matrix');tb.innerHTML=h;tb.querySelectorAll('td[data-l]').forEach(td=>{td.onmousemove=e=>showTip(e,td.dataset.l);td.onmouseleave=hideTip});
Object.entries(AREAS).forEach(([k,a])=>{const cnt=order.filter(g=>M[g][k]).length;$('#areas').innerHTML+=`<div class="area" style="border-left-color:${a.c}"><h3>${a.n}</h3><div class="yr">In ${cnt} of ${order.length} games (counting analogues)</div><p>${AREA_TEXT[k]}</p></div>`});
gpHome();
</script></body></html>'''
open('site/index.html','w').write(html)
