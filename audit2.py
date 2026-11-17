import asyncio,os,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vp,name in [({'width':1300,'height':1000},'desk'),({'width':390,'height':844},'mob')]:
            pg=await b.new_page(viewport=vp)
            errs=[];bad=[]
            pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
            pg.on('requestfailed',lambda r:bad.append(r.url))
            import time;t=time.time()
            await pg.goto('file:///home/claude/site/index.html',wait_until='load'); await pg.wait_for_timeout(500)
            print(name,'load s',round(time.time()-t,2))
            r=await pg.evaluate("""()=>{
             const imgs=new Set();GAMES.concat(SKY).forEach(g=>{imgs.add(g.img);(g.v||[]).forEach(v=>imgs.add(v[0]));(g.extra||[]).forEach(e=>imgs.add(e[0]))});
             Object.values(DUNG).forEach(D=>D.m.forEach(m=>imgs.add(m.img)));
             let oob=0,emptyItems=0;Object.entries(XL).forEach(([g,cs])=>cs.forEach(c=>{if(!c.it.length)emptyItems++;c.it.forEach(r=>{if(r[0]<0||r[0]>100||r[1]<0||r[1]>100)oob++})}));
             let doob=0,dempty=[];Object.entries(DUNG).forEach(([g,D])=>D.m.forEach(m=>{if(!m.it.length)dempty.push(g+':'+m.d+':'+m.f);m.it.forEach(r=>{if(r[0]<0||r[0]>100||r[1]<0||r[1]>100)doob++})}));
             const tabs={};GAMES.forEach(g=>{const ks=[g.bl].concat((g.v||[]).map(v=>v[3]));(XL[g.id]||[]).forEach(c=>c.it.forEach(r=>{if(!ks.includes(r[2]))tabs[g.id+':'+r[2]]=1}))});
             const docW=document.documentElement.scrollWidth;
             return {imgs:[...imgs],oob,emptyItems,doob,dempty,orphanTabs:Object.keys(tabs),docW,games:GAMES.length,dom:document.querySelectorAll('*').length}}""")
            miss=[i for i in r['imgs'] if not os.path.exists('site/maps/'+i)]
            print(name,{k:v for k,v in r.items() if k!='imgs'},'missing imgs',miss,'errs',errs[:5],'failed',bad[:5])
            await pg.screenshot(path=f'shots/audit_{name}.png')
            await pg.close()
        await b.close()
asyncio.run(main())
