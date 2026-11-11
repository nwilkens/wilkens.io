import sys,numpy as np,pandas as pd
from scipy.spatial import cKDTree
d=sys.argv[1]
neo=pd.read_pickle(d+'/neo.pkl')
neo=neo[neo['class'].isin(['APO','AMO','ATE','IEO'])].dropna(subset=['e','q','i','om','w']).reset_index(drop=True)
neo['cc']=pd.to_numeric(neo.condition_code,errors='coerce')
r=np.radians
def feats(q,e,i,om,w):
    s=2*np.sin(r(i)/2); lp=r(om+w)
    return np.c_[q,e,s*np.cos(r(om)),s*np.sin(r(om)),e*np.cos(lp),e*np.sin(lp)]
def dsh(a,b):
    q1,e1,i1,o1,w1=a; q2,e2,i2,o2,w2=b
    i1,i2,o1,o2,w1,w2=map(r,(i1,i2,o1,o2,w1,w2))
    I2=(2*np.sin((i2-i1)/2))**2+np.sin(i1)*np.sin(i2)*(2*np.sin((o2-o1)/2))**2
    I=2*np.arcsin(np.clip(np.sqrt(I2)/2,0,1))
    x=np.cos((i2+i1)/2)*np.sin((o2-o1)/2)/np.cos(I/2)
    P=(w2-w1)+2*np.arcsin(np.clip(x,-1,1))
    P=np.where(np.abs(o2-o1)>np.pi, (w2-w1)-2*np.arcsin(np.clip(x,-1,1)), P)
    return np.sqrt((e1-e2)**2+(q1-q2)**2+I2+((e1+e2)/2*2*np.sin(P/2))**2)
def pairs(om):
    F=feats(neo.q.values,neo.e.values,neo.i.values,om,neo.w.values)
    pr=cKDTree(F).query_pairs(0.04,output_type='ndarray')
    A=[neo[k].values[pr[:,0]] for k in ['q','e','i']]+[om[pr[:,0]],neo.w.values[pr[:,0]]]
    B=[neo[k].values[pr[:,1]] for k in ['q','e','i']]+[om[pr[:,1]],neo.w.values[pr[:,1]]]
    return pr,dsh(A,B)
pr,D=pairs(neo.om.values)
rng=np.random.default_rng(1)
thr=[0.003,0.005,0.0075,0.01,0.015,0.02]
nul=[]
for k in range(20):
    # null: shift each node by a random amount, keeps q,e,i,w marginals
    _,Dn=pairs((neo.om.values+rng.uniform(0,360,len(neo)))%360)
    nul.append([(Dn<t).sum() for t in thr])
nul=np.array(nul)
print('N objects',len(neo))
print('thr   observed  null_mean  null_sd')
for j,t in enumerate(thr): print(f'{t:6.4f} {(D<t).sum():7d} {nul[:,j].mean():9.1f} {nul[:,j].std():7.1f}')
o=np.argsort(D)[:60]
out=pd.DataFrame({'D':D[o],'A':neo.pdes.values[pr[o,0]],'B':neo.pdes.values[pr[o,1]]})
for s,ix in (('A',0),('B',1)):
    for k in ['a','e','i','om','w','H','data_arc','cc']: out[k+s]=neo[k].values[pr[o,ix]]
    out['first'+s]=neo.first_obs.dt.date.values[pr[o,ix]]
pd.set_option('display.width',250)
print(out[['D','A','B','aA','aB','eA','eB','iA','iB','omA','omB','wA','wB','HA','HB','data_arcA','data_arcB','ccA','ccB','firstA','firstB']].round(4).to_string())
out.to_csv(d+'/pairs_top.csv',index=False)
