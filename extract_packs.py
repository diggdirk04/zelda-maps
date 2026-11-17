import json,sys,re,os
sys.path.insert(0,'/home/claude')
from packparse import parse
from align_lib import align
from PIL import Image
E='ext'; MP='site/maps'
def dims(f): return Image.open(f).size
def affine(M,x,y): return (M[0][0]*x+M[0][1]*y+M[0][2], M[1][0]*x+M[1][1]*y+M[1][2])
def mk_conv(src,dst,minin=50):
    inl,n,M=align(src,dst); W,H=dims(dst); print('align',src.split('/')[-1],'->',dst.split('/')[-1],inl,'/',n)
    assert inl>minin,(src,dst,inl)
    M=M.tolist(); return lambda x,y:(lambda p:(p[0]/W*100,p[1]/H*100))(affine(M,x,y))
def ident(img):  # pack image used directly as a tab: pixel -> percent
    W,H=dims(img); return lambda x,y:(x/W*100,y/H*100)
RULES=[('Gold Skulltulas',r'^GS |Gold Skulltula|Skulltula Token|Spider House'),
       ('Heart pieces',r'Heart Piece|\bHP\b|Piece of Heart|Heart Container'),
       ('Maiamai',r'Maiamai'),('Cracks',r'\bCrack\b'),('Weather vanes',r'Weather Vane'),
       ('Gasha spots',r'Gasha'),('Seed trees',r'Seed Tree'),('Stray fairies',r'Stray Fairy'),
       ('Shops',r'\bShop\b|Store|Merchant|Salesman|Business Scrub|Bazaar'),
       ('Secret seashells & kinstones',r'Kinstone|Seashell|Fusion'),
       ('Great Fairies',r'Great Fairy|Fairy Fountain'),
       ('Dungeons',r'Dungeon|Temple|Palace|\(D\d+\)|Tower of|Labyrinth|Fortress|Cavern\b|Castle$|Ruins$|Shrine$|Lair|Crypt|Maze')]
def classify(o):
    txt=o['name']+' | '+' | '.join(o['secs'])+' | '+' / '.join(o['path'])
    if o['path'] and o['path'][0] in ('Dungeons',) : return 'Dungeons'
    for cat,rx in RULES:
        if cat=='Dungeons':
            if re.search(rx,o['name']) and (len(o['secs'])>=3 or '(D' in o['name']): return cat
            continue
        if re.search(rx,txt,re.I if cat!='Dungeons' else 0): return cat
    return 'Item checks'
def detail(o,extra=''):
    s=[x for x in o['secs'] if x and x!=o['name']]
    area=o['path'][0] if o['path'] and o['path'][0] not in('World','Overworld','Overworld_Past','Root') and not o['path'][0].startswith('_') else ''
    d=(f"{len(s)} checks: " if len(s)>1 else '')+', '.join(s[:12])+('…' if len(s)>12 else '')
    parts=[p for p in (extra,area,d) if p]
    return ' · '.join(parts)
