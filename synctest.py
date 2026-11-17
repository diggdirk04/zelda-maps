import asyncio
from playwright.async_api import async_playwright
U='http://localhost:8765/index.html'
MOCK="""(function(){const bc=new BroadcastChannel('mockdb');const store=JSON.parse(localStorage.getItem('__mock')||'null')||{};window.__store=store;const subs=[];
function snap(prefix){const docs=Object.entries(store).filter(([p])=>p.startsWith(prefix+'/')&&!p.slice(prefix.length+1).includes('/')).map(([p,b])=>({id:p.split('/').pop(),exists:true,data:()=>b,metadata:{fromCache:false,hasPendingWrites:false}}));return {docs,size:docs.length,empty:!docs.length,metadata:{fromCache:false,hasPendingWrites:false},docChanges:()=>[]}}
bc.onmessage=e=>{store[e.data.p]=e.data.b;subs.forEach(s=>s())};
const col=path=>({path,doc:id=>({id,path:path+'/'+id,set:async b=>{if(!/^[A-Za-z0-9_\\-.~:@+]+$/.test(id))throw {code:'invalid_argument',message:'bad id '+id};store[path+'/'+id]=JSON.parse(JSON.stringify(b));bc.postMessage({p:path+'/'+id,b});subs.forEach(s=>s())}}),
 onSnapshot:(next,err)=>{const f=()=>setTimeout(()=>next(snap(path)),5);subs.push(f);f();return ()=>{}}});
window.claude={use:async n=>n==='db'?{collection:col}:n==='user'?{id:async()=>'u123'}:null};})();"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        A=await b.new_context(viewport={'width':1300,'height':800});B=await b.new_context(viewport={'width':1300,'height':800})
        errs=[]
        # contexts don't share BroadcastChannel -> bridge via python relay
        pa=await A.new_page();pb=await B.new_page()
        for pg in (pa,pb):
            await pg.add_init_script(MOCK);pg.on('pageerror',lambda e:errs.append(str(e)))
        # pre-existing local progress on B before sync existed
        await pb.goto(U+'#/g/la/d/0');await pb.wait_for_timeout(800)
        await pb.evaluate("localStorage.setItem('zm:done:la',JSON.stringify(['preB']));localStorage.removeItem('zmmt')")
        await pa.goto(U+'#/g/la/d/0');await pa.wait_for_timeout(1500)
        await pa.click('.gpchk li[data-u] >> nth=0 >> input');await pa.wait_for_timeout(1800)
        storeA=await pa.evaluate("JSON.stringify(window.__store)")
        print('A synced status:',(await pa.inner_text('.gpsync'))[:40],'| docs',list(__import__('json').loads(storeA).keys())[:5])
        # relay A's store into B's mock (simulates server), then load B
        await pb.evaluate(f"localStorage.setItem('__mock',{storeA!r})")
        await pb.reload();await pb.wait_for_timeout(2500)
        print('B done after sync (expects A tick + preB merged):',await pb.evaluate("JSON.parse(localStorage.getItem('zm:done:la'))"))
        print('B page shows ticks:',await pb.evaluate("document.querySelectorAll('.gpchk li.done').length"))
        print(errs);await b.close()
asyncio.run(main())
