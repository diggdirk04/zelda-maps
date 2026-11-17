// ================= controller support =================
// Gamepad API polling: reading it makes Android WebView hand stick/button input to the page instead of scrolling natively.
const PAD={owner:'main',v:{x:0,y:0},z:0,prev:[],t:0,active:false,keys:new Map(),hl:-1,lastSeen:0};
const PB={A:0,B:1,X:2,Y:3,L1:4,R1:5,L2:6,R2:7,SEL:8,START:9,L3:10,R3:11,UP:12,DOWN:13,LEFT:14,RIGHT:15};
const dz=(v,d)=>{const a=Math.abs(v);if(a<d)return 0;const n=(a-d)/(1-d);return Math.sign(v)*n*n};
function padMine(){const r=typeof ZD!=='undefined'?ZD.role:'solo';return r==='solo'||r===PAD.owner}
function padOwner(o,quiet){PAD.owner=o;PAD.v.x=PAD.v.y=0;PAD.z=0;PAD.hl=-1;document.querySelectorAll('.padhl').forEach(e=>e.classList.remove('padhl'));padFrame();
 if(!quiet&&typeof zdSend==='function')zdSend({t:'pad',owner:o});padToast();padFlash()}
function padFrame(){}
function padFlash(){const r=typeof ZD!=='undefined'?ZD.role:'solo';if(r==='solo'||r!==PAD.owner)return;const b=document.body;b.classList.add('padflash');clearTimeout(PAD.fh);PAD.fh=setTimeout(()=>b.classList.remove('padflash'),700)}
function padToast(){const r=typeof ZD!=='undefined'?ZD.role:'solo';if(r==='solo'||r!==PAD.owner)return;let t=document.getElementById('padtoast');if(!t){t=document.createElement('div');t.id='padtoast';document.body.appendChild(t)}
 t.textContent=r==='main'?'Controller: map':'Controller: this screen';t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('on'),1400)}
function padActive(on){if(PAD.active===on)return;PAD.active=on;document.body.classList.toggle('gpad',on);padFrame()}
function padRet(){const h=document.getElementById('gpv');if(h&&!h.querySelector('.gvret')){const r=document.createElement('div');r.className='gvret';h.appendChild(r)}}
function padNearest(){const V=GP.V;if(!V)return null;const hr=V.host.getBoundingClientRect(),cx=hr.left+hr.width/2,cy=hr.top+hr.height/2;let best=null,bd=48*48;
 V.mk.querySelectorAll('.gm').forEach(e=>{if(e.offsetParent===null)return;const r=e.getBoundingClientRect();const d=(r.left+r.width/2-cx)**2+(r.top+r.height/2-cy)**2;if(d<bd){bd=d;best=e}});return best}
