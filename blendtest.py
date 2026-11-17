import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1300,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U+'#/g/alttp/o/0');await pg.wait_for_timeout(1000)
        await pg.evaluate("(()=>{const r=document.querySelector('.gpblr');r.value=60;r.dispatchEvent(new Event('input',{bubbles:true}))})()");await pg.wait_for_timeout(500)
        print('game page ovl',await pg.evaluate("(()=>{const o=document.querySelector('#gpv .gvovl');return [o.src.split('/').pop(),getComputedStyle(o).opacity,o.naturalWidth,o.getBoundingClientRect().width,getComputedStyle(o).display,getComputedStyle(o).zIndex]})()"))
        # real drag on slider
        bb=await pg.evaluate("(()=>{const r=document.querySelector('.gpblr').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
        await pg.mouse.click(bb[0]+bb[2]*0.9,bb[1]+bb[3]/2);await pg.wait_for_timeout(300)
        print('after click slider',await pg.evaluate("[document.querySelector('.gpblr')?.value,getComputedStyle(document.querySelector('#gpv .gvovl')).opacity]"))
        await pg.screenshot(path='shots/blend_gp.png')
        await pg.goto(U);await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{const r=document.querySelector('#compare .blend input[type=range]');r.value=60;r.dispatchEvent(new Event('input',{bubbles:true}))})()");await pg.wait_for_timeout(300)
        print('home ovl',await pg.evaluate("(()=>{const o=document.querySelector('#compare .map .ovl');return [o.src.split('/').pop(),getComputedStyle(o).opacity,o.naturalWidth]})()"))
        print(errs);await b.close()
asyncio.run(main())
