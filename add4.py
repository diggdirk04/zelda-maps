import json
b=open('build.py').read()
new=[
('alttp',{"id":"la","t":"Link's Awakening (Koholint Island, Switch map)","y":1993,"img":"la.webp","w":1500,"h":857,
 "mk":[["mount",41,6,"Mt. Tamaranch (Wind Fish's Egg)"],["woods",15,45,"Mysterious Forest"],["grave",45,47,"Cemetery"],["castle",60,44,"Kanalet Castle"],["kak",18,66,"Mabe Village"],["lake",58,85,"Martha's Bay"],["gerudo",90,84,"Yarna Desert"]],
 "note":"Koholint isn't Hyrule, but it reuses the pattern: a mountain range across the north, a maze forest in the west, a castle and graveyard in the middle, a bay to the south and a desert in the southeast."}),
('mm',{"id":"oos","t":"Oracle of Seasons (Holodrum, summer)","y":2001,"img":"oos_summer.webp","w":1500,"h":1200,
 "mk":[["woods",9,28,"Lost Woods"],["deku",59,77,"Maku Tree"],["kak",47,90,"Horon Village"],["grave",7,88,"Western Coast graveyard"],["gerudo",88,82,"Samasa Desert"]],
 "note":"Holodrum is the same land in four seasons. The Maku Tree in Horon Village does the Deku Tree's job as guardian, the Lost Woods are in the west, and there's a desert in the southeast and a graveyard on the west coast.",
 "extra":[["oos_spring.webp","Spring"],["oos_autumn.webp","Autumn"],["oos_winter.webp","Winter"],["oos_gb.webp","The original Game Boy Color overview map"]]}),
('oos',{"id":"ooa","t":"Oracle of Ages (Labrynna, present)","y":2001,"img":"ooa_present.webp","w":1500,"h":1200,
 "mk":[["deku",60,24,"Maku Tree"],["kak",55,39,"Lynna City"],["grave",86,52,"Yoll Graveyard"],["woods",15,62,"Deku Forest"],["goron",82,10,"Rolling Ridge (Gorons)"]],
 "note":"Labrynna appears in two eras. The Maku Tree is again the guardian in the middle of the map. The Gorons are on the northeastern ridge, the graveyard is to the east and the forest is to the southwest.",
 "extra":[["ooa_past.webp","Labrynna in the past"],["ooa_nav_present.webp","Present-day overview map"],["ooa_nav_past.webp","Past overview map"]]}),
('tp',{"id":"ph","t":"Phantom Hourglass (World of the Ocean King)","y":2007,"img":"ph.webp","w":512,"h":384,"mk":[],
 "note":"Four sea charts: NW, NE, SW and SE. The recurring biomes turn into islands: Goron Island and the Isle of Frost in the northeastern sea, and the Isle of Ember (the fire island) in the southwestern sea. I haven't put markers on the individual islands because I couldn't confirm which one is which on this image."}),
]
for after,g in new:
    i=b.index('{"id":"%s"'%after)
    j=b.find('\n{"id"',i+5)
    b=b[:j]+'\n'+json.dumps(g,separators=(',',':'))+','+b[j:]
b=b.replace('const order=["loz","aol","alttp","oot","mm","ww","fsa","mc","tp","st","ss","albw","botw","totk","eow"];',
 'const order=["loz","aol","alttp","la","oot","mm","oos","ooa","ww","fsa","mc","tp","ph","st","ss","albw","botw","totk","eow"];')
b=b.replace("Link's Awakening, the Oracle games, Phantom Hourglass, A Link Between Worlds and Tri Force Heroes don't have uploaded maps, so they appear only in the table.","A Link Between Worlds and Tri Force Heroes don't have uploaded maps, so they appear only in the table.")
open('build.py','w').write(b)
r=open('reuse.js').read()
def ins(before,txt):
    global r
    assert before in r,before
    r=r.replace(before,txt+before,1)
ins('\nalttp:{','\nla:{castle:"A|Kanalet Castle",mount:"A|Tal Tal Heights / Mt. Tamaranch",kak:"A|Mabe Village",lake:"A|Martha\'s Bay",woods:"A|Mysterious Forest",gerudo:"A|Yarna Desert",grave:"P|Cemetery"},')
ins('\nww:{','\noos:{mount:"A|Goron Mountain / Mt. Cucco",kak:"A|Horon Village",woods:"P|Lost Woods",gerudo:"A|Samasa Desert",grave:"A|Western Coast graveyard",deku:"A|Maku Tree",goron:"A|Goron Mountain"},\nooa:{mount:"A|Talus Peaks / Rolling Ridge",kak:"A|Lynna City",woods:"A|Deku Forest",zora:"A|Zora Village",grave:"A|Yoll Graveyard",deku:"A|Maku Tree",goron:"A|Rolling Ridge"},')
ins('\nst:{','\nph:{mount:"A|Isle of Ember",snow:"A|Isle of Frost",goron:"A|Goron Island"},')
r=r.replace('const SHORT={','const SHORT={la:"LA \'93",oos:"OoS \'01",ooa:"OoA \'01",ph:"PH \'07",')
r=r.replace('Echoes of Wisdom puts him deep in the Eternal Forest.','Echoes of Wisdom puts him deep in the Eternal Forest. In the Oracle games the Maku Tree plays the same guardian role, in the middle of Holodrum and Labrynna.')
open('reuse.js','w').write(r)
