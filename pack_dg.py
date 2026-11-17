# Bundle PH/ST floor maps into one file per game (artifact file-count limit).
import os,json,glob
def run(OUT='site/maps/dg'):
    idx={}
    for pre in('ph','st','albwf','loz','la','mm','alttp')+tuple(sorted({os.path.basename(f).split('_')[0] for f in glob.glob(f'{OUT}/hd*_*.webp')})):
        fs=sorted(glob.glob(f'{OUT}/{pre}_*.webp'))
        if not fs: continue
        off=0;ent={}
        with open(f'{OUT}/_{pre}pack.webp','wb') as o:
            for f in fs:
                b=open(f,'rb').read();o.write(b)
                ent['dg/'+os.path.basename(f)]=[off,len(b)];off+=len(b)
        idx[pre]=ent
    return idx
if __name__=='__main__':
    i=run();print({k:len(v) for k,v in i.items()})
