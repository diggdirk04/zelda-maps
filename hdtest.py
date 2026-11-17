import asyncio
from playwright.async_api import async_playwright
import sys
import sys
U=sys.argv[1] if len(sys.argv)>1 else 'file:///home/claude/site/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1280,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U);await pg.wait_for_timeout(600)
        todo=await pg.evaluate("GAMES.flatMap(g=>gpModel(g).tabs.map((t,i)=>[g.id,i,t.img]).filter(x=>HDMAPS[x[2]]))")
        print(len(todo),'tabs with HD');bad=[]
        for gid,i,img in todo:
            await pg.goto(U+f'#/g/{gid}/o/{i}');await pg.wait_for_timeout(700)
            await pg.evaluate("(()=>{const V=GP.V;V.s=6;V.tx=-V.W*2.2;V.ty=-V.H*2.2;V.apply();gpHdUpdate()})()")
            await pg.wait_for_timeout(1500)
            r=await pg.evaluate("[GP.hd?GP.hd.cfg.pre:null,document.querySelectorAll('.gvhd img.on').length,document.querySelectorAll('.gvhd img').length,document.querySelector('.gvhd').className]")
            print(gid,i,img,r)
            if not r[1]: bad.append((gid,img))
        await pg.screenshot(path='shots/hd_last.png')
        print('bad',bad,'errs',errs[:3]);await b.close()
asyncio.run(main())
