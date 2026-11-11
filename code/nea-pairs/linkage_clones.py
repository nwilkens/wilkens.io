"""Linkage test across a long gap: propagate clones of the recent object back to the
dates the older object was observed and look for one clone that matches on every night.
usage: linkage_clones.py PAIRDIR MPCDIR "older designation" NCLONES"""
import sys,json,numpy as np,rebound
d,mpc,old,NCL=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from clones_common import build
obs=[]
for l in json.load(open(f"{mpc}/{old.replace(' ','_')}.json"))[0]['OBS80'].split('\n'):
    if len(l)<80 or l[14] in 'sSRrVvXx': continue
    y,m,dd=int(l[15:19]),int(l[20:22]),float(l[23:32])
    a=(14-m)//12; yy=y+4800-a; mm=m+12*a-3
    jd=int(dd)+(153*mm+2)//5+365*yy+yy//4-yy//100+yy//400-32045-0.5+(dd-int(dd))
    ra=(int(l[32:34])+int(l[35:37])/60+float(l[38:44])/3600)*15
    dec=(-1 if l[44]=='-' else 1)*(int(l[45:47])+int(l[48:50])/60+float(l[51:56])/3600)
    obs.append((jd,ra,dec))
obs.sort(reverse=True)
# one observation per night is enough
nights={}
for o in obs: nights.setdefault(int(o[0]+0.5),o)
obs=sorted(nights.values(),reverse=True)
sim,n0,cl,t0=build(d,NCL,with_primary=False)
N=sim.N; xyz=np.zeros((N,3)); eps=np.radians(23.4392911)
res=np.zeros((len(obs),NCL)); dist=np.zeros((len(obs),NCL))
for k,(jd,ra,dec) in enumerate(obs):
    sim.integrate(jd+69.184/86400-t0); sim.serialize_particle_data(xyz=xyz)
    r=xyz[n0:]-xyz[3]                      # geocentric, ecliptic J2000 (index 3 is Earth)
    x,y,z=r[:,0],r[:,1]*np.cos(eps)-r[:,2]*np.sin(eps),r[:,1]*np.sin(eps)+r[:,2]*np.cos(eps)
    rr=np.linalg.norm(r,axis=1); cra=np.degrees(np.arctan2(y,x))%360; cdec=np.degrees(np.arcsin(z/rr))
    c=np.sin(np.radians(dec))*np.sin(np.radians(cdec))+np.cos(np.radians(dec))*np.cos(np.radians(cdec))*np.cos(np.radians(ra-cra))
    res[k]=np.degrees(np.arccos(np.clip(c,-1,1))); dist[k]=rr
worst=res.max(axis=0); b=worst.argmin()
print(f"{d.split('/')[-1]}: {NCL} clones, {len(obs)} nights of {old} from JD {obs[-1][0]:.1f} to {obs[0][0]:.1f}")
print(f"  best clone: worst-night residual {worst[b]:.3f} deg; per-night {np.round(res[:,b],3).tolist()}; geocentric distance {dist[:,b].min():.4f}-{dist[:,b].max():.4f} au (parallax allowance {np.degrees(4.26e-5/dist[:,b].min()):.3f} deg)")
print(f"  clones within 0.5 deg on every night: {(worst<0.5).sum()}; within 2 deg: {(worst<2).sum()}; nominal clone worst residual {worst[0]:.1f} deg")
print(f"  per-night closest clone (any): {np.round(res.min(axis=1),3).tolist()}")
