import sys,os,json,re
sys.path.insert(0,'/home/claude')
from packparse import parse,loadj
from PIL import Image
import glob
E='ext'; OUT='site/maps/dg'; os.makedirs(OUT,exist_ok=True)
def mapdefs(pk):
    md={}
    for f in set(glob.glob(pk+'/**/maps*.json*',recursive=True)+glob.glob(pk+'/maps/*.json*')):
        try: d=loadj(f)
        except Exception: continue
        if isinstance(d,dict): d=d.get('maps',[d])
        for m in d:
            if isinstance(m,dict) and m.get('name') and m.get('img'): md.setdefault(m['name'],m['img'])
    return md
def kind(name,secs):
    t=(name+' '+' '.join(secs)).lower()
    if re.search(r'big key|boss key',t): return 'bkey'
    if re.search(r'heart piece|piece of heart',t): return 'heart'
    if re.search(r'skulltula|\bpoe\b|stray fairy|\bsf\b|maiamai|kinstone|seashell',t): return 'coll'
    if re.search(r'boss|heart container|essence|instrument|triforce|remains|majora|ganon|vaati|yuga|miniboss',t): return 'boss'
    if re.search(r'small key|key chest|keydoor|key drop|\bkey\b',t): return 'key'
    return 'chest'
G={
 'loz':('Br00ty_tloz_brooty','The Legend of Zelda','Br00ty/tloz_brooty',[(f'level{i}',f'Level {i} — {n}','') for i,n in enumerate(['Eagle','Moon','Manji','Snake','Lizard','Dragon','Demon','Lion','Death Mountain'],1)]),
 'mc':('CandyCrystal_CandyCrystal_TMCR_Map_Tracker','The Minish Cap','CandyCrystal TMCR tracker (MIT)',[('dws','Deepwood Shrine',''),('cof','Cave of Flames',''),('fow','Fortress of Winds',''),('tod','Temple of Droplets',''),('rc','Royal Crypt',''),('pow','Palace of Winds',''),('dhc','Dark Hyrule Castle',''),('mines','Trilby Highlands digging caves','')]),
 'oos':('OmegaZeron_Oracle-of-Seasons-AP-Poptracker-Pack','Oracle of Seasons','OmegaZeron OoS AP pack (MIT)',[('heros_cave',"Hero's Cave",''),('gnarled_root_dungeon','D1 Gnarled Root Dungeon',''),('snakes_remains1',"D2 Snake's Remains",'Front'),('snakes_remains2',"D2 Snake's Remains",'Back'),('poison_moths_lair2',"D3 Poison Moth's Lair",'1F'),('poison_moths_lair1',"D3 Poison Moth's Lair",'B1F'),('dancing_dragon_dungeon2','D4 Dancing Dragon Dungeon','1F'),('dancing_dragon_dungeon1','D4 Dancing Dragon Dungeon','2F'),('unicorns_cave',"D5 Unicorn's Cave",''),('ancient_ruins1','D6 Ancient Ruins','1F–2F'),('ancient_ruins2','D6 Ancient Ruins','3F–5F'),('explorers_crypt1',"D7 Explorer's Crypt",'1F–B1F'),('explorers_crypt2',"D7 Explorer's Crypt",'B2F'),('sword_and_shield_maze1','D8 Sword & Shield Dungeon','1F'),('sword_and_shield_maze2','D8 Sword & Shield Dungeon','B1F'),('linked_cave',"Hero's Cave (linked game)",''),('natzu','Natzu region (animal companion)','')]),
 'ooa':('Dranzior_ooa_brooty','Oracle of Ages','Dranzior/ooa_brooty (MIT)',[('d0_1','D0 Maku Path','1F'),('d1_1',"D1 Spirit's Grave",'1F'),('d2_1','D2 Wing Dungeon','1F'),('d2_B1','D2 Wing Dungeon','B1'),('d3_1','D3 Moonlit Grotto','1F'),('d3_B1','D3 Moonlit Grotto','B1'),('d4_1','D4 Skull Dungeon','1F'),('d4_B1','D4 Skull Dungeon','B1'),('d5_1','D5 Crown Dungeon','1F'),('d5_B1','D5 Crown Dungeon','B1'),('d6_Present_1',"D6 Mermaid's Cave",'Present 1F'),('d6_Past_1',"D6 Mermaid's Cave",'Past 1F'),('d6_Past_B1',"D6 Mermaid's Cave",'Past B1'),('d7_1',"D7 Jabu-Jabu's Belly",'1F'),('d7_2',"D7 Jabu-Jabu's Belly",'2F'),('d7_3',"D7 Jabu-Jabu's Belly",'3F'),('d8_1','D8 Ancient Tomb','1F'),('d8_B1','D8 Ancient Tomb','B1'),('d8_B2','D8 Ancient Tomb','B2'),('d8_B3','D8 Ancient Tomb','B3'),('d11_1',"Hero's Cave (linked game)",'1F'),('animal_regions','Nuun Highlands (animal companions)','All three')]),
 'albw':('Legendgreat_albw-ap-poptracker','A Link Between Worlds','Legendgreat ALBW AP pack (GPL-3)',[('eastern','Eastern Palace',''),('gales','House of Gales',''),('hera','Tower of Hera',''),('hyrule_castle','Hyrule Castle',''),('dark','Dark Palace',''),('swamp','Swamp Palace',''),('skull','Skull Woods',''),('thieves',"Thieves' Hideout",''),('ice','Ice Ruins',''),('desert','Desert Palace',''),('turtle','Turtle Rock',''),('lorule_castle','Lorule Castle','')]),
 'mm':('G4M3RL1F3_Majoras-Mask-AP-PopTracker-Pack',"Majora's Mask",'G4M3RL1F3 MM AP pack (MIT)',[('woodfall_temple','Woodfall Temple',''),('snowhead_temple','Snowhead Temple',''),('great_bay_temple','Great Bay Temple',''),('stone_tower_temple','Stone Tower Temple',''),('swamp_spider_house','Swamp Spider House',''),('ocean_spider_house','Oceanside Spider House',''),('pirates_fortress',"Pirates' Fortress",''),('beneath_the_well','Beneath the Well',''),('ikana_castle','Ancient Castle of Ikana',''),('secret_shrine','Secret Shrine',''),('moon','The Moon',''),('woods_of_mystery','Woods of Mystery',''),('zora_hall','Zora Hall','')]),
}

