import asyncio
from playwright.async_api import async_playwright
U='http://localhost:8765/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context()
        top=await ctx.new_page();await top.set_viewport_size({'width':540,'height':960})
        msgs=[];top.on('console',lambda m:msgs.append('T '+m.text))
        await top.goto(U+'#/g/oot/d/9');await top.wait_for_timeout(700)
        bot=await ctx.new_page();await bot.set_viewport_size({'width':360,'height':413})
        bot.on('console',lambda m:msgs.append('B '+m.text))
        await bot.goto(U+'?panel=1');await bot.wait_for_timeout(1000)
        print('bot hash',await bot.evaluate('location.hash'))
        await top.evaluate("document.querySelectorAll('#gpv .gm.dot')[4].click()");await top.wait_for_timeout(600)
        print('top sel',await top.evaluate("GP.sel&&GP.sel.name"),'bot hl',await bot.evaluate("document.querySelector('.gpchk li.hl b')?.textContent"))
        pass
        await bot.evaluate("location.hash='#/'");await bot.wait_for_timeout(800)
        print('home sync',await top.evaluate("document.body.classList.contains('gp-on')"),await top.evaluate('location.hash'))
        print('\n'.join(msgs[-8:]));await b.close()
asyncio.run(main())
