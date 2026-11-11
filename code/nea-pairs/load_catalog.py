import json,sys,numpy as np,pandas as pd
d=sys.argv[1]
c=json.load(open(d+'/cad.json')); cad=pd.DataFrame(c['data'],columns=c['fields'])
for k in ['jd','dist','dist_min','dist_max','v_rel','v_inf','h']: cad[k]=pd.to_numeric(cad[k],errors='coerce')
cad['t']=pd.to_datetime(cad['cd'],format='%Y-%b-%d %H:%M')
s=json.load(open(d+'/sbdb_neo.json')); neo=pd.DataFrame(s['data'],columns=s['fields'])
for k in ['H','e','a','q','i','om','w','ma','moid','data_arc','n_obs_used','diameter','albedo','rot_per']: neo[k]=pd.to_numeric(neo[k],errors='coerce')
neo['first_obs']=pd.to_datetime(neo['first_obs'],errors='coerce'); neo['last_obs']=pd.to_datetime(neo['last_obs'],errors='coerce')
cad.to_pickle(d+'/cad.pkl'); neo.to_pickle(d+'/neo.pkl')
print('cad',len(cad),'neo',len(neo), neo['class'].value_counts().to_dict())
m=cad.merge(neo[['pdes','first_obs','last_obs','a','e','i','data_arc','condition_code','class']],left_on='des',right_on='pdes',how='left')
print('unmatched',m.pdes.isna().sum())
m['LD']=m.dist/0.002569
# discovered relative to approach
m['lead_days']=(m.t-m.first_obs).dt.total_seconds()/86400
print('\nclose approaches per year (<1 LD), and share first observed AFTER closest approach')
x=m[m.LD<1]; g=x.groupby(x.t.dt.year); print(pd.DataFrame({'n':g.size(),'post_frac':g.apply(lambda q:(q.lead_days<0).mean()).round(2)}).T.to_string())
print('\nlowest v_inf approaches')
print(m.sort_values('v_inf').drop_duplicates('des').head(40)[['des','cd','LD','v_inf','h','a','e','i','data_arc','condition_code']].to_string())
print('\nEarth-like orbits: 0.9<a<1.1, e<0.1, i<5')
q=neo[(neo.a.between(0.9,1.1))&(neo.e<0.1)&(neo.i<5)].sort_values('e')
print(len(q)); print(q[['pdes','H','a','e','i','moid','first_obs','data_arc','condition_code']].to_string())
