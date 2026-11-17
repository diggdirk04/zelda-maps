// ================= dual-screen mode =================
// main screen: map only. panel screen: game list, layers, checklists, search.
// Transport: Android bridge (window.ZDual) on dual-screen handhelds, BroadcastChannel for a pop-out window on desktop.
const ZD={role:'solo',rx:false,last:'',native:false,bc:null,peer:false};
function zdSend(o){const s=JSON.stringify(o);try{if(ZD.native)ZDual.send(s);else if(ZD.bc)ZD.bc.postMessage(s)}catch(e){}}
function zdSnap(){const g=GP.g;const home=!document.body.classList.contains('gp-on');
 return {t:'state',hash:home?'#/':location.hash,gid:home||!g?null:g.id,on:[...GP.on],done:[...GP.done],hide:GP.hide,lbl:GP.lbl,ms:GP.ms,kinds:[...GP.kinds],spoil:GP.spoil,rev:[...GP.rev],grp:GP.grp,bl:GP.bl||null}}
function zdState(){if(ZD.rx||ZD.role==='solo'||(ZD.role==='panel'&&!ZD.synced))return;const o=zdSnap(),s=JSON.stringify(o);if(s===ZD.last)return;ZD.last=s;zdSend(o)}
function zdSel(u){if(ZD.rx||ZD.role==='solo')return;zdSend({t:'sel',u})}
function zdRole(r){ZD.role=r;document.body.classList.toggle('zd-main',r==='main');document.body.classList.toggle('zd-panel',r==='panel');
 zdButtons();if(GP.V)setTimeout(()=>GP.V.layout(),30);if(r==='main'){ZD.last='';zdState();typeof PAD!=='undefined'&&zdSend({t:'pad',owner:PAD.owner})}if(r==='solo'&&typeof PAD!=='undefined'){PAD.owner='main';padFrame()}if(r==='panel'){ZD.synced=false;zdHome()}}
function zdFind(u){if(!GP.g)return null;if(GP.mode==='o'){for(const c of gpModel(GP.g).cats)for(const r of c.it)if(r.u===u)return r;return null}
 return (dgItems(GP.g.id)[GP.dm]||[]).find(r=>r.u===u)||null}
function zdRecv(s){let m;try{m=typeof s==='string'?JSON.parse(s):s}catch(e){return}
 if(m.t==='hello'){if(ZD.role==='solo'&&!ZD.native)zdRole('main');ZD.last='';zdState();typeof PAD!=='undefined'&&zdSend({t:'pad',owner:PAD.owner});return}
 if(m.t==='bye'){if(!ZD.native&&ZD.role==='main')zdRole('solo');return}
 if(m.t==='req'){ZD.last='';zdState();return}
 if(m.t==='pad'){if(typeof padOwner==='function')padOwner(m.owner,true);return}
 ZD.rx=true;try{
  if(m.t==='state'){ZD.last=JSON.stringify(m);ZD.synced=true;
   if(m.gid&&(!GP.g||GP.g.id!==m.gid||location.hash!==m.hash)){history.replaceState(null,'',m.hash);gpRoute()}
   else if(!m.gid&&document.body.classList.contains('gp-on')){history.replaceState(null,'','#/');gpRoute()}
   const core=JSON.stringify(Object.assign({},m,{bl:null}));if(m.gid&&GP.g&&GP.g.id===m.gid&&ZD.core===core&&location.hash===m.hash){GP.bl=m.bl||null;gpBlendApply();return}ZD.core=core;
   if(m.gid&&GP.g&&GP.g.id===m.gid){GP.on=new Set(m.on);GP.done=new Set(m.done);GP.hide=m.hide;GP.lbl=m.lbl;GP.ms=m.ms;GP.kinds=new Set(m.kinds);GP.spoil=!!m.spoil;GP.rev=new Set(m.rev||[]);GP.grp=m.grp||'cat';GP.bl=m.bl||null;ZS.set('done:'+m.gid,m.done);
    Promise.resolve(GP.busy).then(()=>{ZD.rx=true;try{gpRender(false)}finally{ZD.rx=false}})}}
  else if(m.t==='sel'){Promise.resolve(GP.busy).then(()=>{const r=zdFind(m.u);if(!r)return;ZD.rx=true;try{
    if(GP.mode==='o'){gpShowItem(r);if(ZD.role==='main')GP.V.focus(r.x,r.y,Math.max(GP.V.s,2))}else gpShowCheck(r,ZD.role==='main')}finally{ZD.rx=false}})}
 }finally{ZD.rx=false}}
