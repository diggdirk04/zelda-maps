# Deep-zoom tiles for the BotW map, aligned to site/maps/botw.webp (1500x1200).
# Source: BotW-Map.png (6000x5000) from MrCheeze/botw-object-map; aligned by ECC (corr 0.9993).
import cv2,numpy as np,os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
OUT='/home/claude/site/maps/dg';TS=512
W=np.load('/home/claude/hd/W_lo2hs.npy').astype(np.float64)   # lo px -> hs px (hs = hi * 0.25)
hi=np.array(Image.open('/home/claude/ext3/botw-object-map/BotW-Map.png').convert('RGB'))
K=10/3;OW,OH=5000,4000                                           # level-3 frame = lo * 10/3
# out u,v -> lo = u/K -> hs = W.lo -> hi = 4*hs
M=4*np.array([[W[0,0]/K,W[0,1]/K,W[0,2]],[W[1,0]/K,W[1,1]/K,W[1,2]]])
L3=cv2.warpAffine(hi,M,(OW,OH),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
L2=cv2.resize(L3,(3000,2400),interpolation=cv2.INTER_AREA)
meta={}
for lv,img in ((2,L2),(3,L3)):
    h,w=img.shape[:2];nx,ny=-(-w//TS),-(-h//TS);meta[lv]=[w,h,nx,ny]
    for ty in range(ny):
        for tx in range(nx):
            t=img[ty*TS:(ty+1)*TS,tx*TS:(tx+1)*TS]
            Image.fromarray(t).save(f'{OUT}/hdbotw{lv}_{tx}_{ty}.webp',quality=80,method=4)
print(meta)
