import asyncio
from playwright.async_api import async_playwright
U='http://localhost:8765/index.html'
def stub(role): return """window.ZDual={_r:'%s',role(){return this._r},hasSecond(){return true},send(s){this._bc.postMessage(s)},openPanel(){},closePanel(){}};
ZDual._bc=new BroadcastChannel('fake');ZDual._bc.onmessage=e=>{const f=()=>window.zdRecv?zdRecv(e.data):setTimeout(f,50);f()};"""%role
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');ctx=await b.new_context();errs=[]
        top=await ctx.new_page();await top.set_viewport_size({'width':960,'height':540});await top.add_init_script(stub('main'));top.on('pageerror',lambda e:errs.append(str(e)))
        await top.goto(U+'#/g/tp/d/2');await top.wait_for_timeout(800)
        bot=await ctx.new_page();await bot.set_viewport_size({'width':360,'height':413});await bot.add_init_script(stub('panel'));bot.on('pageerror',lambda e:errs.append(str(e)))
        await bot.goto(U);await bot.wait_for_timeout(1200)
        print('bot follows',await bot.evaluate('location.hash'),await top.evaluate('ZD.role'),await bot.evaluate('ZD.role'))
        await bot.click('.gpchk li[data-u] >> nth=0');await bot.wait_for_timeout(700)
        print('top popup',await top.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        await top.evaluate("zdRole('solo')");await top.wait_for_timeout(300)
        print('side visible solo',await top.evaluate("getComputedStyle(document.querySelector('.gpside')).display"))
        await top.screenshot(path='shots/d3_top.png')
        print(errs);await b.close()
asyncio.run(main())