OOTX=[('Deku Tree','Inside the Deku Tree'),('Dodongos Cavern',"Dodongo's Cavern"),('Jabu Jabus Belly',"Jabu-Jabu's Belly"),('Forest Temple','Forest Temple'),('Fire Temple','Fire Temple'),('Water Temple','Water Temple'),('Shadow Temple','Shadow Temple'),('Spirit Temple','Spirit Temple'),('Bottom of the Well','Bottom of the Well'),('Ice Cavern','Ice Cavern'),('Gerudo Training Ground','Gerudo Training Ground'),('Ganons Castle',"Ganon's Castle"),('Ganons Tower',"Ganon's Tower"),
 ('Kokiri Forest','Area · Kokiri Forest'),('Lost Woods','Area · Lost Woods'),('SFM','Area · Sacred Forest Meadow'),('Hyrule Fields','Area · Hyrule Field'),('Market','Area · Market'),('Temple of Time','Area · Temple of Time'),('Hyrule Castle','Area · Hyrule Castle grounds'),('Lon Lon Ranch','Area · Lon Lon Ranch'),('Kakariko Village','Area · Kakariko Village'),('Graveyard','Area · Graveyard'),('Dampe Race',"Area · Dampé's race"),('DMT','Area · Death Mountain Trail'),('DMC','Area · Death Mountain Crater'),('Goron City','Area · Goron City'),('Zora River',"Area · Zora's River"),('Zoras Domain',"Area · Zora's Domain"),('Zoras Fountain',"Area · Zora's Fountain"),('Lake Hylia','Area · Lake Hylia'),('Gerudo Valley','Area · Gerudo Valley'),('Gerudo Fortress',"Area · Gerudo's Fortress"),('Wasteland','Area · Haunted Wasteland'),('Desert Colossus','Area · Desert Colossus')]
