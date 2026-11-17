
/* PH/ST floor maps ship as one bundle per game; slice images out on demand. */
const DGP={},DGU={};
function dgPack(p){return DGP[p]||(DGP[p]=fetch('maps/dg/_'+p+'pack.webp').then(r=>{if(!r.ok)throw 0;return r.blob()}).catch(()=>null))}
async function dgSrc(img){let p=null;if(typeof DGPACK!=='undefined')for(const k in DGPACK)if(DGPACK[k][img]){p=k;break}const e=location.protocol!=='file:'&&p&&DGPACK[p][img];if(!e)return 'maps/'+img;
 if(DGU[img])return DGU[img];const b=await dgPack(p);if(!b)return 'maps/'+img;return DGU[img]=URL.createObjectURL(b.slice(e[0],e[0]+e[1],'image/webp'))}
// ================= game pages =================
const DGK={chest:['Chest / item','#ffd34f'],key:['Small key','#4fd1ff'],bkey:['Big / boss key','#ff8a4f'],boss:['Boss / reward','#ff4f6a'],heart:['Heart piece','#ff7fd0'],coll:['Collectible','#7dff6b']};
const ZS={get(k,d){try{const v=localStorage.getItem('zm:'+k);return v==null?d:JSON.parse(v)}catch(e){return d}},
 set(k,v){try{localStorage.setItem('zm:'+k,JSON.stringify(v))}catch(e){}},
 keys(){try{return Object.keys(localStorage).filter(k=>k.startsWith('zm:'))}catch(e){return []}}};
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function zhash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return (h>>>0).toString(36)}
const clampP=v=>Math.max(0,Math.min(100,v));const inB=r=>r[0]>=-3&&r[0]<=103&&r[1]>=-3&&r[1]<=103;
if(typeof DUNG!=='undefined')Object.values(DUNG).forEach(D=>D.m.forEach(m=>{m.it=m.it.filter(inB);m.it.forEach(r=>{r[0]=clampP(r[0]);r[1]=clampP(r[1])})}));
if(typeof XL!=='undefined')Object.values(XL).forEach(cs=>cs.forEach(c=>{c.it=c.it.filter(inB);c.it.forEach(r=>{r[0]=clampP(r[0]);r[1]=clampP(r[1])})}));
const gTitle=g=>g.t.replace(/ \(.*/,'');
const hasDG=id=>typeof DUNG!=='undefined'&&!!DUNG[id];

// ---------- zoom/pan viewer ----------
function Viewer(host,opt){
 opt=opt||{};host.classList.add('gv');
 host.innerHTML='<div class="gvin"><img class="gvimg" alt=""><div class="gvhd"></div><img class="gvovl" alt=""><div class="gvhd gvhdo"></div><div class="gvmk"></div></div><div class="gvz"><button data-z="1" title="Zoom in (+)">+</button><button data-z="-1" title="Zoom out (−)">−</button><button data-z="0" title="Reset view (0)">⟲</button>'+(opt.full?'<button data-z="f" title="Fullscreen (F)">⛶</button>':'')+'</div><div class="gvcoord"></div><div class="gvmini"><img alt=""><i></i></div><div class="gvpop"></div><div class="gvtoast"></div>';
 const inn=host.querySelector('.gvin'),img=host.querySelector('.gvimg'),ovl=host.querySelector('.gvovl'),mk=host.querySelector('.gvmk'),coord=host.querySelector('.gvcoord'),pop=host.querySelector('.gvpop');
 const mini=host.querySelector('.gvmini'),mimg=mini.querySelector('img'),mrect=mini.querySelector('i');
 const V={host,inn,mk,pop,ovl,raf:0,goal:null,s:1,tx:0,ty:0,iw:1,ih:1,W:1,H:1,ox:0,oy:0,moved:false,onzoom:null,onclickmap:null};
 const maxZ=()=>Math.max(6,Math.min(16,2*V.iw/V.W));
 V.layout=function(){const cw=host.clientWidth||1,ch=host.clientHeight||1;const f=Math.min(cw/V.iw,ch/V.ih);V.W=V.iw*f;V.H=V.ih*f;V.ox=(cw-V.W)/2;V.oy=(ch-V.H)/2;inn.style.width=V.W+'px';inn.style.height=V.H+'px';V.apply()};
 V.clamp=function(){const cw=host.clientWidth,ch=host.clientHeight,w=V.W*V.s,h=V.H*V.s;
  if(V.s<=1){V.tx=0;V.ty=0;return}
  V.tx=Math.max(Math.min(V.tx,cw*0.5-V.ox),cw*0.5-V.ox-w);V.ty=Math.max(Math.min(V.ty,ch*0.5-V.oy),ch*0.5-V.oy-h)};
 V.apply=function(){V.clamp();inn.style.transform=`translate(${V.ox+V.tx}px,${V.oy+V.ty}px) scale(${V.s})`;
  // Marker/label counter-scaling (--s) is costly on phones: while a zoom is in progress update it at most every 150 ms
  // and let the GPU scale the whole layer; settle it exactly once the zoom stops.
  if(V.s!==V._cs){const now=performance.now();host.classList.add('zooming');
   if(V._cs===undefined||now-(V._ct||0)>100){inn.style.setProperty('--s',V.s);V._cs=V.s;V._ct=now}
   clearTimeout(V._zt);V._zt=setTimeout(()=>{host.classList.add('settle');inn.style.setProperty('--s',V.s);V._cs=V.s;V._ct=performance.now();host.classList.remove('zooming');clearTimeout(V._st);V._st=setTimeout(()=>host.classList.remove('settle'),200)},110)}
  const zl=V.s>=2.2?3:V.s>=1.6?2:1;if(host.dataset.zl!=String(zl)){host.dataset.zl=zl}V.onzoom&&V.onzoom(V.s);V.onlbl&&V.onlbl();V.onhd&&V.onhd();V.miniDraw()};
 V.miniDraw=function(){const on=V.s>1.25&&V.iw>1;mini.classList.toggle('on',on);if(!on)return;const mw=Math.min(150,150*V.iw/V.ih),mh=mw*V.ih/V.iw;mini.style.width=mw+'px';mini.style.height=mh+'px';
  const cw=host.clientWidth,ch=host.clientHeight,fx=X=>(X-V.ox-V.tx)/V.s/V.W,fy=Y=>(Y-V.oy-V.ty)/V.s/V.H;
  const l=Math.max(0,fx(0)),r=Math.min(1,fx(cw)),t=Math.max(0,fy(0)),b=Math.min(1,fy(ch));mrect.style.left=l*mw+'px';mrect.style.top=t*mh+'px';mrect.style.width=Math.max(4,(r-l)*mw)+'px';mrect.style.height=Math.max(4,(b-t)*mh)+'px'};
 V.stop=function(){if(V.raf){cancelAnimationFrame(V.raf);V.raf=0}V.goal=null};
 const ease=t=>1-Math.pow(1-t,3);
 V.tween=function(ns,A,ntx,nty,dur){V.stop();const s0=V.s,tx0=V.tx,ty0=V.ty,t0=performance.now();dur=dur||240;V.goal={s:ns};
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)dur=1;
  const step=now=>{const t=Math.min(1,(now-t0)/dur),e=ease(t);const sc=Math.exp(Math.log(s0)+(Math.log(ns)-Math.log(s0))*e);
   if(A){V.tx=A.x-(A.x-tx0)*sc/s0;V.ty=A.y-(A.y-ty0)*sc/s0}else{V.tx=tx0+(ntx-tx0)*e;V.ty=ty0+(nty-ty0)*e}
   V.s=sc;V.apply();if(t<1)V.raf=requestAnimationFrame(step);else{V.raf=0;V.goal=null}};V.raf=requestAnimationFrame(step)};
 V.zoomAt=function(f,cx,cy,anim,dur){const r=host.getBoundingClientRect();const X=cx-r.left,Y=cy-r.top;
  if(anim){const base=V.goal?V.goal.s:V.s;const ns=Math.min(maxZ(),Math.max(1,base*f));if(ns===V.s&&!V.raf)return;V.tween(ns,{x:X-V.ox,y:Y-V.oy},0,0,dur||220);return}
  const ns=Math.min(maxZ(),Math.max(1,V.s*f));V.tx=(X-V.ox)-(X-V.ox-V.tx)*ns/V.s;V.ty=(Y-V.oy)-(Y-V.oy-V.ty)*ns/V.s;V.s=ns;V.apply()};
 V.zoomBy=function(f,instant){const r=host.getBoundingClientRect();V.zoomAt(f,r.left+r.width/2,r.top+r.height/2,!instant)};
 V.reset=function(){V.tween(1,null,0,0,260)};
 V.focus=function(xp,yp,z,instant){const cw=host.clientWidth,ch=host.clientHeight;const ns=Math.min(maxZ(),Math.max(V.s,z||3));const tx=cw/2-V.ox-xp/100*V.W*ns,ty=ch/2-V.oy-yp/100*V.H*ns;
  if(instant){V.stop();V.s=ns;V.tx=tx;V.ty=ty;V.apply();return}const d=Math.hypot(tx-V.tx,ty-V.ty);V.tween(ns,null,tx,ty,Math.min(520,260+d/6))};
 V.setImg=function(src,w,h,keep){return new Promise(res=>{const done=()=>{V.iw=img.naturalWidth||w||1000;V.ih=img.naturalHeight||h||1000;if(!keep){V.stop();V.s=1;V.tx=V.ty=0}V.layout();res()};mimg.src=src;
  if(w&&h){V.iw=w;V.ih=h;if(!keep){V.s=1;V.tx=V.ty=0}V.layout()}
  img.onload=done;img.onerror=()=>res();img.src=src;if(img.complete&&img.naturalWidth)done()})};
 V.toPct=function(cx,cy){const r=inn.getBoundingClientRect();return [(cx-r.left)/r.width*100,(cy-r.top)/r.height*100]};
 // pointers
 const P=new Map();let start=null,pinch=null;
 let hist=[],lp=0;
 const miniGo=e=>{const r=mini.getBoundingClientRect();V.focus(Math.max(0,Math.min(100,(e.clientX-r.left)/r.width*100)),Math.max(0,Math.min(100,(e.clientY-r.top)/r.height*100)),V.s)};
 mini.addEventListener('pointerdown',e=>{e.stopPropagation();e.preventDefault();miniGo(e);mini.setPointerCapture(e.pointerId);mini._d=1});
 mini.addEventListener('pointermove',e=>{if(mini._d){const r=mini.getBoundingClientRect();V.focus(Math.max(0,Math.min(100,(e.clientX-r.left)/r.width*100)),Math.max(0,Math.min(100,(e.clientY-r.top)/r.height*100)),V.s,true)}});
 mini.addEventListener('pointerup',()=>mini._d=0);mini.addEventListener('click',e=>e.stopPropagation());
 host.addEventListener('pointerdown',e=>{if(e.target.closest('.gvz,.gvpop,.gvmini,.gvtoast'))return;V.stop();P.set(e.pointerId,{x:e.clientX,y:e.clientY});V.moved=false;hist=[{t:performance.now(),x:e.clientX,y:e.clientY}];
  clearTimeout(lp);const gm=e.target.closest('.gm');if(gm&&!gm.classList.contains('note')&&e.pointerType!=='mouse'&&P.size===1)lp=setTimeout(()=>{if(V.moved)return;V.moved=true;navigator.vibrate&&navigator.vibrate(12);V.onlong&&V.onlong(gm.dataset.u)},480);
  if(P.size===1)start={x:e.clientX,y:e.clientY,tx:V.tx,ty:V.ty};
  if(P.size===2){const [a,b]=[...P.values()];pinch={d:Math.hypot(a.x-b.x,a.y-b.y),s:V.s};P.forEach((_,id)=>{try{host.setPointerCapture(id)}catch(_){}})}});
 host.addEventListener('pointermove',e=>{const r=host.getBoundingClientRect();
  if(!P.has(e.pointerId)){if(e.pointerType==='mouse'){const p=V.toPct(e.clientX,e.clientY);coord.textContent=p[0]>=0&&p[0]<=100&&p[1]>=0&&p[1]<=100?`${p[0].toFixed(1)}, ${p[1].toFixed(1)}`:''}return}
  P.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(P.size===2&&pinch){const [a,b]=[...P.values()];const d=Math.hypot(a.x-b.x,a.y-b.y);const f=pinch.s*d/pinch.d/V.s;V.zoomAt(f,(a.x+b.x)/2,(a.y+b.y)/2);V.moved=true;return}
  if(start&&P.size===1){const dx=e.clientX-start.x,dy=e.clientY-start.y;if(Math.abs(dx)+Math.abs(dy)>5){if(!V.moved){try{host.setPointerCapture(e.pointerId)}catch(_){}}V.moved=true;host.classList.add('dragging')}
   if(V.moved){clearTimeout(lp);const now=performance.now();hist.push({t:now,x:e.clientX,y:e.clientY});while(hist.length>2&&now-hist[0].t>90)hist.shift()}
   if(V.moved&&V.s>1){V.tx=start.tx+dx;V.ty=start.ty+dy;V.apply()}}});
 const fling=()=>{if(hist.length<2||V.s<=1)return;const a=hist[0],b=hist[hist.length-1],dt=b.t-a.t;if(dt<=0||performance.now()-b.t>60)return;let vx=(b.x-a.x)/dt,vy=(b.y-a.y)/dt;if(Math.hypot(vx,vy)<0.25)return;
  let last=performance.now();const step=now=>{const d=now-last;last=now;V.tx+=vx*d;V.ty+=vy*d;const k=Math.exp(-d/280);vx*=k;vy*=k;V.apply();if(Math.hypot(vx,vy)>0.02)V.raf=requestAnimationFrame(step);else V.raf=0};V.stop();V.raf=requestAnimationFrame(step)};
 const up=e=>{clearTimeout(lp);const wasDrag=V.moved&&P.size===1&&!pinch;P.delete(e.pointerId);host.classList.remove('dragging');if(wasDrag&&e.type==='pointerup')fling();if(P.size<2)pinch=null;if(P.size===1){const p=[...P.values()][0];start={x:p.x,y:p.y,tx:V.tx,ty:V.ty}}else start=null};
 host.addEventListener('pointerup',up);host.addEventListener('pointercancel',up);
 host.addEventListener('pointerleave',()=>coord.textContent='');
 host.addEventListener('wheel',e=>{e.preventDefault();const dy=e.deltaY*(e.deltaMode?33:1);const f=Math.pow(1.0022,-dy);if(Math.abs(dy)<40&&!e.deltaMode)V.zoomAt(f,e.clientX,e.clientY);else V.zoomAt(f,e.clientX,e.clientY,true,160)},{passive:false});
 host.addEventListener('dblclick',e=>{if(e.target.closest('.gvz,.gvpop,.gm,.gvmini'))return;V.zoomAt(e.shiftKey?0.5:2,e.clientX,e.clientY,true,260)});
 host.addEventListener('click',e=>{if(V.moved||e.target.closest('.gvz,.gvpop,.gm,.gvmini,.gvtoast'))return;V.onclickmap&&V.onclickmap(e)});
 host.querySelectorAll('.gvz button').forEach(b=>b.onclick=e=>{e.stopPropagation();const z=b.dataset.z;if(z==='f')gpFull();else if(z==='0')V.reset();else V.zoomBy(z==='1'?1.5:1/1.5)});
 new ResizeObserver(()=>V.layout()).observe(host);
 V.toast=function(msg,undo,label){const t=host.querySelector('.gvtoast');t.innerHTML=esc(msg)+(undo?` <button>${esc(label||'Undo')}</button>`:'');t.classList.add('on');clearTimeout(V._tt);V._tt=setTimeout(()=>t.classList.remove('on'),4000);
  const b=t.querySelector('button');if(b)b.onclick=e=>{e.stopPropagation();t.classList.remove('on');undo()}};
 V.popup=function(html){pop.innerHTML='<button class="x" title="Close (Esc)">×</button>'+html;pop.classList.add('open');pop.querySelector('.x').onclick=e=>{e.stopPropagation();V.close()}};
 V.close=function(){pop.classList.remove('open');mk.querySelectorAll('.gm.sel').forEach(x=>x.classList.remove('sel'));V.onclose&&V.onclose()};
 return V}
