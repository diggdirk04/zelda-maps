# Hand-placed landmark layers for maps with no open tracker data. Positions read from the map images themselves.
def L(x,y,tab,name,detail='',size=2): return [x,y,tab,name,'',detail,size,0]
def D(x,y,tab,name,detail=''): return [x,y,tab,name,'',detail,0,0]
SRC='Hand-placed from the map image'
def run(add):
    # Zelda II labelled world map (user-supplied), tab z2w
    import sys; sys.path.insert(0,'z2'); from z2world import CATS
    for n,kind,its in CATS:
        add('aol','Zelda II · world map',n,'z2w',[D(round(x/900*100,2),round(y/574*100,2),'z2w',nm,dt) for x,y,nm,dt in its],None,kind='dot',src='Hand-placed from the labelled world map you supplied')
    t='aol'; G='Zelda II'
    add('aol',G,'Towns',t,[D(5.2,12.2,t,'Ruto','Town · teaches Jump (per map label)'),D(27.8,25,t,'Rauru','Town (approx.)'),D(9.7,53.9,t,'Saria','Town'),D(37.3,40.5,t,'Mido','Town · Downward Thrust (per map label)'),D(47.9,28.2,t,'Darunia','Town · Upward Thrust'),D(57.9,48.4,t,'Nabooru','Town'),D(63.6,77.8,t,'Kasuto','Town (approx.)')],None,kind='dot',src=SRC)
    add('aol',G,'Dungeons (palaces)',t,[D(15.9,23.7,t,'North Palace','Starting palace, sleeping Zelda'),D(36.1,8.5,t,'Parapa Palace (1)','approx.'),D(9.8,32.7,t,'Midoro Palace (2)','per map label'),D(33.5,58.3,t,'Island Palace (3)','per map label'),D(93.4,26.5,t,'Maze Island Palace (4)'),D(78.1,48.4,t,'Palace on the Sea (5)','per map label'),D(70,79,t,'Three-Eye Rock Palace (6)','hidden under the rock'),D(48.3,58.2,t,'Great Palace (7)','per map label')],None,kind='dot',src=SRC)
    add('aol',G,'Region names',t,[L(20,32,t,'Western Hyrule'),L(58,40,t,'Eastern Hyrule'),L(10,70,t,'Death Mountain'),L(87,9,t,'Maze Island'),L(55,70,t,'Valley of Death'),L(26,55,t,"King's Tomb",'',1),L(20,6,t,'Parapa Desert','',1)],None,kind='label',src=SRC)
    t='ph'; G='Phantom Hourglass'
    add('ph',G,'Golden Frogs (cyclone warps)',t,[D(29.5,13,t,'Golden Frog N','Northwestern Sea'),D(82.5,25,t,'Golden Frog Z','Northeastern Sea'),D(82.5,59,t,'Golden Frog W','Southeastern Sea'),D(6,70,t,'Golden Frog Φ','Southwestern Sea'),D(38.5,79,t,'Golden Frog X','Southwestern Sea'),D(78,83,t,'Golden Frog Ω','Southeastern Sea')],None,kind='dot',src=SRC)
    add('ph',G,'Island names',t,[L(37,65,t,'Mercay Island','Temple of the Ocean King (approx.)'),L(68,23,t,'Isle of Ruins','approx.',1),L(25,25,t,'Northwestern Sea','',3),L(75,8,t,'Northeastern Sea','',3),L(25,55,t,'Southwestern Sea','',3),L(75,55,t,'Southeastern Sea','',3)],None,kind='label',src=SRC)
    t='st'; G='Spirit Tracks'
    add('st',G,'Realm names',t,[L(18,25,t,'Snow Realm','',3),L(25,72,t,'Forest Realm','',3),L(75,10,t,'Fire Realm','',3),L(75,85,t,'Ocean Realm','',3),L(85,45,t,'Sand Realm','',3),L(50,46,t,'Tower of Spirits','',2)],None,kind='label',src=SRC)
    t='tfh'; G='Tri Force Heroes'
    add('tfh',G,'Stages',t,[D(38,80,t,'Woodlands'),D(70,78,t,'Riverside'),D(26,30,t,'Volcano'),D(70,25,t,'Ice Cavern'),D(86,47,t,'Fortress'),D(15,58,t,'Dunes'),D(11,25,t,'Ruins'),D(45,8,t,'Sky Realm'),D(49,52,t,'Hytopia Castle','Hub town')],None,kind='dot',src=SRC)
    t='fs'; G='Four Swords'
    add('fs',G,'Stages',t,[D(30,22,t,'Death Mountain'),D(20,58,t,'Talus Cave'),D(62,62,t,'Sea of Trees'),D(78,24,t,"Vaati's Palace"),D(50,54,t,'Great Fairy / Realm of Memories hub')],None,kind='dot',src=SRC)
    t='fsa'; G='Four Swords Adventures'
    add('fsa',G,'Stages',t,[D(37,33,t,'Tower of Winds','approx.'),D(58,11,t,'Tower of Flames (Death Mountain)','approx.'),D(20,72,t,'Desert of Doubt (pyramid)'),D(46,66,t,'Frozen Hyrule'),D(72,58,t,'Village of the Blue Maiden'),D(77,47,t,'Lake Hylia'),D(15,30,t,'Lost Woods'),D(48,33,t,'Hyrule Castle'),D(81,70,t,'Eastern Temple')],None,kind='dot',src=SRC)
    t='ner'; G="Majora's Mask"
    add('mm',G,'Dungeons',t,[D(56.7,72.2,t,'Woodfall Temple','Southern Swamp'),D(52.2,15,t,'Snowhead Temple','Snowhead'),D(8.3,59,t,'Great Bay Temple','Great Bay'),D(88.9,48.4,t,'Stone Tower Temple','Ikana'),D(51.7,49.2,t,'Clock Town / Clock Tower','Hub, final night on the tower')],None,kind='dot',src=SRC)
    t='eow'; G='Echoes of Wisdom'
    add('eow',G,'Dungeons (approx.)',t,[D(57.5,89,t,'Suthorn Ruins','near Suthorn Forest, approx.'),D(83,33,t,'Jabul Ruins','Jabul Waters, approx.'),D(14,80,t,'Gerudo Sanctum','Gerudo Desert, approx.'),D(14,15,t,'Eldin Temple','Eldin Volcano, approx.'),D(85,80,t,'Faron Temple','Faron Wetlands, approx.'),D(60,18,t,'Lanayru Temple','Holy Mount Lanayru, approx.'),D(47.9,40.1,t,'Hyrule Castle','')],None,kind='dot',src=SRC)
    t='ph'; G='Phantom Hourglass'
    add('ph',G,'Dungeons',t,[D(37,63,t,'Temple of the Ocean King','Mercay Island, approx.')],None,kind='dot',src=SRC)
    t='st'; G='Spirit Tracks'
    add('st',G,'Dungeons',t,[D(49.7,51.5,t,'Tower of Spirits','Central hub dungeon'),D(79,19.6,t,'Fire Temple','Fire Realm'),D(82,52.8,t,'Sand Temple','Sand Realm')],None,kind='dot',src=SRC)

