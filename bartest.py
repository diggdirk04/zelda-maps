import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1300,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html');await pg.wait_for_timeout(700)
        st=lambda: pg.evaluate("(()=>{const b=document.querySelector('.bar');const r=b.getBoundingClientRect();return [b.classList.contains('bar-hide'),Math.round(r.top),Math.round(r.bottom)]})()")
        print('top of page',await st())
        for i in range(10): await pg.mouse.wheel(0,250);await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(400);print('scrolled down',await st())
        await pg.mouse.wheel(0,-150);await pg.wait_for_timeout(400);print('scrolled up a bit',await st())
        await pg.screenshot(path='shots/bar_up.png')
        await pg.wait_for_timeout(2800);print('after 2.8s idle',await st())
        await pg.mouse.wheel(0,-150);await pg.wait_for_timeout(300);await pg.hover('.bar .chip >> nth=0');await pg.wait_for_timeout(3000);print('hovering keeps it',await st())
        await pg.evaluate('scrollTo(0,0)');await pg.wait_for_timeout(400);print('back at top',await st())
        print(errs);await b.close()
asyncio.run(main())
