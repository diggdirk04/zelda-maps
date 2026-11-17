import json,re
src=open('refs.js').read(); R=json.loads(src[len('const REFS='):].rstrip().rstrip(';'))
# name -> (x,y) in-game coords, note
C={
"Aquame Bridge":(-1128,-956),"Carok Bridge":(-1044,427),"Helmhead Bridge":(396,1154),"Rebonae Bridge":(821,-21),
"Digdogg Suspension Bridge":(-1626,-1888),"Eagus, Horwell and Owlan Bridges":(709,-993),"Faron Woods":(407,-3002),
"Temple of Time":(-859,-2035),"Gorko Lake, Gortram Cliff":(2011,2039),"Horon Lagoon":(4244,-255),"Lake Darman":(2372,3060),
"Oren Bridge":(2912,-65),"Ralis Pond":(2957,254),"Tabahl Woods":(2676,290),"Tarm Point":(4474,-831),"Ulria Grotto":(4120,659),
"Pico Pond":(1247,1232),"Crenel Hills":(492,731),"Mount Nabooru":(-1966,-2059),"Ranch Ruins":(7,-157),
"Rauru Hillside, Rauru Settlement Ruins":(670,1330),"Sahasra Slope":(1374,-1197),"Tuft Mountain":(2520,-3602),
"Goponga Island and Goponga Village Ruins":(1528,-330),"Mabe Village Ruins":(-70,-162),"Zauz Island":(1438,-137),
"Mount Daphnes":(-1315,-623),"Tingel Island":(4706,1306),"Lake Saria":(63,1907),"Mikau Lake, Lulu Lake, Toto Lake":(3471,835),
"Lake Siela":(1600,-1300),
}
O={
"Tal Tal Peak":["la","mount"],"Mabe Village Ruins":["la","kak"],"Martha's Landing":["la","lake"],"Kanalet Ridge":["la","castle"],
"Temple of Time":["oot","tot"],"Ranch Ruins":["oot","ranch"],"Fresh Milk bottle logo":["oot","ranch"],"Lake Saria":["oot","deku"],
"Ruto Mountain, Ruto Lake, Ruto Precipice":["oot","zora"],"Darunia Lake":["oot","goron"],"Mount Nabooru":["oot","gerudo"],
"Mido Swamp":["oot","deku"],"Rauru Hillside, Rauru Settlement Ruins":["oot","tot"],
"Lake Darman":["mm","mount"],"Mikau Lake, Lulu Lake, Toto Lake":["mm","lake"],
"Horon Lagoon":["oos","kak"],"Crenel Hills":["mc","mount"],"Minshi Woods":["mc","woods"],"Pico Pond":["mc","woods"],
"Arbiter's Grounds":["tp","gerudo"],"Faron Woods":["tp","faron"],"Ralis Pond":["tp","zora"],"Rutala Dam":["tp","zora"],
"Pillars of Levia":["sky_ss","snow"],"Thunderhead Isles":["sky_ss","snow"],"Eagus, Horwell and Owlan Bridges":["sky_ss","castle"],
"Sahasra Slope":["alttp","eastern"],"Oren Bridge":["albw","zora"],"Mekar Island, Lake Mekar":["ww","deku"],"Mount Daphnes":["ww","castle"],
"Flowers around the Master Sword pedestal":["alttp","tot"],
}
n1=n2=0
for r in R:
    c=C.get(r[1]); o=O.get(r[1])
    while len(r)<7: r.append(None)
    if c: r[5]=[round((c[0]+5000)/100,1),round((4000-c[1])/80,1)]; n1+=1
    if o: r[6]=o; n2+=1
