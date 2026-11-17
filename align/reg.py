import cv2,numpy as np,json,sys
M='/home/claude/site/maps/'
def load(f,N=600):
    im=cv2.imread(M+f);h,w=im.shape[:2];s=N/max(h,w);return cv2.resize(im,(round(w*s),round(h*s)),interpolation=cv2.INTER_AREA)
def water(im):
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV);b,g,r=[im[...,i].astype(int) for i in range(3)]
    m=((b>g+15)&(b>r+40)).astype(np.float32)
    return cv2.GaussianBlur(m,(0,0),3)
def ecc(src,dst,A0,mode=cv2.MOTION_AFFINE):
    W=A0.astype(np.float32)
    try:
        cc,W=cv2.findTransformECC(dst,src,W,mode,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,300,1e-6),None,5)
    except cv2.error as e: return None,str(e)
    return W,cc
