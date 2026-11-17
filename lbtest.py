import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
INIT="""window.__pad={axes:[0,0,0,0],buttons:Array.from({length:17},()=>({pressed:false,value:0})),connected:true,id:'fake'};navigator.getGamepads=()=>[window.__pad];"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1280,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(INIT);await pg.goto(U);await pg.wait_for_timeout(800)
        await pg.evaluate("document.querySelectorAll('.foldbody').forEach(d=>d.hidden=false)");await pg.wait_for_timeout(300)
        await pg.evaluate("document.querySelector('#maps').scrollIntoView()");await pg.wait_for_timeout(200)
        y0=await pg.evaluate('scrollY')
        await pg.click('#maps .card .map >> nth=2');await pg.wait_for_timeout(600)
        st=lambda: pg.evaluate("LBZ?[+LBZ.s.toFixed(2),Math.round(LBZ.tx),Math.round(LBZ.ty)]:null")
        print('open',await st(),'lb display',await pg.evaluate("getComputedStyle(document.getElementById('lightbox')).display"))
        await pg.screenshot(path='shots/lb_open.png')
        # right stick zoom
        await pg.evaluate("__pad.axes[3]=-1");await pg.wait_for_timeout(600);await pg.evaluate("__pad.axes[3]=0");await pg.wait_for_timeout(200);print('stick zoom',await st())
        await pg.evaluate("__pad.axes[0]=0.9;__pad.axes[1]=0.6");await pg.wait_for_timeout(500);await pg.evaluate("__pad.axes[0]=0;__pad.axes[1]=0");await pg.wait_for_timeout(300);print('stick pan',await st())
        print('background scrolled?',await pg.evaluate('scrollY')!=y0)
        await pg.mouse.move(640,350);await pg.mouse.wheel(0,-400);await pg.wait_for_timeout(400);print('wheel zoom',await st(),'bg',await pg.evaluate('scrollY')==y0)
        await pg.screenshot(path='shots/lb_zoom.png')
        # tab switch via R1
        t0=await pg.evaluate("document.querySelector('#lbinner .vtabs button.on')?.textContent")
        await pg.evaluate("__pad.buttons[5].pressed=true");await pg.wait_for_timeout(150);await pg.evaluate("__pad.buttons[5].pressed=false");await pg.wait_for_timeout(300)
        print('R1 tab',t0,'->',await pg.evaluate("document.querySelector('#lbinner .vtabs button.on')?.textContent"))
        # drag pans, click on map doesn't close
        await pg.mouse.move(640,350);await pg.mouse.down();await pg.mouse.move(560,330,steps=6);await pg.mouse.up();await pg.wait_for_timeout(200)
        print('after drag still open',await pg.evaluate("document.body.classList.contains('lb-open')"))
        await pg.evaluate("__pad.buttons[1].pressed=true");await pg.wait_for_timeout(150);await pg.evaluate("__pad.buttons[1].pressed=false");await pg.wait_for_timeout(300)
        print('B closes',not await pg.evaluate("document.body.classList.contains('lb-open')"),'bg same',await pg.evaluate('scrollY')==y0)
        # callbacks pin
        await pg.fill('#rq','hylia');await pg.wait_for_timeout(300)
        await pg.evaluate("document.querySelector('.rb[data-m=then]').click()");await pg.wait_for_timeout(900)
        print('callback pin open',await st(),await pg.inner_text('#lbcap'))
        await pg.screenshot(path='shots/lb_pin.png')
        await pg.keyboard.press('Escape');await pg.wait_for_timeout(200);print('esc closes',not await pg.evaluate("document.body.classList.contains('lb-open')"))
        # extras figure (solo image)
        await pg.evaluate("document.querySelector('#stacks figure')?.click()");await pg.wait_for_timeout(700);print('solo image',await st())
        await pg.click('.lbx');await pg.wait_for_timeout(200)
        # touch pinch on mobile
        t=await b.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True);t.on('pageerror',lambda e:errs.append(str(e)))
        await t.goto(U);await t.wait_for_timeout(800);await t.evaluate("document.querySelector('#maps .card .map').click()");await t.wait_for_timeout(600)
        cdp=await t.context.new_cdp_session(t)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':150,'y':300,'id':1},{'x':240,'y':300,'id':2}]})
        for i in range(1,8): await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':150-i*12,'y':300,'id':1},{'x':240+i*12,'y':300,'id':2}]});await t.wait_for_timeout(16)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await t.wait_for_timeout(200)
        print('mobile pinch',await t.evaluate("[+LBZ.s.toFixed(2),visualViewport.scale]"))
        await t.screenshot(path='shots/lb_mob.png')
        print(errs);await b.close()
asyncio.run(main())
