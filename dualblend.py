import asyncio
from playwright.async_api import async_playwright
U='http://localhost:8765/index.html'
exec(open('dualpad.py').read().split('async def both')[0].split("U='http://localhost:8765/index.html'")[1])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');ctx=await b.new_context();errs=[]
        top=await ctx.new_page();await top.set_viewport_size({'width':960,'height':540});await top.add_init_script(stub('main'));top.on('pageerror',lambda e:errs.append(str(e)))
        await top.goto(U+'#/g/botw/o/1');await top.wait_for_timeout(1200)
        bot=await ctx.new_page();await bot.set_viewport_size({'width':360,'height':700});await bot.add_init_script(stub('panel'));bot.on('pageerror',lambda e:errs.append(str(e)))
        await bot.goto(U);await bot.wait_for_timeout(1500)
        await bot.select_option('.gpbl',label='Sky (TotK)');
        await bot.evaluate("(()=>{const r=document.querySelector('.gpblr');for(const v of [20,40,70]){r.value=v;r.dispatchEvent(new Event('input',{bubbles:true}))}})()");await top.wait_for_timeout(800)
        o=lambda: top.evaluate("(()=>{const o=document.querySelector('#gpv .gvovl');return [o.src.split('/').pop(),getComputedStyle(o).opacity]})()")
        print('top overlay after panel slider',await o())
        await bot.click('.gpseg button[data-v="list"]');await top.wait_for_timeout(800)
        print('top overlay after another sync',await o(),'| panel slider',await bot.evaluate("document.querySelector('.gpblr')?.value"))
        await bot.click('.gpside [data-t="0"]');await top.wait_for_timeout(1200);print('after tab change',await o())
        print(errs);await b.close()
asyncio.run(main())
