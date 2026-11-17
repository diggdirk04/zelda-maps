# Deep-zoom tiles for every overworld map that has a sharper source than the shipped base image.
# Each source is registered onto the base by ECC (affine), so tiles line up exactly with markers.
import cv2,numpy as np,os,json,sys,glob
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
U='/mnt/user-data/uploads/';X='/home/claude/ext/';M='/home/claude/site/maps/';OUT=M+'dg/';TS=512
PIX={'alttp_dark','alttp_light','loz','ooa_past','ooa_present','oos_spring','oos_summer','oos_autumn','oos_winter','mc','mc_full','ph','st','aol_full','la'}
JOBS=[('alttp_dark',U+'6afec92e-image.png'),('alttp_light',U+'c3b86ec2-image.png'),('aol_full',U+'6478b0fa-image.png'),
 ('eow',U+'7f18d109-image.png'),('la',U+'34082100-image.png'),('loz',U+'b0abbb5e-image.png'),
 ('mc',X+'CandyCrystal_CandyCrystal_TMCR_Map_Tracker/images/maps/overworld.png'),('mc_full',U+'9f658092-image.webp'),
 ('ooa_past',U+'7e966a8e-image.png'),('ooa_present',U+'001b5a97-image.png'),
 ('oos_spring',U+'29bd07a1-image.png'),('oos_summer',U+'4a5d558e-image.png'),('oos_autumn',U+'c1b7524a-image.png'),('oos_winter',U+'a3954136-image.png'),
 ('oot',U+'27deb59d-image.png'),('oot_original',U+'43077d3a-image.jpg'),
 ('ph','/home/claude/ext2/ph_ap/worlds/tloz_ph/tracker/images/seamap.png'),('ph_full',U+'f16837b0-image.jpg'),
 ('ss_hd',X+'sshdr/tracker/assets/images/ss-map.png'),('ss_surface',U+'908f001b-image.png'),
 ('st','/home/claude/ext2/st_ap/worlds/tloz_st/tracker/images/train/all.png'),('totk_depths',U+'7ff2ec70-image.png'),
 ('tp','/home/claude/ext3/tprando_jim/images/overworld.png'),('tp_hd',X+'DarkZant_tp-map/Submaps/GameMap.png'),
 ('tp_labeled',U+'dc9d2d38-image.jpg'),('totk_surface',U+'base_map.png','sift'),('ww',U+'ce8bc10b-image.webp'),('ww_sea',U+'1a134ce4-image.png')]
def rgb(p):
    im=Image.open(p)
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA');bg=Image.new('RGB',im.size,(20,20,24));bg.paste(im,mask=im.split()[3]);return np.array(bg)
    return np.array(im.convert('RGB'))
def sift_init(base,src):
    # rough base->src affine from features, for sources framed differently from the base
    bh,bw=base.shape[:2];sh,sw=src.shape[:2];kb=1200/bw;ks=1200/sw
    a=cv2.cvtColor(cv2.resize(base,(1200,round(bh*kb))),cv2.COLOR_RGB2GRAY);b=cv2.cvtColor(cv2.resize(src,(1200,round(sh*ks))),cv2.COLOR_RGB2GRAY)
    f=cv2.SIFT_create(4000);ka,da=f.detectAndCompute(a,None);kc,dc=f.detectAndCompute(b,None)
    m=[x for x,y in cv2.BFMatcher().knnMatch(da,dc,k=2) if x.distance<.7*y.distance]
    H,_=cv2.estimateAffine2D(np.float32([ka[x.queryIdx].pt for x in m]),np.float32([kc[x.trainIdx].pt for x in m]),ransacReprojThreshold=3)
    return np.diag([1/ks,1/ks,1])@np.vstack([H,[0,0,1]])@np.diag([kb,kb,1])
