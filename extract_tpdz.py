import re,os
from PIL import Image
SRC='ext/DarkZant_tp-map'
BUGS={'ant','beetle','butterfly','dayfly','dragonfly','grasshopper','ladybug','mantis','phasmid','pillbug','snail','stagBeetle'}
def cat(v):
    b=v.split('.')[0]
    if b in('chest','smallChest','bossChest'): return 'Chests'
    if b in('poeSoul','nightPoe'): return 'Poe Souls'
    if b in('heartPiece','heartContainer'): return 'Heart pieces & containers'
    if b in('goldenWolf','howlingStone'): return 'Howling Stones & Golden Wolves'
    if b[:-1] in BUGS and b[-1] in 'MF': return 'Golden Bugs'
    if b in('rupeeBoulder','Rupees'): return 'Rupees'
    if b in('skybookChar','skybook'): return 'Sky characters'
    if b=='Portals': return 'Warp portals'
    if b in('randoHint',) or b.endswith('Lock') or b.endswith('BossLock'): return None
    return 'Key items & gifts'
def stitch():
    T=SRC+'/Tiles/4'; xs=[int(x) for x in os.listdir(T)]
    ys={int(f.split('.')[0]) for x in xs for f in os.listdir(f'{T}/{x}')}
    im=Image.new('RGBA',((max(xs)+1)*256,(max(ys)+1)*256),(0,0,0,0))
    for x in xs:
        for f in os.listdir(f'{T}/{x}'): im.paste(Image.open(f'{T}/{x}/{f}').convert('RGBA'),(x*256,int(f.split('.')[0])*256))
    im=im.crop((0,0,round(8515/4),round(9826/4)))
    bg=Image.new('RGB',im.size,(18,22,30)); bg.paste(im,mask=im.split()[3]); bg.save('site/maps/tp_dz.webp','WEBP',quality=86)
    return im
def run(add):
    im=Image.open('site/maps/tp_dz.webp') if os.path.exists('site/maps/tp_dz.webp') else stitch()
    W,H=im.size
    txt=open(SRC+'/Scripts/flagsData.js',encoding='utf-8').read()
    cut=txt.index('// Forest Temple'); hints=txt.index('// Rando Hints')
    parts=re.split(r"\n\s*\[\s*(['\"])",txt)
    out={}
    for m in re.finditer(r"\[\s*(['\"])(.+?)\1\s*,\s*new Flag\(\s*([\w.]+)[^,\[]*?(?:\([^)]*\))?\s*,\s*\[\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\]",txt):
        pos=m.start(); name=m.group(2); var=m.group(3)
        if pos>=cut and not var.startswith('Portals'): continue
        c=cat(var)
        if not c: continue
        x=float(m.group(5))/4/W*100; y=-float(m.group(4))/4/H*100
        if not(0<=x<=100 and 0<=y<=100): continue
        seg=txt[m.end():m.end()+1500]; dm=re.search(r"baseDesc:\s*(['\"])(.+?)(?<!\\)\1",seg,re.S)
        desc=dm.group(2).replace("\\'","'")[:220] if dm else ''
        out.setdefault(c,[]).append([round(x,2),round(y,2),'dz',name,'',desc,0,0])
    order=['Chests','Heart pieces & containers','Poe Souls','Golden Bugs','Howling Stones & Golden Wolves','Sky characters','Rupees','Warp portals','Key items & gifts']
    for c in order:
        if c in out: add('tp','Twilight Princess (DarkZant map)',c,'dz',out[c],None,kind='dot',src='DarkZant tp-map')
    print('tpdz',{c:len(v) for c,v in out.items()})
if __name__=='__main__': stitch()
