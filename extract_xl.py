import json,glob,os,shutil,re
ZD='ext/zeldadungeon_maps/public'
AL=json.load(open('/tmp/align.json'))
os.makedirs('site/icons/zd',exist_ok=True)
def icon(game,url):
    if not url: return None
    src=f'{ZD}/{game}/icons/{url}'
    if not os.path.exists(src): return None
    dst=f'{game}_{url}'; shutil.copy(src,'site/icons/zd/'+dst); return dst
def load(game,f):
    return json.load(open(f'{ZD}/{game}/markers/{f}'))
def wl(link): return link.replace(' ','_') if link else ''
OUT={}
def add(gid,group,name,tab,items,ic,kind='icon',src='zd',size=None):
    cats=OUT.setdefault(gid,[])
    key=(group,name)
    for c in cats:
        if (c['g'],c['n'])==key:
            c['it']+=items; return
    cats.append({'g':group,'n':name,'i':ic,'kind':kind,'src':src,'it':items})
def items_from(cat,game,tab,conv,elv=False,defname=None):
    out=[];ic0=None
    for l in cat.get('layers',[]):
        ic=icon(game,l.get('icon',{}).get('url'))
        ic0=ic0 or ic
        z=l.get('minZoom',0)
        for m in l.get('markers',[]):
            c=m['coords']
            if c and isinstance(c[0],list): c=c[0]
            x,y=conv(c)
            if not(-1<=x<=101 and -1<=y<=101): continue
            nm=m.get('name') or defname or cat['name']
            extra=m.get('loc','')
            if elv and 'elv' in m: extra=(extra+' ' if extra else '')+f"{round(c[1])}, {round(c[0])}, {round(m['elv'])}"
            out.append([round(x,2),round(y,2),tab,nm,wl(m.get('link','')),extra,ic if ic!=ic0 else 0,z])
    return out,ic0
# ---------- BotW ----------
bconv=lambda c:((c[1]/2+5000)/100,(4000-c[0]/2)/80)
G={'Sheikah Tower':'Travel','Shrine':'Travel','Tech Lab':'Travel','Stable':'Travel','Village':'Places','Settlement':'Places','Memory':'Places','Great Fairy':'Places','Goddess Statue':'Places',
   'Stone Talus':'Bosses','Hinox':'Bosses','Lynel':'Bosses','Molduga':'Bosses','Guardian':'Bosses','Raft':'Other','Cooking Pot':'Other',
   'Main Quest':'Quests','Shrine Quest':'Quests','Side Quest':'Quests','Quest Objective':'Quests','Inn':'Shops','General Store':'Shops','Armor Shop':'Shops','Dye Shop':'Shops','Jewelry Shop':'Shops'}
for f in ['pins.json','wiki.json']:
    for c in load('botw',f):
        it,ic=items_from(c,'botw','botw',bconv); add('botw','BotW · '+G.get(c['name'],'Other'),c['name'],'botw',it,ic)
for c in load('botw','seeds.json'):
    it,ic=items_from(c,'botw','botw',bconv,defname='Korok seed')
    for r in it: r[5]=c['name']+(' · '+r[5] if r[5] else '')
    add('botw','BotW · Collectibles','Korok seeds','botw',it,ic)
for c in load('botw','treasures.json'):
    it,ic=items_from(c,'botw','botw',bconv)
    for r in it: r[5]=c['name']
    add('botw','BotW · Collectibles','Treasure chests','botw',it,ic)
for c in load('botw','locations.json'):
    it,_=items_from(c,'botw','botw',bconv)
    sz={'Region':3,'Subregion':2}.get(c['name'],1)
    for r in it: r[6]=sz
    add('botw','BotW · Places','Place names','botw',it,None,kind='label')
# ---------- TotK extras ----------
tconv=lambda c:((c[1]+5000)/100,(4000-c[0])/80)
SKIP={'Skyview Tower','Shrine of Light','Lightroot','Korok Seed','Device Dispenser'}
TG={'Chasm':'Places','Cave':'Places','Well':'Places','Dungeon':'Places','Tech Lab':'Places','Stable':'Places','Village':'Places','Great Fairy':'Places','Goddess Statue':'Places','Ascend Point':'Places','Other Travel Gate':'Places','Cherry Tree':'Places',
 'Treasure Chest':'Collectibles','Armor':'Collectibles','Unique Weapon':'Collectibles','Old Map':'Collectibles',"Sage's Will":'Collectibles','Yiga Schematic':'Collectibles','Large Zonaite Deposit':'Collectibles',"Dragon's Tear":'Collectibles','Stone Tablet':'Collectibles','Hudson Sign':'Collectibles',
 'Inn':'Shops','General Store':'Shops','Armor Shop':'Shops','Bargainer Statue':'Shops','Other Shops':'Shops','Cooking Pot':'Other'}