function gpMax(on){const gp=document.getElementById('gp');gp.classList.toggle('gpmax',on);setTimeout(()=>GP.V&&GP.V.layout(),30);if(on&&GP.V)GP.V.toast('Map only. Press Back, Esc or ⛶ to return.')}
function gpFull(){const el=document.getElementById('gp');if(el.classList.contains('gpmax')){gpMax(false);return}
 if(document.fullscreenElement){document.exitFullscreen().catch(()=>{});return}
 const native=typeof ZD!=='undefined'&&ZD.native;const rf=el.requestFullscreen||el.webkitRequestFullscreen;
 if(native||!rf||!document.fullscreenEnabled){gpMax(true);return}
 try{const p=rf.call(el);if(p&&p.catch)p.catch(()=>gpMax(true))}catch(e){gpMax(true)}}
window.zdBack=function(){const m=document.querySelector('.gpmodal.open');if(m){m.classList.remove('open');return true}
 const sr=document.querySelector('.gpres.open');if(sr){sr.classList.remove('open');document.activeElement&&document.activeElement.blur();return true}
 if(document.activeElement&&document.activeElement.matches('input[type=search],textarea')){document.activeElement.blur();return true}
 if(GP.notemode){gpNoteMode();return true}
 if(GP.V&&GP.V.pop.classList.contains('open')){GP.V.close();return true}
 const gp=document.getElementById('gp');if(gp&&gp.classList.contains('gpmax')){gpMax(false);return true}
 if(typeof lbClose==='function'&&lbClose())return true;
 return false};

// ---------- per-game data model ----------
const GPC={};// cache
function gpModel(g){if(GPC[g.id])return GPC[g.id];
 const tabs=[[g.img,g.base||'Map',true,g.bl]].concat(g.v||[]).map((v,i)=>({img:v[0],n:v[1],al:!!v[2],k:v[3]||('t'+i),i,fo:v[4]||null,hid:!!v[5]}));
 const cats=[];
 if(g.mk&&g.mk.length)cats.push({id:'A',g:'Series',n:'Recurring areas',kind:'area',chk:false,it:g.mk.map(m=>({x:m[1],y:m[2],tab:'*al',name:m[3],det:'Recurring area: '+AREAS[m[0]].n,col:AREAS[m[0]].c,area:m[0]}))});
 if(g.layers&&typeof TOTK!=='undefined')LYR.forEach(l=>{const it=[];TOTK[l[0]].forEach(r=>{const lay=(l[0]==='tower'||l[0]==='shop')?'surface':r[4];const [x,y]=lyrPos(r[1],r[2]);if(x<0||x>100||y<0||y>100)return;
   it.push({x,y,tab:lay,name:l[0]==='korok'?'Korok seed':l[0]==='disp'?'Device Dispenser':r[0],det:lyrInfo(l[0],r).replace(/^<b>[^<]*<\/b>(<br>)?/,''),icon:'icons/'+lyrIcon(l[0],r)+'.png',html:1})});
  cats.push({id:'T'+l[0],g:'TotK · Alshival layers',n:l[1],kind:'icon',icon:'icons/'+l[2]+'.png',chk:true,it})});
 const dd=(c,its)=>{if(c.kind!=='label')return its;const seen=[];return its.filter(r=>{if(seen.some(q=>q[2]===r[2]&&q[3]===r[3]&&Math.abs(q[0]-r[0])<1.5&&Math.abs(q[1]-r[1])<1.5))return false;seen.push(r);return true})};
 (XL[g.id]||[]).forEach((c,ci)=>cats.push({id:'X'+ci,g:c.g,n:c.n,kind:c.kind==='label'?'label':(c.kind==='dot'||!c.i)?'dot':'icon',icon:c.i?'icons/zd/'+c.i:null,col:DOTC[ci%DOTC.length],chk:c.kind!=='label',src:c.src,
  it:dd(c,c.it).map(r=>({x:r[0],y:r[1],tab:r[2],name:r[3],wiki:r[4],det:r[5],icon:c.kind==='label'?null:(r[6]&&typeof r[6]==='string'?'icons/zd/'+r[6]:c.i?'icons/zd/'+c.i:null),sz:c.kind==='label'?(r[6]||1):0,mz:c.kind==='label'?(+r[7]||0):0}))}));
 cats.forEach(c=>{const seen=new Set();c.it=c.it.filter(r=>{if(!r.name||!String(r.name).trim())r.name=r.det&&String(r.det).length<60&&!r.html?String(r.det):c.n;const k=r.name+'|'+r.tab+'|'+Math.round(r.x*5)+','+Math.round(r.y*5)+'|'+(r.html?'':r.det||'');if(seen.has(k))return false;seen.add(k);return true})});
 cats.forEach(c=>c.it.forEach((r,i)=>{r.c=c;r.i=i;r.u=zhash(c.n+'|'+r.name+'|'+r.tab+'|'+(+r.x).toFixed(1)+','+(+r.y).toFixed(1))}));
 const _us=new Set();cats.forEach(c=>c.it.forEach(r=>{let u=r.u,n=1;while(_us.has(u))u=r.u+'_'+(n++);r.u=u;_us.add(u)}));
 const groups=[...new Set(cats.map(c=>c.g))];
 return GPC[g.id]={tabs,cats,groups}}
const onTab=(r,t)=>r.tab===t.k||(r.tab==='*al'&&t.al);
const DGI={};function dgItems(gid){if(DGI[gid])return DGI[gid];const D=DUNG[gid];const us=new Set();return DGI[gid]=D.m.map((m,mi)=>m.it.map((r,i)=>{let u=zhash('d|'+m.img+'|'+r[2]+'|'+r[0]+','+r[1]),k=u,n=1;while(us.has(k))k=u+'_'+(n++);us.add(k);return {x:r[0],y:r[1],name:r[2],det:r[3],kind:r[4],mi,i,u:k}}))}

// ---------- state ----------
const GP={spoil:false,rev:new Set(),grp:'cat',g:null,mode:'o',tab:0,dm:0,V:null,done:new Set(),on:new Set(),hide:false,lbl:true,ms:1,kinds:new Set(),notemode:false,sel:null};
function gpSaveDone(){ZS.set('done:'+GP.g.id,[...GP.done]);typeof zdState==='function'&&zdState()}
function gpPref(){ZS.set('pref:'+GP.g.id,{on:[...GP.on],hide:GP.hide,lbl:GP.lbl,ms:GP.ms,tab:GP.tab,dm:GP.dm,kinds:[...GP.kinds],spoil:GP.spoil,rev:[...GP.rev],grp:GP.grp});typeof zdState==='function'&&zdState()}
function gpNotes(key){return ZS.get('notes:'+GP.g.id+':'+key,[])}
function gpSetNotes(key,a){ZS.set('notes:'+GP.g.id+':'+key,a)}

function gpEnsure(){if(document.getElementById('gp'))return;
 const d=document.createElement('div');d.id='gp';d.innerHTML=`<div class="gpbar"><a class="gpback" href="#/">← All maps</a><h2></h2><span class="yr"></span>
 <select class="gpsel" title="Switch game"></select><div class="gpmodes"></div><div class="gpsp"></div>
 <div class="gpsearch"><input type="search" placeholder="Search this game… ( / )" autocomplete="off"><div class="gpres"></div></div>
 <button class="gpbtn gpside-t" title="Hide or show the side panel">☰</button><button class="gpbtn gphelp" title="Keyboard shortcuts (?)">?</button></div>
 <div class="gpbody"><div class="gv" id="gpv"></div><div class="gpside"></div></div>
 <div class="gpmodal"><div></div></div>`;
 document.body.appendChild(d);
 const sel=d.querySelector('.gpsel');sel.innerHTML=GAMES.slice().sort((a,b)=>a.y-b.y).map(g=>`<option value="${g.id}">${g.y} · ${esc(gTitle(g))}</option>`).join('');sel.setAttribute('aria-label','Switch game');
 sel.onchange=()=>{location.hash='#/g/'+sel.value};
 d.querySelector('.gpside-t').onclick=()=>{d.querySelector('.gpbody').classList.toggle('full');GP.V&&GP.V.layout()};
 d.querySelector('.gphelp').onclick=gpHelp;
 d.querySelector('.gpmodal').onclick=e=>{if(e.target.classList.contains('gpmodal'))e.target.classList.remove('open')};
 GP.V=Viewer(d.querySelector('#gpv'),{full:true});
 GP.V.onclickmap=gpMapClick;GP.V.onlong=u=>{const r=gpItem(u);if(!r)return;if(GP.mode==='o'&&!r.c?.chk)return;gpToggle(u)};GP.V.onclose=()=>{GP.sel=null;document.querySelectorAll('.gpchk li.hl').forEach(x=>x.classList.remove('hl'))};
 gpSearchInit(d.querySelector('.gpsearch'));
 document.addEventListener('keydown',gpKeys);
 document.addEventListener('fullscreenchange',()=>setTimeout(()=>GP.V.layout(),50))}

function gpOpen(gid,mode,idx){const g=GAMES.find(x=>x.id===gid);if(!g){location.hash='#/';return}
 gpEnsure();const first=!GP.g||GP.g.id!==gid;
 if(first){GP.g=g;const p=ZS.get('pref:'+gid,null);const M=gpModel(g);
  GP.done=new Set(ZS.get('done:'+gid,[]));
  GP.spoil=!!(p&&p.spoil);GP.rev=new Set(p&&p.rev||[]);GP.grp=p&&p.grp||'cat';
  if(p){GP.on=new Set(p.on.filter(id=>M.cats.some(c=>c.id===id)));GP.hide=!!p.hide;GP.lbl=p.lbl!==false;GP.ms=p.ms||1;GP.kinds=new Set(p.kinds||[])}
  else{GP.on=new Set();const tot=M.cats.reduce((a,c)=>a+c.it.length,0);M.cats.forEach(c=>{if(c.kind==='label'||c.kind==='area'||tot<600||/shrine|tower|dungeon|lightroot/i.test(c.n))GP.on.add(c.id)});GP.hide=false;GP.lbl=true;GP.ms=1;GP.kinds=new Set()}
  GP.dm=p?p.dm||0:0;GP.tab=p?p.tab||0:0}
 if(idx==null)idx=mode==='d'?GP.dm:GP.tab;
 if(mode==='d'&&!hasDG(gid))mode='o';
 GP.mode=mode;if(mode==='d')GP.dm=Math.max(0,Math.min(idx||0,DUNG[gid].m.length-1));else GP.tab=Math.max(0,Math.min(idx||0,gpModel(g).tabs.length-1));
 ZS.set('last',gid);document.body.classList.add('gp-on');document.title=gTitle(g)+' · Zelda Maps';
 const d=document.getElementById('gp');d.querySelector('h2').textContent=gTitle(g);d.querySelector('.yr').textContent=g.y;d.querySelector('.gpsel').value=gid;
 const M=gpModel(g);const nOw=M.cats.reduce((a,c)=>a+c.it.length,0);
 d.querySelector('.gpmodes').innerHTML=`<button class="gpbtn ${mode==='o'?'on':''}" data-m="o" title="Overworld (O)">Overworld <small>${nOw}</small></button>`+(hasDG(gid)?`<button class="gpbtn ${mode==='d'?'on':''}" data-m="d" title="Dungeons (D)">Dungeons <small>${DUNG[gid].m.length}</small></button>`:'');
 d.querySelectorAll('.gpmodes button').forEach(b=>b.onclick=()=>gpGo(b.dataset.m));
 GP.V.close();GP.notemode=false;GP.V.host.classList.remove('notemode');
 typeof zdButtons==='function'&&zdButtons();
 gpRender(true)}
