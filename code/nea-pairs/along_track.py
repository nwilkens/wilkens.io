import sys,json,numpy as np,pandas as pd
d=sys.argv[1]
s=json.load(open(d+'/sbdb_extra.json')); x=pd.DataFrame(s['data'],columns=s['fields']).set_index('pdes')
for k in x.columns:
    if k not in('producer','orbit_id'): x[k]=pd.to_numeric(x[k],errors='coerce')
p=pd.read_csv(d+'/pairs_top.csv').head(20)
pd.set_option('display.width',250)
rows=[]
for _,r in p.iterrows():
    A,B=x.loc[r.A],x.loc[r.B]
    # propagate mean anomaly of B to A's epoch (two-body)
    mb=(B.ma+B.n*(A.epoch-B.epoch))%360
    dM=((mb-A.ma+180)%360)-180
    # uncertainty of that along-track difference, dominated by sigma_n*dt + sigma_ma
    rows.append(dict(A=r.A,B=r.B,D=round(r.D,4),epA=A.epoch,epB=B.epoch,dM_deg=round(dM,3),sig_maA=A.sigma_ma,sig_maB=B.sigma_ma,per_yr=round(A.per/365.25,2),dTp_days=round(dM/A.n,2),HA=r.HA,HB=r.HB,arcA=r.data_arcA,arcB=r.data_arcB))
print(pd.DataFrame(rows).to_string())