print(n1,n2,[k for k in C if k not in [r[1] for r in R]],[k for k in O if k not in [r[1] for r in R]])
open('refs.js','w').write('const REFS='+json.dumps(R)+';\n')
b=open('build.py').read()
old_start=b.index("(function(){const kinds=");old_end=b.index("})();",old_start)+5
js=r'''(function(){const kinds=[...new Set(REFS.map(r=>r[4]))].sort();$('#rk').innerHTML+=kinds.map(k=>`<option>${k}</option>`).join('');
const tag=g=>`<span style="font-size:11px;border:1px solid var(--line);border-radius:999px;padding:1px 7px;color:var(--mute);white-space:nowrap">${g}</span>`;
const ALLG=GAMES.concat(SKY);const gname=id=>{const g=ALLG.find(x=>x.id===id);return g?g.t.replace(/ \(.*/,''):id};
function draw(){const q=$('#rq').value.toLowerCase(),gm=$('#rg').value,k=$('#rk').value,pm=$('#rp').checked;
 const rows=REFS.filter(r=>(!q||r.slice(0,5).join(' ').toLowerCase().includes(q))&&(!gm||r[3].includes(gm))&&(!k||r[4]===k)&&(!pm||r[5]||r[6]));
 const by={};rows.forEach(r=>(by[r[0]]=by[r[0]]||[]).push(r));
 $('#refs').innerHTML=Object.entries(by).map(([g,rs])=>`<div class="area" style="border-left-color:var(--gold)"><h3>${g} <span style="color:var(--mute);font-weight:400;font-size:13px">(${rs.length})</span></h3>${rs.map(r=>`<div class="ref"><div style="display:flex;gap:8px;justify-content:space-between;align-items:baseline"><span><b>${r[1]}</b>: ${r[2]}</span><span style="display:flex;gap:4px">${tag(r[4])}${tag(r[3])}</span></div>${r[5]||r[6]?`<div class="refbtns">${r[5]?`<button class="rb" data-i="${REFS.indexOf(r)}" data-m="now">📍 On the BotW/TotK map</button>`:''}${r[6]?`<button class="rb" data-i="${REFS.indexOf(r)}" data-m="then">↩ Original in ${gname(r[6][0])}</button>`:''}</div>`:''}</div>`).join('')}</div>`).join('')||'<p class="sub">No matches.</p>';
 $('#rc').textContent=`${rows.length} callbacks across ${Object.keys(by).length} games`;
 $('#refs').querySelectorAll('.rb').forEach(bt=>bt.onclick=()=>showRef(REFS[+bt.dataset.i],bt.dataset.m))}
['#rq','#rg','#rk','#rp'].forEach(s=>$(s).addEventListener('input',draw));draw();
$('#rall').onclick=()=>{const g=GAMES.find(x=>x.id==='botw');openLB(g);const m=$('#lbinner .map');m.classList.add('nomk');
 REFS.filter(r=>r[5]).forEach(r=>addPin(m,r[5][0],r[5][1],r[1],false));$('#lbcap').textContent=`Every pinned callback place (${REFS.filter(r=>r[5]).length}) on the Breath of the Wild / Tears of the Kingdom map. Hover a pin for its name.`};
function addPin(m,x,y,label,big){const p=document.createElement('div');p.className='pin'+(big?' big':'');p.style.left=x+'%';p.style.top=y+'%';p.innerHTML=`<span>${label}</span>`;m.appendChild(p);return p}
function showRef(r,mode){if(mode==='now'){const g=GAMES.find(x=>x.id==='botw');openLB(g);const m=$('#lbinner .map');m.classList.add('nomk');const p=addPin(m,r[5][0],r[5][1],r[1],true);
  $('#lbcap').textContent=`${r[1]}: named after ${r[2]} (${r[0]}).`;setTimeout(()=>p.scrollIntoView({block:'center',inline:'center',behavior:'smooth'}),60)}
 else{const g=ALLG.find(x=>x.id===r[6][0]);openLB(g);const m=$('#lbinner .map');
  m.querySelectorAll('.mk').forEach(e=>{const hit=e.dataset.a===r[6][1];e.classList.toggle('hot',hit);e.classList.toggle('dim',!hit)});
  const h=m.querySelector('.mk.hot');$('#lbcap').textContent=`${g.t}: ${h?h.querySelector('.lb').textContent:''}, the original of "${r[1]}" in BotW/TotK.`;if(h)setTimeout(()=>h.scrollIntoView({block:'center',inline:'center',behavior:'smooth'}),60)}}
})();'''
b=b[:old_start]+js+b[old_end:]
b=b.replace('<select id="rk"><option value="">All types</option></select>','<select id="rk"><option value="">All types</option></select><label><input type="checkbox" id="rp"> Only with map buttons</label><button id="rall" class="peek">📍 Show all on the map</button>')
css='''.ref{margin:6px 0 9px}.refbtns{display:flex;gap:6px;margin-top:4px;flex-wrap:wrap}
.rb{background:transparent;color:var(--gold);border:1px solid #6b5a2c;border-radius:6px;padding:2px 8px;font:500 12px Inter,sans-serif;cursor:pointer}.rb:hover{background:#3a321f}
.pin{position:absolute;transform:translate(-50%,-50%);width:12px;height:12px;border-radius:50%;background:#ff3b6b;border:2px solid #fff;box-shadow:0 0 0 2px #000a;z-index:3}
.pin span{display:none;position:absolute;left:14px;top:-5px;white-space:nowrap;background:#000d;color:#fff;font-size:11.5px;padding:1px 6px;border-radius:4px}
.pin:hover span,.pin.big span{display:block}.pin.big{width:22px;height:22px;animation:pp 1.2s infinite}.pin.big span{font-size:13px;font-weight:600}
@keyframes pp{0%{box-shadow:0 0 0 0 #ff3b6bcc}70%{box-shadow:0 0 0 18px #ff3b6b00}100%{box-shadow:0 0 0 0 #ff3b6b00}}
'''
b=b.replace("footer{color:var(--mute)",css+"footer{color:var(--mute)")
b=b.replace("Many names are slightly misspelled on purpose, as if worn down by history.","Many names are slightly misspelled on purpose, as if worn down by history. Click 📍 to see a place on the Breath of the Wild / Tears of the Kingdom map, or ↩ to see what it refers to on the older game's map. Pins come from in-game coordinates; where a landmark has none, the pin uses a cave or well named after it.")
open('build.py','w').write(b)
