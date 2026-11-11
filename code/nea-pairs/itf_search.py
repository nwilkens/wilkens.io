"""Search the MPC isolated tracklet file for unlinked detections of an object,
using clones of its orbit. Also self-tests the topocentric prediction on the
object's own published observations.
usage: itf_search.py PAIRDIR ITF.gz ObsCodes.html MPC_OBS.json START END NCLONES"""
import sys,gzip,json,re,collections,numpy as np
d,itf,obscodes,own,START,END,NCL=sys.argv[1:8]; NCL=int(NCL)
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from clones_common import build
AU=1.495978707e8; RE=6378.137/AU; C=173.1446327   # au/day
def jd_of(y,m,dd):
    a=(14-m)//12; yy=y+4800-a; mm=m+12*a-3
    return int(dd)+(153*mm+2)//5+365*yy+yy//4-yy//100+yy//400-32045-0.5+(dd-int(dd))
def parse(l):
    y,m,dd=int(l[15:19]),int(l[20:22]),float(l[23:32])
    ra=(int(l[32:34])+int(l[35:37])/60+float(l[38:44])/3600)*15
    dec=(-1 if l[44]=='-' else 1)*(int(l[45:47])+int(l[48:50])/60+float(l[51:56])/3600)
    mag=float(l[65:70]) if l[65:70].strip() else np.nan
    return jd_of(y,m,dd),ra,dec,mag,l[70],l[77:80]
sites={}
for l in open(obscodes,errors='replace'):
    if len(l)>30 and re.match(r'^[A-Z0-9]{3} [ 0-9]',l):
        try: sites[l[:3]]=(float(l[4:13]),float(l[13:21]),float(l[21:30]))
        except ValueError: pass
def site_vec(code,jd):
    lon,rc,rs=sites[code]; th=np.radians((280.46061837+360.98564736629*(jd-2451545.0)+lon)%360)
    return np.array([rc*np.cos(th),rc*np.sin(th),rs])*RE
eps=np.radians(23.4392911)
def predict(sim,n0,jd,code,xyz,vxyz):
    """Topocentric astrometric RA/Dec (deg) of every small body in sim at UTC JD."""
    sim.integrate(jd+69.184/86400-t0); sim.serialize_particle_data(xyz=xyz,vxvyvz=vxyz)
    r=xyz[n0:]-xyz[3]; v=vxyz[n0:]
    r=r-v*(np.linalg.norm(r,axis=1)/C)[:,None]
    q=np.c_[r[:,0],r[:,1]*np.cos(eps)-r[:,2]*np.sin(eps),r[:,1]*np.sin(eps)+r[:,2]*np.cos(eps)]-site_vec(code,jd)
    rr=np.linalg.norm(q,axis=1)
    return np.degrees(np.arctan2(q[:,1],q[:,0]))%360,np.degrees(np.arcsin(q[:,2]/rr))
def resid(ra,dec,cra,cdec):
    return (ra-cra+180)%360-180,dec-cdec
# ---- self-test on the object's own observations
ownobs=[parse(l) for l in json.load(open(own))[0]['OBS80'].split('\n') if len(l)>=80 and l[14] not in 'sSRrVvXx' and l[77:80] in sites]
sim,n0,cl,t0=build(d,2,with_primary=False); N=sim.N; xyz=np.zeros((N,3)); vxyz=np.zeros((N,3))
rs=[]
for jd,ra,dec,mag,band,code in sorted(ownobs,reverse=True):
    cra,cdec=predict(sim,n0,jd,code,xyz,vxyz); a,b=resid(ra,dec,cra[0],cdec[0]); rs.append(np.hypot(a*np.cos(np.radians(dec)),b)*3600)
