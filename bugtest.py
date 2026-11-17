import asyncio,json,os,time
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
R=[]
def bug(area,msg): R.append((area,msg)); print('BUG',area,'|',msg)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context(viewport={'width':1366,'height':820})
        pg=await ctx.new_page();errs=[];fails=[]
        pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('requestfailed',lambda r:fails.append(r.url))
        await pg.goto(U);await pg.wait_for_timeout(800)
        games=await pg.evaluate("GAMES.map(g=>({id:g.id,tabs:1+(g.v||[]).length,dg:!!DUNG[g.id],dn:DUNG[g.id]?DUNG[g.id].m.length:0}))")
        # 1 every overworld tab, all layers on
        for g in games:
            for t in range(g['tabs']):
                await pg.evaluate(f"location.hash='#/g/{g['id']}/o/{t}'");await pg.wait_for_timeout(250)
                r=await pg.evaluate("""async()=>{await GP.busy;const side=document.querySelector('.gpside');const all=side.querySelector('[data-a="all"]');if(all)all.click();await new Promise(r=>setTimeout(r,60));
                 const img=document.querySelector('#gpv .gvimg');const ok=img.complete&&img.naturalWidth>0;
                 const mk=document.querySelectorAll('#gpv .gm').length+(GP.lbls?GP.lbls.length:document.querySelectorAll('#gpv .gl').length);const t=gpModel(GP.g).tabs[GP.tab];
                 const exp=gpModel(GP.g).cats.reduce((a,c)=>a+c.it.filter(r=>onTab(r,t)).length,0);
                 const W=GP.V.W,H=GP.V.H;return {ok,mk,exp,W,H,hash:location.hash,src:img.src.split('/').pop()}}""")
                if not r['ok']: bug('overworld',f"{g['id']} tab {t}: image not loaded ({r['src']})")
                if r['mk']!=r['exp']: bug('overworld',f"{g['id']} tab {t}: {r['mk']} markers drawn, {r['exp']} expected")
                if r['W']<50: bug('overworld',f"{g['id']} tab {t}: viewer has no size")
                if r['hash']!=f"#/g/{g['id']}/o/{t}": bug('routing',f"{g['id']} tab {t}: hash {r['hash']}")
        # 2 every dungeon map
        for g in games:
            if not g['dg']:continue
            for i in range(g['dn']):
                await pg.evaluate(f"location.hash='#/g/{g['id']}/d/{i}'");await pg.wait_for_timeout(120)
                r=await pg.evaluate("""async()=>{await GP.busy;await new Promise(r=>setTimeout(r,30));const img=document.querySelector('#gpv .gvimg');const m=DUNG[GP.g.id].m[GP.dm];
                 return {ok:img.complete&&img.naturalWidth>0,src:img.src.split('/').pop(),mk:document.querySelectorAll('#gpv .gm.dot').length,li:document.querySelectorAll('.gpchk li[data-u]').length,n:m.it.length,dm:GP.dm,
                 ar:img.naturalWidth?Math.abs(img.naturalWidth/img.naturalHeight-m.w/m.h):0}}""")
                if not r['ok']: bug('dungeon',f"{g['id']} #{i}: image not loaded {r['src']}")
                if r['mk']!=r['n'] or r['li']!=r['n']: bug('dungeon',f"{g['id']} #{i}: {r['mk']} markers / {r['li']} list items, {r['n']} checks (kind filter?)")
                if r['ar']>0.02: bug('dungeon',f"{g['id']} #{i}: image aspect differs from data ({r['ar']:.3f})")
                if r['dm']!=i: bug('routing',f"{g['id']} d/{i} opened {r['dm']}")
        # 3 uid collisions
        r=await pg.evaluate("""()=>{const out=[];GAMES.forEach(g=>{const s=new Map();gpModel(g).cats.forEach(c=>{if(!c.chk)return;c.it.forEach(r=>{if(s.has(r.u)&&s.get(r.u)!==r)out.push(g.id+' '+r.name)
             ;s.set(r.u,r)})});if(DUNG[g.id]){const d=new Map();dgItems(g.id).flat().forEach(r=>{if(d.has(r.u))out.push(g.id+' dg '+r.name);d.set(r.u,r)})}});return out}""")
        if r: bug('progress',f"{len(r)} duplicate progress IDs (ticking one ticks another): {r[:6]}")
        # 4 search per game
        for g in games:
            await pg.evaluate(f"location.hash='#/g/{g['id']}/o/0'");await pg.wait_for_timeout(200)
            r=await pg.evaluate("""async()=>{await GP.busy;const idx=gpIndex();const bad=idx.filter(x=>!x.n||x.n.trim()==='').length;return {n:idx.length,bad}}""")
            if r['n']==0: bug('search',f"{g['id']}: search index empty")
            if r['bad']: bug('search',f"{g['id']}: {r['bad']} results with blank names")
        await pg.evaluate("location.hash='#/g/tp/o/0'");await pg.wait_for_timeout(400)
        await pg.fill('.gpsearch input','lakebed');await pg.wait_for_timeout(200)
        n=await pg.evaluate("document.querySelectorAll('.gpres [data-i]').length")
        if not n: bug('search','"lakebed" found nothing in TP')
        await pg.keyboard.press('Enter');await pg.wait_for_timeout(700)
        if '/d/' not in await pg.evaluate('location.hash'): bug('search','picking a dungeon result did not open dungeons')
        await pg.fill('.gpsearch input','zzzqqq');await pg.wait_for_timeout(200)
        if 'No matches' not in await pg.inner_text('.gpres'): bug('search','no "No matches" message')
        await pg.keyboard.press('Escape')
        # 5 keyboard shortcuts
        await pg.evaluate("location.hash='#/g/oot/d/3'");await pg.wait_for_timeout(500);await pg.mouse.click(400,400)
        h0=await pg.evaluate('location.hash')
        for k,chk in [(']','floor'),('.','dungeon'),('o','mode')]:
            await pg.keyboard.press(k);await pg.wait_for_timeout(450);h=await pg.evaluate('location.hash')
            if h==h0: bug('keys',f"'{k}' ({chk}) did nothing")
            h0=h
        s0=await pg.evaluate('GP.V.s');await pg.keyboard.press('+');await pg.wait_for_timeout(100)
        if await pg.evaluate('GP.V.s')<=s0: bug('keys',"'+' did not zoom")
        await pg.keyboard.press('0');await pg.wait_for_timeout(400)
        if await pg.evaluate('GP.V.s')!=1: bug('keys',"'0' did not reset")
        await pg.keyboard.press('?');await pg.wait_for_timeout(150)
        if not await pg.evaluate("!!document.querySelector('.gpmodal.open')"): bug('keys',"'?' no help")
        await pg.keyboard.press('Escape');await pg.wait_for_timeout(100)
        if await pg.evaluate("!!document.querySelector('.gpmodal.open')"): bug('keys','Esc did not close help')
        await pg.keyboard.press('h');await pg.wait_for_timeout(100)
        if not await pg.evaluate("GP.hide"): bug('keys',"'h' did not hide found")
        await pg.keyboard.press('h')
        # 6 mark found persists + counts update
        await pg.evaluate("location.hash='#/g/la/d/0'");await pg.wait_for_timeout(500)
        t0=await pg.inner_text('.gpside h4')
        await pg.click('.gpchk li[data-u] >> nth=0 >> input');await pg.wait_for_timeout(200)
        t1=await pg.inner_text('.gpside h4')
        if t0==t1: bug('progress',f'header count did not change after ticking ({t1})')
        if not await pg.evaluate("document.querySelector('#gpv .gm.dot.done')"): bug('progress','ticked marker not shown as found on map')
        await pg.reload();await pg.wait_for_timeout(800)
        if not await pg.evaluate("GP.done.size"): bug('progress','tick lost after reload')
        # hide found then untick
        await pg.click('.gpside .gphide');await pg.wait_for_timeout(100)
        vis=await pg.evaluate("[...document.querySelectorAll('.gpchk li.done')].filter(e=>e.offsetParent).length")
        if vis: bug('progress','hide found leaves found checks visible in list')
        await pg.click('.gpside .gphide')
        # mark all / clear
        await pg.click('.gpside [data-a="all"]');await pg.wait_for_timeout(150)
        a=await pg.evaluate("document.querySelectorAll('.gpchk li.done').length"); n=await pg.evaluate("document.querySelectorAll('.gpchk li[data-u]').length")
        if a!=n: bug('progress',f'mark all found ticked {a}/{n}')
        await pg.click('.gpside [data-a="none"]');await pg.wait_for_timeout(150)
        if await pg.evaluate("document.querySelectorAll('.gpchk li.done').length"): bug('progress','clear left ticks')
        # kind filter
        await pg.click('.gpkinds button >> nth=0');await pg.wait_for_timeout(150)
        m1=await pg.evaluate("document.querySelectorAll('#gpv .gm.dot').length")
        await pg.click('.gpkinds button >> nth=0');await pg.wait_for_timeout(150)
        m2=await pg.evaluate("document.querySelectorAll('#gpv .gm.dot').length")
        if m1>=m2: bug('dungeon','marker-type filter did not hide anything')
        # 7 notes
        await pg.keyboard.press('n');await pg.mouse.click(500,420);await pg.wait_for_timeout(150);await pg.keyboard.type('test note');await pg.click('.gvpop [data-do="save"]')
        await pg.reload();await pg.wait_for_timeout(800)
        if not await pg.evaluate("document.querySelectorAll('#gpv .gm.note').length"): bug('notes','note missing after reload')
        await pg.click('#gpv .gm.note');await pg.wait_for_timeout(150);txt=await pg.evaluate("document.querySelector('.gvpop textarea')?.value")
        if txt!='test note': bug('notes',f'note text wrong: {txt}')
        await pg.click('.gvpop [data-do="del"]');await pg.wait_for_timeout(150)
        if await pg.evaluate("document.querySelectorAll('#gpv .gm.note').length"): bug('notes','delete did not remove note')
        # 8 export/import/reset
        await pg.click('.gpchk li[data-u] >> nth=1 >> input')
        await pg.click('[data-x="exp"]');ex=await pg.evaluate("document.querySelector('.gpmodal textarea').value");await pg.keyboard.press('Escape')
        await pg.click('[data-x="rst"]');await pg.click('.gpmodal [data-do="go"]');await pg.wait_for_timeout(200)
        if await pg.evaluate("GP.done.size"): bug('data','reset did not clear')
        await pg.click('[data-x="imp"]');await pg.fill('.gpmodal textarea','not json');await pg.click('.gpmodal [data-do="go"]')
        if 'not a valid' not in await pg.inner_text('.gpmodal'): bug('data','bad import gives no error')
        await pg.fill('.gpmodal textarea',ex);await pg.click('.gpmodal [data-do="go"]');await pg.wait_for_timeout(400)
        if not await pg.evaluate("GP.done.size"): bug('data','import did not restore progress')
        # 9 home page parts
        await pg.evaluate("location.hash='#/'");await pg.wait_for_timeout(500)
        if await pg.evaluate("document.body.classList.contains('gp-on')"): bug('home','#/ did not return home')
        if await pg.evaluate("document.querySelectorAll('.ages li').length")!=len(games): bug('home','timeline count wrong')
        if not await pg.evaluate("!!document.querySelector('.cont')"): bug('home','no Continue button after visiting')
        await pg.select_option('#cmpA','mm');await pg.wait_for_timeout(200)
        if 'Majora' not in await pg.inner_text('#compare'): bug('home','compare select did not switch')
        await pg.click('.chip >> nth=0');await pg.wait_for_timeout(100)
        if 'Highlighting' not in await pg.inner_text('#status'): bug('home','area chip did not highlight')
        await pg.click('.chip >> nth=0')
        await pg.evaluate("document.querySelectorAll('.foldbody').forEach(d=>d.hidden=false)")
        await pg.click('#maps .card .map >> nth=0');await pg.wait_for_timeout(300)
        if await pg.evaluate("getComputedStyle(document.querySelector('#lightbox')).display")!='flex': bug('home','map click did not open lightbox')
        await pg.click('#lightbox .lbx');await pg.wait_for_timeout(100)
        if await pg.evaluate("document.body.classList.contains('lb-open')"): bug('home','close button did not close lightbox')
        await pg.fill('#rq','hylia');await pg.wait_for_timeout(200)
        if 'callbacks' not in await pg.inner_text('#rc'): bug('home','callback search broke')
        await pg.click('.dghome a >> nth=1');await pg.wait_for_timeout(600)
        if '/d/0' not in await pg.evaluate('location.hash'): bug('home','dungeon grid link failed')
        await pg.go_back();await pg.wait_for_timeout(500)
        if await pg.evaluate("document.body.classList.contains('gp-on')"): bug('routing','browser Back did not return home')
        # bad routes
        await pg.evaluate("location.hash='#/g/nope'");await pg.wait_for_timeout(300)
        if await pg.evaluate("document.body.classList.contains('gp-on')"): bug('routing','unknown game id opened a page')
        await pg.evaluate("location.hash='#/g/oot/d/999'");await pg.wait_for_timeout(500)
        if not await pg.evaluate("GP.dm<DUNG.oot.m.length"): bug('routing','out-of-range dungeon index')
        await pg.evaluate("location.hash='#/g/aol/d/0'");await pg.wait_for_timeout(500)
        await pg.evaluate("location.hash='#/g/fs/d/0'");await pg.wait_for_timeout(500)
        if '/o/' not in await pg.evaluate('location.hash'): bug('routing','game without dungeons on /d/ not redirected to overworld')
        if errs: bug('js',f'{len(errs)} errors: {errs[:3]}')
        bad=[f for f in fails if 'googleapis' not in f]
        if bad: bug('files',f'{len(bad)} failed loads: {bad[:5]}')
        # 10 mobile + panel sizes
        for vp in [(390,844),(360,413),(1080//2,1240//2),(844,390)]:
            m=await ctx.new_page();await m.set_viewport_size({'width':vp[0],'height':vp[1]});me=[];m.on('pageerror',lambda e:me.append(str(e)))
            for h in ['','#/g/botw/o/1','#/g/oot/d/9','#/g/aol/d/3']:
                await m.goto(U+h);await m.wait_for_timeout(700)
                w=await m.evaluate('document.documentElement.scrollWidth')
                if w>vp[0]+1: bug('layout',f'{vp} {h or "home"}: page wider than screen ({w}px)')
                if h:
                    gh=await m.evaluate("document.querySelector('#gpv').getBoundingClientRect().height")
                    if gh<150: bug('layout',f'{vp} {h}: map only {gh:.0f}px tall')
                    ov=await m.evaluate("(()=>{const b=document.querySelector('.gpbar').getBoundingClientRect();return [...document.querySelectorAll('.gpbar > *')].filter(e=>e.offsetParent&&e.getBoundingClientRect().right>innerWidth+1).map(e=>e.className)})()")
                    if ov: bug('layout',f'{vp} {h}: top bar items off-screen {ov}')
            if me: bug('js',f'{vp}: {me[:2]}')
            await m.close()
        print('DONE',len(R),'issues')
        json.dump(R,open('bugs.json','w'),indent=1)
        await b.close()
asyncio.run(main())