function gpGo(mode,idx){const g=GP.g;location.hash='#/g/'+g.id+'/'+mode+(idx!=null?'/'+idx:'')}
function gpReplace(){const h='#/g/'+GP.g.id+'/'+GP.mode+'/'+(GP.mode==='d'?GP.dm:GP.tab);if(location.hash!==h)history.replaceState(null,'',h);gpPref()}

function gpRender(newImg){return GP.busy=gpRender2(newImg)}
async function gpRender2(newImg){const g=GP.g,V=GP.V;if(typeof ZD!=='undefined'&&ZD.role==='panel')newImg=false;V.host.classList.toggle('hidedone',GP.hide);V.host.classList.toggle('nolbl',!GP.lbl);V.inn.style.setProperty('--ms',GP.ms);
 if(GP.mode==='o'){const t=gpModel(g).tabs[GP.tab];if(newImg)await V.setImg('maps/'+t.img,GP.tab===0?g.w:0,GP.tab===0?g.h:0);gpHdSet(t.img);gpOwMarkers();gpOwSide()}
 else{const m=DUNG[g.id].m[GP.dm];gpHdSet(null);gpHdSetO(null,0);if(newImg)await V.setImg(await dgSrc(m.img),m.w,m.h);gpDgMarkers();gpDgSide()}
 gpBlendApply();gpReplace()}