REN={'Armor':'Armor chests','Treasure Chest':'Treasure chests','Unique Weapon':'Unique weapon chests'}
for lay in ['surface','sky','depths']:
    for f in sorted(glob.glob(f'{ZD}/totk/markers/{lay}/*.json')):
        for c in json.load(open(f)):
            if c['name'] in SKIP: continue
            it,ic=items_from(c,'totk',lay,tconv,elv=True)
            if not it: continue
            if c['name']=='Location':
                for r in it: r[6]=2 if r[7]==0 else 1
                add('botw','TotK · Places','Place names (TotK)',lay,it,None,kind='label'); continue
            g=TG.get(c['name'],'Bosses')
            add('botw','TotK · '+g,REN.get(c['name'],c['name']),lay,it,ic)
# ---------- LA ----------
LM=AL['la']['M'];LW,LH=AL['la']['w'],AL['la']['h']
def lconv(c):
    px=c[1]+1640; py=1640-c[0]-720
    return ((LM[0][0]*px+LM[0][1]*py+LM[0][2])/LW*100,(LM[1][0]*px+LM[1][1]*py+LM[1][2])/LH*100)
for c in load('la','pins.json'):
    it,ic=items_from(c,'la','la',lconv)
    if not it: continue
    if c['name']=='Regions':
        for r in it: r[6]=2
        add('la','Link\'s Awakening','Region names','la',it,None,kind='label');continue
    add('la','Link\'s Awakening',c['name'],'la',it,ic)
# ---------- EoW ----------
EM=AL['eow']['M'];EW,EH=AL['eow']['w'],AL['eow']['h']
def econv(c):
    px=(c[1]+636)/1272*7200; py=(636-c[0])/1272*7200
    return ((EM[0][0]*px+EM[0][1]*py+EM[0][2])/EW*100,(EM[1][0]*px+EM[1][1]*py+EM[1][2])/EH*100)
for f in ['labels.json','landmarks.json','items.json']:
    for c in load('eow',f):
        it,ic=items_from(c,'eow','eow',econv)
        if c['name']=='Location':
            for r in it: r[6]=2
            add('eow','Echoes of Wisdom','Place names','eow',it,None,kind='label');continue
        add('eow','Echoes of Wisdom',c['name'],'eow',it,ic)
# ---------- ALttP (easymac tracker, MIT) ----------
pts=json.load(open('/tmp/alttp_pts.json'));grp={}
for lay,n,x,y in pts:
    t='light' if lay=='lightworld' else 'dark'
    base=re.sub(r'\s*\[[^\]]*chest[^\]]*\]','',re.sub(r'^\[cave-[^\]]+\]\s*','',n)).strip()
    k=(t,round(x,2),round(y,2)); g=grp.setdefault(k,[base,0]); g[1]+=1
it=[[x,y,t,(b+(f' ({c} items)' if c>1 else '')),'','',0,0] for (t,x,y),(b,c) in grp.items()]
hp=[r for r in it if re.search('heart',r[3],re.I)]
it=[r for r in it if r not in hp]
add('alttp','A Link to the Past','Item locations','light',it,None,kind='dot',src='alttp')
add('alttp','A Link to the Past','Heart pieces','light',hp,None,kind='dot',src='alttp')
import extract_packs
extract_packs.run(add)
extract_packs.run_ds(add)
import manual_layers
manual_layers.run(add)
manual_layers.run_castle(add,OUT)
import extract_tpdz
extract_tpdz.run(add)
conv,SW,SH=extract_packs.run_remakes(add)
for cat in list(OUT.get('ss',[])):
    if any(r[2]=='ss' for r in cat['it']):
        new=[]
        for r in cat['it']:
            if r[2]!='ss': continue
            x2,y2=conv(r[0]/100*SW,r[1]/100*SH); new.append([round(x2,2),round(y2,2),'sshd']+r[3:])
        cat['it']=cat['it']+new
for g in OUT: OUT[g]=[c for c in OUT[g] if c['it']]
cnt={g:sum(len(c['it']) for c in v) for g,v in OUT.items()}
print(cnt)
for g,v in OUT.items():
    for c in v: print(g,c['g'],'|',c['n'],len(c['it']))
open('xldata.js','w').write('const XL='+json.dumps(OUT,separators=(',',':'),ensure_ascii=False)+';\n')
print(os.path.getsize('xldata.js'))