G['oot']=('StripesOO7_oot-tracker','Ocarina of Time','StripesOO7 OoT AP pack (MIT)',[(k,n,'') for k,n in OOTX])
G['alttp']=('StripesOO7_alttp-ap-poptracker-pack','A Link to the Past','StripesOO7 ALttP AP pack (MIT); pots and enemy drops left out',[('HC','Hyrule Castle',''),('CE','Hyrule Castle','Sewers escape'),('EP','Eastern Palace',''),('DP','Desert Palace',''),('ToH','Tower of Hera',''),('AT',"Agahnim's Tower",''),('PoD','Palace of Darkness',''),('SP','Swamp Palace',''),('SW','Skull Woods',''),('TT',"Thieves' Town",''),('IP','Ice Palace',''),('MM','Misery Mire',''),('TR','Turtle Rock',''),('GT_Bottom',"Ganon's Tower",'Lower floors'),('GT_Top',"Ganon's Tower",'Upper floors')])
TPD=[('ft','Forest Temple'),('gm','Goron Mines'),('lt','Lakebed Temple'),('ag',"Arbiter's Grounds"),('sr','Snowpeak Ruins'),('tt','Temple of Time'),('cs','City in the Sky'),('pt','Palace of Twilight'),('hc','Hyrule Castle')]
TPA=[('ordon','Ordon'),('fw','Faron Woods'),('sg','Sacred Grove'),('ff','Faron Field'),('kakariko','Kakariko Village'),('kg','Kakariko Gorge'),('ef','Eldin Field'),('dm','Death Mountain'),('hv','Hidden Village'),('lf','Lanayru Field'),('ct','Castle Town'),('sct','South Castle Town'),('bct','Beside Castle Town'),('lh','Lake Hylia'),('zd',"Zora's Domain"),('uzr',"Upper Zora's River"),('sm','Snowpeak Mountain'),('gd','Gerudo Desert')]
G['tp']=('Kizugaya_TPRAP_poptracker','Twilight Princess','Kizugaya TP AP pack (GPL-3)',[(k+'full',n,'All floors') for k,n in TPD]+[(k,'Area · '+n,'') for k,n in TPA])
G['ww']=('Mysteryem_ww-poptracker','The Wind Waker','Mysteryem WW AP pack (MIT)',[('drc','Dragon Roost Cavern',''),('fw','Forbidden Woods',''),('totg','Tower of the Gods',''),('ff','Forsaken Fortress',''),('et','Earth Temple',''),('wt','Wind Temple','')])
G['la']=('Br00ty_lasr_brooty',"Link's Awakening",'Br00ty LAS randomizer pack',[('d1','D1 Tail Cave',''),('d2','D2 Bottle Grotto',''),('d3','D3 Key Cavern',''),('d4',"D4 Angler's Tunnel",''),('d5',"D5 Catfish's Maw",''),('d6','D6 Face Shrine',''),('d7',"D7 Eagle's Tower",''),('d8','D8 Turtle Rock',''),('d0','Color Dungeon','')])
SKIPRX=re.compile(r' - hint$|Pot #\d|\bdoor\b|Enemy|Spawn #\d|Bush #',re.I)
DUNG={};total=0;bytes_=0