// ---------- regions & spoiler-free ----------
const GRG={};const CMP=['North-west','North','North-east','West','Centre','East','South-west','South','South-east'];
function gpRegions(g,t){const key=g.id+'|'+t.k;if(GRG[key])return GRG[key];const M=gpModel(g);const labs=[];
 M.cats.forEach(c=>{if(c.kind==='label')c.it.forEach(r=>{if(r.tab===t.k)labs.push(r)})});
 let seeds=[],lvl=0;const by={};labs.forEach(r=>(by[r.sz||1]=by[r.sz||1]||[]).push(r));
 for(const sz of [3,2]){const c=by[sz]||[];if(c.length>=4&&c.length<=40){seeds=c;lvl=sz;break}}
 if(seeds.length<4){const c=labs.filter(r=>(r.sz||1)>=2);if(c.length>=3&&c.length<=40){seeds=c;lvl=2}}
 if(seeds.length<3&&t.al&&g.mk&&g.mk.length>=3){seeds=g.mk.map(m=>({name:m[3].replace(/ \(.*/,''),x:m[1],y:m[2]}));lvl=9}
 if(seeds.length<3){seeds=CMP.map((n,i)=>({name:n,x:100/6+(i%3)*100/3,y:100/6+Math.floor(i/3)*100/3}));lvl=8}
 const ar=(g.h||1)/(g.w||1);const names=[...new Set(seeds.map(r=>r.name))];
 const list=names.map(n=>{const pts=seeds.filter(r=>r.name===n);return {id:t.k+':'+n,name:n,x:pts.reduce((a,r)=>a+r.x,0)/pts.length,y:pts.reduce((a,r)=>a+r.y,0)/pts.length,pts}});
 const cache=new Map();const of=r=>{const ck=r.u||r;if(cache.has(ck))return cache.get(ck);let best=null,bd=1e9;list.forEach(L=>L.pts.forEach(p=>{const d=(p.x-r.x)**2+((p.y-r.y)*ar)**2;if(d<bd){bd=d;best=L}}));cache.set(ck,best);return best};
 return GRG[key]={list,of,lvl,seedSet:new Set(seeds)}}
const gpRev=id=>!GP.spoil||GP.rev.has(id);
function gpVisible(r,t){if(!GP.spoil)return true;if(GP.done.has(r.u))return true;const R=gpRegions(GP.g,t);if(r.c.kind==='label'&&R.seedSet.has(r))return true;const L=R.of(r);return !L||GP.rev.has(L.id)}
function gpReveal(id,on){on===false?GP.rev.delete(id):GP.rev.add(id);gpPref();GP.resetSearch&&GP.resetSearch();gpRender(false)}
function gpRegionStats(t){const R=gpRegions(GP.g,t),st=new Map(R.list.map(L=>[L.id,{L,d:0,n:0}]));gpModel(GP.g).cats.forEach(c=>{if(!c.chk)return;c.it.forEach(r=>{if(!onTab(r,t))return;const L=R.of(r);if(!L)return;const s=st.get(L.id);s.n++;if(GP.done.has(r.u))s.d++})});return [...st.values()].filter(s=>s.n)}

// ---------- overworld ----------
function gpMarkerEl(r,kind,col,M){let e;
 if(kind==='label'){e=document.createElement('span');const T=gpTier(r,M);e.className='gl sz'+(r.sz||1)+' gt'+T;e.dataset.t=T;e.textContent=r.name}
 else{e=document.createElement('i');e.className='gm';
  if(kind==='area'){e.classList.add('area');e.style.background=col}
  else if(r.icon&&kind!=='dot'){const im=document.createElement('img');im.src=r.icon;im.alt='';im.loading='lazy';e.appendChild(im)}
  else{e.classList.add('dot');e.style.background=col}
  if(GP.done.has(r.u))e.classList.add('done')}
 e.style.left=r.x+'%';e.style.top=r.y+'%';e.dataset.u=r.u;return e}
// Cross-game blends: which game's markers belong to each blended image, and how to place them on this map (% -> %).
const XALBL={"xa_albw_on_alttp.webp":["albw",0,[[1.05082,-0.00228,-2.404398],[-0.001689,1.050352,-2.528582]]],"xa_lorule_on_alttp.webp":["albw",1,[[1.05082,-0.00228,-2.404398],[-0.001689,1.050352,-2.528582]]],"xa_eow_on_alttp.webp":["eow",0,[[1.567152,0.0,-23.656167],[0.0,1.239618,-11.782819]]],"xa_alttp_on_albw.webp":["alttp",0,[[0.951641,0.002065,2.293346],[0.00153,0.952065,2.411054]]],"xa_dark_on_albw.webp":["alttp",1,[[0.951641,0.002065,2.293346],[0.00153,0.952065,2.411054]]],"xa_eow_on_albw.webp":["eow",0,[[1.491366,0.00256,-20.243165],[0.002398,1.180197,-8.843153]]],"xa_alttp_on_eow.webp":["alttp",0,[[0.6381,-0.0,15.095],[-0.0,0.8067,9.5052]]],"xa_albw_on_eow.webp":["albw",0,[[0.670528,-0.001455,13.560753],[-0.001362,0.847319,7.465393]]]};
// Where markers come from: this map, or (when "flip labels" is on and a blend is showing) the blended map.
function gpMkSrc(){const M=gpModel(GP.g),t=M.tabs[GP.tab],b=GP.bl;
 if(GP.mode!=='o'||!b||!b.f||b.tab!==GP.tab||b.i==null||!b.v||!M.tabs[b.i])return {M,t,own:true,key:'own'};
 const bt=M.tabs[b.i],x=XALBL[bt.img];
 if(!x)return {M,t:bt,own:false,same:true,key:'t'+b.i,n:bt.n};
 const g2=GAMES.find(q=>q.id===x[0]);if(!g2)return {M,t,own:true,key:'own'};const M2=gpModel(g2),t2=M2.tabs[x[1]],A=x[2];
 const p=ZS.get('pref:'+g2.id,null),on=p&&p.on?new Set(p.on):null,tot=M2.cats.reduce((a,c)=>a+c.it.length,0);
 return {M:M2,t:t2,own:false,g:g2,on:c=>on?on.has(c.id):(c.kind==='label'||c.kind==='area'||tot<600||/shrine|tower|dungeon|lightroot/i.test(c.n)),
  T:r=>[A[0][0]*r.x+A[0][1]*r.y+A[0][2],A[1][0]*r.x+A[1][1]*r.y+A[1][2]],key:'x'+bt.img,n:bt.n}}
function gpOwMarkers(){const V=GP.V,S=gpMkSrc(),M=S.M,t=S.t;GP.mkKey=S.key;GP.mkForeign=!!S.g;V.mk.innerHTML='';const fr=document.createDocumentFragment();
 V.host.classList.toggle('mkflip',!S.own);
 M.cats.forEach(c=>{if(S.g?!S.on(c):!GP.on.has(c.id))return;c.it.forEach(r=>{if(!onTab(r,t)||(!S.g&&!gpVisible(r,t)))return;const e=gpMarkerEl(r,c.kind,r.col||c.col,M);
  if(S.T){const q=S.T(r);if(q[0]<-2||q[0]>102||q[1]<-2||q[1]>102)return;e.style.left=q[0]+'%';e.style.top=q[1]+'%'}if(c.kind!=='label'){e.onclick=ev=>{ev.stopPropagation();if(!V.moved)gpShowItem(r)};e.onmouseenter=ev=>showTip(ev,`<b>${esc(r.name)}</b><br><span style="color:var(--mute)">${esc(c.n)}</span>`);e.onmouseleave=hideTip}fr.appendChild(e)})});
 if(!S.g)gpNotes('o'+t.k).forEach((n,ni)=>fr.appendChild(gpNoteEl(n,ni,'o'+t.k)));
 V.mk.appendChild(fr);gpLblInit()}
// ---------- place-name tiers: reveal by zoom, like the in-game map ----------
// tier 0 = regions, 2 = sub-regions, 3 = generic small labels, 4 = places, 5 = minor spots / rooms
function gpTier(r,M){M=M||(GP.g&&gpModel(GP.g));if(M&&M._lz===undefined)M._lz=M.cats.some(c=>c.kind==='label'&&c.it.some(x=>x.mz>0));
 if(M&&M._lz){if((r.sz||1)>=2&&r.mz<=1)return 0;if(r.mz<=0)return (r.sz||1)>=2?0:5;return r.mz<=2?2:r.mz<=4?4:5}
 return (r.sz||1)>=3?0:(r.sz||1)===2?2:3}
const LT_MIN={0:0,2:1.25,3:1.6,4:2.1,5:3.4},LT_MIN_SM={0:0,2:1,3:1.2,4:1.5,5:2.4},LT_FS={0:19,2:14,3:11.5,4:11.5,5:10.5},LT_CW={0:.78,2:.62,3:.56,4:.56,5:.55};
function gpLblInit(){const V=GP.V;if(!V)return;const host=V.mk.closest('.gv')||V.mk.parentNode;if(zmSafe(GP.g)){host&&host.classList.add('lsafe');GP.lbls=null;V.onlbl=null;return}host&&host.classList.remove('lsafe');const L=[];V.mk.querySelectorAll('.gl').forEach((e,i)=>{const t=+e.dataset.t||0,n=e.textContent.length,fs=LT_FS[t];
  L.push({e,t,x:parseFloat(e.style.left),y:parseFloat(e.style.top),w:n*fs*LT_CW[t]+8,h:fs*1.35,i})});
 L.sort((a,b)=>a.t-b.t||b.w-a.w);GP.lbls=L;GP.lblS=0;GP.lblFade=false;V.onlbl=gpLblSched;gpLblLayout()}
function gpLblSched(force){const V=GP.V;if(!GP.lbls)return;if(force===true){GP.lblS=0}
 clearTimeout(GP.lblEnd);GP.lblEnd=setTimeout(()=>{GP.lblS=0;GP.lblRaf||(GP.lblRaf=requestAnimationFrame(()=>{GP.lblRaf=0;gpLblLayout()}))},140);
 if(GP.lblRaf)return;const host=V.mk.closest('.gv')||V.mk.parentNode,cw=host.clientWidth||1,ch=host.clientHeight||1;
 if(host.classList.contains('zooming')&&GP.lblS&&Math.abs(Math.log(V.s/GP.lblS))<0.7)return; // re-lay names when the zoom settles
 const dz=GP.lblS?Math.abs(Math.log(V.s/GP.lblS)):9,dp=GP.lblP?Math.hypot(V.tx-GP.lblP[0],V.ty-GP.lblP[1])/Math.max(cw,ch):9;
 if(dz<0.115&&dp<0.3)return;GP.lblRaf=requestAnimationFrame(()=>{GP.lblRaf=0;gpLblLayout()})}
function gpLblLayout(){const V=GP.V,L=GP.lbls;if(!V||!L)return;const s=V.s;GP.lblS=s;GP.lblP=[V.tx,V.ty];const hasLow=L.some(o=>o.t>0);
 const host=V.mk.closest('.gv')||V.mk.parentNode,small=(host.clientWidth<640||host.clientHeight<480);host.classList.toggle('lsm',small);
 // visible window in map-pixel space (the map is drawn at offset ox+tx, oy+ty), with half a screen of margin each side
 const cw=host.clientWidth,ch=host.clientHeight,vx0=-(V.ox+V.tx)-cw*.5,vy0=-(V.oy+V.ty)-ch*.5,vx1=vx0+cw*2,vy1=vy0+ch*2;
 const MIN=small?LT_MIN_SM:LT_MIN,F=small?0.85:1;
 const C=new Map(),cell=80,W=V.W*s,H=V.H*s;
 const hit=(x0,y0,x1,y1)=>{for(let gx=Math.floor(x0/cell);gx<=Math.floor(x1/cell);gx++)for(let gy=Math.floor(y0/cell);gy<=Math.floor(y1/cell);gy++){const b=C.get(gx+','+gy);if(b)for(const q of b)if(x0<q[2]&&x1>q[0]&&y0<q[3]&&y1>q[1])return true}return false};
 const put=(r)=>{for(let gx=Math.floor(r[0]/cell);gx<=Math.floor(r[2]/cell);gx++)for(let gy=Math.floor(r[1]/cell);gy<=Math.floor(r[3]/cell);gy++){const k=gx+','+gy;(C.get(k)||C.set(k,[]).get(k)).push(r)}};
 for(const o of L){let show=s>=MIN[o.t];if(o.t===0&&hasLow&&s>=3.6)show=false;
  if(show){const cx0=o.x/100*W,cy0=o.y/100*H;if(cx0<vx0||cx0>vx1||cy0<vy0||cy0>vy1)show=false}
  if(show){const cx=o.x/100*W,cy=o.y/100*H,w=o.w*F,h=o.h*F,r=[cx-w/2-3,cy-h/2-2,cx+w/2+3,cy+h/2+2];if(hit(...r))show=false;else put(r)}
  if(show){if(o.e.parentNode!==V.mk){if(GP.lblFade)o.e.classList.add('gin');else o.e.classList.remove('gin');V.mk.appendChild(o.e)}}else if(o.e.parentNode)o.e.remove()}GP.lblFade=true}
function gpCount(c,t){let n=0,d=0;c.it.forEach(r=>{if(t&&!onTab(r,t))return;n++;if(GP.done.has(r.u))d++});return [d,n]}
function gpBlendApply(){const V=GP.V;if(!V)return;const M=GP.g&&gpModel(GP.g);const b=GP.bl;
 if(GP.mode==='o'&&M&&GP.mkKey!==undefined&&gpMkSrc().key!==GP.mkKey){gpOwMarkers();const fb=document.querySelector('.gpside .gpflip');if(fb)gpFlipBtn(fb)}
 if(GP.mode!=='o'||!M||!b||b.tab!==GP.tab||b.i==null||!b.v){V.ovl.style.opacity=0;gpHdSetO(null,0);return}
 const src='maps/'+M.tabs[b.i].img;if(!V.ovl.src.endsWith(src))V.ovl.src=src;V.ovl.style.opacity=b.v/100;gpHdSetO(M.tabs[b.i].img,b.v/100)}
function gpFlipBtn(fb){const M=gpModel(GP.g),b=GP.bl,S=gpMkSrc(),bt=b&&b.i!=null&&M.tabs[b.i];
 fb.disabled=!b||!b.v;fb.classList.toggle('on',!S.own);
 fb.innerHTML='⇄ Labels: '+esc(S.own?(M.tabs[GP.tab].n||'this map'):(bt?bt.n:''))+(fb.disabled?' <small style="color:var(--mute)">(blend first)</small>':'')}
function gpFlip(){const b=GP.bl;if(!b||b.tab!==GP.tab||!b.v){GP.V&&GP.V.toast&&GP.V.toast('Blend in a map first, then flip labels');return}
 b.f=!b.f;gpBlendApply();const fb=document.querySelector('.gpside .gpflip');if(fb)gpFlipBtn(fb);typeof zdState==='function'&&zdState()}
function gpOwSide(){const g=GP.g,M=gpModel(g),t=M.tabs[GP.tab],side=document.querySelector('.gpside');const ssc=side.scrollTop;
 const aligned=M.tabs.filter(x=>x.al);
 const cats=M.cats.filter(c=>c.it.some(r=>onTab(r,t)));
 let all=0,dn=0;M.cats.forEach(c=>{if(!c.chk)return;c.it.forEach(r=>{all++;if(GP.done.has(r.u))dn++})});
 let h='';
 if(M.tabs.filter(x=>!x.hid).length>1)h+=`<h4>Map version</h4><div class="gprow">${M.tabs.filter(x=>!x.hid).map(x=>`<button class="gpbtn ${x.i===GP.tab?'on':''}" data-t="${x.i}" title="${x.al?'Same layout as the main map':'Different layout: series markers hidden'}">${esc(x.n)}${x.al?'':' *'}</button>`).join('')}</div>`;
 const blOpts=aligned.filter(x=>x!==t&&x.img!==t.img&&(!x.fo||x.fo===t.k));if(!GP.bl||GP.bl.tab!==GP.tab||!blOpts.some(x=>x.i===GP.bl.i))GP.bl={tab:GP.tab,i:blOpts[0]?blOpts[0].i:null,v:0};
 if(t.al&&blOpts.length)h+=`<div class="gprow"><span style="color:var(--mute)">Blend in</span><select class="gpbl">${blOpts.map(x=>`<option value="${x.i}"${x.i===GP.bl.i?' selected':''}>${esc(x.n)}</option>`).join('')}</select><input type="range" class="gpblr" min="0" max="100" value="${GP.bl.v}" style="flex:1;min-width:80px"><small class="gpblv" style="color:var(--mute);width:34px;text-align:right">${GP.bl.v}%</small></div>`;
 if(t.al&&blOpts.length)h+=`<div class="gprow"><button class="gpbtn gpflip" title="Show the markers and names of the blended map instead (X)"></button></div>`;
 h+=`<h4>Progress</h4><div>${dn} of ${all} found${all?` (${Math.round(dn/all*100)}%)`:''}</div><div class="gpprog"><i style="width:${all?dn/all*100:0}%"></i></div>`;
 h+=`<div class="gprow"><label><input type="checkbox" class="gphide" ${GP.hide?'checked':''}> Hide found <small style="color:var(--mute)">(H)</small></label><label><input type="checkbox" class="gplbl" ${GP.lbl?'checked':''}> Labels <small style="color:var(--mute)">(L)</small></label></div>`;
 {const rs=gpRegionStats(t);if(rs.length>1)h+=`<details class="gpreg"><summary>Progress by region</summary>${rs.map(s=>{const rv=GP.rev.has(s.L.id);return `<div class="gpregrow"><button class="gplink" data-go="${esc(s.L.id)}">${esc(s.L.name)}</button><span class="gpprog"><i style="width:${s.d/s.n*100}%"></i></span><small>${s.d}/${s.n}</small>${GP.spoil?`<button class="gplink" data-rv="${esc(s.L.id)}">${rv?'Hide':'Reveal'}</button>`:''}</div>`}).join('')}</details>`}
 h+=`<div class="gprow"><label title="Hide markers until you reveal their region"><input type="checkbox" class="gpspoil" ${GP.spoil?'checked':''}> Spoiler-free</label>${GP.spoil?'<small style="color:var(--mute)">Tap the map to reveal a region</small>':''}</div>`;
 h+=`<div class="gprow"><span style="color:var(--mute)">Marker size</span><input type="range" class="gpms" min="0.6" max="1.8" step="0.1" value="${GP.ms}" style="flex:1"></div>`;
 h+=`<div class="gpseg" role="tablist"><button class="${GP.owView!=='list'?'on':''}" data-v="layers">Layers</button><button class="${GP.owView==='list'?'on':''}" data-v="list">Checklist</button></div>`;
 if(GP.owView==='list'){h+=gpOwListHTML(M,t)+'<div class="gprow"><button class="gplink gpnote">📌 Add a note (N)</button></div>'}else{
 h+=`<h4>Layers on this map</h4><div class="gprow"><button class="gplink" data-a="all">Show all</button>·<button class="gplink" data-a="none">Hide all</button>·<button class="gplink gpnote">📌 Add a note (N)</button></div>`;
 if(!cats.length)h+='<div style="color:var(--mute)">No marker layers for this map version. Try another version above.</div>';
 const elsewhere=M.tabs.filter(x=>x!==t).map(x=>[x,M.cats.reduce((a,c)=>a+c.it.filter(r=>r.tab===x.k).length,0)]).filter(x=>x[1]&&!(x[0].al&&x[0].k===t.k));
 if(elsewhere.length)h+=`<div style="color:var(--mute);font-size:12px;margin:2px 0 6px">More markers on: ${elsewhere.map(([x,n])=>`<button class="gplink" data-t="${x.i}">${esc(x.n)} (${n})</button>`).join(', ')}</div>`;
 h+='<div class="gpcats">'+M.groups.map(gr=>{const cs=cats.filter(c=>c.g===gr);if(!cs.length)return '';
  const [gd,gn]=cs.filter(c=>c.chk).reduce((a,c)=>{const [d,n]=gpCount(c,t);return [a[0]+d,a[1]+n]},[0,0]);
  return `<details ${cs.length<=12||cs.some(c=>GP.on.has(c.id))?'open':''}><summary>${esc(gr)}<small>${gn?gd+'/'+gn:''}</small></summary>`+cs.map(c=>{const [d,n]=gpCount(c,t);
   const ic=c.kind==='label'?'<b class="xlA">Aa</b>':c.kind==='area'?'<i class="xldot" style="background:conic-gradient(#ff6a3d,#4fb0ff,#4fd364,#ffc23d,#ff6a3d)"></i>':c.icon&&c.kind!=='dot'?`<img src="${c.icon}" alt="">`:`<i class="xldot" style="background:${c.col}"></i>`;
   return `<label><input type="checkbox" data-c="${c.id}" ${GP.on.has(c.id)?'checked':''}> ${ic} ${esc(c.n)} <small>${c.chk?d+'/'+n:n}</small></label>`}).join('')+'</details>'}).join('')+'</div>';
 }
 h+=gpDataBlock();
 h+=`<div class="dsrc" style="margin-top:10px">${esc(g.note||'')}</div>`;
 side.innerHTML=h;side.scrollTop=ssc;
 side.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{GP.owView=b.dataset.v;gpOwSide()});
 side.querySelector('.gpspoil').onchange=e=>{GP.spoil=e.target.checked;gpPref();GP.resetSearch&&GP.resetSearch();gpRender(false);GP.V.toast(GP.spoil?'Spoiler-free on: tap a region on the map to reveal it':'Spoiler-free off')};
 side.querySelectorAll('[data-rv]').forEach(b=>b.onclick=e=>{e.stopPropagation();gpReveal(b.dataset.rv,!GP.rev.has(b.dataset.rv))});
 side.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{const L=gpRegions(GP.g,t).list.find(L=>L.id===b.dataset.go);if(L)GP.V.focus(L.x,L.y,2.2)});
 const gpr=side.querySelector('.gpreg');if(gpr){gpr.open=!!GP.regOpen;gpr.addEventListener('toggle',()=>GP.regOpen=gpr.open)}
 gpOwListWire(side,M,t);
 side.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{GP.tab=+b.dataset.t;GP.V.close();gpRender(true)});
 const bl=side.querySelector('.gpbl'),blr=side.querySelector('.gpblr');gpBlendApply();
 if(bl){const set=()=>{GP.bl={tab:GP.tab,i:+bl.value,v:+blr.value,f:!!(GP.bl&&GP.bl.f)};side.querySelector('.gpblv').textContent=blr.value+'%';gpBlendApply();const fb=side.querySelector('.gpflip');fb&&gpFlipBtn(fb);typeof zdState==='function'&&zdState()};bl.onchange=set;blr.oninput=set;const fb=side.querySelector('.gpflip');if(fb){gpFlipBtn(fb);fb.onclick=()=>gpFlip()}blr.addEventListener('keydown',e=>e.stopPropagation())}
 side.querySelector('.gphide').onchange=e=>{GP.hide=e.target.checked;GP.V.host.classList.toggle('hidedone',GP.hide);gpPref()};
 side.querySelector('.gplbl').onchange=e=>{GP.lbl=e.target.checked;GP.V.host.classList.toggle('nolbl',!GP.lbl);gpPref()};
 side.querySelector('.gpms').oninput=e=>{GP.ms=+e.target.value;GP.V.inn.style.setProperty('--ms',GP.ms);gpPref()};
 side.querySelectorAll('.gpcats input').forEach(cb=>cb.onchange=()=>{cb.checked?GP.on.add(cb.dataset.c):GP.on.delete(cb.dataset.c);gpOwMarkers();gpPref()});
 side.querySelectorAll('.gpcats summary').forEach(s=>s.addEventListener('dblclick',e=>{e.preventDefault();const cbs=[...s.parentElement.querySelectorAll('input')];const v=!cbs.every(c=>c.checked);cbs.forEach(c=>{c.checked=v;v?GP.on.add(c.dataset.c):GP.on.delete(c.dataset.c)});gpOwMarkers();gpPref()}));
 side.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{cats.forEach(c=>b.dataset.a==='all'?GP.on.add(c.id):GP.on.delete(c.id));gpOwSide();gpOwMarkers();gpPref()});
 side.querySelector('.gpnote').onclick=gpNoteMode;
 gpDataWire(side)}
