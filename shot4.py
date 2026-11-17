import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html')
        await pg.evaluate("document.querySelector('.bar').style.position='static'")
        await pg.wait_for_timeout(1000)
        el=await pg.query_selector('#callbacks'); await el.screenshot(path='shots/cb.png')
        print(errs, await pg.inner_text('#rc'))
        await b.close()
asyncio.run(main())
