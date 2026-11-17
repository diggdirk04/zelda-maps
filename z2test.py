import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1400,'height':900});errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U+'#/g/aol/o/1');await pg.wait_for_timeout(1000)
        await pg.click('.gpside [data-a="all"]');await pg.wait_for_timeout(300)
        await pg.screenshot(path='shots/z2_world.png')
        await pg.evaluate("location.hash='#/g/aol/d/5'");await pg.wait_for_timeout(1000)
        await pg.screenshot(path='shots/z2_pal.png')
        print(await pg.evaluate("Object.keys(DUNG).join(',')"),errs);await b.close()
asyncio.run(main())