function gpOwListItems(its,showCat){const col=new Intl.Collator(undefined,{numeric:true});its=its.slice().sort((a,b)=>col.compare(a.name,b.name));
 return '<ul class="gpchk'+(GP.hide?' hidedone':'')+'">'+its.map(r=>{const dt=r.html?String(r.det||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim():r.det||'';const sub=(showCat?r.c.n+(dt?' · ':''):'')+dt;return `<li data-u="${r.u}" class="${GP.done.has(r.u)?'done':''}"><input type="checkbox" ${GP.done.has(r.u)?'checked':''}><span><b>${esc(r.name)}</b>${sub?`<small>${esc(sub.slice(0,110))}${sub.length>110?'…':''}</small>`:''}</span></li>`}).join('')+'</ul>'}
function gpOwFilt(r,t){const q=(GP.lq||'').toLowerCase(),f=GP.lf||'all';return onTab(r,t)&&gpVisible(r,t)&&(!q||(r.name+' '+(r.html?'':r.det||'')).toLowerCase().includes(q))&&(f==='all'||(f==='done')===GP.done.has(r.u))}
function gpOwGroups(M,t){if(GP.grp==='reg'){const R=gpRegions(GP.g,t);const by=new Map(R.list.map(L=>[L.id,[]]));M.cats.forEach(c=>{if(!c.chk)return;c.it.forEach(r=>{if(!onTab(r,t))return;const L=R.of(r);if(L)by.get(L.id).push(r)})});
  return R.list.map(L=>({id:'R:'+L.id,rid:L.id,name:L.name,all:by.get(L.id),L})).filter(x=>x.all.length)}
 return M.cats.filter(c=>c.chk&&c.it.some(r=>onTab(r,t))).map(c=>({id:c.id,name:c.n,all:c.it.filter(r=>onTab(r,t)),c}))}
function gpOwListHTML(M,t){const q=(GP.lq||'').toLowerCase(),f=GP.lf||'all';GP.lopen=GP.lopen||new Set();
 const grps=gpOwGroups(M,t);
 let h=`<div class="gprow gplfrow"><input type="search" class="gplq" placeholder="Filter this list" value="${esc(GP.lq||'')}"><select class="gplf" aria-label="Show"><option value="all"${f==='all'?' selected':''}>All</option><option value="todo"${f==='todo'?' selected':''}>Not found</option><option value="done"${f==='done'?' selected':''}>Found</option></select><select class="gplg" aria-label="Group by"><option value="cat"${GP.grp!=='reg'?' selected':''}>By type</option><option value="reg"${GP.grp==='reg'?' selected':''}>By region</option></select></div>`;
 const body=grps.map(G=>{const d=G.all.filter(r=>GP.done.has(r.u)).length,n=G.all.length;
  if(G.L&&GP.spoil&&!GP.rev.has(G.rid))return q?'':`<div class="gpregh"><span>🔒 ${esc(G.name)}</span><small>${d}/${n}</small><button class="gplink" data-rv="${esc(G.rid)}">Reveal</button></div>`;
  const its=G.all.filter(r=>gpOwFilt(r,t));if(!its.length)return '';const c=G.c;
  const ic=c?(c.icon&&c.kind!=='dot'?`<img src="${c.icon}" alt="">`:`<i class="xldot" style="background:${c.kind==='area'?'#fff':c.col}"></i>`):'<span class="gpregdot"></span>';const open=!!q||GP.lopen.has(G.id);
  return `<details data-c="${G.id}" ${open?'open':''}><summary>${ic} ${esc(G.name)}<small>${q||f!=='all'?its.length+' shown · ':''}${d}/${n}</small></summary>${open?gpOwListItems(its,!c):''}</details>`}).join('');
 return h+'<div class="gplist gpcats">'+(body||'<div style="color:var(--mute);padding:8px 0">Nothing matches. Clear the filter or pick All.</div>')+'</div>'}
function gpOwListWire(side,M,t){const q=side.querySelector('.gplq');if(!q)return;let tm;
 q.addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(()=>{GP.lq=q.value;const pos=q.selectionStart;gpOwSide();const n=document.querySelector('.gpside .gplq');n.focus();n.setSelectionRange(pos,pos)},180)});
 q.addEventListener('keydown',e=>e.stopPropagation());
 side.querySelector('.gplf').onchange=e=>{GP.lf=e.target.value;gpOwSide()};
 side.querySelector('.gplg').onchange=e=>{GP.grp=e.target.value;gpPref();gpOwSide()};
 side.querySelectorAll('.gplist details').forEach(d=>d.addEventListener('toggle',()=>{const id=d.dataset.c;if(d.open){GP.lopen.add(id);if(!d.querySelector('ul')){const G=gpOwGroups(M,t).find(G=>G.id===id);if(!G)return;
   d.insertAdjacentHTML('beforeend',gpOwListItems(G.all.filter(r=>gpOwFilt(r,t)),!G.c));wireLis(d)}}else GP.lopen.delete(id)}));
 const wireLis=root=>root.querySelectorAll('li[data-u]').forEach(li=>{const u=li.dataset.u;
  li.querySelector('input').onclick=e=>{e.stopPropagation();gpToggle(u)};
  li.onclick=()=>{const r=gpItem(u);if(!r)return;if(!GP.on.has(r.c.id)){GP.on.add(r.c.id);gpOwMarkers();gpPref()}GP.V.focus(r.x,r.y,Math.max(GP.V.s,2.5));gpShowItem(r);side.querySelectorAll('li.hl').forEach(x=>x.classList.remove('hl'));li.classList.add('hl')}});
 wireLis(side)}
function gpShowItem(r){const V=GP.V,c=r.c;GP.sel=r;typeof zdSel==='function'&&zdSel(r.u);V.mk.querySelectorAll('.gm.sel').forEach(x=>x.classList.remove('sel'));const el=V.mk.querySelector(`[data-u="${r.u}"]`);el&&el.classList.add('sel');
 const src=c.src==='alttp'?'easymac/alttp-map-tracker':c.src==='zd'?'Zelda Dungeon maps':c.src||(c.id.startsWith('T')?'Alshival TOTK data (CC0)':'');
 const dn=GP.done.has(r.u);
 V.popup(`<b class="t">${esc(r.name)}</b><div class="m">${esc(c.g)} · ${esc(c.n)}${src?' · '+esc(src):''}</div>${r.det?`<div class="d">${r.html?r.det:esc(r.det)}</div>`:''}
  <div class="gprow">${c.chk&&!GP.mkForeign?`<button class="gpbtn ${dn?'on':''}" data-do="done">${dn?'✓ Found':'Mark found'} <small>(Space)</small></button>`:''}${r.wiki?`<a class="gpbtn" href="${ZDW}${encodeURIComponent(r.wiki).replace(/%2F/g,'/')}" target="_blank" rel="noopener">Wiki ↗</a>`:''}<button class="gpbtn" data-do="center">Center</button></div>`);
 V.pop.querySelector('[data-do="done"]')?.addEventListener('click',e=>{e.stopPropagation();gpToggle(r.u)});
 V.pop.querySelector('[data-do="center"]').onclick=e=>{e.stopPropagation();V.focus(el?parseFloat(el.style.left):r.x,el?parseFloat(el.style.top):r.y,Math.max(V.s,2.5))}}
function gpItem(u){if(!GP.g)return null;if(GP.mode==='o'){for(const c of gpModel(GP.g).cats)for(const r of c.it)if(r.u===u)return r;return null}return (dgItems(GP.g.id)[GP.dm]||[]).find(r=>r.u===u)||null}
function gpToggle(u,quiet){GP.done.has(u)?GP.done.delete(u):GP.done.add(u);gpSaveDone();
 if(!quiet&&GP.V){const r=gpItem(u);const on=GP.done.has(u);GP.V.toast((on?'Marked found: ':'Unmarked: ')+(r?r.name:''),()=>gpToggle(u,true))}
 const el=GP.V.mk.querySelector(`[data-u="${u}"]`);el&&el.classList.toggle('done',GP.done.has(u));
 if(GP.mode==='o'){gpOwSide();if(GP.sel&&GP.sel.u===u)gpShowItem(GP.sel)}else{gpDgSide(true);if(GP.sel&&GP.sel.u===u)gpShowCheck(GP.sel)}}

// ---------- notes ----------
function gpNoteKey(){return GP.mode==='o'?'o'+gpModel(GP.g).tabs[GP.tab].k:'d'+DUNG[GP.g.id].m[GP.dm].img}
function gpNoteMode(){GP.notemode=!GP.notemode;GP.V.host.classList.toggle('notemode',GP.notemode);
 const hint=GP.V.host.querySelector('.gvhint');if(GP.notemode){const h=document.createElement('div');h.className='gvhint';h.textContent='Click the map to place a note. Esc to cancel.';GP.V.host.appendChild(h)}else hint&&hint.remove()}
function gpMapClick(e){if(!GP.notemode){const open=GP.V.pop.classList.contains('open');GP.V.close();
  if(GP.spoil&&!open){const [x,y]=GP.V.toPct(e.clientX,e.clientY);if(x<0||x>100||y<0||y>100)return;
   if(GP.mode==='o'){const t=gpModel(GP.g).tabs[GP.tab];const L=gpRegions(GP.g,t).of({x,y});if(L&&!GP.rev.has(L.id))GP.V.toast('Reveal '+L.name+'?',()=>gpReveal(L.id),'Reveal')}
   else{const m=DUNG[GP.g.id].m[GP.dm];if(!GP.rev.has('d:'+m.d))GP.V.toast('Reveal checks in '+m.d+'?',()=>gpReveal('d:'+m.d),'Reveal')}}
  return}const [x,y]=GP.V.toPct(e.clientX,e.clientY);if(x<0||x>100||y<0||y>100)return;
 const key=gpNoteKey(),a=gpNotes(key);a.push({x:+x.toFixed(2),y:+y.toFixed(2),t:''});gpSetNotes(key,a);gpNoteMode();
 const el=gpNoteEl(a[a.length-1],a.length-1,key);GP.V.mk.appendChild(el);gpEditNote(a.length-1,key,true)}
function gpNoteEl(n,ni,key){const e=document.createElement('i');e.className='gm note';e.textContent='📌';e.style.left=n.x+'%';e.style.top=n.y+'%';e.dataset.u='note'+ni;
 e.onclick=ev=>{ev.stopPropagation();if(!GP.V.moved)gpEditNote(ni,key)};e.onmouseenter=ev=>n.t&&showTip(ev,esc(n.t));e.onmouseleave=hideTip;return e}
function gpEditNote(ni,key,isNew){const a=gpNotes(key),n=a[ni];if(!n)return;const V=GP.V;
 V.popup(`<b class="t">📌 Your note</b><div class="m">Saved in this browser only.</div><textarea placeholder="Write a note…">${esc(n.t)}</textarea><div class="gprow" style="margin-top:6px"><button class="gpbtn on" data-do="save">Save</button><button class="gpbtn" data-do="del">Delete</button></div>`);
 const ta=V.pop.querySelector('textarea');if(isNew)setTimeout(()=>ta.focus(),30);
 ta.addEventListener('keydown',e=>e.stopPropagation());
 V.pop.querySelector('[data-do="save"]').onclick=e=>{e.stopPropagation();const b=gpNotes(key);b[ni].t=ta.value;gpSetNotes(key,b);V.close()};
 V.pop.querySelector('[data-do="del"]').onclick=e=>{e.stopPropagation();const b=gpNotes(key);b.splice(ni,1);gpSetNotes(key,b);V.close();GP.mode==='o'?gpOwMarkers():gpDgMarkers()}}

// ---------- dungeons ----------
function gpDgMarkers(){const V=GP.V,m=DUNG[GP.g.id].m[GP.dm],its=dgItems(GP.g.id)[GP.dm];V.mk.innerHTML='';const fr=document.createDocumentFragment();
 const hid=GP.spoil&&!GP.rev.has('d:'+m.d);its.forEach(r=>{if(GP.kinds.has(r.kind)||(hid&&!GP.done.has(r.u)))return;const e=document.createElement('i');e.className='gm dot'+(GP.done.has(r.u)?' done':'');e.style.background=DGK[r.kind][1];e.style.left=r.x+'%';e.style.top=r.y+'%';e.dataset.u=r.u;
  e.onclick=ev=>{ev.stopPropagation();if(!V.moved)gpShowCheck(r)};e.onmouseenter=ev=>{showTip(ev,`<b>${esc(r.name)}</b>${r.det?'<br>'+esc(r.det):''}`);gpHl(r.u,true)};e.onmouseleave=()=>{hideTip();gpHl(r.u,false)};fr.appendChild(e)});
 gpNotes(gpNoteKey()).forEach((n,ni)=>fr.appendChild(gpNoteEl(n,ni,gpNoteKey())));
 V.mk.appendChild(fr)}
