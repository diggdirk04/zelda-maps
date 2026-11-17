import json
b=open('build.py').read()
def seg(gid):
    i=b.index('{"id":"%s"'%gid); j=b.find('\n{"id"',i+5)
    if j<0: j=b.index('\n]',i)
    return i,j
def get(gid):
    i,j=seg(gid); t=b[i:j].rstrip().rstrip(','); return json.loads(t)
def put(gid,d):
    global b
    i,j=seg(gid); b=b[:i]+json.dumps(d,separators=(',',':'))+','+b[j:]
def drop(gid):
    global b
    i,j=seg(gid); b=b[:i]+b[j+1:]
g=get('aol'); g.pop('extra',None); put('aol',g)
g=get('oot64'); g['id']='oot'; g['t']='Ocarina of Time'
g['note']="The original 1998 layout, from the official foldout poster: Gerudo in the far west, Death Mountain northeast, the forest southeast and Lake Hylia southwest. The 2026 Switch 2 remake keeps the same arrangement, and its map is the first thumbnail."
g['extra']=[["oot.webp","Official map from the 2026 Switch 2 remake"],["oot_manual_labeled.webp","Hyrule World Atlas from the original manual"]]
drop('oot'); put('oot64',g)
g=get('mm'); g['img']='mm_official.webp'; g['w']=1333; g['h']=948
g['mk']=[["snow",45,15,"Snowhead"],["mount",45,22,"Snowhead mountains (Gorons)"],["castle",50,48,"Clock Town (the hub)"],["lake",16,45,"Great Bay"],["gerudo",10,53,"Pirates' Fortress"],["woods",50,67,"Southern Swamp / Woodfall"],["grave",74,46,"Ikana Canyon"],["tot",83,40,"Stone Tower"]]
g['t']="Majora's Mask (Termina)"
g['note']="Official Termina map. The same biomes as Hyrule in new places: snowy mountain to the north, sea to the west, swamp to the south and the haunted canyon to the east, with Clock Town at the centre. The Stone Tower marker uses the Temple of Time colour only because it's the sacred site; it isn't a Temple of Time."
g['extra']=[["mm.webp","Detailed fan map by Nick Johnson, with every area named"]]
put('mm',g)
g=get('ooa'); g['extra']=[["ooa_past.webp","Labrynna in the past"]]; put('ooa',g)
g=get('mc'); g['extra']=[["mc.webp","The official in-game world map"]]; g['note']=g['note'].replace("Hyrule Town sits","Full map assembled from in-game graphics. Hyrule Town sits"); put('mc',g)
g=get('ww'); g['extra']=[["ww.webp","Decorative sea chart in Hylian script"]]; g['note']+=" The main image is a fan-labelled grid of the in-game chart."; put('ww',g)
g=get('botw'); g['extra'][0][1]="Official 'Explorer's Edition' parchment map of the same Hyrule"; put('botw',g)
open('build.py','w').write(b)
