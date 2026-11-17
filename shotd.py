import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1400,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U);await pg.wait_for_timeout(1500);await pg.screenshot(path='shots/t_home.png')
        await pg.evaluate("scrollTo(0,1100)");await pg.wait_for_timeout(500);await pg.screenshot(path='shots/t_home2.png')
        await pg.goto(U+'#/g/tp/d/0');await pg.wait_for_timeout(1500);await pg.click('.gpchk li[data-u] >> nth=2');await pg.wait_for_timeout(500);await pg.screenshot(path='shots/t_dg.png')
        await pg.goto(U+'#/g/botw/o/1');await pg.wait_for_timeout(1500);await pg.screenshot(path='shots/t_ow.png')
        m=await b.new_page(viewport={'width':390,'height':844});await m.goto(U);await m.wait_for_timeout(1200);await m.screenshot(path='shots/t_mob.png')
        print(errs);await b.close()
asyncio.run(main())
