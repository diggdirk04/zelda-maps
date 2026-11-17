// ================= full-size map popup: zoom/pan stage =================
let LBZ=null;
function Zoomer(stage,target,aspect){const Z={s:1,tx:0,ty:0,W:1,H:1,ox:0,oy:0,raf:0,moved:false};
 const maxZ=()=>Math.max(5,Math.min(14,2*(target.naturalW||2000)/Z.W));
 Z.layout=function(){const cw=stage.clientWidth||1,ch=stage.clientHeight||1;const f=Math.min(cw/aspect.w,ch/aspect.h);Z.W=aspect.w*f;Z.H=aspect.h*f;Z.ox=(cw-Z.W)/2;Z.oy=(ch-Z.H)/2;target.style.width=Z.W+'px';target.style.height=Z.H+'px';Z.apply()};
 Z.apply=function(){const cw=stage.clientWidth,ch=stage.clientHeight,w=Z.W*Z.s,h=Z.H*Z.s;if(Z.s<=1){Z.tx=0;Z.ty=0}else{Z.tx=Math.max(Math.min(Z.tx,cw*.5-Z.ox),cw*.5-Z.ox-w);Z.ty=Math.max(Math.min(Z.ty,ch*.5-Z.oy),ch*.5-Z.oy-h)}
  target.style.transform=`translate(${Z.ox+Z.tx}px,${Z.oy+Z.ty}px) scale(${Z.s})`;stage.style.setProperty('--lbs',Z.s);stage.classList.toggle('zoomed',Z.s>1.01)};
 Z.stop=()=>{if(Z.raf){cancelAnimationFrame(Z.raf);Z.raf=0}};
 Z.tween=function(ns,A,ntx,nty,dur){Z.stop();const s0=Z.s,x0=Z.tx,y0=Z.ty,t0=performance.now();dur=matchMedia('(prefers-reduced-motion: reduce)').matches?1:(dur||230);
  const st=now=>{const t=Math.min(1,(now-t0)/dur),e=1-Math.pow(1-t,3),sc=Math.exp(Math.log(s0)+(Math.log(ns)-Math.log(s0))*e);
   if(A){Z.tx=A.x-(A.x-x0)*sc/s0;Z.ty=A.y-(A.y-y0)*sc/s0}else{Z.tx=x0+(ntx-x0)*e;Z.ty=y0+(nty-y0)*e}Z.s=sc;Z.apply();Z.raf=t<1?requestAnimationFrame(st):0};Z.raf=requestAnimationFrame(st)};
 Z.zoomAt=function(f,cx,cy,anim){const r=stage.getBoundingClientRect(),X=cx-r.left-Z.ox,Y=cy-r.top-Z.oy;const ns=Math.min(maxZ(),Math.max(1,Z.s*f));
  if(anim){Z.tween(ns,{x:X,y:Y});return}Z.tx=X-(X-Z.tx)*ns/Z.s;Z.ty=Y-(Y-Z.ty)*ns/Z.s;Z.s=ns;Z.apply()};
 Z.zoomBy=function(f,instant){const r=stage.getBoundingClientRect();Z.zoomAt(f,r.left+r.width/2,r.top+r.height/2,!instant)};
 Z.reset=()=>Z.tween(1,null,0,0,260);
 Z.focus=function(xp,yp,z){const cw=stage.clientWidth,ch=stage.clientHeight,ns=Math.min(maxZ(),Math.max(Z.s,z||2.5));Z.tween(ns,null,cw/2-Z.ox-xp/100*Z.W*ns,ch/2-Z.oy-yp/100*Z.H*ns,420)};
 const P=new Map();let start=null,pinch=null,hist=[];
 stage.addEventListener('pointerdown',e=>{if(e.target.closest('button,select,input,a'))return;Z.stop();P.set(e.pointerId,{x:e.clientX,y:e.clientY});Z.moved=false;hist=[{t:performance.now(),x:e.clientX,y:e.clientY}];
  if(P.size===1)start={x:e.clientX,y:e.clientY,tx:Z.tx,ty:Z.ty};if(P.size===2){const [a,b]=[...P.values()];pinch={d:Math.hypot(a.x-b.x,a.y-b.y),s:Z.s};P.forEach((_,id)=>{try{stage.setPointerCapture(id)}catch(_){}})}});
 stage.addEventListener('pointermove',e=>{if(!P.has(e.pointerId))return;P.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(P.size===2&&pinch){const [a,b]=[...P.values()];Z.zoomAt(pinch.s*Math.hypot(a.x-b.x,a.y-b.y)/pinch.d/Z.s,(a.x+b.x)/2,(a.y+b.y)/2);Z.moved=true;return}
  if(start&&P.size===1){const dx=e.clientX-start.x,dy=e.clientY-start.y;if(Math.abs(dx)+Math.abs(dy)>5){if(!Z.moved){try{stage.setPointerCapture(e.pointerId)}catch(_){}}Z.moved=true}
   if(Z.moved){const now=performance.now();hist.push({t:now,x:e.clientX,y:e.clientY});while(hist.length>2&&now-hist[0].t>90)hist.shift();if(Z.s>1){Z.tx=start.tx+dx;Z.ty=start.ty+dy;Z.apply()}}}});
 const up=e=>{const drag=Z.moved&&P.size===1&&!pinch;P.delete(e.pointerId);if(P.size<2)pinch=null;if(P.size===1){const p=[...P.values()][0];start={x:p.x,y:p.y,tx:Z.tx,ty:Z.ty}}else start=null;
  if(drag&&e.type==='pointerup'&&hist.length>1&&Z.s>1){const a=hist[0],b=hist[hist.length-1],dt=b.t-a.t;if(dt>0&&performance.now()-b.t<60){let vx=(b.x-a.x)/dt,vy=(b.y-a.y)/dt;if(Math.hypot(vx,vy)>.25){let last=performance.now();
   const st=now=>{const d=now-last;last=now;Z.tx+=vx*d;Z.ty+=vy*d;const k=Math.exp(-d/280);vx*=k;vy*=k;Z.apply();Z.raf=Math.hypot(vx,vy)>.02?requestAnimationFrame(st):0};Z.raf=requestAnimationFrame(st)}}}};
 stage.addEventListener('pointerup',up);stage.addEventListener('pointercancel',up);
 stage.addEventListener('wheel',e=>{e.preventDefault();e.stopPropagation();const dy=e.deltaY*(e.deltaMode?33:1);Z.zoomAt(Math.pow(1.0022,-dy),e.clientX,e.clientY,Math.abs(dy)>=40||!!e.deltaMode)},{passive:false});
 stage.addEventListener('dblclick',e=>{if(e.target.closest('button,select,input,a'))return;Z.zoomAt(e.shiftKey?.5:2,e.clientX,e.clientY,true)});
 stage.addEventListener('click',e=>{if(Z.moved){e.stopPropagation();e.preventDefault()}},true);
 Z.ro=new ResizeObserver(()=>Z.layout());Z.ro.observe(stage);
 return Z}
