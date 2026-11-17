import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=await b.new_page(viewport={'width':1366,'height':820});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U+'#/g/botw/o/1');await pg.wait_for_timeout(1200)
        # animated zoom: sample mid-animation
        await pg.click('.gvz button[data-z="1"]');await pg.wait_for_timeout(90);mid=await pg.evaluate('GP.V.s');await pg.wait_for_timeout(300);end=await pg.evaluate('GP.V.s')
        print('button zoom mid',round(mid,2),'end',round(end,2))
        # fling
        await pg.evaluate('GP.V.zoomBy(3,true)');await pg.wait_for_timeout(100)
        x0=await pg.evaluate('GP.V.tx')
        await pg.mouse.move(700,400);await pg.mouse.down()
        for i in range(6): await pg.mouse.move(700-i*40,400);await pg.wait_for_timeout(16)
        await pg.mouse.up();x1=await pg.evaluate('GP.V.tx');await pg.wait_for_timeout(700);x2=await pg.evaluate('GP.V.tx')
        print('fling: at release moved',round(x1-x0),'glide extra',round(x2-x1))
        print('minimap on',await pg.evaluate("document.querySelector('.gvmini').classList.contains('on')"))
        await pg.click('.gvmini',position={'x':10,'y':10});await pg.wait_for_timeout(700)
        r=await pg.evaluate("GP.V.toPct(GP.V.host.getBoundingClientRect().left+GP.V.host.clientWidth/2,GP.V.host.getBoundingClientRect().top+GP.V.host.clientHeight/2)")
        print('after minimap click center at %',[round(v) for v in r])
        await pg.screenshot(path='shots/s_mini.png')
        # checklist
        await pg.click('.gpseg button[data-v="list"]');await pg.wait_for_timeout(200)
        await pg.fill('.gplq','lynel');await pg.wait_for_timeout(500)
        n=await pg.evaluate("document.querySelectorAll('.gplist li[data-u]').length");print('checklist lynel items',n)
        await pg.click('.gplist li[data-u] >> nth=0');await pg.wait_for_timeout(700);print('list click popup',await pg.evaluate("document.querySelector('.gvpop.open b.t')?.textContent"))
        await pg.click('.gplist li[data-u] >> nth=0 >> input');await pg.wait_for_timeout(200)
        print('toast',await pg.evaluate("document.querySelector('.gvtoast').textContent"),'done',await pg.evaluate('GP.done.size'))
        await pg.screenshot(path='shots/s_list.png')
        await pg.click('.gvtoast button');await pg.wait_for_timeout(200);print('after undo',await pg.evaluate('GP.done.size'))
        await pg.select_option('.gplf','done');await pg.wait_for_timeout(200);print('found filter text',(await pg.inner_text('.gplist'))[:60])
        # long press touch
        t=await b.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True);t.on('pageerror',lambda e:errs.append(str(e)))
        await t.goto(U+'#/g/tp/d/3');await t.wait_for_timeout(1000)
        box=await t.evaluate("(()=>{const r=document.querySelectorAll('#gpv .gm.dot')[1].getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
        cdp=await t.context.new_cdp_session(t)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':box[0],'y':box[1]}]});await t.wait_for_timeout(650)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await t.wait_for_timeout(300)
        print('long-press done',await t.evaluate('GP.done.size'),'popup',await t.evaluate("document.querySelector('.gvpop').classList.contains('open')"))
        print(errs);await b.close()
asyncio.run(main())
