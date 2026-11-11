"""Predicted brightness of both asteroids across the 2018-2026 apparitions."""
import sys,json,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
d,mpc,out=sys.argv[1],sys.argv[2],sys.argv[3]
def load(n):
    rows=[];on=False
    for l in open(f'{d}/obs_{n}.txt'):
        if l.startswith('$$SOE'): on=True; continue
        if l.startswith('$$EOE'): break
        if on:
            p=[x.strip() for x in l.split(',')]; rows.append((pd.Timestamp(p[0]),float(p[5]),float(p[9])))
    return pd.DataFrame(rows,columns=['t','mag','elong']).set_index('t')
A,B=load('2018_NC15'),load('2026_LD1')
A=A[A.index>='2018-01-01']; B=B[B.index>='2018-01-01']
def nights(n):
    s=set()
    for l in json.load(open(f'{mpc}/{n}.json'))[0]['OBS80'].split('\n'):
        if len(l)>=80 and l[14] not in 'sSRrVv': s.add(pd.Timestamp(l[15:19]+'-'+l[20:22]+'-'+l[23:25]))
    return sorted(s)
BG='#0a0a0a'; INK='#fafafa'; MUTED='#a6a6a6'; GRID='#1f1f1f'; BLUE='#3987E5'; ORANGE='#EF5F2E'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,ax=plt.subplots(figsize=(8.4,4.8),dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.plot(A.index,A.mag,color=BLUE,lw=2,label='2018 NC15'); ax.plot(B.index,B.mag,color=ORANGE,lw=2,label='2026 LD1 (predicted before June 2026)')
na,nb=nights('2018_NC15'),nights('2026_LD1')
ax.scatter(na,[24.55]*len(na),marker='|',s=90,color=BLUE,linewidth=1.5); ax.scatter(nb,[24.9]*len(nb),marker='|',s=90,color=ORANGE,linewidth=1.5)
ax.text(pd.Timestamp('2019-05-25'),24.72,'Nights observed',ha='center',color=MUTED,fontsize=9,va='center')
ax.axhline(21.5,color=MUTED,lw=1,ls=(0,(4,4))); ax.text(pd.Timestamp('2018-02-01'),21.42,'Approximate reach of survey telescopes',color=MUTED,fontsize=10,va='bottom')
j=B.loc['2024-05-01':'2024-08-01'].mag.idxmin()
ax.annotate('June 2024: predicted magnitude %.1f,\nnot detected at the time'%B.mag[j],xy=(j,B.mag[j]),xytext=(pd.Timestamp('2021-03-01'),19.3),color=INK,fontsize=10,ha='center',va='center',arrowprops=dict(arrowstyle='-',color=MUTED,lw=1))
ax.set_ylim(25.2,17.8); ax.set_xlim(pd.Timestamp('2018-01-01'),pd.Timestamp('2026-11-01'))
ax.set_ylabel('Apparent magnitude (brighter is up)',color=MUTED)
ax.tick_params(colors=MUTED,length=0); ax.grid(True,color=GRID,lw=1); ax.set_axisbelow(True)
for sp in ax.spines.values(): sp.set_visible(False)
leg=ax.legend(loc='lower left',bbox_to_anchor=(0,1.0),frameon=False,fontsize=10,ncol=2); [t.set_color(INK) for t in leg.get_texts()]
fig.tight_layout(); fig.savefig(out,facecolor=BG); print('peak 2024',j,B.mag[j])
