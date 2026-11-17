import json,re
b=open('build.py').read()
def seg(gid):
    i=b.index('{"id":"%s"'%gid); j=b.find('\n{"id"',i+5)
    if j<0: j=b.index('\n]',i)
    return i,j
def get(gid):
    i,j=seg(gid); return json.loads(b[i:j].rstrip().rstrip(','))
def put(gid,d):
    global b
    i,j=seg(gid); b=b[:i]+json.dumps(d,separators=(',',':'))+','+b[j:]
def setv(gid,base,vs,drop_extra=()):
    g=get(gid); g['base']=base
    g['v']=vs
    if 'extra' in g:
        g['extra']=[e for e in g['extra'] if e[0] not in drop_extra]
        if not g['extra']: g.pop('extra')
    put(gid,g)
# v entries: [img,label,aligned]
setv('alttp','Light World',[["alttp_dark.webp","Dark World",True]],["alttp_dark.webp"])
setv('albw','Hyrule',[["albw_lorule.webp","Lorule",True]],["albw_lorule.webp"])
setv('oos','Summer',[["oos_spring.webp","Spring",True],["oos_autumn.webp","Autumn",True],["oos_winter.webp","Winter",True]],["oos_spring.webp","oos_autumn.webp","oos_winter.webp"])
setv('ooa','Present',[["ooa_past.webp","Past",True]],["ooa_past.webp"])
setv('botw','Surface',[["totk_sky.webp","Sky (TotK)",True],["totk_depths.webp","Depths (TotK)",True],["botw_parchment.webp","Parchment map",False]],["totk_sky.webp","totk_depths.webp","botw_parchment.webp"])
setv('ss','Surface',[["ss_sky.webp","The Sky",False]],["ss_sky.webp"])
setv('oot','1998 poster',[["oot.webp","2026 remake",False],["oot_manual_labeled.webp","Manual atlas",False]],["oot.webp","oot_manual_labeled.webp"])
setv('tp','In-game map',[["tp_english.webp","English fan map",False],["tp_select.webp","Area select",False]],["tp_english.webp","tp_select.webp"])
setv('mm','Official',[["mm.webp","Fan map (named)",False]],["mm.webp"])
setv('ww','Labelled grid',[["ww.webp","Decorative chart",False]],["ww.webp"])
setv('mc','Full world',[["mc.webp","In-game map",False]],["mc.webp"])
g=get('botw'); g['note']=g['note'].replace(' Both games share this surface map:',' Both games share this surface map. Use the tabs to switch to the sky or the Depths, which line up exactly, or the blend slider to overlay one:') ; put('botw',g)
# JS: replace mapEl
old_start=b.index("function mapEl(g,big){"); old_end=b.index("function openLB(")
new_js=r'''function mapEl(g,big){const wrap=document.createElement('div');
 const V=[[g.img,g.base||'Map',true]].concat(g.v||[]);let cur=0;
 const d=document.createElement('div');d.className='map';
 d.innerHTML=`<img class="baseimg" src="maps/${g.img}" alt="${g.t} map" loading="lazy" width="${g.w}" height="${g.h}"><img class="ovl" alt="" style="opacity:0">`+g.mk.map(m=>`<div class="mk" data-a="${m[0]}" style="left:${m[1]}%;top:${m[2]}%;background:${AREAS[m[0]].c};color:${AREAS[m[0]].c}"><span class="lb">${m[3]}</span></div>`).join('');
 if(!big)d.onclick=e=>{if(e.target.closest('.vctl'))return;openLB(g)};
 wrap.appendChild(d);if(V.length<2)return d;
 const base=d.querySelector('.baseimg'),ovl=d.querySelector('.ovl');
 const ctl=document.createElement('div');ctl.className='vctl';
 const aligned=V.filter(x=>x[2]);
 ctl.innerHTML=`<div class="vtabs">${V.map((x,i)=>`<button data-i="${i}" class="${i?'':'on'}">${x[1]}${x[2]?'':' <span title="Different layout, so markers are hidden">*</span>'}</button>`).join('')}</div>`+
  (aligned.length>1?`<div class="blend"><span>Blend in</span><select>${V.map((x,i)=>x[2]?`<option value="${i}">${x[1]}</option>`:'').join('')}</select><input type="range" min="0" max="100" value="0"><span class="pct">0%</span><button class="peek" title="Hold to show the blended map at full strength">Hold to peek</button></div>`:'');
 const tabs=ctl.querySelectorAll('.vtabs button'),sel=ctl.querySelector('select'),rng=ctl.querySelector('input[type=range]'),pct=ctl.querySelector('.pct');
 function show(i){cur=i;const x=V[i];base.src='maps/'+x[0];tabs.forEach(t=>t.classList.toggle('on',+t.dataset.i===i));d.classList.toggle('nomk',!x[2]);
  if(sel){ctl.querySelector('.blend').style.display=x[2]?'':'none';if(+sel.value===i){const o=[...sel.options].find(o=>+o.value!==i);if(o)sel.value=o.value}setOvl()}}
 function setOvl(){if(!sel)return;ovl.src='maps/'+V[+sel.value][0];const v=V[cur][2]?+rng.value:0;ovl.style.opacity=v/100;pct.textContent=rng.value+'%'}
 tabs.forEach(t=>t.onclick=e=>{e.stopPropagation();show(+t.dataset.i)});
 if(sel){sel.value=aligned.length>1?V.indexOf(aligned[1]):0;sel.onchange=setOvl;rng.oninput=setOvl;
  const pk=ctl.querySelector('.peek');let keep=0;
  const on=e=>{e.preventDefault();keep=rng.value;rng.value=100;setOvl()},off=()=>{rng.value=keep;setOvl()};
  pk.addEventListener('pointerdown',on);pk.addEventListener('pointerup',off);pk.addEventListener('pointerleave',off);
  ctl.querySelectorAll('select,input,button').forEach(el=>el.addEventListener('click',e=>e.stopPropagation()));setOvl()}
 wrap.appendChild(ctl);return wrap}
'''
b=b[:old_start]+new_js+b[old_end:]
css='''.map img.ovl{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;pointer-events:none;transition:opacity .08s}
.map.nomk .mk{display:none}
.vctl{margin-top:8px;display:flex;flex-direction:column;gap:6px}
.vtabs{display:flex;flex-wrap:wrap;gap:5px}
.vtabs button,.peek{background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 10px;font:500 12.5px Inter,sans-serif;cursor:pointer}
.vtabs button.on{background:var(--gold);color:#1a160c;border-color:var(--gold)}
.blend{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mute);flex-wrap:wrap}
.blend input{flex:1;min-width:120px;accent-color:var(--gold)}.blend .pct{width:34px}
.peek{user-select:none;touch-action:none}
'''
b=b.replace("footer{color:var(--mute)",css+"footer{color:var(--mute)")
b=b.replace('<div class="sub">Put any two games side by side.</div>','<div class="sub">Put any two games side by side. Cards with tabs have other versions of the same map. Where versions line up (light and dark worlds, seasons, eras, sky, surface and Depths), use the blend slider or hold "Hold to peek" to see one over the other. Tabs marked * have a different layout, so their markers are hidden.</div>')
open('build.py','w').write(b)
# sky marker fix in layerdata
l=open('layerdata.js').read()
l=l.replace('"w": 1500, "h": 1250','"w": 1500, "h": 1200')
def fy(m):
    a,x,y=m.group(1),m.group(2),float(m.group(3))
    old=125+y*12.5; new=(old-149.5)/12
    return '["%s", %s, %d,'%(a,x,round(new))
i=l.index('"sky_totk"'); j=l.index('"note"',i)
l=l[:i]+re.sub(r'\["(\w+)", (\d+), (\d+),',fy,l[i:j])+l[j:]
open('layerdata.js','w').write(l)
