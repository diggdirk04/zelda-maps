import cv2,numpy as np,sys
def feat(path,maxd=1600):
    a=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    if a is None:
        from PIL import Image; a=np.array(Image.open(path).convert('L'))
    s=min(1,maxd/max(a.shape)); a2=cv2.resize(a,None,fx=s,fy=s,interpolation=cv2.INTER_AREA) if s<1 else a
    k,d=cv2.SIFT_create(10000).detectAndCompute(a2,None); return k,d,s,a.shape
def align(src,dst):
    ka,da,sa,_=feat(src); kb,db,sb,shb=feat(dst)
    if da is None or db is None: return None
    m=cv2.BFMatcher().knnMatch(da,db,k=2); g=[x[0] for x in m if len(x)==2 and x[0].distance<0.75*x[1].distance]
    if len(g)<6: return (0,len(g),None)
    pa=np.float32([ka[x.queryIdx].pt for x in g])/sa; pb=np.float32([kb[x.trainIdx].pt for x in g])/sb
    M,inl=cv2.estimateAffinePartial2D(pa,pb,ransacReprojThreshold=6,maxIters=20000)
    return (int(inl.sum()) if inl is not None else 0,len(g),M)
if __name__=='__main__':
    src=sys.argv[1]
    for dst in sys.argv[2:]:
        r=align(src,dst); print(dst, r[0],r[1], None if r[2] is None else np.round(r[2],3).tolist())