# ---- Phantom Hourglass & Spirit Tracks (Archipelago map trackers, MIT) ----
def _natkey(f):
    f=f or ''
    if f in('','Main'): return (0,0)
    if f.startswith('Lobby'): return (1,0)
    m=re.match(r'^(\d+)F',f)
    if m: return (2,int(m.group(1)))
    m=re.match(r'^B(\d+(?:\.\d)?)',f)
    if m: return (3,float(m.group(1)))
    return (4,f)
def _ds_list(pk,groups,skip,areas_rx,houses_rx,caves_rx):
    P=parse(E+'/'+pk); md=mapdefs(E+'/'+pk); used={}
    for o in P: used[o['map']]=used.get(o['map'],0)+1
    names=[n for n in md if used.get(n) and not re.search(skip,n) and os.path.exists(os.path.join(E+'/'+pk,md[n]))]
    out=[];taken=set()
    for disp,rx,strip in groups:
        ms=[n for n in names if re.search(rx,n) and n not in taken]
        fl=[]
        for n in ms:
            taken.add(n);f=re.sub(strip,'',n).strip(' -') if strip else n
            fl.append((n,disp,f or 'Main'))
        fl.sort(key=lambda t:_natkey(t[2]));out+=fl
    rest=[n for n in names if n not in taken]
    for lab,rx in (('Caves & tunnels',caves_rx),('Houses, shops & ships',houses_rx)):
        ms=sorted(n for n in rest if re.search(rx,n));taken.update(ms);rest=[n for n in rest if n not in ms]
        out+=[(n,lab,n) for n in ms]
    areas={}
    for n in rest:
        base=re.sub(r'\s*\((?:NE|NW|SE|SW|North|South|East|West)\)$|\s+(?:NE|NW|SE|SW)$','',n);areas.setdefault(base,[]).append(n)
    for base in sorted(areas):
        for n in sorted(areas[base],key=lambda n:(n!=base,n)):
            out.append((n,'Area · '+base,'Whole area' if n==base else n.replace(base,'').strip(' ()') or n))
    return out
_PHG=[('Temple of the Ocean King',r'^Temple of the Ocean King',r'^Temple of the Ocean King'),('Temple of Fire',r'^Temple of Fire|^Blaaz',r'^Temple of Fire'),('Temple of Wind',r'^Temple of Wind|^Cyclok',r'^Temple of Wind'),
 ('Temple of Courage',r'^Temple of Courage|^Crayk',r'^Temple of Courage'),('Ghost Ship',r'^Ghost Ship|^Cubus',r'^Ghost Ship'),('Temple of Ice',r'^Temple of Ice|^Gleeok',r'^Temple of Ice'),
 ('Goron Temple',r'^Goron Temple|^Dongorongo',r'^Goron Temple'),("Mutoh's Temple",r"^Mutoh's Temple|^Eox",r"^Mutoh's Temple"),('Isle of Ruins temples',r"^Brant's|^Bremeur's|^Doylan's",'')]
G['ph']=('ph_ap_tracker','Phantom Hourglass','Phantom Hourglass Archipelago map tracker by carrotinator and contributors (MIT)',
 _ds_list('ph_ap_tracker',_PHG,r'Overview$',None,r"House|Shop|Workshop|Ship$|Ship |Basement|Chamber|Shrine",r'Cave|Passage|Tunnel'))
_STG=[('Tower of Spirits',r'^Tower of Spirits',r'^Tower of Spirits'),('Tunnel to the Tower',r'^Tunnel to ToS',r'^Tunnel to ToS'),
 ('Forest Temple',r'^Wooded Temple|^Stagnox',r'^Wooded Temple'),('Snow Temple',r'^Blizzard Temple|^Fraaz',r'^Blizzard Temple'),('Ocean Temple',r'^Marine Temple|^Phytops',r'^Marine Temple'),
 ('Fire Temple',r'^Mountain Temple|^Cragma',r'^Mountain Temple'),('Sand Temple',r'^Desert Temple|^Skeldritch',r'^Desert Temple'),('Hyrule Castle',r"^Hyrule Castle|^Zelda's Room",r'^Hyrule Castle'),
 ('Dark Ore Mine',r'^Dark Ore',''),('Lost at Sea',r'^Lost at Sea',r'^Lost at Sea'),('Disorientation',r'^Disorientation',r'^Disorientation'),('Ends of the Earth',r'^Ends of the Earth',r'^Ends of the Earth'),
 ('Boss & mini-boss arenas',r'Arena$',''),('Lokomo sanctuaries',r"(?<!Island )Sanctuary$|Sanctuary$(?<!Island Sanctuary)",'')]
