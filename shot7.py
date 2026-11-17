import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/site/index.html'); await pg.wait_for_timeout(800)
        for gid in ['/tp_hd','/ss_surface','/mm_official']:
            c=await pg.evaluate_handle(f"""[...document.querySelectorAll('.card')].find(c=>(c.querySelector('.baseimg')?.src||'').includes('{gid}'))""")
            await c.evaluate("""c=>{c.querySelectorAll('.xlpanel details').forEach(d=>d.open=true);const ins=[...c.querySelectorAll('.xlpanel input')];const i=ins[ins.length-1];i.checked=true;i.dispatchEvent(new Event('change'));c.scrollIntoView()}""")
            await pg.wait_for_timeout(900)
            n=await c.evaluate("c=>[c.querySelectorAll('.lyrs [data-c]').length,c.querySelector('.vtabs button.on')?.textContent||'-',c.querySelector('.xlpanel .lyrinfo').textContent]")
            print(gid,n)
            await c.screenshot(path='shots/x7'+gid.replace('/','_')+'.png')
        print(errs); await b.close()
asyncio.run(main())
