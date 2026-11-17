// ================= cloud sync (claude.ai artifact storage) =================
// Every zm:* key is mirrored to one private document per key under data/users/<id>/.
// Newest write wins per key. Only runs where the page is served by claude.ai; the offline apps keep using Export/Import.
const SY={state:'off',col:null,mt:{},pending:new Set(),busy:false,applying:false,last:0,timer:0};
try{SY.mt=JSON.parse(localStorage.getItem('zmmt')||'{}')}catch(e){SY.mt={}}
const syDocId=k=>k.replace(/[^A-Za-z0-9_\-.~:@+]/g,c=>c==='/'?'~':'+'+c.charCodeAt(0).toString(16)+'.');
function sySaveMt(){try{localStorage.setItem('zmmt',JSON.stringify(SY.mt))}catch(e){}}
(function(){const orig=ZS.set;ZS.set=function(k,v){orig.call(ZS,k,v);if(SY.applying)return;SY.mt[k]=Date.now();sySaveMt();if(SY.col){SY.pending.add(k);syQueue()}}})();
function syQueue(){clearTimeout(SY.timer);SY.timer=setTimeout(syFlush,1200)}
async function syFlush(){if(SY.busy||!SY.col)return;SY.busy=true;try{
 while(SY.pending.size){const k=SY.pending.values().next().value;SY.pending.delete(k);let v=null;try{v=JSON.parse(localStorage.getItem('zm:'+k))}catch(e){}
  if(v===null||v===undefined)continue;
  try{await SY.col.doc(syDocId(k)).set({k,v,t:SY.mt[k]||Date.now()});SY.last=Date.now();syStatus('on')}
  catch(e){if(e&&e.code==='quota_exceeded'){syStatus('full');break}if(e&&e.code==='unavailable'){SY.pending.add(k);setTimeout(syQueue,3000+Math.random()*2000);break}if(e&&(e.code==='revoked'||e.code==='invalid_argument')){syStatus('off');SY.col=null;break}}}
}finally{SY.busy=false}}
function syStatus(s){SY.state=s;document.querySelectorAll('.gpsync').forEach(e=>e.innerHTML=syText())}
function syText(){if(SY.state==='on')return `<span class="dot on"></span>Synced to your claude.ai account${SY.last?' · '+new Date(SY.last).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'}):''}. Open this page on any device you're signed in on and your progress follows.`;
 if(SY.state==='connecting')return '<span class="dot"></span>Connecting to sync…';
 if(SY.state==='full')return '<span class="dot off"></span>Sync storage is full. Use Export to keep a copy.';
 if(SY.state==='stale')return '<span class="dot off"></span>Sync can\'t be reached right now. Changes are saved here and will upload when it reconnects.';
 return '<span class="dot off"></span>Use Export and Import to move progress between devices.'}
function syApply(changed){if(!changed.size)return;const g=GP.g;
 if(g&&[...changed].some(k=>k==='done:'+g.id||k==='pref:'+g.id||k.startsWith('notes:'+g.id+':'))&&document.body.classList.contains('gp-on')){const id=g.id,mode=GP.mode,idx=mode==='d'?GP.dm:GP.tab;GP.g=null;gpOpen(id,mode,idx)}
 GP.navDraw&&GP.navDraw()}
(async function syInit(){if(typeof window.claude==='undefined'||!window.claude||typeof window.claude.use!=='function'){syStatus('off');return}
 syStatus('connecting');let db=null,user=null,uid=null;
 try{db=await window.claude.use('db');user=await window.claude.use('user');uid=user?await user.id():null}catch(e){}
 if(!db||!uid){syStatus('off');return}
 try{SY.col=db.collection('data/users/'+uid)}catch(e){syStatus('off');return}
 let first=true;const to=setTimeout(()=>{if(first)syStatus('stale')},10000);
 SY.col.onSnapshot(snap=>{const changed=new Set();const remote=new Set();
  snap.docs.forEach(d=>{const b=d.data();if(!b||typeof b.k!=='string'||!/^[\w:.~\/\-@+]+$/.test(b.k))return;remote.add(b.k);
   const lt=SY.mt[b.k]||0;
   if(!lt&&localStorage.getItem('zm:'+b.k)!==null&&(b.k.startsWith('done:')||b.k.startsWith('notes:'))){let loc=[];try{loc=JSON.parse(localStorage.getItem('zm:'+b.k))||[]}catch(e){}
    const rv=Array.isArray(b.v)?b.v:[];const seen=new Set(rv.map(x=>JSON.stringify(x)));const merged=rv.concat(loc.filter(x=>!seen.has(JSON.stringify(x))));
    SY.applying=true;try{localStorage.setItem('zm:'+b.k,JSON.stringify(merged))}finally{SY.applying=false}SY.mt[b.k]=Date.now();SY.pending.add(b.k);changed.add(b.k);return}
   if((b.t||0)>lt&&!SY.pending.has(b.k)){SY.applying=true;try{localStorage.setItem('zm:'+b.k,JSON.stringify(b.v));SY.mt[b.k]=b.t;changed.add(b.k)}catch(e){}finally{SY.applying=false}}
   else if(lt>(b.t||0))SY.pending.add(b.k)});
  if(!snap.metadata.fromCache&&first){first=false;clearTimeout(to);
   ZS.keys().forEach(fk=>{const k=fk.slice(3);if(!remote.has(k)){if(!SY.mt[k])SY.mt[k]=1;SY.pending.add(k)}});syStatus('on');syQueue()}
  else if(SY.pending.size)syQueue();
  if(changed.size){sySaveMt();syApply(changed)}},
  e=>{clearTimeout(to);syStatus(e&&e.code==='revoked'?'off':'stale')})})();