function gpHl(u,on){document.querySelector(`.gpchk li[data-u="${u}"]`)?.classList.toggle('hl',on)}
const dgFam=f=>/master quest/i.test(f||'')?'mq':/soh|peardian/i.test(f||'')?'soh':/darkzant|^interior/i.test(f||'')?'dz':'main';
const FAMN={main:'',mq:'Master Quest',soh:'Peardian (SoH) maps',dz:'DarkZant floors'};
function gpDgProg(gid,fam){const its=dgItems(gid);const D=DUNG[gid];const by={};D.m.forEach((m,mi)=>{const b=by[m.d]=by[m.d]||[0,0,-1,-1];if(b[3]<0)b[3]=mi;if(dgFam(m.f)!==fam)return;if(b[2]<0)b[2]=mi;its[mi].forEach(r=>{b[1]++;if(GP.done.has(r.u))b[0]++})});
 Object.values(by).forEach(b=>{if(b[2]<0)b[2]=b[3]});return by}
function gpDgSide(keepScroll){const g=GP.g,D=DUNG[g.id],m=D.m[GP.dm],its=dgItems(g.id)[GP.dm],side=document.querySelector('.gpside');const sc=keepScroll?side.querySelector('.gpchk')?.parentElement.scrollTop:0;const ssc=side.scrollTop;
 const fam=dgFam(m.f);const by=gpDgProg(g.id,fam);const names=Object.keys(by);
 let ta=0,td=0;Object.values(by).forEach(b=>{ta+=b[1];td+=b[0]});
 const floors=D.m.map((x,i)=>[x,i]).filter(([x])=>x.d===m.d);
 const vis=its.filter(r=>!GP.kinds.has(r.kind));const fd=its.filter(r=>GP.done.has(r.u)).length;
 let h=`<h4>All dungeons${FAMN[fam]?' · '+FAMN[fam]:''} · ${td}/${ta} found</h4><div class="gpprog"><i style="width:${ta?td/ta*100:0}%"></i></div>
 <div class="gpdl">${names.map(n=>{const b=by[n];return `<button class="${n===m.d?'on':''} ${b[1]&&b[0]===b[1]?'full':''}" data-i="${b[2]}"><span>${esc(n)}</span><small>${b[1]?b[0]+'/'+b[1]:'—'}</small></button>`}).join('')}</div>`;
 if(floors.length>1)h+=`<h4>Floor / version <small style="text-transform:none;letter-spacing:0">([ and ])</small></h4><div class="gpfl">${floors.map(([x,i])=>`<button class="gpbtn ${i===GP.dm?'on':''}" data-i="${i}">${esc(x.f||'Map')}</button>`).join('')}</div>`;
 h+=`<h4>${esc(m.d)}${m.f?' · '+esc(m.f):''} · ${fd}/${its.length}</h4><div class="gpprog"><i style="width:${its.length?fd/its.length*100:0}%"></i></div>`;
 const kinds=Object.keys(DGK).filter(k=>its.some(r=>r.kind===k));
 h+=`<div class="gpkinds">${kinds.map(k=>`<button class="${GP.kinds.has(k)?'off':''}" data-k="${k}" title="Show or hide"><i style="background:${DGK[k][1]}"></i>${DGK[k][0]} ${its.filter(r=>r.kind===k).length}</button>`).join('')}</div>`;
 h+=`<div class="gprow"><label><input type="checkbox" class="gphide" ${GP.hide?'checked':''}> Hide found (H)</label><button class="gplink" data-a="all">Mark all found</button>·<button class="gplink" data-a="none">Clear</button>·<button class="gplink gpnote">📌 Note (N)</button></div>`;
 h+=`<div class="gprow"><label title="Hide checks until you reveal the dungeon"><input type="checkbox" class="gpspoil" ${GP.spoil?'checked':''}> Spoiler-free</label></div>`;
 if(GP.spoil&&!GP.rev.has('d:'+m.d))h+=`<div class="gphidden">Checks in ${esc(m.d)} are hidden. <button class="gpbtn" data-rvd="${esc('d:'+m.d)}">Reveal them</button></div>`;
 else{if(GP.spoil)h+=`<div class="gprow"><button class="gplink" data-rvd="${esc('d:'+m.d)}" data-hide="1">Hide this dungeon's checks again</button></div>`;
 h+=`<div><ul class="gpchk ${GP.hide?'hidedone':''}">${vis.map(r=>`<li data-u="${r.u}" class="${GP.done.has(r.u)?'done':''}"><input type="checkbox" ${GP.done.has(r.u)?'checked':''}><i style="background:${DGK[r.kind][1]}"></i><span><b>${esc(r.name)}</b>${r.det?`<small>${esc(r.det)}</small>`:''}</span></li>`).join('')||'<li style="color:var(--mute)">No checks recorded on this map.</li>'}</ul></div>`}
 h+=gpDataBlock()+`<div class="dsrc">Map and positions: ${esc(D.src)}.</div>`;
 side.innerHTML=h;side.scrollTop=ssc;
 side.querySelectorAll('.gpdl button,.gpfl button').forEach(b=>b.onclick=()=>{GP.dm=+b.dataset.i;GP.V.close();gpRender(true)});
 side.querySelectorAll('.gpkinds button').forEach(b=>b.onclick=()=>{const k=b.dataset.k;GP.kinds.has(k)?GP.kinds.delete(k):GP.kinds.add(k);gpDgMarkers();gpDgSide(true);gpPref()});
 side.querySelector('.gphide').onchange=e=>{GP.hide=e.target.checked;GP.V.host.classList.toggle('hidedone',GP.hide);side.querySelector('.gpchk').classList.toggle('hidedone',GP.hide);gpPref()};
 side.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{const before=new Set(GP.done);vis.forEach(r=>b.dataset.a==='all'?GP.done.add(r.u):GP.done.delete(r.u));gpSaveDone();gpDgMarkers();gpDgSide(true);
  GP.V.toast(b.dataset.a==='all'?`Marked ${vis.length} found`:'Cleared this map',()=>{GP.done=before;gpSaveDone();gpDgMarkers();gpDgSide(true)})});
 side.querySelector('.gpnote').onclick=gpNoteMode;
 side.querySelector('.gpspoil').onchange=e=>{GP.spoil=e.target.checked;gpPref();GP.resetSearch&&GP.resetSearch();gpRender(false)};
 side.querySelectorAll('[data-rvd]').forEach(b=>b.onclick=()=>gpReveal(b.dataset.rvd,!b.dataset.hide));
 side.querySelectorAll('.gpchk li[data-u]').forEach(li=>{const r=its.find(x=>x.u===li.dataset.u);
  li.querySelector('input').onclick=e=>{e.stopPropagation();gpToggle(r.u)};
  li.onclick=()=>gpShowCheck(r,true);
  li.onmouseenter=()=>GP.V.mk.querySelector(`[data-u="${r.u}"]`)?.classList.add('sel');li.onmouseleave=()=>{if(GP.sel!==r)GP.V.mk.querySelector(`[data-u="${r.u}"]`)?.classList.remove('sel')}});
 gpDataWire(side)}
function gpShowCheck(r,center){const V=GP.V;GP.sel=r;typeof zdSel==='function'&&zdSel(r.u);V.mk.querySelectorAll('.gm.sel').forEach(x=>x.classList.remove('sel'));const el=V.mk.querySelector(`[data-u="${r.u}"]`);
 if(el){el.classList.add('sel');el.classList.remove('pulse');void el.offsetWidth;el.classList.add('pulse')}
 document.querySelectorAll('.gpchk li.hl').forEach(x=>x.classList.remove('hl'));const li=document.querySelector(`.gpchk li[data-u="${r.u}"]`);if(li){li.classList.add('hl');if(!center)li.scrollIntoView({block:'nearest'})}
 if(center&&V.s<1.5)V.focus(r.x,r.y,2);else if(center)V.focus(r.x,r.y,V.s);
 const dn=GP.done.has(r.u);
 V.popup(`<b class="t">${esc(r.name)}</b><div class="m">${esc(DGK[r.kind][0])}</div>${r.det?`<div class="d">${esc(r.det)}</div>`:''}<div class="gprow"><button class="gpbtn ${dn?'on':''}" data-do="done">${dn?'✓ Found':'Mark found'} <small>(Space)</small></button></div>`);
 V.pop.querySelector('[data-do="done"]').onclick=e=>{e.stopPropagation();gpToggle(r.u)}}

// ---------- search ----------
function gpIndex(){const g=GP.g,M=gpModel(g),out=[];
 M.cats.forEach(c=>c.it.forEach(r=>{const t=M.tabs.find(t=>onTab(r,t));if(!t||!gpVisible(r,t))return;out.push({n:r.name,s:c.n+' · '+t.n,txt:(r.name+' '+c.n+' '+(r.html?String(r.det).replace(/<[^>]+>/g,' '):r.det||'')).toLowerCase(),go:()=>{GP.on.add(c.id);gpPref();const ti=t.i;const after=()=>{GP.V.focus(r.x,r.y,3);const el=GP.V.mk.querySelector(`[data-u="${r.u}"]`);if(el){el.classList.remove('pulse');void el.offsetWidth;el.classList.add('pulse')}if(c.kind!=='label')gpShowItem(r)};
   if(GP.mode!=='o'||GP.tab!==ti){GP.mode='o';GP.tab=ti;gpModesOn();gpRender(true).then(after)}else{gpOwMarkers();gpOwSide();after()}}})}));
 if(hasDG(g.id)){const D=DUNG[g.id],its=dgItems(g.id);D.m.forEach((m,mi)=>its[mi].forEach(r=>(GP.spoil&&!GP.rev.has('d:'+m.d)&&!GP.done.has(r.u))||out.push({n:r.name,s:m.d+(m.f?' · '+m.f:''),txt:(r.name+' '+m.d+' '+(m.f||'')+' '+(r.det||'')).toLowerCase(),go:()=>{GP.kinds.delete(r.kind);const after=()=>{gpShowCheck(r,false);GP.V.focus(r.x,r.y,2.5)};if(GP.mode!=='d'||GP.dm!==mi){GP.mode='d';GP.dm=mi;gpModesOn();gpRender(true).then(after)}else{gpDgMarkers();gpDgSide(true);after()}}})));
  [...new Set(D.m.map(m=>m.d))].forEach(n=>{const mi=D.m.findIndex(m=>m.d===n);out.unshift({n,s:'Dungeon map',txt:n.toLowerCase()+' dungeon',go:()=>{GP.mode='d';GP.dm=mi;gpModesOn();gpRender(true)}})})}
 return out}
function gpModesOn(){document.querySelectorAll('.gpmodes button').forEach(b=>b.classList.toggle('on',b.dataset.m===GP.mode))}
function gpSearchInit(box){const inp=box.querySelector('input'),res=box.querySelector('.gpres');let idx=null,gid=null,list=[],sel=0;
 const run=()=>{if(gid!==GP.g.id){idx=gpIndex();gid=GP.g.id}const q=inp.value.trim().toLowerCase();if(!q){res.classList.remove('open');return}
  const ws=q.split(/\s+/);list=idx.filter(x=>ws.every(w=>x.txt.includes(w))).sort((a,b)=>(b.n.toLowerCase().startsWith(q)?1:0)-(a.n.toLowerCase().startsWith(q)?1:0)).slice(0,60);sel=0;
  res.innerHTML=list.map((x,i)=>`<div data-i="${i}" class="${i?'':'sel'}">${esc(x.n)}<small>${esc(x.s)}</small></div>`).join('')||'<div style="color:var(--mute);cursor:default">No matches</div>';res.classList.add('open');
  res.querySelectorAll('[data-i]').forEach(d=>d.onclick=()=>pick(+d.dataset.i))};
 const pick=i=>{const x=list[i];if(!x)return;res.classList.remove('open');inp.blur();x.go()};
 inp.addEventListener('input',run);inp.addEventListener('focus',()=>{if(inp.value)run()});
 inp.addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();sel=Math.max(0,Math.min(list.length-1,sel+(e.key==='ArrowDown'?1:-1)));res.querySelectorAll('[data-i]').forEach((d,i)=>d.classList.toggle('sel',i===sel));res.querySelector('.sel')?.scrollIntoView({block:'nearest'})}
  else if(e.key==='Enter'){pick(sel)}else if(e.key==='Escape'){inp.value='';res.classList.remove('open');inp.blur()}});
 document.addEventListener('click',e=>{if(!box.contains(e.target))res.classList.remove('open')});
 GP.resetSearch=()=>{gid=null}}

