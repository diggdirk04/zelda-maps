import json,re
H=json.load(open('/home/claude/hd/hdmaps.json'));H.update(json.load(open('/home/claude/hd/xa_hd.json')))
H['botw.webp']={'pre':'hdbotw','base':1500,'lv':{'2':[3000,2400,6,5],'3':[5000,4000,10,8]}}
PIX={'alttp_dark','alttp_light','loz','ooa_past','ooa_present','oos_spring','oos_summer','oos_autumn','oos_winter','mc','mc_full','ph','st','aol_full','la'}
for k,v in H.items():
    if k[:-5] in PIX: v['px']=1
s=open('/home/claude/gamepage.js').read()
s=re.sub(r"const HDMAPS=\{.*?\};\n","const HDMAPS="+json.dumps(H,separators=(',',':'))+";\n",s,count=1,flags=re.S)
open('/home/claude/gamepage.js','w').write(s);print(len(H),'maps with deep zoom')