function padPress(b){const gp=document.body.classList.contains('gp-on'),V=GP.V,panel=typeof ZD!=='undefined'&&ZD.role==='panel';
 const modal=document.querySelector('.gpmodal.open');
 if(modal){if(b===PB.B||b===PB.A)modal.classList.remove('open');return}
 if(document.body.classList.contains('lb-open')&&LBZ){const tabs=[...document.querySelectorAll('#lbinner .vtabs button')],ci=tabs.findIndex(t=>t.classList.contains('on'));
  if(b===PB.B||b===PB.SEL&&false){lbClose();return}if(b===PB.A){LBZ.zoomBy(1.6);return}if(b===PB.X){LBZ.zoomBy(1/1.6);return}if(b===PB.R3||b===PB.L3||b===PB.Y){LBZ.reset();return}
  if((b===PB.R1||b===PB.RIGHT||b===PB.L1||b===PB.LEFT)&&tabs.length>1){const d=(b===PB.R1||b===PB.RIGHT)?1:-1;tabs[(ci+d+tabs.length)%tabs.length].click();return}return}
 if(!gp){if(b===PB.A){const a=document.activeElement;if(a&&a.click&&a!==document.body)a.click()}return}
 const key=k=>gpKeys({key:k,target:document.body,preventDefault(){},ctrlKey:false,metaKey:false,altKey:false});
 if(panel){const lis=[...document.querySelectorAll('.gpchk li[data-u], .gpcats label')].filter(e=>e.offsetParent!==null);
  if(b===PB.UP||b===PB.DOWN){if(!lis.length)return;PAD.hl=Math.max(0,Math.min(lis.length-1,PAD.hl+(b===PB.DOWN?1:-1)));lis.forEach((e,i)=>e.classList.toggle('padhl',i===PAD.hl));lis[PAD.hl].scrollIntoView({block:'nearest',behavior:'smooth'});return}
  const cur=lis[PAD.hl];
  if(b===PB.A&&cur){cur.matches('label')?cur.querySelector('input').click():cur.click();return}
  if(b===PB.X&&cur&&cur.matches('li')){cur.querySelector('input').click();return}}
 else{
  if(b===PB.A){if(V.pop.classList.contains('open')&&GP.sel){if(GP.mode==='d'||GP.sel.c?.chk){gpToggle(GP.sel.u);return}}
   const e=padNearest();if(e){e.click();return}V.zoomBy(1.5);return}
  if(b===PB.X){key('h');return}
  if(b===PB.Y){document.querySelector('.gpsearch input')?.focus();return}
  if(b===PB.R3||b===PB.L3){V.reset();return}
  if(b===PB.UP&&GP.mode==='d'){key(',');return}if(b===PB.DOWN&&GP.mode==='d'){key('.');return}
  if(b===PB.LEFT){key('[');return}if(b===PB.RIGHT){key(']');return}}
 if(b===PB.B){if(window.zdBack&&window.zdBack())return;location.hash='#/';return}
 if(b===PB.L1){key('[');return}if(b===PB.R1){key(']');return}
 if(b===PB.START){key(GP.mode==='o'&&hasDG(GP.g.id)?'d':'o');return}
 if(b===PB.SEL){key('?');return}}
