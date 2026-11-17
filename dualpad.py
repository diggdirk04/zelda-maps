import asyncio
from playwright.async_api import async_playwright
U='http://localhost:8765/index.html'
PAD="""window.__pad={axes:[0,0,0,0],buttons:Array.from({length:17},()=>({pressed:false,value:0})),connected:true,id:'fake'};navigator.getGamepads=()=>[window.__pad];"""
def stub(role): return PAD+"""window.ZDual={_r:'%s',role(){return this._r},hasSecond(){return true},send(s){this._bc.postMessage(s)},openPanel(){},closePanel(){}};
ZDual._bc=new BroadcastChannel('fake');ZDual._bc.onmessage=e=>{const f=()=>window.zdRecv?zdRecv(e.data):setTimeout(f,50);f()};"""%role
async def both(pages,js):
    for p in pages: await p.evaluate(js)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');ctx=await b.new_context();errs=[]
        top=await ctx.new_page();await top.set_viewport_size({'width':960,'height':540});await top.add_init_script(stub('main'));top.on('pageerror',lambda e:errs.append(str(e)))
        await top.goto(U+'#/g/oot/d/9');await top.wait_for_timeout(800)
        bot=await ctx.new_page();await bot.set_viewport_size({'width':360,'height':413});await bot.add_init_script(stub('panel'));bot.on('pageerror',lambda e:errs.append(str(e)))
        await bot.goto(U);await bot.wait_for_timeout(1200)
        P=[top,bot]
        await top.evaluate('GP.V.zoomBy(3)')
        st=lambda: top.evaluate('Math.round(GP.V.ty)');sc=lambda: bot.evaluate("Math.round((document.querySelector('.gpside').scrollHeight>document.querySelector('.gpside').clientHeight?document.querySelector('.gpside'):document.scrollingElement).scrollTop)")
        a0,b0=await st(),await sc()
        await both(P,"__pad.axes[1]=0.9");await top.wait_for_timeout(500);await both(P,"__pad.axes[1]=0");await top.wait_for_timeout(300)
        a1,b1=await st(),await sc();print('owner=map: map moved',a0!=a1,'| panel scrolled',b0!=b1,'| frames',await top.evaluate("document.body.classList.contains('padown')"),await bot.evaluate("document.body.classList.contains('padown')"))
        await both(P,"__pad.buttons[8].pressed=true");await top.wait_for_timeout(400);await both(P,"__pad.buttons[8].pressed=false");await top.wait_for_timeout(300)
        print('after Select owner',await top.evaluate('PAD.owner'),await bot.evaluate('PAD.owner'),'frames',await top.evaluate("document.body.classList.contains('padown')"),await bot.evaluate("document.body.classList.contains('padown')"))
        a0,b0=await st(),await sc()
        await both(P,"__pad.axes[1]=0.9");await top.wait_for_timeout(500);await both(P,"__pad.axes[1]=0");await top.wait_for_timeout(300)
        a1,b1=await st(),await sc();print('owner=panel: map moved',a0!=a1,'| panel scrolled',b0!=b1)
        await both(P,"__pad.buttons[13].pressed=true");await top.wait_for_timeout(400);await both(P,"__pad.buttons[13].pressed=false");await top.wait_for_timeout(100)
        await both(P,"__pad.buttons[13].pressed=true");await top.wait_for_timeout(400);await both(P,"__pad.buttons[13].pressed=false");await top.wait_for_timeout(200)
        print('panel hl',await bot.evaluate("document.querySelector('.padhl')?.textContent?.slice(0,30)"),'top hash unchanged',await top.evaluate('location.hash'))
        await both(P,"__pad.buttons[0].pressed=true");await top.wait_for_timeout(400);await both(P,"__pad.buttons[0].pressed=false");await top.wait_for_timeout(500)
        print('A on panel -> top popup',await top.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        await bot.screenshot(path='shots/dp_bot.png');await top.screenshot(path='shots/dp_top.png')
        await both(P,"__pad.buttons[8].pressed=true");await top.wait_for_timeout(400);await both(P,"__pad.buttons[8].pressed=false");await top.wait_for_timeout(200)
        print('back to map',await top.evaluate('PAD.owner'),await bot.evaluate('PAD.owner'))
        print(errs);await b.close()
asyncio.run(main())
