import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html'); await pg.wait_for_timeout(800)
        s=await pg.query_selector('#dungeons-sec'); await s.scroll_into_view_if_needed()
        await pg.click('#dungeons .dgames button[data-g="tp"]'); await pg.wait_for_timeout(300)
        await pg.click('#dungeons .dnames button:nth-child(5)'); await pg.wait_for_timeout(800)
        await s.screenshot(path='shots/dg1.png')
        await pg.click('#dungeons .dgames button[data-g="mm"]'); await pg.wait_for_timeout(900)
        box=await pg.query_selector('.dmapwrap'); bb=await box.bounding_box()
        await pg.mouse.move(bb['x']+bb['width']/2,bb['y']+bb['height']/2)
        for i in range(3): await pg.mouse.wheel(0,-200); await pg.wait_for_timeout(150)
        await s.screenshot(path='shots/dg2.png')
        n=await pg.evaluate("Object.values(DUNG).reduce((a,g)=>a+g.m.length,0)")
        print('maps',n,errs); await b.close()
asyncio.run(main())