function padLoop(ts){const dt=Math.min(0.05,(ts-(PAD.t||ts))/1000);PAD.t=ts;let pads=[];try{pads=navigator.getGamepads?[...navigator.getGamepads()].filter(Boolean):[]}catch(e){}
 let lx=0,ly=0,rx=0,ry=0,zt=0;const btn=[];
 pads.forEach(p=>{const a=p.axes||[];lx+=dz(a[0]||0,.15);ly+=dz(a[1]||0,.15);rx+=dz(a[2]||0,.15);ry+=dz(a[3]||0,.15);
  (p.buttons||[]).forEach((b,i)=>{const v=typeof b==='object'?b.value:b,pr=typeof b==='object'?b.pressed:b>.5;btn[i]=(btn[i]||0)||pr;if(i===6)zt-=v;if(i===7)zt+=v})});
 // keyboard arrows feed the same smooth motion (with a stuck-key guard)
 const now=performance.now();PAD.keys.forEach((t,k)=>{if(now-t>700)PAD.keys.delete(k)});
 if(PAD.keys.has('ArrowLeft'))lx-=1;if(PAD.keys.has('ArrowRight'))lx+=1;if(PAD.keys.has('ArrowUp'))ly-=1;if(PAD.keys.has('ArrowDown'))ly+=1;
 const any=pads.length&&(lx||ly||rx||ry||zt||btn.some(Boolean));if(any){PAD.lastSeen=now;padActive(true)}
 const role=typeof ZD!=='undefined'?ZD.role:'solo';
 btn.forEach((p,i)=>{if(!p||PAD.prev[i]||i===6||i===7)return;
  if(i===PB.SEL&&role!=='solo'){if(role==='main')padOwner(PAD.owner==='main'?'panel':'main');return}
  if(padMine())padPress(i)});PAD.prev=btn;
 if(!padMine()){PAD.v.x=PAD.v.y=0;PAD.z=0;requestAnimationFrame(padLoop);return}
 const gp=document.body.classList.contains('gp-on'),panel=typeof ZD!=='undefined'&&ZD.role==='panel',V=GP.V;
 const typing=document.activeElement&&document.activeElement.matches('input[type=search],textarea');
 if(!typing){
  // smoothed velocity: ease towards the stick target
  const sp=gp&&!panel?1100:900;const tx=lx*sp,ty=ly*sp,k=Math.min(1,dt*14);PAD.v.x+=(tx-PAD.v.x)*k;PAD.v.y+=(ty-PAD.v.y)*k;
  if(Math.abs(PAD.v.x)<1&&!lx)PAD.v.x=0;if(Math.abs(PAD.v.y)<1&&!ly)PAD.v.y=0;
  if(PAD.v.x||PAD.v.y){if(gp&&!panel&&V){if(V.raf&&(lx||ly))V.stop();V.tx-=PAD.v.x*dt;V.ty-=PAD.v.y*dt;V.apply()}
   else if(gp&&panel){const s=document.querySelector('.gpside');(s&&s.scrollHeight>s.clientHeight?s:document.scrollingElement).scrollBy(0,PAD.v.y*dt)}
   else if(document.body.classList.contains('lb-open')&&LBZ){if(LBZ.raf&&(lx||ly))LBZ.stop();if(LBZ.s<=1.001&&(lx||ly)&&Math.hypot(lx,ly)>.5)LBZ.zoomBy(1.0+dt*2,true);LBZ.tx-=PAD.v.x*dt;LBZ.ty-=PAD.v.y*dt;LBZ.apply()}
   else window.scrollBy(PAD.v.x*dt,PAD.v.y*dt)}
  const zr=-ry+zt;PAD.z+=(zr-PAD.z)*Math.min(1,dt*12);if(Math.abs(PAD.z)<.01&&!zr)PAD.z=0;
  if(PAD.z&&gp&&!panel&&V){if(V.raf)V.stop();V.zoomBy(Math.exp(PAD.z*dt*2.4),true)}
  else if(PAD.z&&document.body.classList.contains('lb-open')&&LBZ){LBZ.stop();LBZ.zoomBy(Math.exp(PAD.z*dt*2.4),true)}}
 requestAnimationFrame(padLoop)}
(function padInit(){
 window.addEventListener('gamepadconnected',()=>{padActive(true);padRet()});
 window.addEventListener('gamepaddisconnected',()=>{try{if(![...navigator.getGamepads()].some(Boolean))padActive(false)}catch(e){}});
 document.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')padActive(false)},true);
 // arrows: smooth held movement instead of 60px jumps
 document.addEventListener('keydown',e=>{if(!/^Arrow/.test(e.key)||e.target.matches('input,textarea,select'))return;if(!(document.body.classList.contains('gp-on')||document.body.classList.contains('lb-open'))||(typeof ZD!=='undefined'&&ZD.role==='panel'))return;PAD.keys.set(e.key,performance.now());e.preventDefault();e.stopImmediatePropagation()},true);
 document.addEventListener('keyup',e=>{PAD.keys.delete(e.key)},true);
 window.addEventListener('blur',()=>{PAD.keys.clear();PAD.v.x=PAD.v.y=0;PAD.z=0});
 document.addEventListener('visibilitychange',()=>{PAD.keys.clear();PAD.v.x=PAD.v.y=0});
 setInterval(padRet,1500);requestAnimationFrame(padLoop)})();

document.addEventListener('keydown',e=>{if(!document.body.classList.contains('lb-open')||!LBZ||e.target.matches('input,textarea,select'))return;const k=e.key;
 if(k==='Escape'){lbClose()}else if(k==='+'||k==='='){LBZ.zoomBy(1.5)}else if(k==='-'||k==='_'){LBZ.zoomBy(1/1.5)}else if(k==='0'){LBZ.reset()}else return;e.preventDefault()});
