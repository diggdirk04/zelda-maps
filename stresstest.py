# Stress test: long sessions, rapid input, every layer on, huge progress files. Reports leaks and slow frames.
import asyncio,json,sys,time
from playwright.async_api import async_playwright
U=sys.argv[1] if len(sys.argv)>1 else 'file:///home/claude/site/index.html'
async def mem(pg,cdp):
    await cdp.send('HeapProfiler.collectGarbage')
    m=await pg.evaluate("({heap:Math.round(performance.memory.usedJSHeapSize/1048576),dom:document.getElementsByTagName('*').length,blobs:Object.keys(typeof DGU!=='undefined'?DGU:{}).length,tiles:document.querySelectorAll('.gvhd img').length})")
    return m
FR="""async(fn,n)=>{const gaps=[];let last=performance.now(),go=true;const tick=t=>{gaps.push(t-last);last=t;if(go)requestAnimationFrame(tick)};requestAnimationFrame(tick);
 await fn(n);go=false;gaps.sort((a,b)=>a-b);const k=gaps.length;return {frames:k,p50:+gaps[k>>1].toFixed(1),p95:+gaps[Math.floor(k*.95)].toFixed(1),max:+gaps[k-1].toFixed(1),long:gaps.filter(g=>g>100).length}}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--enable-precise-memory-info','--js-flags=--expose-gc'])
        pg=await b.new_page(viewport={'width':1280,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        cdp=await pg.context.new_cdp_session(pg)
        await pg.goto(U);await pg.wait_for_timeout(1500);base=await mem(pg,cdp);print('home',base,flush=True)
        # 1. game hopping: every game, every tab, three laps
        games=await pg.evaluate("GAMES.map(g=>g.id)");t=time.time()
        for lap in range(3):
            for g in games:
                n=await pg.evaluate(f"(location.hash='#/g/{g}/o/0',0)");await pg.wait_for_timeout(250)
                nt=await pg.evaluate("gpModel(GP.g).tabs.length")
                for i in range(nt): await pg.evaluate(f"location.hash='#/g/{g}/o/{i}'");await pg.wait_for_timeout(120)
            print(f'lap {lap+1}',await mem(pg,cdp),f'{time.time()-t:.0f}s',flush=True)
        # 2. BotW/TotK with every layer switched on
        await pg.goto(U+'#/g/botw/o/1');await pg.wait_for_timeout(1500)
        r=await pg.evaluate("(()=>{const t0=performance.now();gpModel(GP.g).cats.forEach(c=>GP.on.add(c.id));gpOwMarkers();gpOwSide();return [Math.round(performance.now()-t0),document.querySelectorAll('#gpv .gm').length,document.querySelectorAll('#gpv .gl').length]})()")
        print('all layers on: render ms, markers, labels',r,flush=True)
        await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
        z=await pg.evaluate("("+FR+")(async n=>{const V=GP.V,r=V.host.getBoundingClientRect();for(let k=0;k<n;k++){const f=k%80<40?1.05:1/1.05;V.zoomAt(f,r.left+r.width*(.3+.4*Math.random()),r.top+r.height*(.3+.4*Math.random()));await new Promise(q=>requestAnimationFrame(q))}},400)")
        print('zoom x400, all layers, CPU/4',z,flush=True)
        pn=await pg.evaluate("("+FR+")(async n=>{const V=GP.V;V.zoomAt(4,640,400);for(let k=0;k<n;k++){V.tx+=Math.sin(k/9)*25;V.ty+=Math.cos(k/11)*25;V.apply();await new Promise(q=>requestAnimationFrame(q))}},400)")
        print('pan x400, zoomed 4x, CPU/4',pn,await mem(pg,cdp),flush=True)
        await cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
        # 3. blend slider and label flip hammering
        await pg.goto(U+'#/g/alttp/o/0');await pg.wait_for_timeout(1200);await pg.select_option('.gpbl','2')
        bl=await pg.evaluate("("+FR+")(async n=>{const r=document.querySelector('.gpblr');for(let k=0;k<n;k++){r.value=(k*7)%101;r.dispatchEvent(new Event('input'));if(k%25==0&&+r.value>0)document.querySelector('.gpflip').click();if(k%10==0)GP.V.zoomAt(k%20?1.2:1/1.2,640,400);await new Promise(q=>requestAnimationFrame(q))}},300)")
        print('blend slider x300 + flips + zooms',bl,await mem(pg,cdp),flush=True)
        # 4. mark everything found in BotW, reload, export, re-import
        await pg.goto(U+'#/g/botw/o/0');await pg.wait_for_timeout(1500)
        r=await pg.evaluate("(()=>{const t0=performance.now();let n=0;gpModel(GP.g).cats.forEach(c=>c.it.forEach(r=>{if(!GP.done.has(r.u)){gpToggle(r.u);n++}}));return [n,Math.round(performance.now()-t0)]})()")
        print('marked found (count, ms)',r,flush=True)
        await pg.reload();await pg.wait_for_timeout(2000)
        print('after reload found',await pg.evaluate("GP.done.size"),'storage KB',await pg.evaluate("Math.round(JSON.stringify(localStorage).length/1024)"),flush=True)
        # 5. dungeon flipping: every floor of every game
        t=time.time();n=0
        for g in games:
            nd=await pg.evaluate(f"(DUNG['{g}']&&DUNG['{g}'].m.length)||0")
            for i in range(nd): await pg.evaluate(f"location.hash='#/g/{g}/d/{i}'");await pg.wait_for_timeout(60);n+=1
        await pg.wait_for_timeout(1000);print('dungeon floors',n,f'{time.time()-t:.0f}s',await mem(pg,cdp),flush=True)
        # 6. keyboard spam
        await pg.goto(U+'#/g/oot/o/0');await pg.wait_for_timeout(1200)
        for k in range(200): await pg.keyboard.press(['[',']','+','-','l','h','x','ArrowLeft','ArrowRight'][k%9])
        await pg.wait_for_timeout(800);print('key spam x200 ok, hash',await pg.evaluate("location.hash"),flush=True)
        print('final',await mem(pg,cdp),'errors',errs[:5],flush=True)
        await b.close()
asyncio.run(main())
