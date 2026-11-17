import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1366,'height':820})
        await pg.goto(U+'#/g/oot/d/3');await pg.wait_for_timeout(800)
        await pg.click('#gpv .gm.dot >> nth=2');await pg.wait_for_timeout(300)
        print('mouse click popup',await pg.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        await pg.keyboard.press('Escape')
        await pg.evaluate('GP.V.zoomBy(3)');s0=await pg.evaluate('[GP.V.tx,GP.V.ty]')
        await pg.mouse.move(500,400);await pg.mouse.down();await pg.mouse.move(400,350,steps=8);await pg.mouse.up();await pg.wait_for_timeout(100)
        s1=await pg.evaluate('[GP.V.tx,GP.V.ty]');print('drag moved',s0!=s1,'popup after drag',await pg.evaluate("document.querySelector('.gvpop').classList.contains('open')"))
        await pg.mouse.dblclick(600,400);await pg.wait_for_timeout(200);print('dblclick zoom',await pg.evaluate('GP.V.s'))
        t=await b.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
        await t.goto(U+'#/g/tp/d/3');await t.wait_for_timeout(1000)
        await t.tap('#gpv .gm.dot >> nth=1');await t.wait_for_timeout(300)
        print('touch tap popup',await t.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        await t.tap('.gvpop [data-do="done"]');await t.wait_for_timeout(200);print('tap found',await t.evaluate('GP.done.size'))
        await b.close()
asyncio.run(main())
