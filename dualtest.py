import asyncio
from playwright.async_api import async_playwright
U='http://localhost:8765/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context()
        top=await ctx.new_page();await top.set_viewport_size({'width':1080//2,'height':1920//2})
        errs=[];top.on('pageerror',lambda e:errs.append('T '+str(e)))
        await top.goto(U);await top.wait_for_timeout(700)
        bot=await ctx.new_page();await bot.set_viewport_size({'width':360,'height':413})
        bot.on('pageerror',lambda e:errs.append('B '+str(e)))
        await bot.goto(U+'?panel=1');await bot.wait_for_timeout(800)
        print('roles',await top.evaluate('ZD.role'),await bot.evaluate('ZD.role'))
        await bot.screenshot(path='shots/d_bot_home.png')
        await bot.click('#zdhome a[href="#/g/oot"]');await bot.wait_for_timeout(1200)
        print('top hash',await top.evaluate('location.hash'),'bot',await bot.evaluate('location.hash'))
        await bot.click('.gpmodes button[data-m="d"]');await bot.wait_for_timeout(1200)
        print('after d: top',await top.evaluate('location.hash'),'bot',await bot.evaluate('location.hash'))
        await bot.click('.gpdl button >> nth=3');await bot.wait_for_timeout(1200)
        await bot.click('.gpchk li[data-u] >> nth=1');await bot.wait_for_timeout(800)
        await bot.click('.gpchk li[data-u] >> nth=1 >> input');await bot.wait_for_timeout(800)
        print('top hash',await top.evaluate('location.hash'),'done top',await top.evaluate('GP.done.size'),'bot',await bot.evaluate('GP.done.size'),'top popup',await top.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        # main marker click -> panel highlight
        await top.click('#gpv .gm.dot >> nth=4');await top.wait_for_timeout(600)
        print('bot hl',await bot.evaluate("document.querySelector('.gpchk li.hl b')?.textContent"),'top sel',await top.evaluate("GP.sel&&GP.sel.name"))
        # panel search
        await bot.fill('.gpsearch input','kokiri');await bot.wait_for_timeout(300);await bot.keyboard.press('Enter');await bot.wait_for_timeout(1500)
        print('after search top',await top.evaluate('location.hash'),await top.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        await top.screenshot(path='shots/d_top.png');await bot.screenshot(path='shots/d_bot.png',full_page=True)
        await bot.click('.gpback');await bot.wait_for_timeout(800)
        print('home sync',await top.evaluate("document.body.classList.contains('gp-on')"))
        await bot.close();await top.wait_for_timeout(500)
        print('top role after close',await top.evaluate('ZD.role'))
        print('errs',errs);await b.close()
asyncio.run(main())
