import asyncio
from playwright.async_api import async_playwright
exec(open('synctest.py').read().split('async def main')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');ctx=await b.new_context(viewport={'width':1300,'height':800});errs=[]
        await ctx.add_init_script(MOCK)
        pa=await ctx.new_page();pa.on('pageerror',lambda e:errs.append(str(e)));await pa.goto(U+'#/g/mm/d/0');await pa.wait_for_timeout(1500)
        pb=await ctx.new_page();pb.on('pageerror',lambda e:errs.append(str(e)));await pb.goto(U+'#/g/mm/d/0');await pb.wait_for_timeout(1500)
        await pa.bring_to_front();await pa.click('.gpchk li[data-u] >> nth=2 >> input');await pa.wait_for_timeout(2500)
        print('B live ticks',await pb.evaluate("document.querySelectorAll('.gpchk li.done').length"),'A',await pa.evaluate("document.querySelectorAll('.gpchk li.done').length"))
        await pa.click('.gpchk li[data-u] >> nth=2 >> input');await pa.wait_for_timeout(2500)
        print('after untick B',await pb.evaluate("document.querySelectorAll('.gpchk li.done').length"))
        print(errs);await b.close()
asyncio.run(main())
