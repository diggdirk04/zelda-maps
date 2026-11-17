import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html'); await pg.wait_for_timeout(800)
        s=await pg.query_selector('#dungeons-sec'); await s.scroll_into_view_if_needed()
        await pg.click('#dungeons .dgames button[data-g="oot"]'); await pg.wait_for_timeout(300)
        await pg.click('#dungeons .dnames button:nth-child(4)'); await pg.wait_for_timeout(300)
        await pg.click('#dungeons .dfloors button:nth-child(2)'); await pg.wait_for_timeout(900)
        await s.screenshot(path='shots/mq.png'); print(errs); await b.close()
asyncio.run(main())
