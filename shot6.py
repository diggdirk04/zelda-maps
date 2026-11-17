import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        await pg.goto('file:///home/claude/site/index.html'); await pg.wait_for_timeout(800)
        async def card(gid):
            return await pg.evaluate_handle(f"""[...document.querySelectorAll('.card')].find(c=>(c.querySelector('.baseimg')?.src||'').includes('{gid}'))""")
        # BotW: towers + place names
        c=await card('botw.webp')
        await c.evaluate("""c=>{c.querySelectorAll('.xlpanel details').forEach(d=>d.open=true);
          for(const l of c.querySelectorAll('.xlpanel label')){if(/Sheikah Tower|^ *Place names \\(|Stable/.test(l.textContent)&&!/TotK/.test(l.textContent)){const i=l.querySelector('input');i.checked=true;i.dispatchEvent(new Event('change'))}}
          c.scrollIntoView()}""")
        await pg.wait_for_timeout(1200); await c.screenshot(path='shots/xl_botw.png')
        # switch to totk depths via checking zonaite
        await c.evaluate("""c=>{for(const l of c.querySelectorAll('.xlpanel label')){if(/Zonaite|Dungeon Boss/.test(l.textContent)){const i=l.querySelector('input');i.checked=true;i.dispatchEvent(new Event('change'))}}}""")
        await pg.wait_for_timeout(1200); await c.screenshot(path='shots/xl_depths.png')
        for gid,rx in [('/la.webp','Piece of Heart|Region'),('/eow.webp','Might|Place'),('alttp_light','Item')]:
            c=await card(gid)
            await c.evaluate(f"""c=>{{c.querySelectorAll('.xlpanel details').forEach(d=>d.open=true);for(const l of c.querySelectorAll('.xlpanel label')){{if(/{rx}/.test(l.textContent)){{const i=l.querySelector('input');i.checked=true;i.dispatchEvent(new Event('change'))}}}};c.scrollIntoView()}}""")
            await pg.wait_for_timeout(900); await c.screenshot(path='shots/xl_'+gid.strip('/').split('.')[0]+'.png')
        print(errs)
        await b.close()
asyncio.run(main())
