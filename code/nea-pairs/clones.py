"""Backward integration of orbit clones of a pair's secondary against its primary.
usage: clones.py PAIRDIR NCLONES YEARS   (PAIRDIR prepared by prep_pair.sh)"""
import sys,json,time,numpy as np,rebound
from scipy import stats
d=sys.argv[1]; NCL=int(sys.argv[2]); YEARS=float(sys.argv[3])
def row(f):
    on=False
    for l in open(f'{d}/{f}.txt'):
        if l.startswith('$$SOE'): on=True; continue
        if on: return [float(x) for x in l.split(',')[2:] if x.strip()]
def el(f): r=row(f); return np.array([r[0],r[1],r[5],r[3],r[4],r[2]])   # e,q,tp,node,peri,i
A,B=el('el_A'),el('el_B')
cov=np.array(json.load(open(f'{d}/sbdb_B.json'))['orbit']['covariance']['data'],float)
dx=A-B; sig=np.sqrt(np.diag(cov)); ix=[0,1,3,4,5]
m5=dx[ix]@np.linalg.solve(cov[np.ix_(ix,ix)],dx[ix])
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from clones_common import build
AU=1.495978707e8
sim,n0,cl,_=build(d,NCL)
N=sim.N
xyz=np.zeros((N,3)); vxyz=np.zeros((N,3))
ts=-np.arange(0.5,YEARS*365.25,0.5); W=1461
env=np.full((len(ts)//W+1,NCL),np.inf); envt=np.zeros_like(env); envv=np.zeros_like(env)
T0=time.time()
for j,t in enumerate(ts):
    sim.integrate(t); sim.serialize_particle_data(xyz=xyz,vxvyvz=vxyz)
    dd=np.linalg.norm(xyz[n0+1:]-xyz[n0],axis=1)*AU
    w=j//W; mm=dd<env[w]; env[w][mm]=dd[mm]; envt[w][mm]=t; envv[w][mm]=np.linalg.norm(vxyz[n0+1:][mm]-vxyz[n0],axis=1)*AU/86400*1000
np.savez(f'{d}/clones.npz',env=env,envt=envt,envv=envv,cl=cl)
env=env[:-1]; envt=envt[:-1]; envv=envv[:-1]; Wn=env.shape[0]
kk=env.argmin(axis=0); dm=env[kk,np.arange(NCL)]; age=-envt[kk,np.arange(NCL)]/365.25; vv=envv[kk,np.arange(NCL)]
inner=(kk>0)&(kk<Wn-1)
res=dict(pair=d.split('/')[-1],clones=NCL,years=YEARS,runtime_s=round(time.time()-T0),
 elem_diff_sigma=[round(float(x),2) for x in dx/sig],chi2_shape=round(float(m5),1),p_shape=float(stats.chi2.sf(m5,5)),
 sep_now_km=[float(x) for x in np.percentile(env[0],[5,50,95])],
 frac_closest_now=float((kk==0).mean()),frac_still_converging_at_edge=float((kk==Wn-1).mean()),frac_past_minimum=float(inner.mean()))
for thr in (1e5,1e4,3e3,1e3):
    s=inner&(dm<thr)
    res[f'lt_{int(thr)}']=dict(n=int(s.sum()),ages=[int(x) for x in np.sort(age[s])[:15]],v_ms=[round(float(x),2) for x in np.sort(vv[s])[:8]],slow=int((s&(vv<1.0)).sum()))
res['nominal']=dict(min_km=float(dm[0]),age=float(age[0]),v_ms=float(vv[0]))
json.dump(res,open(f'{d}/result.json','w'),indent=1); print(json.dumps(res))
