# Sharper versions of the cross-game blend overlays (xa_*.webp), sampled from the deep-zoom sources.
import cv2,numpy as np,json,os,glob,sys
from PIL import Image
sys.path.insert(0,'/home/claude')
M='/home/claude/site/maps/';OUT=M+'dg/';TS=512
HDJ=json.load(open('/home/claude/hd/hdmaps.json'))
def hd(name):  # reassemble the aligned HD image of a base map (BGRA) and its scale vs the base
    c=HDJ.get(name+'.webp')
    if not c: im=cv2.imread(M+name+'.webp',cv2.IMREAD_UNCHANGED);return cv2.cvtColor(im,cv2.COLOR_BGR2BGRA) if im.shape[2]==3 else im,1.0
    L=max(c['lv'],key=int);LW,LH,NX,NY=c['lv'][L];out=np.zeros((LH,LW,4),np.uint8)
    for ty in range(NY):
        for tx in range(NX):
            t=cv2.imread(f"{OUT}{c['pre']}{L}_{tx}_{ty}.webp",cv2.IMREAD_UNCHANGED);t=cv2.cvtColor(t,cv2.COLOR_BGR2BGRA) if t.shape[2]==3 else t
            out[ty*TS:ty*TS+t.shape[0],tx*TS:tx*TS+t.shape[1]]=t
    return out,LW/c['base']
src=open('/home/claude/build_xa.py').read()
pre=src[:src.index('def remap')]          # transforms only (a2b,b2a,a2e,e2a)
pre=pre.replace("A,AD,B,BL,E=rd('alttp_light.webp'),rd('alttp_dark.webp'),rd('albw_hyrule.webp'),rd('albw_lorule.webp'),rd('eow.webp')","")
exec(pre)
dims={n:Image.open(M+n+'.webp').size for n in ['alttp_light','alttp_dark','albw_hyrule','albw_lorule','eow']}
SRC={n:hd(n) for n in dims}
res={}
def out(name,srcname,mx,my,OW,OH):
    img,k=SRC[srcname]
    r=cv2.remap(img,(mx*k).astype(np.float32),(my*k).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    pre='hd'+name.replace('_','');[os.remove(f) for f in glob.glob(OUT+pre+'2_*')]
    nx,ny=-(-OW//TS),-(-OH//TS)
    for ty in range(ny):
        for tx in range(nx):
            t=r[ty*TS:(ty+1)*TS,tx*TS:(tx+1)*TS]
            Image.fromarray(cv2.cvtColor(t,cv2.COLOR_BGRA2RGBA)).save(f'{OUT}{pre}2_{tx}_{ty}.webp',quality=82,method=4)
    bw=Image.open(M+name+'.webp').size[0]
    res[name+'.webp']={'pre':pre,'base':bw,'lv':{'2':[OW,OH,nx,ny]}};print(name,OW,OH,nx*ny,'tiles',flush=True)
def grid(w,h,OW,OH):
    return np.meshgrid((np.arange(OW)+.5)*w/OW,(np.arange(OH)+.5)*h/OH)
# onto ALttP frame
w,h=dims['alttp_light'];OW=OH=3536;xs,ys=grid(w,h,OW,OH)
bx,by=a2b(xs,ys);out('xa_albw_on_alttp','albw_hyrule',bx,by,OW,OH);out('xa_lorule_on_alttp','albw_lorule',bx,by,OW,OH)
pe_=a2e(np.c_[xs.ravel()/w*100,ys.ravel()/h*100]);E=dims['eow']
out('xa_eow_on_alttp','eow',pe_[:,0].reshape(xs.shape)/100*E[0],pe_[:,1].reshape(xs.shape)/100*E[1],OW,OH)
# onto ALBW frame
w,h=dims['albw_hyrule'];OW=OH=3072;xs,ys=grid(w,h,OW,OH);A=dims['alttp_light']
ax,ay=b2a(xs,ys);out('xa_alttp_on_albw','alttp_light',ax,ay,OW,OH);out('xa_dark_on_albw','alttp_dark',ax,ay,OW,OH)
pe_=a2e(np.c_[ax.ravel()/A[0]*100,ay.ravel()/A[1]*100])
out('xa_eow_on_albw','eow',pe_[:,0].reshape(xs.shape)/100*E[0],pe_[:,1].reshape(xs.shape)/100*E[1],OW,OH)
# onto EoW frame
w,h=dims['eow'];OW,OH=3600,round(3600*h/w);xs,ys=grid(w,h,OW,OH)
pa_=e2a(np.c_[xs.ravel()/w*100,ys.ravel()/h*100]);ax=pa_[:,0].reshape(xs.shape)/100*A[0];ay=pa_[:,1].reshape(xs.shape)/100*A[1]
out('xa_alttp_on_eow','alttp_light',ax,ay,OW,OH);bx,by=a2b(ax,ay);out('xa_albw_on_eow','albw_hyrule',bx,by,OW,OH)
json.dump(res,open('/home/claude/hd/xa_hd.json','w'),indent=0)
