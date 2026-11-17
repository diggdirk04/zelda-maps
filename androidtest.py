import asyncio
from playwright.async_api import async_playwright
U='file:///tmp/at/apkweb/assets/web/index.html'
UA='Mozilla/5.0 (Linux; Android 13; AYN Thor Build/TQ3A; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.0.0 Mobile Safari/537.36'
def stub(role,second=True): return """window.ZDual={_r:'%s',role(){return this._r},hasSecond(){return %s},send(s){this._bc&&this._bc.postMessage(s)},openPanel(){window.__open=(window.__open||0)+1},closePanel(){window.__close=(window.__close||0)+1}};
try{ZDual._bc=new BroadcastChannel('fake');ZDual._bc.onmessage=e=>{const f=()=>window.zdRecv?zdRecv(e.data):setTimeout(f,50);f()}}catch(e){}"""%(role,'true' if second else 'false')
R=[]
def bug(m): R.append(m);print('BUG',m)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context(user_agent=UA,viewport={'width':960,'height':540},device_scale_factor=2,is_mobile=True,has_touch=True)
        await ctx.add_init_script(stub('solo'))
        pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));fails=[];pg.on('requestfailed',lambda r:fails.append(r.url))
        await pg.goto(U);await pg.wait_for_timeout(1200)
        env=await pg.evaluate("({sec:isSecureContext,gp:typeof navigator.getGamepads,ls:(()=>{try{localStorage.setItem('t','1');return true}catch(e){return false}})(),native:ZD.native,role:ZD.role,fonts:document.fonts.check('16px Bonum')})")
        print('environment',env)
        if not env['sec']: bug('file:// page is not a secure context (gamepad may be blocked)')
        if not env['ls']: bug('localStorage unavailable')
        # Dual screen button visible on single screen device w/ second display
        await pg.goto(U+'#/g/oot/o/2');await pg.wait_for_timeout(1000)
        t=await pg.evaluate("(()=>{const b=document.querySelector('.zdbtn');return b&&getComputedStyle(b).display!=='none'?b.textContent:null})()")
        print('dual button:',t)
        await pg.click('.zdbtn');await pg.wait_for_timeout(100)
        if not await pg.evaluate('window.__open'): bug('Dual screen button did not call openPanel')
        # wiki links: must be http(s) so the app hands them to the browser
        await pg.evaluate("(()=>{const c=gpModel(GP.g).cats.find(c=>c.it.some(r=>r.wiki));})()")
        await pg.goto(U+'#/g/botw/o/1');await pg.wait_for_timeout(1200)
        w=await pg.evaluate("(()=>{for(const c of gpModel(GP.g).cats)for(const r of c.it)if(r.wiki&&r.tab==='surface'){GP.on.add(c.id);gpOwMarkers();gpShowItem(r);return document.querySelector('.gvpop a[target=_blank]')?.href}})()")
        print('wiki link',w)
        if not w or not w.startswith('https://'): bug('wiki link not https')
        # Back behaviour (zdBack)
        r=await pg.evaluate("[zdBack(),document.querySelector('.gvpop').classList.contains('open'),zdBack()]")
        print('back closes popup then reports nothing to close',r)
        if r!=[True,False,False]: bug(f'zdBack popup sequence {r}')
        await pg.evaluate("gpFull()");await pg.wait_for_timeout(300)
        mx=await pg.evaluate("[document.getElementById('gp').classList.contains('gpmax'),getComputedStyle(document.querySelector('.gpbar')).display,Math.round(document.querySelector('#gpv').getBoundingClientRect().height)]")
        print('fullscreen fallback (map only)',mx)
        if not mx[0] or mx[1]!='none' or mx[2]<500: bug(f'map-only mode wrong {mx}')
        if not await pg.evaluate("zdBack()"): bug('Back did not leave map-only mode')
        await pg.evaluate("document.querySelector('.gpsearch input').focus()")
        if not await pg.evaluate("zdBack()"): bug('Back did not close keyboard/search')
        await pg.evaluate("document.querySelector('.gphelp').click()")
        if not await pg.evaluate("zdBack()&&!document.querySelector('.gpmodal.open')"): bug('Back did not close help')
        await pg.evaluate("location.hash='#/'");await pg.wait_for_timeout(500)
        await pg.evaluate("document.querySelector('#maps .card .map').click()");await pg.wait_for_timeout(300)
        if not await pg.evaluate("zdBack()"): bug('Back did not close full-size map on home')
        if await pg.evaluate("zdBack()"): bug('Back claimed something to close on plain home page')
        # touch: tap marker, long-press, pinch via CDP
        await pg.goto(U+'#/g/tp/d/3');await pg.wait_for_timeout(1000)
        await pg.tap('#gpv .gm.dot >> nth=1');await pg.wait_for_timeout(300)
        if not await pg.evaluate("document.querySelector('.gvpop').classList.contains('open')"): bug('tap marker no popup')
        cdp=await ctx.new_cdp_session(pg)
        s0=await pg.evaluate('GP.V.s')
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':400,'y':270,'id':1},{'x':500,'y':270,'id':2}]})
        for i in range(1,8):
            await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':400-i*20,'y':270,'id':1},{'x':500+i*20,'y':270,'id':2}]});await pg.wait_for_timeout(16)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await pg.wait_for_timeout(200)
        s1=await pg.evaluate('GP.V.s');print('pinch zoom',round(s0,2),'->',round(s1,2))
        if s1<=s0*1.3: bug('pinch did not zoom')
        # one-finger drag pans
        t0=await pg.evaluate('GP.V.tx')
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':480,'y':300,'id':1}]})
        for i in range(1,8):
            await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':480-i*25,'y':300,'id':1}]});await pg.wait_for_timeout(16)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await pg.wait_for_timeout(500)
        t1=await pg.evaluate('GP.V.tx');print('touch pan',round(t1-t0))
        if t1>=t0-50: bug('touch drag did not pan')
        # page should not scroll/zoom as a whole while using the map
        sy=await pg.evaluate('[scrollX,scrollY,visualViewport.scale]');print('page scroll/zoom after gestures',sy)
        if sy[2]!=1: bug('whole page zoomed during pinch')
        # sizes: Thor top landscape and bottom panel
        for vp,role in [((960,540),'main'),((540,620),'panel'),((390,844),'solo')]:
            c2=await b.new_context(user_agent=UA,viewport={'width':vp[0],'height':vp[1]},device_scale_factor=2,is_mobile=True,has_touch=True);await c2.add_init_script(stub(role))
            q=await c2.new_page();e2=[];q.on('pageerror',lambda e:e2.append(str(e)))
            for h in ['','#/g/botw/o/1','#/g/oot/d/9']:
                await q.goto(U+h);await q.wait_for_timeout(900)
                w=await q.evaluate('document.documentElement.scrollWidth')
                if w>vp[0]+1: bug(f'{role} {vp} {h or "home"}: wider than screen {w}')
                if h and role!='panel':
                    gh=await q.evaluate("document.querySelector('#gpv').getBoundingClientRect().height")
                    if gh<vp[1]*0.5: bug(f'{role} {vp} {h}: map only {gh:.0f}px tall')
                await q.screenshot(path=f'shots/and_{role}_{h.replace("/","_").replace("#","") or "home"}.png')
            if e2: bug(f'{role}: {e2[:2]}')
            await c2.close()
        bad=[f for f in fails if not f.startswith('file://')==False]
        if errs: bug(f'js errors {errs[:3]}')
        missing=[f for f in fails if f.startswith('file://')]
        if missing: bug(f'missing files {missing[:5]}')
        print('DONE',len(R),'issues');await b.close()
asyncio.run(main())