def run_castle(add,OUT=None):
    """Hyrule Castle (BotW) area names from zeldamods/objmap castle.json (GPL-3)."""
    import json,os
    p='ext/objmap/castle.json'
    if not os.path.exists(p): return
    from collections import defaultdict
    G=defaultdict(lambda:[0,0,0,1e9,-1e9,0])
    for f in json.load(open(p))['features']:
        pr=f['properties'];pts=f['geometry']['coordinates'][0]
        a=0;cx=cz=0
        for (x1,z1),(x2,z2) in zip(pts,pts[1:]+pts[:1]):
            c=x1*z2-x2*z1;a+=c;cx+=(x1+x2)*c;cz+=(z1+z2)*c
        a/=2
        if abs(a)<1e-6: continue
        cx/=6*a;cz/=6*a;w=abs(a);g=G[pr['name']]
        g[0]+=cx*w;g[1]+=cz*w;g[2]+=w;g[3]=min(g[3],pr['ymin']);g[4]=max(g[4],pr['ymax']);g[5]+=1
    import re
    norm=lambda t:re.sub(r"princess |'|s\b","",t.lower()).strip()
    have={}
    if OUT:
        for c in OUT.get('botw',[]):
            if c['n']=='Place names':
                for i in c['it']:
                    if 44<=i[0]<=51 and 34<=i[1]<=43: have.setdefault(norm(i[3]),[]).append(i)
    its=[]
    for n,(sx,sz,w,lo,hi,k) in sorted(G.items()):
        X,Z=sx/w,sz/w
        h=f'height {round(lo)}–{round(hi)} m'
        if norm(n) in have:
            for i in have[norm(n)]: i[5]=(i[5]+' · ' if i[5] else '')+'Hyrule Castle · '+h
            continue
        its.append([round((X+5000)/100,3),round((Z+4000)/80,3),'botw',n,'',f'Hyrule Castle · height {round(lo)}–{round(hi)} m',1,0])
    add('botw','BotW · Places','Hyrule Castle rooms','botw',its,None,kind='label',src='zeldamods/objmap castle.json (GPL-3)')