G['st']=('st_ap_tracker','Spirit Tracks','Spirit Tracks Archipelago map tracker by DayKat, carrotinator and contributors (MIT)',
 _ds_list('st_ap_tracker',_STG,r'^Overview$|Realm$|^Cosmic|^Dark Trains|Undersea',None,r"House|Shop|Supermarket|Trailer",r'Cave|Tunnel|Mine'))
for gid,(pk,title,src,lst) in G.items():
    pk=E+'/'+pk; P=parse(pk); md=mapdefs(pk); out=[]
    for key,dn,fl in lst:
        if key not in md: print('nomap',gid,key); continue
        ip=os.path.join(pk,md[key]); im=Image.open(ip); W,H=im.size
        fn=f'{gid}_{key}.webp'.replace(' ','_')
        if gid in('ph','st'): fn=re.sub(r'[^A-Za-z0-9_.-]','',fn)
        im2=im.convert('RGBA'); s=1
        if gid in('ph','st') and max(W,H)<=600: im2=im2.resize((W*3,H*3),Image.NEAREST)
        if max(W,H)>1800: s=1800/max(W,H); im2=im2.resize((round(W*s),round(H*s)),Image.LANCZOS)
        bg=Image.new('RGB',im2.size,(14,14,18)); bg.paste(im2,mask=im2.split()[3])
        import io
        a=io.BytesIO(); bg.save(a,'WEBP',quality=84); b=io.BytesIO(); bg.save(b,'WEBP',lossless=True,method=5)
        open(OUT+'/'+fn,'wb').write(min(a.getvalue(),b.getvalue(),key=len))
        bytes_+=os.path.getsize(OUT+'/'+fn)
        seen=set(); it=[]
        for o in P:
            if o['map']!=key or o.get('x') is None: continue
            try: o['x']=float(o['x']);o['y']=float(o['y'])
            except Exception: continue
            if not str(o['name']).strip(): o['name']=next((p for p in reversed(o.get('path') or []) if str(p).strip()),'Check')
            if SKIPRX.search(o['name']): continue
            k=(o['x'],o['y'],o['name'])
            if k in seen: continue
            seen.add(k)
            secs=[x for x in o['secs'] if x and x!=o['name']]
            secs=[x for x in secs if not x.endswith(o['name']) and x.lower() not in('chest',)] or ([] if not secs or all(x.endswith(o['name']) for x in secs) else secs)
            det=(f'{len(secs)} checks: ' if len(secs)>1 else '')+', '.join(secs[:10])+('…' if len(secs)>10 else '')
            mq=gid=='oot' and o['path'][0].startswith('MQ')
            it.append([round(o['x']/W*100,2),round(o['y']/H*100,2),o['name'],det,kind(o['name'],secs),mq])
        total+=len(it)
        if gid=='oot':
            van=[i[:5] for i in it if not i[5]]; mqi=[i[:5] for i in it if i[5]]
            out.append({'d':dn,'f':fl,'img':'dg/'+fn,'w':bg.width,'h':bg.height,'it':van})
            if mqi: out.append({'d':dn,'f':'Master Quest','img':'dg/'+fn,'w':bg.width,'h':bg.height,'it':mqi})
        else:
            it=[i[:5] for i in it]
            out.append({'d':dn,'f':fl,'img':'dg/'+fn,'w':bg.width,'h':bg.height,'it':it})
    DUNG[gid]={'t':title,'src':src,'m':out}