// ---------- progress export/import ----------
function gpDataBlock(){return `<h4>Your data</h4><div class="gpsync">${typeof syText==='function'?syText():''}</div><div class="gprow"><button class="gplink" data-x="exp">Export progress</button>·<button class="gplink" data-x="imp">Import</button>·<button class="gplink" data-x="rst">Reset this game</button></div><div style="color:var(--mute);font-size:11.5px">Found markers, notes and settings are always saved on this device too.</div>`}
function gpDataWire(side){side.querySelector('[data-x="exp"]').onclick=()=>{const o={};ZS.keys().forEach(k=>{try{o[k]=JSON.parse(localStorage.getItem(k))}catch(e){}});
  gpModal(`<h3>Export progress</h3><p>Copy this text and keep it somewhere safe, or paste it into Import on another device.</p><textarea readonly>${esc(JSON.stringify({zeldamaps:1,data:o}))}</textarea><div class="gprow" style="margin-top:8px"><button class="gpbtn on" data-do="copy">Copy</button><button class="gpbtn" data-do="close">Close</button></div>`);
  const m=document.querySelector('.gpmodal');m.querySelector('[data-do="copy"]').onclick=e=>{const ta=m.querySelector('textarea');ta.select();try{navigator.clipboard.writeText(ta.value).catch(()=>document.execCommand('copy'))}catch(_){document.execCommand('copy')}e.target.textContent='Copied'}};
 side.querySelector('[data-x="imp"]').onclick=()=>{gpModal(`<h3>Import progress</h3><p>Paste exported text. It is merged with what is saved here; matching entries are replaced.</p><textarea placeholder='{"zeldamaps":1,…}'></textarea><div class="gprow" style="margin-top:8px"><button class="gpbtn on" data-do="go">Import</button><button class="gpbtn" data-do="close">Cancel</button><span class="msg" style="color:var(--mute)"></span></div>`);
  const m=document.querySelector('.gpmodal');m.querySelector('[data-do="go"]').onclick=()=>{try{const o=JSON.parse(m.querySelector('textarea').value);if(!o.zeldamaps)throw 0;Object.entries(o.data).forEach(([k,v])=>{if(k.startsWith('zm:'))localStorage.setItem(k,JSON.stringify(v))});m.classList.remove('open');const g=GP.g.id;GP.g=null;gpOpen(g,GP.mode,GP.mode==='d'?GP.dm:GP.tab)}catch(e){m.querySelector('.msg').textContent='That text is not a valid export.'}}};
 side.querySelector('[data-x="rst"]').onclick=()=>{gpModal(`<h3>Reset ${esc(gTitle(GP.g))}?</h3><p>This clears every found marker for this game. Notes and settings stay. It can't be undone unless you exported first.</p><div class="gprow"><button class="gpbtn on" data-do="go">Reset found markers</button><button class="gpbtn" data-do="close">Cancel</button></div>`);
  document.querySelector('.gpmodal [data-do="go"]').onclick=()=>{GP.done.clear();gpSaveDone();document.querySelector('.gpmodal').classList.remove('open');gpRender(false)}}}
function gpModal(html){const m=document.querySelector('.gpmodal');m.firstElementChild.innerHTML=html;m.classList.add('open');m.querySelectorAll('[data-do="close"]').forEach(b=>b.onclick=()=>m.classList.remove('open'));m.querySelectorAll('textarea').forEach(t=>t.addEventListener('keydown',e=>e.stopPropagation()))}
function gpHelp(){gpModal(`<h3>Shortcuts and controls</h3><table>
<tr><td><kbd>/</kbd></td><td>Search markers, checks and dungeons</td></tr><tr><td><kbd>+</kbd> <kbd>−</kbd> <kbd>0</kbd></td><td>Zoom in, zoom out, reset</td></tr>
<tr><td><kbd>←</kbd><kbd>↑</kbd><kbd>→</kbd><kbd>↓</kbd></td><td>Pan the map</td></tr><tr><td><kbd>[</kbd> <kbd>]</kbd></td><td>Previous / next map version or dungeon floor</td></tr>
<tr><td><kbd>,</kbd> <kbd>.</kbd></td><td>Previous / next dungeon</td></tr><tr><td><kbd>O</kbd> <kbd>D</kbd></td><td>Overworld / Dungeons</td></tr>
<tr><td><kbd>Space</kbd></td><td>Mark the selected marker found</td></tr><tr><td><kbd>H</kbd></td><td>Hide found markers</td></tr><tr><td><kbd>L</kbd></td><td>Show or hide place-name labels</td></tr><tr><td><kbd>X</kbd></td><td>Flip markers and names to the blended map</td></tr>
<tr><td><kbd>N</kbd></td><td>Add a note to the map</td></tr><tr><td><kbd>F</kbd></td><td>Fullscreen</td></tr><tr><td><kbd>Esc</kbd></td><td>Close the popup, or go back to all maps</td></tr></table>
<h3 style="margin-top:14px">Controller</h3><table>
<tr><td>Left stick</td><td>Pan smoothly (on the bottom screen: scroll)</td></tr><tr><td>Right stick ↕ · L2 / R2</td><td>Zoom out / in</td></tr>
<tr><td>A</td><td>Open the marker under the crosshair; again to mark it found</td></tr><tr><td>B</td><td>Close the popup, or go back</td></tr>
<tr><td>X</td><td>Hide found markers (bottom screen: tick the highlighted check)</td></tr><tr><td>Y</td><td>Search</td></tr>
<tr><td>L1 / R1 · D-pad ← →</td><td>Previous / next map version or floor</td></tr><tr><td>D-pad ↑ ↓</td><td>Previous / next dungeon (bottom screen: move through the list)</td></tr>
<tr><td>Start · L3/R3</td><td>Overworld ⇄ Dungeons · reset zoom</td></tr><tr><td>Select</td><td>Dual screen: move the controller between the map and the bottom screen (the active one has a blue frame). Single screen: this help</td></tr></table>
<p style="color:var(--mute)">Mouse: scroll to zoom, drag (or flick) to pan, double-click to zoom in (Shift to zoom out). Touch: pinch, drag and flick; press and hold a marker to mark it found. When zoomed in, tap the overview map in the corner to jump. Every tick shows an Undo button for a few seconds. Spoiler-free hides markers until you reveal their region (tap the map) or dungeon. Checklist can group by type or by region; regions come from each map's own region names, or compass areas where a map has none. Double-click a layer group title to toggle the whole group. The numbers at the bottom right are the cursor position in % of the map, handy for reporting a misplaced marker.</p>
<div class="gprow"><button class="gpbtn on" data-do="close">Close</button></div>`)}
function gpKeys(e){if(!document.body.classList.contains('gp-on'))return;if(e.target.matches('input,textarea,select')&&e.target.type!=='checkbox'&&e.target.type!=='range')return;if(e.ctrlKey||e.metaKey||e.altKey)return;
 const V=GP.V,k=e.key,modal=document.querySelector('.gpmodal.open');
 if(modal){if(k==='Escape')modal.classList.remove('open');return}
 const step=60;let used=true;
 if(k==='/'){document.querySelector('.gpsearch input').focus()}
 else if(k==='+'||k==='='){V.zoomBy(1.5)}else if(k==='-'||k==='_'){V.zoomBy(1/1.5)}else if(k==='0'){V.reset()}
 else if(k==='ArrowLeft'){V.tx+=step;V.apply()}else if(k==='ArrowRight'){V.tx-=step;V.apply()}else if(k==='ArrowUp'){V.ty+=step;V.apply()}else if(k==='ArrowDown'){V.ty-=step;V.apply()}
 else if(k==='f'||k==='F'){gpFull()}
 else if(k==='h'||k==='H'){const c=document.querySelector('.gpside .gphide');if(c){c.checked=!c.checked;c.onchange({target:c})}}
 else if((k==='x'||k==='X')&&GP.mode==='o'){gpFlip()}
 else if(k==='l'||k==='L'){const c=document.querySelector('.gpside .gplbl');if(c){c.checked=!c.checked;c.onchange({target:c})}}
 else if(k==='n'||k==='N'){gpNoteMode()}
 else if(k==='o'||k==='O'){if(GP.mode!=='o')gpGo('o')}else if(k==='d'||k==='D'){if(GP.mode!=='d'&&hasDG(GP.g.id))gpGo('d')}
 else if(k==='['||k===']'){const dir=k===']'?1:-1;if(GP.mode==='o'){const T=gpModel(GP.g).tabs,n=T.length;let q=GP.tab;do{q=(q+dir+n)%n}while(T[q].hid&&q!==GP.tab);GP.tab=q;V.close();gpRender(true)}else{const D=DUNG[GP.g.id].m,cur=D[GP.dm];const fl=D.map((m,i)=>[m,i]).filter(([m])=>m.d===cur.d).map(x=>x[1]);const p=fl.indexOf(GP.dm);GP.dm=fl[(p+dir+fl.length)%fl.length];V.close();gpRender(true)}}
 else if((k===','||k==='.')&&GP.mode==='d'){const D=DUNG[GP.g.id].m;const names=[...new Set(D.map(m=>m.d))];const p=names.indexOf(D[GP.dm].d);const nn=names[(p+(k==='.'?1:-1)+names.length)%names.length];GP.dm=D.findIndex(m=>m.d===nn);V.close();gpRender(true)}
 else if(k===' '){if(GP.sel&&(GP.mode==='d'||(GP.sel.c?.chk&&!GP.mkForeign)))gpToggle(GP.sel.u);else used=false}
 else if(k==='Escape'){if(GP.notemode)gpNoteMode();else if(V.pop.classList.contains('open'))V.close();else if(document.getElementById('gp').classList.contains('gpmax'))gpMax(false);else if(document.fullscreenElement)document.exitFullscreen();else location.hash='#/'}
 else if(k==='?'){gpHelp()}else used=false;
 if(used)e.preventDefault()}