def register(base,src,init=None):
    if init is not None:   # crop the source to the base frame first, then refine by ECC
        A0=init(base,src);bh,bw=base.shape[:2]
        crop=cv2.warpAffine(src,A0[:2],(bw*2,bh*2),flags=cv2.INTER_AREA|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE) if False else None
        cc,A1=register(base,cv2.warpAffine(src,(A0@np.diag([.5,.5,1]))[:2],(bw*2,bh*2),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE))
        return cc,A0@np.diag([.5,.5,1])@A1
    bh,bw=base.shape[:2];sh,sw=src.shape[:2]
    k=min(1,1000/bw);w,h=round(bw*k),round(bh*k)
    a=cv2.cvtColor(cv2.resize(base,(w,h),interpolation=cv2.INTER_AREA),cv2.COLOR_RGB2GRAY).astype(np.float32)
    b=cv2.cvtColor(cv2.resize(src,(w,h),interpolation=cv2.INTER_AREA),cv2.COLOR_RGB2GRAY).astype(np.float32)
    a=cv2.GaussianBlur(a,(0,0),1);b=cv2.GaussianBlur(b,(0,0),1)
    W=np.eye(2,3,dtype=np.float32)
    cc,W=cv2.findTransformECC(a,b,W,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,300,1e-6),None,5)
    # W: small-base px -> small-src px.  Full: src = D_s * W * D_b^-1 * base
    Ds=np.diag([sw/w,sh/h,1]);Db=np.diag([w/bw,h/bh,1]);A=Ds@np.vstack([W,[0,0,1]])@Db
    return cc,A
res={}
only=sys.argv[1:]
for J in JOBS:
    name,sp=J[:2]
    if only and name not in only: continue
    base=rgb(M+name+'.webp');src=rgb(sp);bh,bw=base.shape[:2]
    cc,A=register(base,src,sift_init if len(J)>2 else None)
    s=float(np.sqrt(abs(np.linalg.det(A[:2,:2]))))
    if cc<0.9 or s<1.3: print(name,'skip cc=%.3f s=%.2f'%(cc,s));continue
    fs=[round(s,3)] if s<=2.6 else [2,round(min(s,4),3)]
    for f in glob.glob(OUT+'hd'+name.replace('_','')+'*'): os.remove(f)
    lv={};pre='hd'+name.replace('_','')
    for i,f in enumerate(fs,2):
        LW,LH=round(bw*f),round(bh*f)
        T=A@np.diag([bw/LW,bh/LH,1])   # out px -> base px -> src px
        interp=cv2.INTER_NEAREST if (name in PIX and abs(f-s)<.05) else cv2.INTER_CUBIC if f>=s*0.98 else cv2.INTER_AREA
        if interp==cv2.INTER_AREA:   # downsample: warp at native then shrink
            NW,NH=round(bw*s),round(bh*s);T2=A@np.diag([bw/NW,bh/NH,1])
            big=cv2.warpAffine(src,T2[:2],(NW,NH),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
            img=cv2.resize(big,(LW,LH),interpolation=cv2.INTER_AREA)
        else:
            img=cv2.warpAffine(src,T[:2],(LW,LH),flags=interp|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
        nx,ny=-(-LW//TS),-(-LH//TS);lv[i]=[LW,LH,nx,ny]
        q=88 if name in PIX else 80
        for ty in range(ny):
            for tx in range(nx):
                Image.fromarray(img[ty*TS:(ty+1)*TS,tx*TS:(tx+1)*TS]).save(f'{OUT}{pre}{i}_{tx}_{ty}.webp',quality=q,method=4)
    res[name+'.webp']={'pre':pre,'base':bw,'lv':lv}
    print(name,'cc=%.4f s=%.2f'%(cc,s),lv,flush=True)
old=json.load(open('/home/claude/hd/hdmaps.json')) if os.path.exists('/home/claude/hd/hdmaps.json') else {}
old.update(res);json.dump(old,open('/home/claude/hd/hdmaps.json','w'),indent=0)
