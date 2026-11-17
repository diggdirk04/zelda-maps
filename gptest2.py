import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1400,'height':900});errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U+'#/g/oot/d/10');await pg.wait_for_timeout(900)
        print(await pg.evaluate("document.querySelector('.gpside h4').textContent"), await pg.evaluate("location.hash"))
        await pg.keyboard.press(']');await pg.wait_for_timeout(500);print('after ]',await pg.evaluate("location.hash"),await pg.evaluate("document.querySelector('.gpside h4').textContent"))
        await pg.keyboard.press('.');await pg.wait_for_timeout(500);print('after .',await pg.evaluate("location.hash"))
        await pg.keyboard.press('n');await pg.mouse.click(500,400);await pg.wait_for_timeout(300)
        await pg.keyboard.type('Hidden switch here');await pg.click('.gvpop [data-do="save"]');await pg.wait_for_timeout(200)
        print('notes',await pg.evaluate("document.querySelectorAll('#gpv .gm.note').length"))
        await pg.keyboard.press('o');await pg.wait_for_timeout(800);print('o ->',await pg.evaluate("location.hash"))
        await pg.click('.gpside [data-t="2"]');await pg.wait_for_timeout(800)
        await pg.click('#gpv .gm.dot >> nth=3');await pg.wait_for_timeout(300)
        await pg.screenshot(path='shots/g_atlas.png')
        await pg.click('[data-x="exp"]');await pg.wait_for_timeout(200)
        t=await pg.evaluate("document.querySelector('.gpmodal textarea').value");print('export len',len(t))
        await pg.keyboard.press('Escape');await pg.evaluate("localStorage.clear()")
        await pg.click('[data-x="imp"]');await pg.fill('.gpmodal textarea',t);await pg.click('.gpmodal [data-do="go"]');await pg.wait_for_timeout(500)
        print('after import done',await pg.evaluate("GP.done.size"),await pg.evaluate("Object.keys(localStorage).length"))
        await pg.keyboard.press('?');await pg.wait_for_timeout(200);await pg.screenshot(path='shots/g_help.png');await pg.keyboard.press('Escape')
        await pg.keyboard.press('Escape');await pg.keyboard.press('Escape');await pg.wait_for_timeout(500)
        await pg.screenshot(path='shots/g_home2.png')
        print('errs',errs);await b.close()
asyncio.run(main())
