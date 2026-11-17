import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html')
        await pg.wait_for_timeout(800)
        await pg.click('#rall'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='shots/all.png')
        await pg.evaluate("document.getElementById('lightbox').style.display='none'")
        bts=await pg.query_selector_all('.rb[data-m="then"]')
        for bt in bts:
            t=await bt.evaluate("e=>e.closest('.ref').innerText")
            if 'Ranch Ruins' in t: await bt.click(); break
        await pg.wait_for_timeout(1500); await pg.screenshot(path='shots/then.png')
        print(errs)
        await b.close()
asyncio.run(main())