# ---- extra sources merged as alternate tabs ----
def insert_after(gid,entries):
    m=DUNG[gid]['m']
    for e in entries:
        idx=max([i for i,x in enumerate(m) if x['d']==e['d']],default=None)
        if idx is None: m.append(e)
        else: m.insert(idx+1,e)
import dz_dungeons
insert_after('tp',dz_dungeons.run(OUT))
insert_after('tp',dz_dungeons.run_submaps(OUT))
_mqd={x['d'] for x in DUNG['oot']['m'] if x['f']=='Master Quest'}
for x in DUNG['oot']['m']:
    if not x['f']: x['f']='Original' if x['d'] in _mqd else 'StripesOO7 map'
def norm(t): return re.sub(r'[^a-z]','',t.lower().replace('area · ',''))
disp={norm(n):n for k,n in OOTX}
disp.update({norm(k):n for k,n in OOTX})
disp.update({norm('Death Mountain Crater'):'Area · Death Mountain Crater',norm('Death Mountain Trail'):'Area · Death Mountain Trail',norm('Sacred Forest Meadow'):'Area · Sacred Forest Meadow',norm('Haunted Wasteland'):'Area · Haunted Wasteland',norm('Hyrule Field'):'Area · Hyrule Field',norm("Zora's River"):"Area · Zora's River",norm('Deku Tree'):'Inside the Deku Tree',norm("Ganon's Castle"):"Ganon's Castle",norm("Gerudo Fortress"):"Area · Gerudo's Fortress",norm("Outside Ganon's Castle"):"Area · Outside Ganon's Castle"})
pk=E+'/Brian0255_ship-of-harkinian-ap-tracker'; P=parse(pk); md=mapdefs(pk); extra=[]
for key,img in md.items():
    if key=='Overworld' or norm(key) not in disp: continue
    ip=os.path.join(pk,img)
    if not os.path.exists(ip): continue
    im=Image.open(ip).convert('RGB'); W,H=im.size; fn=f"ootsoh_{re.sub(r'[^A-Za-z]','_',key)}.webp"
    if max(W,H)>1800: im=im.resize((round(W*1800/max(W,H)),round(H*1800/max(W,H))),Image.LANCZOS)
    im.save(OUT+'/'+fn,'WEBP',quality=84)
    it=[];seen=set()
    for o in P:
        if o['map']!=key or o.get('x') is None: continue
        try: x=float(o['x']);y=float(o['y'])
        except Exception: continue
        k=(x,y,o['name'])
        if k in seen or SKIPRX.search(o['name']): continue
        seen.add(k); secs=[t for t in o['secs'] if t and t!=o['name']]
        it.append([round(x/W*100,2),round(y/H*100,2),o['name'],(f'{len(secs)} checks: ' if len(secs)>1 else '')+', '.join(secs[:10]),kind(o['name'],secs),any('MQ' in p for p in o['path'][:1])])
    van=[i[:5] for i in it if not i[5]]; mqi=[i[:5] for i in it if i[5]]
    extra.append({'d':disp[norm(key)],'f':'Peardian map (SoH)','img':'dg/'+fn,'w':im.width,'h':im.height,'it':van})
    if mqi: extra.append({'d':disp[norm(key)],'f':'Master Quest (SoH)','img':'dg/'+fn,'w':im.width,'h':im.height,'it':mqi})
insert_after('oot',extra)
DUNG['tp']['src']+='; alternate floor maps with every obtainable from DarkZant tp-map'
DUNG['oot']['src']+='; alternate maps by Peardian from the Ship of Harkinian AP tracker (MIT)'
# ---- Zelda II palaces (user-supplied guide maps) ----
sys.path.insert(0,'z2'); from z2pts import P as Z2P
import shutil
z2m=[]
for f,n,pts in Z2P:
    im=Image.open('z2/img/'+f+'.webp'); W,H=im.size; fn='aol_'+f+'.webp'; shutil.copy('z2/img/'+f+'.webp',OUT+'/'+fn)
    z2m.append({'d':n,'f':'','img':'dg/'+fn,'w':W,'h':H,'it':[[round(x/W*100,2),round(y/H*100,2),nm,dt,k] for x,y,nm,dt,k in pts]})