// ---------- router + home ----------
let homeY=0;
function gpRoute(){const h=decodeURIComponent(location.hash);const m=h.match(/^#\/g\/(\w+)(?:\/([od])(?:\/(\d+))?)?/);
 if(m){if(!document.body.classList.contains('gp-on'))homeY=scrollY;gpOpen(m[1],m[2]||'o',m[3]!=null?+m[3]:null);window.scrollTo(0,0)}
 else if(document.body.classList.contains('gp-on')){document.body.classList.remove('gp-on');document.title=GP.homeTitle||document.title;GP.g&&ZS.set('last',GP.g.id);GP.navDraw&&GP.navDraw();hideTip();if(typeof ZD!=='undefined'){ZD.role==='panel'&&zdHome();zdState()}requestAnimationFrame(()=>window.scrollTo(0,homeY))}}
function barAuto(){const bar=document.querySelector('body>main>.bar,main .bar');if(!bar)return;let lastY=scrollY,hideT=0,home0=0;
 const natural=()=>{if(getComputedStyle(bar).position!=='sticky')return 1e9;const m=bar.parentElement;return m.getBoundingClientRect().top+scrollY+(parseFloat(getComputedStyle(bar).marginTop)||0)};
 const show=()=>{bar.classList.remove('bar-hide');clearTimeout(hideT);hideT=setTimeout(()=>{if(!bar.matches(':hover,:focus-within')&&scrollY>natural()+40)bar.classList.add('bar-hide')},2500)};
 const hide=()=>{clearTimeout(hideT);if(!bar.matches(':focus-within'))bar.classList.add('bar-hide')};
 addEventListener('scroll',()=>{if(document.body.classList.contains('gp-on'))return;const y=scrollY,dy=y-lastY;lastY=y;
  if(y<=natural()+10){bar.classList.remove('bar-hide');clearTimeout(hideT);return}
  if(dy>4)hide();else if(dy<-4)show()},{passive:true});
 bar.addEventListener('mouseleave',()=>{if(scrollY>natural()+40)show()});
 bar.addEventListener('focusin',()=>bar.classList.remove('bar-hide'))}
function gpHome(){barAuto();GP.homeTitle=document.title;
 const hd=document.querySelector('header');const nav=document.createElement('div');nav.className='agesw';
 const navDraw=()=>{const last=ZS.get('last',null),lg=GAMES.find(x=>x.id===last);const seq=GAMES.map((g,i)=>[g,i]).sort((a,b)=>a[0].y-b[0].y||a[1]-b[1]).map(x=>x[0]);
  nav.innerHTML=`<nav class="ages" aria-label="Games by release year"><ol>${seq.map(g=>{const n=ZS.get('done:'+g.id,[]).length;return `<li><a href="#/g/${g.id}" class="${g.id===last?'last':''}" title="${esc(g.t)}"><span class="y">${g.y}</span><span class="th"><img src="maps/${g.img}" alt="" loading="lazy">${hasDG(g.id)?`<span class="dgb">${new Set(DUNG[g.id].m.map(m=>m.d).filter(d=>!/^(Area|Interior) ·/.test(d))).size} dungeons</span>`:''}</span><span class="t">${esc(gTitle(g))}</span>${n?`<span class="m"><b>${n} found</b></span>`:''}</a></li>`}).join('')}</ol></nav>`+(lg?`<a class="cont" href="#/g/${lg.id}">Continue ${esc(gTitle(lg))}</a>`:'')};
 navDraw();GP.navDraw=navDraw;hd.appendChild(nav);const ag=()=>{const a=nav.querySelector('.ages');if(a)a.classList.toggle('end',a.scrollLeft+a.clientWidth>=a.scrollWidth-4)};nav.addEventListener('scroll',ag,true);setTimeout(ag,50);
 const sec=document.getElementById('dungeons');if(sec){sec.className='dghome';sec.innerHTML=Object.keys(DUNG).map(id=>{const D=DUNG[id];const n=new Set(D.m.map(m=>m.d)).size;const c=D.m.reduce((a,m)=>a+m.it.length,0);return `<a href="#/g/${id}/d/0"><b>${esc(D.t)}</b><small>${n} dungeons and areas · ${D.m.length} maps · ${c} checks</small></a>`}).join('')}
 window.addEventListener('hashchange',()=>{gpRoute();zmMark()});gpRoute();zmBoot();zmMark()}

// ---------- crash guard: if the app dies while a game page is open, reopen that game in safe mode ----------
function zmIsPanel(){try{return !!(window.ZDual&&ZDual.role&&ZDual.role()==='panel')}catch(e){return false}}
function zmSafeList(){try{return JSON.parse(localStorage.getItem('zm_safe')||'[]')}catch(e){return []}}
function zmSafe(g){return !!g&&zmSafeList().includes(g.id)}
function zmMark(){if(zmIsPanel())return;try{const on=document.body.classList.contains('gp-on')&&GP.g&&document.visibilityState!=='hidden';
 if(on)localStorage.setItem('zm_open',GP.g.id);else localStorage.removeItem('zm_open')}catch(e){}}
['visibilitychange','pagehide'].forEach(ev=>addEventListener(ev,()=>{if(ev==='pagehide'){try{if(!zmIsPanel())localStorage.removeItem('zm_open')}catch(e){}}else zmMark()}));
function zmBoot(){if(zmIsPanel())return;let gid=null,why='';try{gid=localStorage.getItem('zm_open');localStorage.removeItem('zm_open')}catch(e){}
 try{if(window.ZDual&&ZDual.lastCrash)why=ZDual.lastCrash()||''}catch(e){}
 if(!gid&&!why)return;const g=gid&&GAMES.find(x=>x.id===gid);
 if(g){const L=zmSafeList();if(!L.includes(g.id)){L.push(g.id);try{localStorage.setItem('zm_safe',JSON.stringify(L))}catch(e){}}}
 const what=why==='crash'?'the map view crashed':why==='kill'?'Android closed the map view to free memory':'the app closed unexpectedly';
 const b=document.createElement('div');b.className='zmcrash';b.setAttribute('role','alert');
 b.innerHTML=`<b>Last time ${esc(what)}${g?' on '+esc(gTitle(g)):''}.</b> ${g?'Simple labels are on for that game to keep it stable.':''} <button data-a="ok">OK</button>${g?' <button data-a="off">Turn safe mode off</button>':''}`;
 b.onclick=e=>{const a=e.target.dataset.a;if(!a)return;if(a==='off'){try{localStorage.setItem('zm_safe',JSON.stringify(zmSafeList().filter(x=>x!==g.id)))}catch(e){}if(GP.g&&GP.g.id===g.id)gpRender(true)}b.remove()};
 document.body.appendChild(b)}

// 1.9.5: the 1.9 crash was the home page's <details> folds, not labels, so retire test switches and safe-mode entries once
try{localStorage.removeItem('zm_dbg');if(!localStorage.getItem('zm_m195')){localStorage.removeItem('zm_safe');localStorage.setItem('zm_m195','1')}}catch(e){}

addEventListener('resize',()=>{if(GP.lbls&&GP.V)gpLblSched(true)});

// ---------- deep zoom: sharper tiles for maps that have a high-resolution source ----------
// levels: [width,height,cols,rows] of the tiled image, aligned exactly to the base map.
const HDMAPS={"alttp_dark.webp":{"pre":"hdalttpdark","base":1500,"lv":{"2":[2048,2048,4,4]},"px":1},"alttp_light.webp":{"pre":"hdalttplight","base":1500,"lv":{"2":[3536,3536,7,7]},"px":1},"aol_full.webp":{"pre":"hdaolfull","base":1600,"lv":{"2":[3128,2127,7,5]},"px":1},"eow.webp":{"pre":"hdeow","base":1500,"lv":{"2":[3601,2442,8,5]}},"la.webp":{"pre":"hdla","base":1500,"lv":{"2":[2800,1600,6,4]},"px":1},"loz.webp":{"pre":"hdloz","base":2400,"lv":{"2":[4354,1408,9,3]},"px":1},"mc.webp":{"pre":"hdmc","base":800,"lv":{"2":[1600,1016,4,2],"3":[3200,2032,7,4]},"px":1},"mc_full.webp":{"pre":"hdmcfull","base":1500,"lv":{"2":[3000,2380,6,5],"3":[3982,3159,8,7]},"px":1},"ooa_past.webp":{"pre":"hdooapast","base":1000,"lv":{"2":[2240,1792,5,4]},"px":1},"ooa_present.webp":{"pre":"hdooapresent","base":1500,"lv":{"2":[2240,1792,5,4]},"px":1},"oos_spring.webp":{"pre":"hdoosspring","base":1000,"lv":{"2":[2560,2048,5,4]},"px":1},"oos_summer.webp":{"pre":"hdoossummer","base":1500,"lv":{"2":[2560,2048,5,4]},"px":1},"oos_autumn.webp":{"pre":"hdoosautumn","base":1000,"lv":{"2":[2560,2048,5,4]},"px":1},"oos_winter.webp":{"pre":"hdooswinter","base":1000,"lv":{"2":[2560,2048,5,4]},"px":1},"oot.webp":{"pre":"hdoot","base":1500,"lv":{"2":[1982,1440,4,3]}},"oot_original.webp":{"pre":"hdootoriginal","base":1500,"lv":{"2":[2838,1960,6,4]}},"ph.webp":{"pre":"hdph","base":512,"lv":{"2":[1025,768,3,2]},"px":1},"ph_full.webp":{"pre":"hdphfull","base":1600,"lv":{"2":[3200,2416,7,5],"3":[5619,4242,11,9]}},"ss_hd.webp":{"pre":"hdsshd","base":2400,"lv":{"2":[3461,1957,7,4]}},"ss_surface.webp":{"pre":"hdsssurface","base":1500,"lv":{"2":[2272,1267,5,3]}},"st.webp":{"pre":"hdst","base":512,"lv":{"2":[1024,768,2,2]},"px":1},"totk_depths.webp":{"pre":"hdtotkdepths","base":1500,"lv":{"2":[3000,2400,6,5],"3":[5700,4560,12,9]}},"tp.webp":{"pre":"hdtp","base":569,"lv":{"2":[1191,1256,3,3]}},"tp_hd.webp":{"pre":"hdtphd","base":1476,"lv":{"2":[2543,2584,5,6]}},"tp_labeled.webp":{"pre":"hdtplabeled","base":1078,"lv":{"2":[2250,3131,5,7]}},"ww.webp":{"pre":"hdww","base":1500,"lv":{"2":[3238,2591,7,6]}},"ww_sea.webp":{"pre":"hdwwsea","base":2000,"lv":{"2":[4000,1890,8,4],"3":[7584,3583,15,7]}},"botw.webp":{"pre":"hdbotw","base":1500,"lv":{"2":[3000,2400,6,5],"3":[5000,4000,10,8]}},"totk_surface.webp":{"pre":"hdtotksurface","base":1500,"lv":{"2":[3000,2400,6,5],"3":[6000,4800,12,10]}},"xa_albw_on_alttp.webp":{"pre":"hdxaalbwonalttp","base":1500,"lv":{"2":[3536,3536,7,7]}},"xa_lorule_on_alttp.webp":{"pre":"hdxaloruleonalttp","base":1500,"lv":{"2":[3536,3536,7,7]}},"xa_eow_on_alttp.webp":{"pre":"hdxaeowonalttp","base":1500,"lv":{"2":[3536,3536,7,7]}},"xa_alttp_on_albw.webp":{"pre":"hdxaalttponalbw","base":1500,"lv":{"2":[3072,3072,6,6]}},"xa_dark_on_albw.webp":{"pre":"hdxadarkonalbw","base":1500,"lv":{"2":[3072,3072,6,6]}},"xa_eow_on_albw.webp":{"pre":"hdxaeowonalbw","base":1500,"lv":{"2":[3072,3072,6,6]}},"xa_alttp_on_eow.webp":{"pre":"hdxaalttponeow","base":1500,"lv":{"2":[3600,2441,8,5]}},"xa_albw_on_eow.webp":{"pre":"hdxaalbwoneow","base":1500,"lv":{"2":[3600,2441,8,5]}}};
function gpHdMk(img,L){return img&&HDMAPS[img]&&L?{cfg:HDMAPS[img],img,el:L,tiles:new Map(),lv:0,s:0,p:null}:null}
function gpHdSet(img){const V=GP.V;if(!V)return;const L=V.mk.parentNode.querySelector('.gvhd');if(!L)return;
 if(GP.hd&&GP.hd.img===img)return gpHdSched(true);
 GP.hd=gpHdMk(img,L);L.innerHTML='';V.onhd=gpHdSched;gpHdSched(true)}
// sharper tiles for the blend overlay; drawn in their own layer above it, at the overlay's opacity
function gpHdSetO(img,op){const V=GP.V;if(!V)return;const L=V.mk.parentNode.querySelector('.gvhdo');if(!L)return;
 L.style.opacity=op||0;if(!op)img=null;
 if(GP.hdo&&GP.hdo.img===img)return;GP.hdo=gpHdMk(img,L);L.innerHTML='';V.ovl.style.visibility='';V.onhd=gpHdSched;gpHdSched(true)}
function gpHdAll(){return [GP.hd,GP.hdo].filter(Boolean)}
function gpHdSched(force){const V=GP.V;if(!V)return;const Hs=gpHdAll();if(!Hs.length)return;
 clearTimeout(GP.hdEnd);GP.hdEnd=setTimeout(()=>gpHdAll().forEach(gpHdUpdate),160);
 if(force===true){Hs.forEach(gpHdUpdate);return}if(GP.hdRaf)return;const host=V.mk.closest('.gv'),cw=host.clientWidth||1,ch=host.clientHeight||1,H=Hs[0];
 const dz=H.s?Math.abs(Math.log(V.s/H.s)):9,dp=H.p?Math.hypot(V.tx-H.p[0],V.ty-H.p[1])/Math.max(cw,ch):9;
 if(host.classList.contains('zooming')||(dz<0.15&&dp<0.25))return;GP.hdRaf=requestAnimationFrame(()=>{GP.hdRaf=0;gpHdAll().forEach(gpHdUpdate)})}
const HD_MAXT=20; // tiles on screen at once; beyond this a coarser level is used (keeps phones smooth)
function gpHdUpdate(H){const V=GP.V;if(!H||!V||(H!==GP.hd&&H!==GP.hdo))return;H.s=V.s;H.p=[V.tx,V.ty];
 const host=V.mk.closest('.gv'),cw=host.clientWidth,ch=host.clientHeight,dpr=Math.min(2,window.devicePixelRatio||1);
 const need=V.W*V.s*dpr/H.cfg.base,LV=Object.keys(H.cfg.lv).map(Number).sort((a,b)=>a-b);
 // visible map area in map-CSS px, plus a small margin
 const mx0=(-(V.ox+V.tx)-cw*.15)/V.s,mx1=(cw*1.15-(V.ox+V.tx))/V.s,my0=(-(V.oy+V.ty)-ch*.15)/V.s,my1=(ch*1.15-(V.oy+V.ty))/V.s,TS=512;
 const span=l=>{const [LW,LH,NX,NY]=H.cfg.lv[l],k=LW/V.W;const r=[Math.max(0,Math.floor(mx0*k/TS)),Math.min(NX-1,Math.floor(mx1*k/TS)),Math.max(0,Math.floor(my0*k/TS)),Math.min(NY-1,Math.floor(my1*k/TS))];r.n=(r[1]-r[0]+1)*(r[3]-r[2]+1);return r};
 let i=-1;
 if(need>1.4){i=LV.length-1;for(let j=0;j<LV.length;j++)if(H.cfg.lv[LV[j]][0]/H.cfg.base*1.25>=need){i=j;break}
  while(i>=0&&span(LV[i]).n>HD_MAXT)i--}
 const lv=i<0?0:LV[i];
 H.el.classList.toggle('px',!!(H.cfg.px&&lv&&need>H.cfg.lv[lv][0]/H.cfg.base*1.05));
 const want=new Set();
 if(lv){const [LW,LH]=H.cfg.lv[lv],[tx0,tx1,ty0,ty1]=span(lv);
  for(let ty=ty0;ty<=ty1;ty++)for(let tx=tx0;tx<=tx1;tx++){const key=lv+'_'+tx+'_'+ty;want.add(key);if(H.tiles.has(key))continue;
   const im=document.createElement('img');im.alt='';im.decoding='async';im.draggable=false;
   const w=Math.min(TS,LW-tx*TS),h=Math.min(TS,LH-ty*TS);
   im.style.cssText=`left:${tx*TS/LW*100}%;top:${ty*TS/LH*100}%;width:${w/LW*100}%;height:${h/LH*100}%;z-index:${lv}`;
   im.onload=()=>{im.classList.add('on');if(H.wait){H.wait=0;setTimeout(()=>gpHdUpdate(H),250)}};H.tiles.set(key,im);H.el.appendChild(im);
   dgSrc('dg/'+H.cfg.pre+key+'.webp').then(src=>{if(H.tiles.get(key)===im)im.src=src})}}
 // drop tiles we no longer need, but keep other levels under the new ones until those have loaded
 const pending=[...want].some(k=>!H.tiles.get(k).classList.contains('on'));H.wait=pending?1:0;
 // the blend's sharp tiles replace its low-res image once they are all in (otherwise the two stack and the blur shows through)
 if(H===GP.hdo)V.ovl.style.visibility=lv&&!pending?'hidden':'';
 H.tiles.forEach((im,key)=>{if(want.has(key))return;if(pending&&lv&&+key.split('_')[0]!==lv)return;im.remove();H.tiles.delete(key)});
 H.lv=lv}
