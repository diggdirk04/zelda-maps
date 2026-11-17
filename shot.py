import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1300,'height':900})
        await pg.goto('file:///home/claude/site/index.html')
        await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
        await pg.wait_for_timeout(2500)
        cards=await pg.query_selector_all('#maps .card')
        for i,c in enumerate(cards):
            await c.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
            await c.screenshot(path=f'shots/c{i}.png')
        await b.close()
asyncio.run(main())
