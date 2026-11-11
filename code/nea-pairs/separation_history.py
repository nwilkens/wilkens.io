import sys,numpy as np
d=sys.argv[1]
def load(n):
    rows=[]; on=False
    for l in open(f"{d}/{n.replace(' ','_')}.txt"):
        if l.startswith('$$SOE'): on=True; continue
        if l.startswith('$$EOE'): break
        if on:
            p=l.split(','); rows.append([float(p[0])]+[float(x) for x in p[2:8]])
    return np.array(rows)
pairs=[('2018 NC15','2026 LD1'),('357414','2023 YD2'),('2024 SO3','2026 FO1'),('2005 TF','2024 WS19'),('2022 MY3','2022 OP8'),('2012 QG8','2024 GE1')]
yr=lambda jd:2000+(jd-2451545)/365.25
for a,b in pairs:
    A,B=load(a),load(b)
    r=np.linalg.norm(A[:,1:4]-B[:,1:4],axis=1); v=np.linalg.norm(A[:,4:7]-B[:,4:7],axis=1)
    k=r.argmin()
    print(f"\n{a} / {b}: min separation {r[k]:.3e} km at {yr(A[k,0]):.1f}, rel speed there {v[k]*1000:.2f} m/s")
    for y in (2026.5,2020,2000,1975,1950,1900,1850,1800,1750,1701):
        j=np.abs(yr(A[:,0])-y).argmin()
        # yearly-window minimum to smooth orbital-phase oscillation
        w=slice(max(0,j-180),j+180)
        print(f"   {y:7.1f}: sep min/median over +-1yr = {r[w].min():.3e} / {np.median(r[w]):.3e} km ; rel speed median {np.median(v[w])*1000:8.2f} m/s")
