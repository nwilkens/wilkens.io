import sys,numpy as np,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]); env,envt=z['env'][:-1],z['envt'][:-1]
W,N=env.shape; x=4*np.arange(W)+2
BG='#0a0a0a'; INK='#fafafa'; MUTED='#a6a6a6'; GRID='#1f1f1f'; BLUE='#3987E5'; ORANGE='#EF5F2E'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,ax=plt.subplots(figsize=(8.4,4.8),dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
lo,med,hi=np.percentile(env,[5,50,95],axis=1)
ax.fill_between(x,lo,hi,color=BLUE,alpha=0.22,lw=0)
ax.plot(x,med,color=BLUE,lw=2)
k=env.argmin(axis=0); dm=env[k,np.arange(N)]; age=-envt[k,np.arange(N)]/365.25
s=(k>0)&(k<W-1)&(dm<1e4)
ax.scatter(age[s],dm[s],s=70,color=ORANGE,edgecolor=BG,linewidth=2,zorder=5)
ax.axhline(384400,color=MUTED,lw=1,ls=(0,(4,4)))
ax.text(298,384400*0.8,'Earth to Moon distance',color=MUTED,ha='right',va='top',fontsize=10)
ax.text(150,med[37]*1.5,'Median of 400 clones',color=INK,ha='center',va='bottom',fontsize=10)
ax.text(250,4.5e6,'5th to 95th percentile',color=INK,ha='center',va='center',fontsize=10)
ax.text(150,2.2e4,'Clones that pass within 10,000 km (13 of 400)',color=INK,fontsize=10,ha='center',va='center')
ax.set_yscale('log'); ax.set_xlim(0,300); ax.set_ylim(3e2,2e8)
ax.set_xlabel('Years before 2026',color=MUTED); ax.set_ylabel('Closest separation in each 4-year window (km)',color=MUTED)
ax.tick_params(colors=MUTED,length=0); ax.grid(True,which='major',color=GRID,lw=1); ax.set_axisbelow(True)
for sp in ax.spines.values(): sp.set_visible(False)
fig.tight_layout(); fig.savefig(sys.argv[2],facecolor=BG)
print('points',int(s.sum()),np.sort(age[s]).round(0),np.sort(dm[s]).round(0))
