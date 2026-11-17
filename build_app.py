import os,shutil,hashlib,json,re
SITE='site'; APP='dist/zelda-maps-app'; WEB=APP+'/web'
for d in ['maps','icons']:
    if os.path.exists(WEB+'/'+d): shutil.rmtree(WEB+'/'+d)
    shutil.copytree(SITE+'/'+d,WEB+'/'+d,ignore=shutil.ignore_patterns('_*pack.webp'))
h=open(SITE+'/index.html',encoding='utf-8').read()
head='<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#13232a"><link rel="icon" href="appicons/icon-192.png"><link rel="apple-touch-icon" href="appicons/icon-192.png">'
h=h.replace('</title>','</title>'+head,1)
h=h.replace('</body></html>',"<script>try{if('serviceWorker' in navigator&&location.protocol.startsWith('http'))navigator.serviceWorker.register('sw.js').catch(()=>{})}catch(e){}</script></body></html>")
open(WEB+'/index.html','w',encoding='utf-8').write(h)
files=['./','index.html','manifest.webmanifest']
for root,_,fs in os.walk(WEB):
    for f in fs:
        p=os.path.relpath(os.path.join(root,f),WEB).replace(os.sep,'/')
        if p in('index.html','manifest.webmanifest','sw.js') or p.startswith('maps/dg/'): continue
        files.append(p)
sig=hashlib.sha1(h.encode()+json.dumps(sorted(files)).encode()).hexdigest()[:8]
sw=open(WEB+'/sw.js').read()
sw=re.sub(r"const VERSION='[^']*';",f"const VERSION='zelda-maps-{sig}';",sw)
sw=re.sub(r"const FILES=\[.*?\];","const FILES="+json.dumps(files)+";",sw,flags=re.S)
sw=sw.replace("// Offline cache for Zelda Maps. Bump VERSION when files change.","// Offline cache for Zelda Maps. Bump VERSION when files change.\n// Overworld maps are cached on install; dungeon maps (maps/dg/) are cached the first time you open them.")
open(WEB+'/sw.js','w').write(sw)
print('precache',len(files),'version',sig)