print(f'self-test on {len(rs)} own observations: median residual {np.median(rs):.2f}", 90th pct {np.percentile(rs,90):.2f}", max {max(rs):.2f}"')
# ---- ITF
j0,j1=[jd_of(*map(float,s.split('-'))) if False else jd_of(int(s[:4]),int(s[5:7]),float(s[8:10])) for s in (START,END)]
ys={START[:4],END[:4]}; rows=[]
with gzip.open(itf,'rt',errors='replace') as f:
    for l in f:
        if len(l)<80 or l[15:19] not in ys or l[14] in 'sSRrVvXx': continue
        try: jd,ra,dec,mag,band,code=parse(l)
        except ValueError: continue
        if j0<=jd<=j1 and code in sites: rows.append((l[:12].strip(),jd,ra,dec,mag,band,code))
print('ITF observations in window:',len(rows),'tracklets:',len({r[0] for r in rows}))
sim,n0,cl,t0=build(d,NCL,with_primary=False); N=sim.N; xyz=np.zeros((N,3)); vxyz=np.zeros((N,3))
rows.sort(key=lambda r:-r[1])
# coarse filter per day using the clone cloud's sky extent
keep=[]; cache={}
for r in rows:
    day=round(r[1])
    if day not in cache:
        cra,cdec=predict(sim,n0,float(day),'500' if '500' in sites else r[6],xyz,vxyz)
        u=np.c_[np.cos(np.radians(cdec))*np.cos(np.radians(cra)),np.cos(np.radians(cdec))*np.sin(np.radians(cra)),np.sin(np.radians(cdec))]
        c=u.mean(axis=0); c/=np.linalg.norm(c); cache[day]=(c,np.degrees(np.arccos(np.clip(u@c,-1,1))).max())
    c,rad=cache[day]; o=np.array([np.cos(np.radians(r[3]))*np.cos(np.radians(r[2])),np.cos(np.radians(r[3]))*np.sin(np.radians(r[2])),np.sin(np.radians(r[3]))])
    if np.degrees(np.arccos(np.clip(o@c,-1,1)))<rad+1.0: keep.append(r)
print('after coarse sky filter:',len(keep),'observations in',len({r[0] for r in keep}),'tracklets; cloud radius range deg',round(min(v[1] for v in cache.values()),1),round(max(v[1] for v in cache.values()),1))
sim,n0,cl,t0=build(d,NCL,with_primary=False)
per=collections.defaultdict(list)
for trk,jd,ra,dec,mag,band,code in keep:
    cra,cdec=predict(sim,n0,jd,code,xyz,vxyz); a,b=resid(ra,dec,cra,cdec)
    per[trk].append((jd,a*np.cos(np.radians(dec))*3600,b*3600,mag,band,code,ra,dec))
out=[]
for trk,obs in per.items():
    if len(obs)<2: continue
    A=np.array([o[1] for o in obs]); B=np.array([o[2] for o in obs])       # (nobs, NCL) arcsec
    dist=np.hypot(A,B); worst=dist.max(axis=0); k=worst.argmin()
    # rate consistency: the residual vector should be the same on every observation
    spread=np.hypot(A[:,k]-A[:,k].mean(),B[:,k]-B[:,k].mean()).max()
    out.append((worst[k],spread,trk,len(obs),int(k),obs))
out.sort(key=lambda x:x[0])
import collections as _c; print('kept by station:',dict(_c.Counter(o[5] for v in per.values() for o in v).most_common(8))); print('kept nights:',sorted(_c.Counter(int(o[0]+0.5) for v in per.values() for o in v).items())[:60])
print('\nbest tracklet matches (worst-observation offset from one clone, residual spread within tracklet):')
for w,s,trk,n,k,obs in out[:15]:
    mags=[o[3] for o in obs if not np.isnan(o[3])]
    print(f'  {trk:10s} n={n} {obs[0][5]} JD {min(o[0] for o in obs):.4f}  offset {w:8.1f}"  spread {s:6.1f}"  mag {np.median(mags) if mags else float("nan"):.1f}{obs[0][4]}  clone {k}')
json.dump([dict(trk=t,offset=float(w),spread=float(s),n=n,clone=k,obs=[[float(o[0]),float(o[1][k]),float(o[2][k]),float(o[3]),o[4],o[5],float(o[6]),float(o[7])] for o in obs]) for w,s,t,n,k,obs in out[:200]],open(f'{d}/itf_matches.json','w'))