def add_pack(add,gid,group,L,conv,tab,src,extra=lambda o:''):
    buckets={};seen=set()
    for o in L:
        if o.get('x') is None: continue
        if '->' in o['name'] or o['name'].lower().startswith(('child spawn','adult spawn','version mismatch')): continue
        x,y=conv(o['x'],o['y'])
        if not(-1<=x<=101 and -1<=y<=101): continue
        k=(round(x,1),round(y,1),o['name'])
        if k in seen: continue
        seen.add(k)
        buckets.setdefault(classify(o),[]).append([round(x,2),round(y,2),tab,o['name'],'',detail(o,extra(o)),0,0])
    order=['Dungeons','Item checks','Heart pieces','Gold Skulltulas','Stray fairies','Maiamai','Cracks','Weather vanes','Gasha spots','Seed trees','Secret seashells & kinstones','Great Fairies','Shops']
    for cat in sorted(buckets,key=lambda c:order.index(c) if c in order else 99):
        add(gid,group,cat,tab,buckets[cat],None,kind='dot',src=src)
    # region-name labels at the median point of each tracker region
    GEN={'World','Overworld','Overworld_Past','Root','Dungeons','Inside Dungeons','Overworld Markers','Lightworld Markers'}
    reg={}
    for o in L:
        if o.get('x') is None: continue
        r=next((p for p in o['path'][:-1] if p and p not in GEN and not p.startswith('_')),None)
        if not r: continue
        r=re.sub(r' - Entrances$','',r)
        x,y=conv(o['x'],o['y'])
        if -1<=x<=101 and -1<=y<=101: reg.setdefault(r,[]).append((x,y))
    labs=[]
    for r,pts in reg.items():
        if len(pts)<2: continue
        xs=sorted(p[0] for p in pts); ys=sorted(p[1] for p in pts)
        labs.append([round(xs[len(xs)//2],2),round(ys[len(ys)//2],2),tab,r,'','Region (from tracker data)',2,0])
    if labs: add(gid,group,'Region names',tab,labs,None,kind='label',src=src)
def save_tab(src,name,maxw=1800):
    im=Image.open(src).convert('RGBA'); 
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    bg=Image.new('RGB',im.size,(20,20,24)); bg.paste(im,mask=im.split()[3]); bg.save(MP+'/'+name,'WEBP',quality=86); return name
def run_ds(add):
    # Spirit Tracks: tracker world map is a clean copy of our rail map -> align onto it
    pk=E+'/st_ap_tracker'; P=parse(pk); c=mk_conv(pk+'/images/train/all.png',MP+'/st_full.webp',minin=30)
    add_pack(add,'st','Spirit Tracks',[o for o in P if o['map']=='Overview'],c,'st','Spirit Tracks Archipelago tracker (DayKat, carrotinator; MIT)')
    # Phantom Hourglass: sharper copy of the in-game sea chart becomes the sea-chart tab
    pk=E+'/ph_ap_tracker'; P=parse(pk); src=pk+'/images/seamap.png'
    im=Image.open(src).convert('RGB'); im.save(MP+'/ph_sea.webp','WEBP',quality=88)
    c=ident(src)
    add_pack(add,'ph','Phantom Hourglass',[o for o in P if o['map'] in('Sea Overview','Check Overview')],c,'sea','Phantom Hourglass Archipelago tracker (carrotinator; MIT)')
def run(add):
    # LoZ
    pk=E+'/Br00ty_tloz_brooty'; P=parse(pk); c=mk_conv(pk+'/images/maps/overworld.png',MP+'/loz.webp')
    add_pack(add,'loz','The Legend of Zelda',[o for o in P if o['map']=='overworld'],c,'loz','Br00ty/tloz_brooty')
    # OoT (Hamsda) on manual atlas
    pk=E+'/Hamsda_EmoTrackerPacks/ootrando_overworldmap_hamsda'; P=parse(pk)
    c=mk_conv(pk+'/images/map_spawns.png',MP+'/oot_manual_labeled.webp')
    ch={(o['name'],o['x'],o['y']) for o in P if o['map']=='child'}; ad={(o['name'],o['x'],o['y']) for o in P if o['map']=='adult'}
    L=[o for o in P if o['map'] in('child','adult')]
    def age(o):
        k=(o['name'],o['x'],o['y']); return 'Child & Adult' if (k in ch and k in ad) else ('Child' if k in ch else 'Adult')
    for o in L:
        if o['path'] and o['path'][0]!='World' and len(o['secs'])>=3: o['path']=['Dungeons']+o['path']
    add_pack(add,'oot','Ocarina of Time',L,c,'atlas','Hamsda/EmoTrackerPacks',extra=age)
    # Minish Cap
    pk=E+'/CandyCrystal_CandyCrystal_TMCR_Map_Tracker'; P=parse(pk); c=mk_conv(pk+'/images/maps/overworld.png',MP+'/mc_full.webp')
    add_pack(add,'mc','The Minish Cap',[o for o in P if o['map']=='map'],c,'mc','CandyCrystal TMCR tracker (MIT)')
    # Twilight Princess
    pk=E+'/j-imbo_tprando_jim'; P=parse(pk); c=mk_conv(pk+'/images/overworld.png',MP+'/tp_hd.webp')
    L=[o for o in P if o['map']=='overworld']
    for o in L:
        if o['path'][0]!='World': o['path']=['Dungeons']+o['path']
    add_pack(add,'tp','Twilight Princess',L,c,'tp','j-imbo/tprando_jim')
    # Wind Waker (grid)
    pk=E+'/Vrontis_Wind-Waker-Item-and-Map-Tracker'; P=parse(pk); W,H=dims(MP+'/ww_chart.webp')
    cw=lambda x,y:((66+(x-6)/1021*1374)/W*100,(66+(y-8)/1029*1374)/H*100)
    add_pack(add,'ww','The Wind Waker',[o for o in P if o['map'] in('map','Map')],cw,'chart','Vrontis WW map tracker')
    # Skyward Sword (robojumper)
    d=json.load(open(E+'/robo_ss/src/data/mapData.json')); reg=[];ent=[]
    bg=Image.open(MP+'/ss_surface.webp').convert('L');BW,BH=bg.size
    def onmap(r):
        x,y=int(r[0]/100*BW),int(r[1]/100*BH)
        return 0<=x<BW and 0<=y<BH and max(bg.getpixel((min(BW-1,max(0,x+dx)),min(BH-1,max(0,y+dy)))) for dx in(-6,0,6) for dy in(-6,0,6))>25
    for key,img in [('faronSubmap','Faron'),('eldinSubmap','Eldin'),('lanayruSubmap','Lanayru')]:
        src=E+f'/robo_ss/src/assets/maps/{img}.png'; sw,sh=dims(src); cc=mk_conv(src,MP+'/ss_surface.webp')
        for m in d[key]['markers']:
            x,y=cc(m['markerX']/100*sw,m['markerY']/100*sh); reg.append([round(x,2),round(y,2),'ss',m['region'],'',d[key]['name'],0,2])
        for m in d[key].get('entranceMarkers',[]):
            x,y=cc(m['markerX']/100*sw,m['markerY']/100*sh); ent.append([round(x,2),round(y,2),'ss',m['entryName'],'',m['exitPool'].replace('_',' ').title(),0,0])
    add('ss','Skyward Sword','Region names','ss',[r for r in reg if onmap(r)],None,kind='label',src='robojumper SS tracker (GPL-3)')
    add('ss','Skyward Sword','Dungeons & Silent Realms','ss',[r for r in ent if onmap(r)],None,kind='dot',src='robojumper SS tracker (GPL-3)')
    # ALttP entrances
    pk=E+'/StripesOO7_alttp-ap-poptracker-pack'; P=parse(pk)
    for m,img,tab,dst in [('lightworld_er','lttp_lightworld.png','light','alttp_light.webp'),('darkworld_er','lttp_darkworld.png','dark','alttp_dark.webp')]:
        c=mk_conv(pk+'/images/maps/'+img,MP+'/'+dst)
        L=[o for o in P if o['map']==m and not o['path'][0].startswith('Retro')]
        out=[]
        for o in L:
            x,y=c(o['x'],o['y']); out.append([round(x,2),round(y,2),tab,o['name'],'',o['path'][0].replace(' - Entrances',''),0,0])
        add('alttp','A Link to the Past','Entrances (houses, caves, dungeons)',tab,out,None,kind='dot',src='StripesOO7 ALttP pack (MIT)')
        reg={}
        for r in out: reg.setdefault(r[5],[]).append(r)
        labs=[]
        for k,v in reg.items():
            if len(v)<2: continue
            xs=sorted(r[0] for r in v); ys=sorted(r[1] for r in v)
            labs.append([xs[len(xs)//2],ys[len(ys)//2],tab,k,'','Region (from tracker data)',2,0])
        add('alttp','A Link to the Past','Region names',tab,labs,None,kind='label',src='StripesOO7 ALttP pack (MIT)')
    # Oracle of Seasons (OmegaZeron, MIT) — Holodrum on every season tab, Subrosia on its tab
    pk=E+'/OmegaZeron_Oracle-of-Seasons-AP-Poptracker-Pack'; P=parse(pk)
    c=mk_conv(pk+'/images/maps/map_holodrum.png',MP+'/oos_summer.webp')
    add_pack(add,'oos','Oracle of Seasons',[o for o in P if o['map']=='holodrum'],c,'holo','OmegaZeron OoS AP pack (MIT)')
    c=mk_conv(pk+'/images/maps/map_subrosia.png',MP+'/oos_subrosia.webp')
    add_pack(add,'oos','Oracle of Seasons',[o for o in P if o['map']=='subrosia'],c,'sub','OmegaZeron OoS AP pack (MIT)')
    # Oracle of Ages (Dranzior/Br00ty, MIT)
    pk=E+'/Dranzior_ooa_brooty'; P=parse(pk)
    for m,img,tab,dst in [('present','Present.png','present','ooa_present.webp'),('past','Past.png','past','ooa_past.webp')]:
        c=mk_conv(pk+'/images/maps/'+img,MP+'/'+dst)
        add_pack(add,'ooa','Oracle of Ages',[o for o in P if o['map']==m],c,tab,'Dranzior/ooa_brooty (MIT)')
    # A Link Between Worlds (Legendgreat AP pack, GPL-3) — pack maps are 4x our old ones
    pk=E+'/Legendgreat_albw-ap-poptracker'; P=parse(pk)
    for m,tab,dst in [('hyrule','hyrule','albw_hyrule.webp'),('lorule','lorule','albw_lorule.webp')]:
        c=ident(pk+f'/images/maps/{m}.png')
        add_pack(add,'albw','A Link Between Worlds',[o for o in P if o['map']==m],c,tab,'Legendgreat ALBW AP pack (GPL-3)')
    # Majora's Mask (G4M3RL1F3 AP pack, MIT) — its own Termina and Clock Town maps become tabs
    pk=E+'/G4M3RL1F3_Majoras-Mask-AP-PopTracker-Pack'; P=parse(pk)
    c=ident(pk+'/images/maps/termina_nerrel.png')
    add_pack(add,'mm',"Majora's Mask",[o for o in P if o['map']=='overworld'],c,'ner','G4M3RL1F3 MM AP pack (MIT)')
    c=ident(pk+'/images/maps/clock_town.png')
    add_pack(add,'mm',"Majora's Mask",[o for o in P if o['map']=='clock_town'],c,'ct','G4M3RL1F3 MM AP pack (MIT)')
def run_remakes(add):
    # Majora's Mask 3D (GonzaloJMora mm3drTracker, MIT): region markers on the 3DS Termina map
    pk=E+'/GonzaloJMora_mm3drTracker/data'; out=[];names=[]
    for f in sorted(os.listdir(pk)):
        if not f.endswith('.json') or f=='Items.json': continue
        try: d=json.load(open(pk+'/'+f))
        except Exception: continue
        if not isinstance(d,dict): continue
        mc=d.get('map_coordinates')
        if not mc: continue
        ch=[c.get('name','') for c in d.get('item_checks',[])]
        out.append([mc['xPercent'],mc['yPercent'],'mm3d',d.get('region_name',f[:-5]),'',f"{len(ch)} checks: "+', '.join(ch[:12])+('…' if len(ch)>12 else ''),0,0])
    add('mm',"Majora's Mask 3D",'Regions & checks (3DS remake)','mm3d',out,None,kind='dot',src='GonzaloJMora mm3drTracker (MIT)')
    # Skyward Sword HD: copy the Surface layers onto the HD map tab
    c=mk_conv(MP+'/ss_surface.webp',MP+'/ss_hd.webp')
    W,H=dims(MP+'/ss_surface.webp')
    return c,W,H
def images():
    pk=E+'/G4M3RL1F3_Majoras-Mask-AP-PopTracker-Pack/images/maps/'
    save_tab(pk+'termina_nerrel.png','mm_nerrel.webp'); save_tab(pk+'clock_town.png','mm_clocktown.webp',1200)
    pk=E+'/Legendgreat_albw-ap-poptracker/images/maps/'
    save_tab(pk+'hyrule.png','albw_hyrule.webp',2048); save_tab(pk+'lorule.png','albw_lorule.webp',2048)
if __name__=='__main__':
    images()
    im=Image.open(E+'/sshdr/tracker/assets/images/ss-map.png').convert('RGBA');im=im.resize((2400,round(im.height*2400/im.width)),Image.LANCZOS)
    bg=Image.new('RGB',im.size,(20,20,24));bg.paste(im,mask=im.split()[3]);bg.save(MP+'/ss_hd.webp','WEBP',quality=86)
    im=Image.open(E+'/GonzaloJMora_mm3drTracker/images/TerminaMap.png').convert('RGBA')
    bg=Image.new('RGB',im.size,(20,20,24));bg.paste(im,mask=im.split()[3]);bg.save(MP+'/mm3d.webp','WEBP',quality=88)
