import json,re
b=open('build.py').read()
def seg(gid):
    i=b.index('{"id":"%s"'%gid); j=b.find('\n{"id"',i+5)
    if j<0: j=b.index('\n]',i)
    return i,j
def setgame(gid,newtext):
    global b
    i,j=seg(gid); b=b[:i]+newtext+b[j:]
def getgame(gid):
    i,j=seg(gid); return b[i:j]
# TP transform
T=json.load(open('tp_aff.json'));A=T['A']
s=getgame('tp')
def tr(m):
    a,x,y=m.group(1),float(m.group(2)),float(m.group(3))
    px,py=x/100*T['ow'],y/100*T['oh']
    nx=A[0][0]*px+A[0][1]*py+A[0][2]; ny=A[1][0]*px+A[1][1]*py+A[1][2]
    return '["%s",%d,%d,'%(a,round(nx/T['nw']*100),round(ny/T['nh']*100))
s=re.sub(r'\["(\w+)",(\d+),(\d+),',tr,s)
s=s.replace('"img":"tp.webp","w":569,"h":600','"img":"tp_hd.webp","w":1476,"h":1500')
s=s.replace('"note":"The map labels are in Hylian script.','"extra":[["tp_english.webp","Fan-made English-labelled map (Wei-Hua Huang), for reading the place names"],["tp_select.webp","The area-select map"]],"note":"The in-game map is labelled in Hylian script; the English fan map underneath has the names.')
setgame('tp',s)
def J(d): return json.dumps(d,separators=(',',':'))
setgame('mc',J({"id":"mc","t":"The Minish Cap","y":2004,"img":"mc_full.webp","w":1500,"h":1190,
 "mk":[["mount",12,25,"Mt. Crenel"],["grave",31,18,"Royal Valley"],["castle",50,13,"Hyrule Castle"],["kak",50,60,"Hyrule Town"],["zora",70,20,"Veil Falls"],["snow",87,14,"Cloud Tops"],["ranch",73,52,"Lon Lon Ranch"],["lake",89,52,"Lake Hylia"],["woods",87,84,"Minish Woods"],["faron",12,68,"Castor Wilds"]],
 "note":"Hyrule Town sits under the castle in the centre. Mt. Crenel takes Death Mountain's place in the northwest. Lon Lon Ranch is east of town, with Lake Hylia just past it and the Minish Woods to the south. The Cloud Tops above aren't a snow region; they're marked with that colour only because they're the high, cold-looking area.",
 "extra":[["mc.webp","The earlier, smaller version of the map"]]})+',')
setgame('aol',J({"id":"aol","t":"Zelda II: The Adventure of Link (full overworld)","y":1987,"img":"aol_full.webp","w":1600,"h":1088,
 "mk":[["castle",16,25,"North Castle (sleeping Zelda)"],["gerudo",19,9,"Desert (Parapa)"],["grave",30,51,"King's Tomb graveyard"],["mount",12,78,"Death Mountain maze"],["tot",48,57,"Great Palace (Triforce of Courage)"]],
 "note":"Two continents. Western Hyrule (left) has North Castle, the towns, the graveyard and the Death Mountain cave maze; Eastern Hyrule (right) holds the Great Palace, Maze Island and the later towns. The map image credits Rick N. Bruns / NESMaps.",
 "extra":[["aol_east.webp","The earlier eastern-only map"]]})+',')
# MM official as extra
s=getgame('mm'); s=s.replace('"note":"The same biomes','"extra":[["mm_official.webp","Official Majora\'s Mask 3D-style map of Termina"]],"note":"The same biomes'); setgame('mm',s)
# new games
def insert_after(gid,d):
    global b
    i,j=seg(gid); b=b[:j]+'\n'+J(d)+','+b[j:]
