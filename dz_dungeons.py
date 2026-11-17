import re,os,json
from PIL import Image
SRC='ext/DarkZant_tp-map'
FL=["B3","B2","B1","1F","2F","3F","4F","5F","6F","7F","8F"]
def match(s,i,o='[',c=']'):
    d=0;j=i
    while True:
        ch=s[j]
        if ch=='/' and s[j+1]=='/':
            j=s.index('\n',j); continue
        if ch in '"\'`':
            q=ch;j+=1
            while s[j]!=q:
                if s[j]=='\\': j+=1
                j+=1
        elif ch==o: d+=1
        elif ch==c:
            d-=1
            if d==0: return j
        j+=1
def flags():
    t=open(SRC+'/Scripts/flagsData.js',encoding='utf-8').read();F={}
    for m in re.finditer(r"\[\s*(['\"])(.+?)\1\s*,\s*new Flag\(\s*([\w.]+)[^\[]*?\[\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\]",t):
        seg=t[m.end():m.end()+1500]; dm=re.search(r"baseDesc:\s*(['\"])(.+?)(?<!\\)\1",seg,re.S)
        F[m.group(2)]=(float(m.group(4)),float(m.group(5)),m.group(3),dm.group(2).replace("\\'","'")[:220] if dm else '')
    return F
def kind(var,name):
    b=var.split('.')[0]
    if b in('bossChest',) or 'BossLock' in b or b in('diababa','fyrus','morpheel','stallord','blizzeta','armogohma','argorok','zant'): return 'boss'
    if 'Lock' in b: return 'key'
    if b in('poeSoul','nightPoe','ooccooPot','ooccoo'): return 'coll'
    if b in('heartPiece','heartContainer'): return 'heart'
    if re.search(r'small key|\bSK\b|key',name,re.I) or b.endswith('SK'): return 'key'
    if re.search(r'big key|\bBK\b',name,re.I): return 'bkey'
    return 'chest'
def run(OUT='site/maps/dg'):
    s=open(SRC+'/Scripts/submaps.js',encoding='utf-8').read();F=flags();res=[]
    for m in re.finditer(r"new Dungeon\(\s*\[[^\]]*\]\s*,\s*\[[^\]]*\]\s*,\s*[^,]+?\s*,\s*(['\"])(.+?)\1\s*,\s*",s):
        name=m.group(2); a=m.end(); b=match(s,a)
        tail=s[b:b+200]; fo=re.search(r"floorOffset:\s*(\d)",tail.split('}),')[0]); fo=int(fo.group(1)) if fo else 3
        body=s[a+1:b]; floors=[];i=0
        while True:
            k=body.find('[',i)
            if k<0: break
            e=match(body,k); floors.append(body[k+1:e]); i=e+1
        d='Dungeons/'+name.replace(' ','_')
        if not os.path.isdir(SRC+'/'+d): continue
        bgp=SRC+'/'+d+'/Background.png'
        for fi,fb in enumerate(floors):
            lab=FL[fi+fo]; p=f'{SRC}/{d}/{lab}.png'
            if not os.path.exists(p): continue
            im=Image.open(p).convert('RGBA'); IW,IH=im.size
            w,h=IW,IH
            if h>1350: w=1350/h*w;h=1350
            if w>2300: h=2300/w*h;w=2300
            cLat,cLng=-4913,4257.5
            items=[]
            for fn in re.findall(r"^\s*(['\"])(.+?)\1\s*,?",fb,re.M):
                f=F.get(fn[1])
                if not f: continue
                la,ln,var,desc=f
                x=(ln-(cLng-w))/(2*w)*100; y=((cLat+h)-la)/(2*h)*100
                if 0<=x<=100 and 0<=y<=100: items.append([round(x,2),round(y,2),fn[1],desc,kind(var,fn[1])])
            base=Image.new('RGBA',im.size,(16,16,20,255))
            if os.path.exists(bgp):
                bg=Image.open(bgp).convert('RGBA').resize(im.size); base.alpha_composite(bg)
            base.alpha_composite(im)
            sc=min(1,1800/max(IW,IH)); out=base.convert('RGB')
            if sc<1: out=out.resize((round(IW*sc),round(IH*sc)),Image.LANCZOS)
            fn=f"tpdz_{name.replace(' ','_').replace(chr(39),'')}_{lab}.webp"; out.save(OUT+'/'+fn,'WEBP',quality=84)
            res.append({'d':name,'f':lab+' (DarkZant)','img':'dg/'+fn,'w':out.width,'h':out.height,'it':items})
    return res
if __name__=='__main__':
    r=run(); print(len(r),sum(len(x['it']) for x in r)); print([(x['d'],x['f'],len(x['it'])) for x in r])

def run_submaps(OUT='site/maps/dg'):
    s=open(SRC+'/Scripts/submaps.js',encoding='utf-8').read();F=flags();res=[]
    for m in re.finditer(r"new (SimpleSubmap|SimpleFlooredSubmap)\(\s*\[\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\]\s*,\s*[^,]+?\s*,\s*(['\"])(.+?)\4\s*,\s*",s):
        typ,plat,plng,name=m.group(1),float(m.group(2)),float(m.group(3)),m.group(5)
        a=m.end()
        if s[a]!='[': continue
        b=match(s,a); body=s[a+1:b]
        tail=s[b:b+120]; fo=re.search(r"floorOffset:\s*(\d)",tail.split(')')[0]); fo=int(fo.group(1)) if fo else 3
        if typ=='SimpleSubmap': floors=[('1F',body,f"{SRC}/Submaps/{name.replace(' ','_')}.png")]
        else:
            floors=[];i=0;fi=0
            while True:
                k=body.find('[',i)
                if k<0: break
                e=match(body,k); lab=FL[fi+fo]
                floors.append((lab,body[k+1:e],f"{SRC}/Submaps/{name.replace(' ','_')}/{fi}.png")); i=e+1; fi+=1
        for lab,fb,p in floors:
            if not os.path.exists(p): continue
            names=[x[1] for x in re.findall(r"^\s*(['\"])(.+?)\1\s*,?",fb,re.M) if x[1] in F]
            if not names: continue
            im=Image.open(p).convert('RGBA'); IW,IH=im.size; w,h=IW,IH
            if h>330: w=330/h*w;h=330
            items=[]
            for n in names:
                la,ln,var,desc=F[n]
                x=(ln-(plng-w))/(2*w)*100; y=((plat+h)-la)/(2*h)*100
                if -2<=x<=102 and -2<=y<=102: items.append([round(min(100,max(0,x)),2),round(min(100,max(0,y)),2),n,desc,kind(var,n)])
            if not items: continue
            base=Image.new('RGBA',im.size,(16,16,20,255)); base.alpha_composite(im); out=base.convert('RGB')
            sc=min(1,1400/max(IW,IH))
            if sc<1: out=out.resize((round(IW*sc),round(IH*sc)),Image.LANCZOS)
            fn=f"tpdzs_{re.sub(r'[^A-Za-z0-9]','_',name)}_{lab}.webp"; out.save(OUT+'/'+fn,'WEBP',quality=84)
            res.append({'d':'Interior · '+name,'f':(lab+' ') if len(floors)>1 else '','img':'dg/'+fn,'w':out.width,'h':out.height,'it':items})
    for r in res: r['f']=r['f'].strip()
    return res