function zdButtons(){const bar=document.querySelector('.gpbar');if(!bar)return;let b=bar.querySelector('.zdbtn');
 const can=ZD.native?(()=>{try{return ZDual.hasSecond()}catch(e){return false}})():true;
 if(!b){b=document.createElement('button');b.className='gpbtn zdbtn';bar.insertBefore(b,bar.querySelector('.gpside-t'));b.onclick=zdToggle}
 b.style.display=can&&ZD.role!=='panel'?'':'none';
 const lbl=ZD.role==='main'?(ZD.native?'Single screen':'Close panel'):(ZD.native?'Dual screen':'Pop out');b.innerHTML='⧉<span class="zt"> '+lbl+'</span>';b.setAttribute('aria-label',lbl);
 b.title=ZD.native?'Put the layers, checklists and search on the second screen':'Open the side panel in its own window (for a second monitor)'}
function zdToggle(){if(ZD.native){try{ZD.role==='main'?ZDual.closePanel():ZDual.openPanel()}catch(e){}return}
 if(ZD.role==='main'){zdSend({t:'close'});zdRole('solo');return}
 const u=location.href.split('#')[0].split('?')[0]+'?panel=1'+location.hash;const w=window.open(u,'zmpanel','width=420,height=760');if(!w){gpModal('<h3>Pop-up blocked</h3><p>Allow pop-ups for this page to open the panel in its own window.</p><div class="gprow"><button class="gpbtn on" data-do="close">OK</button></div>')}}
function zdHome(){let h=document.getElementById('zdhome');if(!h){h=document.createElement('div');h.id='zdhome';document.body.appendChild(h)}
 const last=ZS.get('last',null);
 h.innerHTML=`<h2>Zelda Maps</h2><p>Pick a game. The map opens on the other screen.</p>${last&&GAMES.find(g=>g.id===last)?`<a class="cont" href="#/g/${last}">▶ Continue: ${esc(gTitle(GAMES.find(g=>g.id===last)))}</a>`:''}<div class="zdgl">${GAMES.map(g=>{const n=ZS.get('done:'+g.id,[]).length;return `<a href="#/g/${g.id}"><b>${esc(gTitle(g))}</b><small>${g.y}${hasDG(g.id)?' · dungeons':''}${n?' · ✓'+n:''}</small></a>`}).join('')}</div>`}
(function zdInit(){
 try{if(window.ZDual&&ZDual.role){ZD.native=true;ZD.role=ZDual.role()}}catch(e){}
 if(!ZD.native&&/[?&]panel=1/.test(location.search))ZD.role='panel';
 if(!ZD.native&&typeof BroadcastChannel!=='undefined'){try{ZD.bc=new BroadcastChannel('zm-dual');ZD.bc.onmessage=e=>{let m;try{m=JSON.parse(e.data)}catch(_){return}if(m.t==='close'&&ZD.role==='panel'){window.close();return}zdRecv(m)}}catch(e){}}
 window.zdRecv=zdRecv;window.zdRole=zdRole;
 if(ZD.role==='panel'){window.addEventListener('beforeunload',()=>zdSend({t:'bye'}))}
 document.addEventListener('DOMContentLoaded',()=>{});
 setTimeout(()=>{zdRole(ZD.role);if(ZD.role==='panel'){zdSend({t:'hello'});zdSend({t:'req'})}},0)})();
