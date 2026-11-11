"""Does object X's orbit predict the positions at which object Y was observed?
usage: linkage.py MPCDIR "X" "Y"   (uses JPL Horizons for X's topocentric ephemeris)"""
import sys,json,subprocess,collections,numpy as np
d,X,Y=sys.argv[1:4]
obs=collections.defaultdict(list)
for l in json.load(open(f"{d}/{Y.replace(' ','_')}.json"))[0]['OBS80'].split('\n'):
    if len(l)<80 or l[14] in 'sSRrVvXx': continue
    try:
        y,m,dd=int(l[15:19]),int(l[20:22]),float(l[23:32])
        a=(14-m)//12; yy=y+4800-a; mm=m+12*a-3
        jd=int(dd)+(153*mm+2)//5+365*yy+yy//4-yy//100+yy//400-32045-0.5+(dd-int(dd))
        ra=(int(l[32:34])+int(l[35:37])/60+float(l[38:44])/3600)*15
        dec=(-1 if l[44]=='-' else 1)*(int(l[45:47])+int(l[48:50])/60+float(l[51:56])/3600)
        obs[l[77:80]].append((jd,ra,dec))
    except ValueError: pass
res=[]
for stn,rows in obs.items():
    tl=','.join(f"{r[0]:.6f}" for r in rows)
    out=subprocess.run(['/usr/bin/curl','-sS','-m','120','-G','https://ssd.jpl.nasa.gov/api/horizons.api','--data-urlencode','format=text','--data-urlencode',f"COMMAND='DES={X};'",'--data-urlencode','EPHEM_TYPE=OBSERVER','--data-urlencode',f"CENTER='{stn}@399'",'--data-urlencode',f"TLIST='{tl}'",'--data-urlencode','TLIST_TYPE=JD','--data-urlencode',"QUANTITIES='1,36'",'--data-urlencode','ANG_FORMAT=DEG','--data-urlencode','CSV_FORMAT=YES','--data-urlencode','OBJ_DATA=NO','--data-urlencode','EXTRA_PREC=YES'],capture_output=True,text=True).stdout
    on=False; eph=[]
    for l in out.split('\n'):
        if l.startswith('$$SOE'): on=True; continue
        if l.startswith('$$EOE'): break
        if on:
            p=[x.strip() for x in l.split(',')]; eph.append((float(p[3]),float(p[4]),float(p[5]) if p[5] not in ('','n.a.') else np.nan,float(p[6]) if p[6] not in ('','n.a.') else np.nan))
    if len(eph)!=len(rows): print('  station',stn,'skipped: Horizons returned',len(eph),'of',len(rows)); continue
    for (jd,ra,dec),(era,edec,s_ra,s_dec) in zip(rows,eph):
        dra=(ra-era)*np.cos(np.radians(dec))*3600; ddec=(dec-edec)*3600
        res.append((jd,stn,dra,ddec,np.hypot(dra,ddec),np.hypot(s_ra,s_dec)))
r=np.array([(x[4],x[5]) for x in res])
print(f"{X} orbit vs {Y} observations: n={len(res)}  residual median {np.median(r[:,0]):.1f}\"  max {r[:,0].max():.1f}\"   predicted 3-sigma uncertainty median {np.nanmedian(r[:,1]):.1f}\"")
for x in res[:3]+res[-2:]: print(f"   JD {x[0]:.4f} {x[1]}  dRA {x[2]:9.1f}\"  dDec {x[3]:9.1f}\"  (3-sigma {x[5]:.1f}\")")
