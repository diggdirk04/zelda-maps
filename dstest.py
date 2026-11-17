import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1366,'height':860});errs=[];fails=[]
        pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('requestfailed',lambda r:fails.append(r.url))
        for h in ['#/g/ph/o/1','#/g/st/o/0']:
            await pg.goto(U+h);await pg.wait_for_timeout(1200);await pg.click('.gpside [data-a="all"]');await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"shots/ds_{h.split('/')[2]}_o.png")
        for g in ['ph','st']:
            n=await pg.evaluate(f"DUNG.{g}.m.length")
            bad=0
            for i in range(n):
                await pg.evaluate(f"location.hash='#/g/{g}/d/{i}'");await pg.wait_for_timeout(60)
                ok=await pg.evaluate("(async()=>{await GP.busy;const im=document.querySelector('#gpv .gvimg');return im.complete&&im.naturalWidth>0})()")
                if not ok: bad+=1
            print(g,'dungeon maps',n,'not loaded',bad)
        await pg.goto(U+'#/g/ph/d/0');await pg.wait_for_timeout(900);await pg.screenshot(path='shots/ds_ph_d.png')
        await pg.goto(U+'#/g/st/d/3');await pg.wait_for_timeout(900);await pg.screenshot(path='shots/ds_st_d.png')
        print(errs,fails[:3]);await b.close()
asyncio.run(main())