# ---- Four Swords Adventures stages (user-supplied guide scans) ----
sys.path.insert(0,'fsa'); from pts import P as FSAP
fsam=[];DET={'Start':('Stage start','coll'),'Boss':('Boss','boss'),'Goal':('Stage goal / exit','boss')}
for f,slug,lvl,stg,pts in FSAP:  # lvl=stage page, stg=version
    im=Image.open(FSAP and ('/mnt/user-data/uploads/'+f) if os.path.exists('/mnt/user-data/uploads/'+f) else 'fsa/img/'+slug+'.webp').convert('RGB')
    os.makedirs('fsa/img',exist_ok=True)
    if not os.path.exists('fsa/img/'+slug+'.webp'): im.save('fsa/img/'+slug+'.webp',quality=(80 if slug.endswith('_rip') else 86),method=4)
    W,H=im.size;fn='fsa_'+slug+'.webp';shutil.copy('fsa/img/'+slug+'.webp',OUT+'/'+fn)
    fsam.append({'d':lvl,'f':stg,'img':'dg/'+fn,'w':W,'h':H,'it':[[round(x/W*100,2),round(y/H*100,2),n,DET[n][0],DET[n][1]] for x,y,n in pts]})
_d={}
for k,v in DUNG.items():
    _d[k]=v
    if k=='ww': _d['fsa']={'t':'Four Swords Adventures','src':'stage maps supplied by you: Nintendo Power guide scans (via Zelda Wiki) with Start, Boss and Goal markers placed from their labels, and full ripped maps by Piranhaplant','m':fsam}
    if k=='loz': _d['aol']={'t':'Zelda II: The Adventure of Link','src':'palace maps supplied by you (Nintendo Power-style guide scans); markers hand-placed from their labels','m':z2m}
DUNG=_d
# ---- ALBW: split multi-floor sheets into one map per floor ----
from albw_floors import F as _AF
from scipy import ndimage as _nd
import numpy as _np
def _fkey(f):
    f=f.rstrip('*');return (1,int(f[1:])) if f.startswith('B') else (0,int(f[:-1]))
_new=[]
for m in DUNG['albw']['m']:
    k=m['img'][3:-5].replace('albw_','',1)
    if k not in _AF: _new.append(m);continue
    p=OUT+'/'+m['img'][3:];im=Image.open(p).convert('RGB');a=_np.asarray(im).astype(int);H,W=a.shape[:2]
    bg=_np.median(_np.array([a[0,0],a[-1,0],a[-1,-1]]),axis=0)
    lab,n=_nd.label(_nd.binary_opening(_np.abs(a-bg).max(axis=2)>30,iterations=2))
    ps=[(sl[1].start,sl[0].start,sl[1].stop,sl[0].stop) for sl in _nd.find_objects(lab) if (sl[0].stop-sl[0].start)*(sl[1].stop-sl[1].start)>=0.02*W*H]
    fl=_AF[k].split()
    if len(ps)!=len(fl): print('albw split skipped',k,len(ps),len(fl));_new.append(m);continue
    parts=[]
    for (x0,y0,x1,y1),f in zip(ps,fl):
        fn=f'albwf_{k}_{f.rstrip("*")}.webp';im.crop((x0,y0,x1,y1)).save(OUT+'/'+fn,quality=88,method=4)
        parts.append({'d':m['d'],'f':f.rstrip('*')+(' (boss)' if f.endswith('*') else ''),'img':'dg/'+fn,'w':x1-x0,'h':y1-y0,'it':[],'_b':(x0,y0,x1,y1),'_k':_fkey(f)})
    for it in m['it']:
        X,Y=it[0]/100*W,it[1]/100*H
        q=min(parts,key=lambda q:0 if q['_b'][0]<=X<q['_b'][2] and q['_b'][1]<=Y<q['_b'][3] else 1e9+min(abs(X-(q['_b'][0]+q['_b'][2])/2),abs(Y-(q['_b'][1]+q['_b'][3])/2)))
        b=q['_b'];q['it'].append([round((X-b[0])/(b[2]-b[0])*100,2),round((Y-b[1])/(b[3]-b[1])*100,2)]+it[2:])
    parts.sort(key=lambda q:q['_k'])
    for q in parts: del q['_b'],q['_k']
    os.remove(p);_new+=parts
