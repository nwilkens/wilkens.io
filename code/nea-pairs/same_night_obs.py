import sys,json,numpy as np,pandas as pd
d=sys.argv[1]
def load(n):
    rows=[]
    for l in json.load(open(f'{d}/{n}.json'))[0]['OBS80'].split('\n'):
        if len(l)<80 or l[14] in 'sSRrVv': continue
        try:
            y,m,dd=int(l[15:19]),int(l[20:22]),float(l[23:32])
            ra=(int(l[32:34])+int(l[35:37])/60+float(l[38:44])/3600)*15
            sg=-1 if l[44]=='-' else 1
            dec=sg*(int(l[45:47])+int(l[48:50])/60+float(l[51:56])/3600)
            mag=float(l[65:70]) if l[65:70].strip() else np.nan
            t=pd.Timestamp(year=y,month=m,day=1)+pd.Timedelta(days=dd-1)
            rows.append(dict(t=t,ra=ra,dec=dec,mag=mag,band=l[70],stn=l[77:80]))
        except Exception as e: pass
    return pd.DataFrame(rows)
A=load('2018_NC15'); B=load('2026_LD1')
print('NC15 obs',len(A),A.t.min(),A.t.max()); print('LD1 obs',len(B),B.t.min(),B.t.max())
print('NC15 by year',A.groupby(A.t.dt.year).size().to_dict())
A26=A[A.t>'2026']; print('NC15 2026 stations',A26.stn.value_counts().to_dict()); print('LD1 stations',B.stn.value_counts().to_dict())
print('NC15 2026 median mag %.2f ; LD1 median mag %.2f'%(A26.mag.median(),B.mag.median()))
# same station, within 0.2 d: sky separation
rows=[]
for _,b in B.iterrows():
    c=A26[(A26.stn==b.stn)]
    if len(c)==0: continue
    k=(c.t-b.t).abs().idxmin(); a=c.loc[k]; dt=(a.t-b.t).total_seconds()/86400
    if abs(dt)<0.25:
        sep=np.degrees(np.arccos(np.clip(np.sin(np.radians(a.dec))*np.sin(np.radians(b.dec))+np.cos(np.radians(a.dec))*np.cos(np.radians(b.dec))*np.cos(np.radians(a.ra-b.ra)),-1,1)))
        rows.append(dict(t=b.t.round('min'),stn=b.stn,dt_d=round(dt,3),sep_deg=round(sep,3),magLD1=b.mag,magNC15=a.mag,raB=round(b.ra,3),decB=round(b.dec,3),raA=round(a.ra,3),decA=round(a.dec,3)))
R=pd.DataFrame(rows); pd.set_option('display.width',200)
print('same-station near-simultaneous pairs:',len(R)); print(R.drop_duplicates(['stn','sep_deg']).head(25).to_string())
print(B.groupby(B.t.dt.date).agg(n=('mag','size'),mag=('mag','median'),stn=('stn',lambda s:','.join(sorted(set(s))))).to_string())
print(A26.groupby(A26.t.dt.date).agg(n=('mag','size'),mag=('mag','median'),stn=('stn',lambda s:','.join(sorted(set(s))))).to_string())
