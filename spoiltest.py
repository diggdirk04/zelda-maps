import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1366,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        r=await pg.goto(U);await pg.wait_for_timeout(600)
        regs=await pg.evaluate("GAMES.map(g=>{const M=gpModel(g);return g.id+':'+M.tabs.map(t=>{const R=gpRegions(g,t);return R.list.length+(R.lvl===8?'g':R.lvl===9?'a':'')}).join('/')}).join(' ')")
        print('regions per tab:',regs)
        await pg.evaluate("location.hash='#/g/botw/o/1'");await pg.wait_for_timeout(1200)
        n0=await pg.evaluate("document.querySelectorAll('#gpv .gm').length")
        await pg.click('.gpspoil');await pg.wait_for_timeout(300)
        n1=await pg.evaluate("document.querySelectorAll('#gpv .gm').length");print('markers before/after spoiler-free',n0,n1)
        await pg.mouse.click(400,400);await pg.wait_for_timeout(300);print('toast',await pg.inner_text('.gvtoast'))
        await pg.click('.gvtoast button');await pg.wait_for_timeout(300);n2=await pg.evaluate("document.querySelectorAll('#gpv .gm').length");print('after reveal',n2)
        await pg.fill('.gpsearch input','lynel');await pg.wait_for_timeout(200);print('search results in spoiler mode',await pg.evaluate("document.querySelectorAll('.gpres [data-i]').length"));await pg.keyboard.press('Escape')
        await pg.click('.gpseg button[data-v="list"]');await pg.select_option('.gplg','reg');await pg.wait_for_timeout(300)
        print('locked regions',await pg.evaluate("document.querySelectorAll('.gpregh').length"),'open groups',await pg.evaluate("document.querySelectorAll('.gplist details').length"))
        await pg.click('.gpreg summary');await pg.wait_for_timeout(200)
        await pg.screenshot(path='shots/sp_list.png')
        await pg.evaluate("location.hash='#/g/oot/d/3'");await pg.wait_for_timeout(800);await pg.click('.gpspoil');await pg.wait_for_timeout(300)
        print('dungeon hidden box',await pg.evaluate("!!document.querySelector('.gphidden')"),'markers',await pg.evaluate("document.querySelectorAll('#gpv .gm.dot').length"))
        await pg.click('[data-rvd]');await pg.wait_for_timeout(300);print('after reveal dungeon markers',await pg.evaluate("document.querySelectorAll('#gpv .gm.dot').length"))
        await pg.click('.gpspoil');await pg.wait_for_timeout(200)
        print(errs);await b.close()
asyncio.run(main())
