import sys,json,numpy as np,rebound
from scipy import stats
hz,sb,out=sys.argv[1],sys.argv[2],sys.argv[3]
NCL=int(sys.argv[4]); YEARS=float(sys.argv[5])
def row(f):
    on=False
    for l in open(f'{hz}/{f}.txt'):
        if l.startswith('$$SOE'): on=True; continue
        if on: return [float(x) for x in l.split(',')[2:] if x.strip()]
# covariance order: e,q,tp,node,peri,i ; Horizons order: EC,QR,IN,OM,W,Tp
def el(f): r=row(f); return np.array([r[0],r[1],r[5],r[3],r[4],r[2]])
A,B=el('el_NC15'),el('el_LD1')
cov=np.array(json.load(open(f'{sb}/2026_LD1.json'))['orbit']['covariance']['data'],float)
covA=np.array(json.load(open(f'{sb}/2018_NC15.json'))['orbit']['covariance']['data'],float)
dx=A-B; sig=np.sqrt(np.diag(cov))
print('labels      e, q, tp, node, peri, i'); print('NC15-LD1  ',dx); print('in sigma  ',(dx/sig).round(2))
ix=[0,1,3,4,5]
m5=dx[ix]@np.linalg.solve(cov[np.ix_(ix,ix)]+covA[np.ix_(ix,ix)],dx[ix]); m6=dx@np.linalg.solve(cov+covA,dx)
print('orbit shape/orientation (5 el, no timing): chi2=%.2f p=%.3f'%(m5,stats.chi2.sf(m5,5)))
print('all 6 incl. perihelion time: chi2=%.1f p=%.2e'%(m6,stats.chi2.sf(m6,6)))

k=0.01720209895; mu=k*k
masses={'10':1.0,'199':1/6023600.0,'299':1/408523.71,'399':1/332946.0487,'301':1/27068703.2,'4':1/3098703.59,'5':1/1047.348644,'6':1/3497.9018,'7':1/22902.98,'8':1/19412.26}
def el2state(e,q,tp,om,w,inc,t):
    a=q/(1-e); n=np.sqrt(mu/a**3); M=n*(t-tp); E=M.copy() if hasattr(M,'copy') else M
    for _ in range(50): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    xp=a*(np.cos(E)-e); yp=a*np.sqrt(1-e*e)*np.sin(E); r=a*(1-e*np.cos(E))
    vxp=-a*n*np.sin(E)*a/r; vyp=a*n*np.sqrt(1-e*e)*np.cos(E)*a/r
    om,w,inc=np.radians(om),np.radians(w),np.radians(inc)
    cO,sO,cw,sw,ci,si=np.cos(om),np.sin(om),np.cos(w),np.sin(w),np.cos(inc),np.sin(inc)
    P=np.array([cO*cw-sO*sw*ci,sO*cw+cO*sw*ci,sw*si]); Q=np.array([-cO*sw-sO*cw*ci,-sO*sw+cO*cw*ci,cw*si])
    return (P*xp+Q*yp).T,(P*vxp+Q*vyp).T
t0=2461203.5
rng=np.random.default_rng(7)
cl=rng.multivariate_normal(B,cov,NCL); cl[0]=B
sun=np.array(row('v_10'))
sim=rebound.Simulation(); sim.G=mu
for b,m in masses.items():
    r=row('v_'+b); sim.add(m=m,x=r[0],y=r[1],z=r[2],vx=r[3],vy=r[4],vz=r[5])
sim.N_active=sim.N
r=row('v_NC15'); sim.add(m=0,x=r[0],y=r[1],z=r[2],vx=r[3],vy=r[4],vz=r[5])
# check element->state conversion against Horizons state of nominal LD1
p,v=el2state(*[np.array([x]) for x in B],0.0+0*t0) if False else el2state(B[0],B[1],B[2],B[3],B[4],B[5],t0)
hl=np.array(row('v_LD1')); print('conversion check, LD1 nominal vs Horizons (km):',np.linalg.norm(p+sun[:3]-hl[:3])*1.496e8)
P,V=el2state(cl[:,0],cl[:,1],cl[:,2],cl[:,3],cl[:,4],cl[:,5],t0)
for i in range(NCL): sim.add(m=0,x=P[i,0]+sun[0],y=P[i,1]+sun[1],z=P[i,2]+sun[2],vx=V[i,0]+sun[3],vy=V[i,1]+sun[4],vz=V[i,2]+sun[5])
sim.integrator='ias15'; sim.t=0
n0=sim.N_active; N=sim.N
xyz=np.zeros((N,3)); vxyz=np.zeros((N,3))
dmin=np.full(NCL,np.inf); tmin=np.zeros(NCL); vmin=np.zeros(NCL)
AU=1.495978707e8
ts=-np.arange(0.5,YEARS*365.25,0.5); track=[]
W=1461; env=np.full((int(len(ts)/W)+1,NCL),np.inf); envt=np.zeros_like(env); envv=np.zeros_like(env)
for j,t in enumerate(ts):
    sim.integrate(t); sim.serialize_particle_data(xyz=xyz,vxvyvz=vxyz)
    d=np.linalg.norm(xyz[n0+1:]-xyz[n0],axis=1)*AU
    m=d<dmin
    if m.any():
        dmin[m]=d[m]; tmin[m]=t; vmin[m]=np.linalg.norm(vxyz[n0+1:][m]-vxyz[n0],axis=1)*AU/86400*1000
    w=j//W; mm=d<env[w]; env[w][mm]=d[mm]; envt[w][mm]=t; envv[w][mm]=np.linalg.norm(vxyz[n0+1:][mm]-vxyz[n0],axis=1)*AU/86400*1000
    if j%730==0: track.append((t/365.25,d[0],np.median(d)))
np.savez(out,env=env,envt=envt,envv=envv,dmin=dmin,tmin=tmin,vmin=vmin,cl=cl,track=np.array(track))
print('nominal clone separation history (yr, km):',[(round(a),f'{b:.2e}') for a,b,_ in track[::max(1,len(track)//8)]])
age=-tmin/365.25
past=(age>0.01)&(age<YEARS-0.01)
print(f'clones {NCL}; with a separation minimum inside the last {YEARS:.0f} yr: {past.mean():.2f}')
for thr in (1e5,3e4,1e4,3e3,1e3):
    s=past&(dmin<thr)
    print(f' min dist <{thr:8.0f} km: {s.sum():4d} clones; age median {np.median(age[s]) if s.any() else np.nan:7.1f} yr, 5-95% [{np.percentile(age[s],5) if s.any() else np.nan:.1f}, {np.percentile(age[s],95) if s.any() else np.nan:.1f}]; rel speed median {np.median(vmin[s]) if s.any() else np.nan:.2f} m/s')
print('age quantiles of all past-converging clones (yr):',np.percentile(age[past],[5,25,50,75,95]).round(1))
print('min-distance quantiles (km):',np.percentile(dmin[past],[5,25,50,75,95]).round(0))
