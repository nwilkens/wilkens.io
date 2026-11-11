import json,numpy as np,rebound
def build(d,NCL,with_primary=True,seed=7):
    """Simulation with Sun, planets, Moon, optional primary, and NCL clones of the secondary. Returns (sim, index of first small body, clone elements, epoch JD)."""
    def row(f):
        on=False
        for l in open(f'{d}/{f}.txt'):
            if l.startswith('$$SOE'): on=True; continue
            if on: return [float(x) for x in l.split(',')[2:] if x.strip()]
    def el(f): r=row(f); return np.array([r[0],r[1],r[5],r[3],r[4],r[2]])   # e,q,tp,node,peri,i
    A,B=el('el_A'),el('el_B'); t0=float(open(f'{d}/epoch.txt').read())
    cov=np.array(json.load(open(f'{d}/sbdb_B.json'))['orbit']['covariance']['data'],float)
    
    k=0.01720209895; mu=k*k; AU=1.495978707e8
    masses={'10':1.0,'199':1/6023600.0,'299':1/408523.71,'399':1/332946.0487,'301':1/27068703.2,'4':1/3098703.59,'5':1/1047.348644,'6':1/3497.9018,'7':1/22902.98,'8':1/19412.26}
    def el2state(e,q,tp,om,w,inc,t):
        a=q/(1-e); n=np.sqrt(mu/a**3); M=n*(t-tp); E=np.array(M,float)
        for _ in range(60): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
        xp=a*(np.cos(E)-e); yp=a*np.sqrt(1-e*e)*np.sin(E); r=a*(1-e*np.cos(E))
        vxp=-a*n*np.sin(E)*a/r; vyp=a*n*np.sqrt(1-e*e)*np.cos(E)*a/r
        om,w,inc=np.radians(om),np.radians(w),np.radians(inc)
        cO,sO,cw,sw,ci,si=np.cos(om),np.sin(om),np.cos(w),np.sin(w),np.cos(inc),np.sin(inc)
        P=np.array([cO*cw-sO*sw*ci,sO*cw+cO*sw*ci,sw*si]); Q=np.array([-cO*sw-sO*cw*ci,-sO*sw+cO*cw*ci,cw*si])
        return (P*xp+Q*yp).T,(P*vxp+Q*vyp).T
    
    rng=np.random.default_rng(seed); cl=rng.multivariate_normal(B,cov,NCL); cl[0]=B; cl[:,0]=np.clip(cl[:,0],0.0,0.99)
    sun=np.array(row('v_10')); sim=rebound.Simulation(); sim.G=mu
    for b,m in masses.items():
        r=row('v_'+b); sim.add(m=m,x=r[0],y=r[1],z=r[2],vx=r[3],vy=r[4],vz=r[5])
    sim.N_active=sim.N; n0=sim.N
    if with_primary:
        r=row('v_A'); sim.add(m=0,x=r[0],y=r[1],z=r[2],vx=r[3],vy=r[4],vz=r[5])
    P,V=el2state(cl[:,0],cl[:,1],cl[:,2],cl[:,3],cl[:,4],cl[:,5],t0)
    for i in range(NCL): sim.add(m=0,x=P[i,0]+sun[0],y=P[i,1]+sun[1],z=P[i,2]+sun[2],vx=V[i,0]+sun[3],vy=V[i,1]+sun[4],vz=V[i,2]+sun[5])
    sim.integrator='ias15'; sim.t=0
    return sim,n0,cl,t0
