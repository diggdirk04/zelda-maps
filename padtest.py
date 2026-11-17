import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
INIT="""window.__pad={axes:[0,0,0,0],buttons:Array.from({length:17},()=>({pressed:false,value:0})),connected:true,id:'fake'};
navigator.getGamepads=()=>[window.__pad];"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1280,'height':720});errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)));await pg.add_init_script(INIT)
        await pg.goto(U+'#/g/oot/o/2');await pg.wait_for_timeout(900)
        st=lambda: pg.evaluate("[+GP.V.s.toFixed(2),Math.round(GP.V.tx),Math.round(GP.V.ty)]")
        await pg.evaluate("__pad.axes[3]=-1");await pg.wait_for_timeout(500);await pg.evaluate("__pad.axes[3]=0");await pg.wait_for_timeout(300)
        print('after zoom',await st())
        await pg.evaluate("__pad.axes[0]=0.8");await pg.wait_for_timeout(400);a=await st();await pg.evaluate("__pad.axes[0]=0");await pg.wait_for_timeout(150);b1=await st();await pg.wait_for_timeout(600);c=await st()
        print('pan',a,'release+150ms',b1,'later',c)
        await pg.evaluate("__pad.axes[1]=0.08");await pg.wait_for_timeout(500);print('deadzone drift',await st())
        await pg.evaluate("(()=>{const c=gpModel(GP.g).cats.find(c=>c.it.some(r=>r.tab==='atlas'&&c.kind!=='label'));const r=c.it.find(r=>r.tab==='atlas');GP.on.add(c.id);gpOwMarkers();GP.V.focus(r.x,r.y,3)})()");await pg.wait_for_timeout(200)
        await pg.evaluate("__pad.buttons[0].pressed=true");await pg.wait_for_timeout(100);await pg.evaluate("__pad.buttons[0].pressed=false");await pg.wait_for_timeout(300)
        print('A ->',await pg.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"),'gpad',await pg.evaluate("document.body.classList.contains('gpad')"))
        await pg.evaluate("__pad.buttons[0].pressed=true");await pg.wait_for_timeout(100);await pg.evaluate("__pad.buttons[0].pressed=false");await pg.wait_for_timeout(300)
        print('A again done',await pg.evaluate("GP.done.size"))
        await pg.screenshot(path='shots/pad.png')
        await pg.evaluate("__pad.buttons[5].pressed=true");await pg.wait_for_timeout(100);await pg.evaluate("__pad.buttons[5].pressed=false");await pg.wait_for_timeout(600)
        print('R1 ->',await pg.evaluate("location.hash"))
        # arrow key held w/o keyup -> must stop
        await pg.evaluate('GP.V.zoomBy(3)');await pg.wait_for_timeout(300);x0=await st();await pg.keyboard.down('ArrowRight');await pg.wait_for_timeout(1500);x1=await st();await pg.wait_for_timeout(800);print('stuck key guard',x0,x1,await st())
        print(errs);await b.close()
asyncio.run(main())
