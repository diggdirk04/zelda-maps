# Cross-game overlays for ALttP / ALBW / EoW. Writes site/maps/xa_*.webp (RGBA; transparent outside the source map).
import cv2,numpy as np,os
from scipy.interpolate import RBFInterpolator
M='/home/claude/site/maps/'
rd=lambda f:cv2.imread(M+f,cv2.IMREAD_UNCHANGED)
A,AD,B,BL,E=rd('alttp_light.webp'),rd('alttp_dark.webp'),rd('albw_hyrule.webp'),rd('albw_lorule.webp'),rd('eow.webp')
# ECC result on 600px water masks: ALBW600 = W @ [ALttP600,1]
W=np.array([[9.51640904e-01,2.06529256e-03,1.37600765e+01],[1.53013458e-03,9.52065051e-01,1.44663239e+01]])
sa,sb=600/1500,600/2048
def a2b(xa,ya): # ALttP px -> ALBW px
    X=W[0,0]*xa*sa+W[0,1]*ya*sa+W[0,2];Y=W[1,0]*xa*sa+W[1,1]*ya*sa+W[1,2];return X/sb,Y/sb
def b2a(xb,yb):
    Mi=np.linalg.inv(np.vstack([W,[0,0,1]]));x,y=xb*sb,yb*sb
    return (Mi[0,0]*x+Mi[0,1]*y+Mi[0,2])/sa,(Mi[1,0]*x+Mi[1,1]*y+Mi[1,2])/sa
# ALttP% <-> EoW% landmark pairs (only true counterparts)
P=[((50,44),(47,45)),((88,50),(66,41)),((82,84),(58,72)),((46,25),(47,29.5)),((15,50),(18,40)),((14,83),(12,80)),
   ((15,15),(34,26)),((60,12),(56,10)),((93,12),(82,24)),((54,67),(44,91.6))]
pa=np.array([p[0] for p in P],float);pe=np.array([p[1] for p in P],float)
# EoW's Hyrule is a reshuffled layout, so a bending warp twists it; use a north-up scale+shift fit
# (weighted least squares on the landmarks above), with the moated castle pinned exactly.
SX,SY=0.6381,0.8067;TX,TY=47-SX*50,45-SY*44
class _L:
    def __init__(s,inv):s.inv=inv
    def __call__(s,p):
        p=np.asarray(p,float)
        return np.c_[(p[:,0]-TX)/SX,(p[:,1]-TY)/SY] if s.inv else np.c_[p[:,0]*SX+TX,p[:,1]*SY+TY]
a2e=_L(False);e2a=_L(True)
def remap(src,mx,my,out):
    s=src if src.shape[2]==4 else cv2.cvtColor(src,cv2.COLOR_BGR2BGRA)
    r=cv2.remap(s,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    from PIL import Image as _I;_I.fromarray(cv2.cvtColor(r,cv2.COLOR_BGRA2RGBA)).save(M+out,'WEBP',quality=82,method=4);print(out,r.shape,os.path.getsize(M+out)//1024,'KB')
def grid(img,cap=1500):
    h,w=img.shape[:2];s=min(1,cap/max(h,w));H,Wd=round(h*s),round(w*s)
    xs,ys=np.meshgrid((np.arange(Wd)+.5)/s,(np.arange(H)+.5)/s);return xs,ys,w,h
# onto ALttP frame
xs,ys,w,h=grid(A);bx,by=a2b(xs,ys);remap(B,bx,by,'xa_albw_on_alttp.webp');remap(BL,bx,by,'xa_lorule_on_alttp.webp')
q=e2a.__class__  # noqa
pe_=a2e(np.c_[xs.ravel()/w*100,ys.ravel()/h*100]);ex,ey=pe_[:,0].reshape(xs.shape)/100*E.shape[1],pe_[:,1].reshape(xs.shape)/100*E.shape[0]
remap(E,ex,ey,'xa_eow_on_alttp.webp')
# onto ALBW frame
xs,ys,w,h=grid(B);ax,ay=b2a(xs,ys);remap(A,ax,ay,'xa_alttp_on_albw.webp');remap(AD,ax,ay,'xa_dark_on_albw.webp')
pe_=a2e(np.c_[ax.ravel()/A.shape[1]*100,ay.ravel()/A.shape[0]*100]);ex,ey=pe_[:,0].reshape(xs.shape)/100*E.shape[1],pe_[:,1].reshape(xs.shape)/100*E.shape[0]
remap(E,ex,ey,'xa_eow_on_albw.webp')
# onto EoW frame
xs,ys,w,h=grid(E);pa_=e2a(np.c_[xs.ravel()/w*100,ys.ravel()/h*100]);ax=pa_[:,0].reshape(xs.shape)/100*A.shape[1];ay=pa_[:,1].reshape(xs.shape)/100*A.shape[0]
remap(A,ax,ay,'xa_alttp_on_eow.webp');bx,by=a2b(ax,ay);remap(B,bx,by,'xa_albw_on_eow.webp')
