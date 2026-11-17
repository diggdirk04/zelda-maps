import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html')
        await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager');document.querySelector('.bar').style.position='static'")
        await pg.wait_for_timeout(2000)
        cards=await pg.query_selector_all('#maps .card')
        for c in cards:
            t=await c.inner_text()
            if t.startswith('Breath'):
                r=await c.query_selector('input[type=range]')
                await r.evaluate("e=>{e.value=55;e.dispatchEvent(new Event('input'))}")
                await pg.wait_for_timeout(500); await c.screenshot(path='shots/v_botw.png')
                btn=(await c.query_selector_all('.vtabs button'))[2]; await btn.click(); await pg.wait_for_timeout(500)
                await c.screenshot(path='shots/v_botw2.png')
            if t.startswith('A Link to the Past'):
                btn=(await c.query_selector_all('.vtabs button'))[1]; await btn.click(); await pg.wait_for_timeout(500)
                await c.screenshot(path='shots/v_alttp.png')
        print(errs)
        await b.close()
asyncio.run(main())