DUNG['albw']['m']=_new
# ---- auto-crop: trim large empty margins (uniform background) and remap markers ----
import numpy as _np
def _autocrop(m):
    p=OUT+'/'+m['img'][3:]
    if not os.path.exists(p): return 0
    im=Image.open(p);W,H=im.size;s=min(1,600/max(W,H))
    a=_np.asarray(im.convert('RGB').resize((max(1,int(W*s)),max(1,int(H*s))))).astype(int)
    cs=_np.array([a[0,0],a[0,-1],a[-1,0],a[-1,-1]]);bg=_np.median(cs,axis=0)
    if (_np.abs(cs-bg).max(axis=1)<20).sum()<3: return 0
    mk=_np.abs(a-bg).max(axis=2)>28
    ys,xs=_np.where(mk)
    if len(xs)==0: return 0
    x0,x1,y0,y1=xs.min()/s,(xs.max()+1)/s,ys.min()/s,(ys.max()+1)/s
    # keep markers inside
    for it in m['it']:
        X,Y=it[0]/100*W,it[1]/100*H;x0,x1,y0,y1=min(x0,X),max(x1,X),min(y0,Y),max(y1,Y)
    pad=max(12,0.025*max(x1-x0,y1-y0))
    x0,y0=max(0,int(x0-pad)),max(0,int(y0-pad));x1,y1=min(W,int(x1+pad)),min(H,int(y1+pad))
    if (x1-x0)*(y1-y0)>0.85*W*H: return 0
    import io as _io
    c=im.convert('RGB').crop((x0,y0,x1,y1));A=_io.BytesIO();c.save(A,'WEBP',quality=88,method=4);B=_io.BytesIO();c.save(B,'WEBP',lossless=True,method=4)
    open(p,'wb').write(min(A.getvalue(),B.getvalue(),key=len))
    nw,nh=x1-x0,y1-y0
    for it in m['it']:
        it[0]=round((it[0]/100*W-x0)/nw*100,2);it[1]=round((it[1]/100*H-y0)/nh*100,2)
    m['w'],m['h']=nw,nh
    return 1
_nc=sum(_autocrop(m) for v in DUNG.values() for m in v['m'])
print('autocropped',_nc)
# ---- de-duplicate byte-identical images (identical houses, repeated floors) ----
import hashlib as _hl
_seen={};_drop=0
for v in DUNG.values():
    for m in v['m']:
        p=OUT+'/'+m['img'][3:]
        if not os.path.exists(p): continue
        hh=_hl.md5(open(p,'rb').read()).hexdigest()
        if hh in _seen and _seen[hh]!=m['img']:
            os.remove(p);m['img']=_seen[hh];_drop+=1
        else: _seen.setdefault(hh,m['img'])
print('deduped images',_drop)
open('dungeons.js','w').write('const DUNG='+json.dumps(DUNG,separators=(',',':'),ensure_ascii=False)+';\n')
print('maps',sum(len(v['m']) for v in DUNG.values()),'markers',total,'img MB',round(bytes_/1e6,1),'js KB',os.path.getsize('dungeons.js')//1024)