insert_after('alttp',{"id":"oot64","t":"Ocarina of Time (1998 original)","y":1998,"img":"oot_original.webp","w":1500,"h":1036,
 "mk":[["gerudo",8,9,"Desert Colossus / Haunted Wasteland"],["castle",58,25,"Hyrule Castle"],["tot",53,32,"Market / Temple of Time"],["mount",70,8,"Death Mountain Crater"],["goron",76,24,"Goron City"],["kak",75,47,"Kakariko Village"],["grave",81,41,"Graveyard"],["zora",88,57,"Zora's Domain"],["ranch",42,61,"Lon Lon Ranch"],["lake",17,82,"Lake Hylia"],["woods",65,76,"Lost Woods"],["deku",56,85,"Kokiri Forest (Deku Tree)"]],
 "note":"The original 1998 layout from the game's foldout poster. It's the same arrangement the remake keeps: Gerudo in the far west, Death Mountain northeast, the forest southeast and Lake Hylia southwest.",
 "extra":[["oot_manual_labeled.webp","The Hyrule World Atlas from the manual, labelled"],["oot_manual.webp","The same atlas, unlabelled"]]})
insert_after('ss',{"id":"albw","t":"A Link Between Worlds (Hyrule)","y":2013,"img":"albw_hyrule.webp","w":512,"h":512,
 "mk":[["woods",13,14,"Lost Woods"],["mount",58,9,"Death Mountain"],["zora",88,17,"Zora's River"],["sanct",47,25,"Sanctuary"],["grave",56,28,"Graveyard"],["kak",13,51,"Kakariko Village"],["castle",50,44,"Hyrule Castle"],["eastern",86,47,"Eastern Palace"],["house",54,67,"Link's House"],["gerudo",10,85,"Desert of Mystery"],["lake",78,84,"Lake Hylia"]],
 "note":"An almost exact remake of A Link to the Past's Hyrule. Every landmark sits in the same square. Lorule is its dark twin.",
 "extra":[["albw_lorule.webp","Lorule, the parallel kingdom (Lorule Castle in the centre, a dark-world mirror of Hyrule)"]]})
insert_after('albw',{"id":"tfh","t":"Tri Force Heroes (Hytopia)","y":2015,"img":"tfh.webp","w":704,"h":407,
 "mk":[["castle",49,52,"Hytopia Castle"],["mount",33,30,"Volcano"],["snow",70,28,"Ice Cavern"],["gerudo",14,47,"Desert / Dunes"],["woods",38,80,"Woodlands"],["lake",67,78,"Riverside"]],
 "note":"A stage-select world, not an open overworld, but it's built from the series' standard biomes around a central castle: woods, water, volcano, ice, desert, a fortress and a sky realm above."})
b=b.replace('"loz","aol","alttp","la","oot",','"loz","aol","alttp","la","oot",').replace('"albw","botw"','"albw","tfh","botw"')
b=b.replace(" A Link Between Worlds and Tri Force Heroes don't have uploaded maps, so they appear only in the table. A Link Between Worlds reuses the A Link to the Past map almost exactly.","")
open('build.py','w').write(b)
r=open('reuse.js').read()
r=r.replace('const SHORT={','const SHORT={tfh:"TFH \'15",')
r=r.replace('\nbotw:{','\ntfh:{castle:"A|Hytopia Castle",mount:"A|Volcano",snow:"A|Ice Cavern",gerudo:"A|Dunes",woods:"A|Woodlands",lake:"A|Riverside"},\nbotw:{',1)
r=r.replace('albw:{castle:"P"','albw:{zora:"P|Zora\'s River / Domain",castle:"P"') if 'albw:{castle' in r else r
open('reuse.js','w').write(r)
l=open('layerdata.js').read()
l=l.replace('["Oracle of Ages: present and past"','["A Link Between Worlds: Hyrule and Lorule", [["albw_hyrule.webp", "Hyrule"], ["albw_lorule.webp", "Lorule"]], "The same idea as A Link to the Past\'s Dark World, but Lorule is its own kingdom with its own castle, and you move between the two through wall cracks."], ["Oracle of Ages: present and past"')
open('layerdata.js','w').write(l)