function lbClose(){const lb=document.getElementById('lightbox');if(lb.style.display!=='flex'&&lb.style.display!=='block')return false;lb.style.display='none';document.body.classList.remove('lb-open');if(LBZ){LBZ.stop();LBZ.ro.disconnect();LBZ=null}return true}
function lbSetup(g,img){const lb=document.getElementById('lightbox'),inn=document.getElementById('lbinner');try{document.activeElement&&document.activeElement.blur()}catch(e){}lb.style.display='flex';document.body.classList.add('lb-open');
 let tgt=inn.querySelector('.map')||inn.querySelector('img.solo');if(!tgt)return;
 const stage=document.createElement('div');stage.className='lbstage';
 const z=document.createElement('div');z.className='lbz';
 if(tgt.matches('img.solo')){tgt.classList.remove('solo');z.appendChild(tgt);tgt.style.width='100%';tgt.style.height='100%'}
 else{tgt.parentNode.insertBefore(stage,tgt);z.appendChild(tgt)}
 stage.appendChild(z);if(!stage.parentNode)inn.prepend(stage);
 const hint=document.createElement('div');hint.className='lbhint';hint.textContent='Pinch, scroll or use the stick to zoom · drag to move';stage.appendChild(hint);setTimeout(()=>hint.classList.add('off'),2600);
 const aspect=g?{w:g.w,h:g.h}:{w:1,h:1};const ctl=inn.querySelector('.vctl');if(ctl)inn.appendChild(ctl);
 LBZ=Zoomer(stage,z,aspect);LBZ.layout();
 if(!g){const im=z.querySelector('img');const fit=()=>{aspect.w=im.naturalWidth||1;aspect.h=im.naturalHeight||1;z.naturalW=im.naturalWidth;LBZ.layout()};if(im.complete&&im.naturalWidth)fit();else im.onload=fit}
 else{const bi=z.querySelector('.baseimg');const fit=()=>{if(bi.naturalWidth){aspect.w=bi.naturalWidth;aspect.h=bi.naturalHeight;z.naturalW=bi.naturalWidth;LBZ.layout()}};bi.addEventListener('load',fit);if(bi.complete)fit()}}
