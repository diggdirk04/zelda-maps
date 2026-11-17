import json,os
from PIL import Image
c=json.load(open('/tmp/ctx.json'));G=c['GAMES'];M=c['M'];XL=c['XL'];REFS=c['REFS']
TITLE={'loz':'The Legend of Zelda (1986)','aol':'Zelda II: The Adventure of Link','alttp':'A Link to the Past','oot':'Ocarina of Time','la':"Link's Awakening",'mm':"Majora's Mask",'oos':'Oracle of Seasons','ooa':'Oracle of Ages','fs':'Four Swords','ww':'The Wind Waker','fsa':'Four Swords Adventures','mc':'The Minish Cap','tp':'Twilight Princess','ph':'Phantom Hourglass','st':'Spirit Tracks','ss':'Skyward Sword','albw':'A Link Between Worlds','tfh':'Tri Force Heroes','botw':'Breath of the Wild','eow':'Echoes of Wisdom'}
STK={'botw':'Tears','ss':'Skyward','alttp':'Light and Dark','albw':'Between','eow':'Echoes','ooa':'Ages','oos':'Seasons','ww':'Wind Waker','ph':'Phantom'}
stack_titles=[s[0] for s in c['STACKS']]
rows=[];gaps={}
for g in G:
    gid=g['id'];gp=gaps.setdefault(gid,[])
    im=Image.open('site/maps/'+g['img']);W,H=im.size
    V=g.get('v',[]);al=[v for v in V if v[2]]
    mkA={m[0] for m in g['mk']}
    mset=M.get(gid,{});present={k for k,v in mset.items() if not str(v).startswith('A|') or True}
    missing_mk=sorted(set(mset)-mkA); extra_mk=sorted(mkA-set(mset))
    xl=XL.get(gid,[]); xn=sum(len(x['it']) for x in xl)
    lbl=any(x['kind']=='label' for x in xl)
    dung=any('ungeon' in x['n'] or 'Dungeon' in x['g'] for x in xl)
    heart=any(k in x['n'] for x in xl for k in('Heart','heart','Korok','Seashell','Treasure','Might'))
    refsrc=[r for r in REFS if r[0]==TITLE[gid] or (gid=='botw' and False)]
    origin=[r for r in REFS if r[6] and r[6][0]==gid]
    stk=any(STK.get(gid,'@@') in t for t in stack_titles)
    multi=len(V)>0
    rows.append((gid,W,H,len(g['mk']),len(mset),len(V),len(al),len(xl),xn,lbl,dung,len(refsrc),len(origin),stk,bool(g.get('extra'))))
    if max(W,H)<1000: gp.append(f'Low-resolution base map ({W}×{H})')
    if missing_mk: gp.append('Matrix lists areas with no map marker: '+', '.join(missing_mk))
    if extra_mk: gp.append('Map markers not in the matrix: '+', '.join(extra_mk))
    if not xl: gp.append('No extra data layers')
    else:
        if not lbl: gp.append('No place-name layer')
        if not dung: gp.append('No dungeon layer')
        if not heart: gp.append('No collectibles layer (heart pieces, etc.)')
    if not V: gp.append('Only one map image (no tabs)')
    if gid not in('botw',) and len(refsrc)==0: gp.append('No BotW/TotK callbacks listed')
    if refsrc and len(origin)==0: gp.append('Callbacks have no "show on this map" pins')
    if gid in STK and not stk: gp.append('Missing from World layers section')
for gid in ['tp','mm','oot','alttp','fsa']:
    pass
hdr=('game','W','H','areaMk','matrix','tabs','aligned','xlCats','xlItems','names','dungeons','collect','refs','refPins','stack','extras')
print('\t'.join(hdr))
for r in rows: print('\t'.join(str(x) for x in r))
print()
for g,v in gaps.items():
    print(g, '|', ' ; '.join(v))
