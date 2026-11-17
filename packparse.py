import json,re,glob,os,sys
def loadj(f):
    s=open(f,encoding='utf-8-sig').read()
    s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
    s=re.sub(r'^\s*//.*$','',s,flags=re.M)
    s=re.sub(r':\s*,',': null,',s)
    s=re.sub(r',(\s*[\]}])',r'\1',s)
    return json.loads(s)
def walk(node,path,out):
    if isinstance(node,list):
        for n in node: walk(n,path,out)
        return
    if not isinstance(node,dict): return
    nm=node.get('name','')
    p=path+[nm] if nm else path
    for ml in node.get('map_locations',[]) or []:
        secs=[s.get('name','') for s in node.get('sections',[]) or []]
        out.append({'map':ml.get('map'),'x':ml.get('x'),'y':ml.get('y'),'name':nm,'path':p,'n':len(secs),'secs':secs})
    for k in ('children',):
        if k in node: walk(node[k],p,out)
def parse(pack):
    out=[]
    for f in glob.glob(pack+'/**/*.json',recursive=True)+glob.glob(pack+'/**/*.jsonc',recursive=True):
        if '/.git/' in f: continue
        try: d=loadj(f)
        except Exception: continue
        b=len(out); walk(d,[],out)
        for o in out[b:]: o['file']=os.path.relpath(f,pack)
    return out
if __name__=='__main__':
    out=parse(sys.argv[1]); from collections import Counter
    print(len(out),Counter(o['map'] for o in out)); 
    for o in out[:5]: print(o)
