"""Animate the 2026 apparition: orbit from above, and LD1's sky offset from NC15."""
import sys,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter
d,out_mp4,out_png=sys.argv[1],sys.argv[2],sys.argv[3]
def rows(f):
    on=False
    for l in open(f'{d}/{f}.txt'):
        if l.startswith('$$SOE'): on=True; continue
        if l.startswith('$$EOE'): break
        if on: yield [x.strip() for x in l.split(',')]
def vec(f):
    r=list(rows(f)); return np.array([float(x[0]) for x in r]),np.array([[float(x[2]),float(x[3]),float(x[4])] for x in r])
def obs(f):
    r=list(rows(f)); return pd.to_datetime([x[0] for x in r]),np.array([[float(x[3]),float(x[4]),float(x[5])] for x in r])
jd,A=vec('v_nc15'); _,B=vec('v_ld1'); _,E=vec('v_earth'); _,ORB=vec('orbit_nc15')
t,oa=obs('o_nc15'); _,ob=obs('o_ld1')
AU=1.495978707e8
dx=-(ob[:,0]-oa[:,0])*np.cos(np.radians(oa[:,1])); dy=ob[:,1]-oa[:,1]   # east to the left
sky=np.hypot(dx,dy); sep=np.linalg.norm(A-B,axis=1)*AU; dist=np.linalg.norm(A-E,axis=1)*AU
i0=np.searchsorted(t,pd.Timestamp('2026-04-15')); i1=np.searchsorted(t,pd.Timestamp('2026-08-15'))
BG='#0a0a0a'; INK='#fafafa'; MUTED='#a6a6a6'; GRID='#262626'; BLUE='#3987E5'; ORANGE='#EF5F2E'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig=plt.figure(figsize=(12.8,6.4),dpi=100); fig.patch.set_facecolor(BG)
a1=fig.add_axes([0.03,0.06,0.45,0.80]); a2=fig.add_axes([0.53,0.06,0.45,0.80])
for a in (a1,a2):
    a.set_facecolor(BG); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_color(GRID)
fig.text(0.03,0.93,'Orbit seen from above',color=INK,fontsize=20,fontweight='bold')
fig.text(0.53,0.93,'Seen from Earth',color=INK,fontsize=20,fontweight='bold')
date_txt=fig.text(0.48,0.93,'',color=MUTED,fontsize=19,ha='right',family='monospace')
# left panel
th=np.linspace(0,2*np.pi,400)
a1.plot(np.cos(th),np.sin(th),color=MUTED,lw=1); a1.plot(ORB[:,0],ORB[:,1],color=BLUE,lw=1.5,alpha=0.7)
a1.scatter([0],[0],s=90,color='#e8c547',zorder=5); a1.text(0.07,0.07,'Sun',color=MUTED,fontsize=17)
a1.text(0.0,1.06,"Earth's orbit",color=MUTED,fontsize=17,ha='center'); a1.text(-2.3,1.9,'Shared asteroid orbit',color=MUTED,fontsize=17,ha='left')
a1.set_xlim(-2.4,2.0); a1.set_ylim(-2.2,2.2)
link,=a1.plot([],[],color=MUTED,lw=1,ls=(0,(3,3)))
earth=a1.scatter([],[],s=70,color=INK,edgecolor=BG,linewidth=2,zorder=6); pair=a1.scatter([],[],s=70,color=ORANGE,edgecolor=BG,linewidth=2,zorder=7)
e_lab=a1.text(0,0,'Earth',color=INK,fontsize=17); p_lab=a1.text(0,0,'The pair',color=INK,fontsize=17,ha='right')
d_txt=a1.text(0.03,0.04,'',transform=a1.transAxes,color=INK,fontsize=18,family='monospace')
# right panel
R=2.6; a2.set_xlim(-R,R); a2.set_ylim(-R,R)
a2.plot(0.26*np.cos(th)-1.9,0.26*np.sin(th)-1.55,color=MUTED,lw=1); a2.text(-1.55,-1.55,'Full Moon, to scale',color=MUTED,fontsize=17,va='center')
a2.scatter([0],[0],s=110,color=BLUE,edgecolor=BG,linewidth=2,zorder=6); a2.text(0.15,0.15,'2018 NC15',color=INK,fontsize=17)
trail,=a2.plot([],[],color=ORANGE,lw=1.5,alpha=0.6)
ld1=a2.scatter([],[],s=60,color=ORANGE,edgecolor=BG,linewidth=2,zorder=7); l_lab=a2.text(0,0,'2026 LD1',color=INK,fontsize=17,ha='right')
s_txt=a2.text(0.03,0.04,'',transform=a2.transAxes,color=INK,fontsize=18,family='monospace')
marks=[(pd.Timestamp('2026-06-05 05:32'),'5 June: Catalina images both'),(pd.Timestamp('2026-06-21 06:27'),'21 June: imaged together again')]
mk=[a2.scatter([],[],s=120,facecolor='none',edgecolor=INK,linewidth=1.5,zorder=8) for _ in marks]
note=a2.text(0.03,0.96,'',transform=a2.transAxes,color=INK,fontsize=18,va='top')
def draw(i):
    date_txt.set_text(t[i].strftime('%Y-%m-%d'))
    earth.set_offsets([E[i,:2]]); pair.set_offsets([A[i,:2]]); link.set_data([E[i,0],A[i,0]],[E[i,1],A[i,1]])
    e_lab.set_position((E[i,0]+0.10,E[i,1]+0.10)); p_lab.set_position((A[i,0]-0.10,A[i,1]-0.34))
    d_txt.set_text(f'{dist[i]/1e6:.1f} million km from Earth')
    ld1.set_offsets([[dx[i],dy[i]]]); trail.set_data(dx[i0:i+1],dy[i0:i+1]); l_lab.set_position((dx[i]+0.05,dy[i]-0.42))
    s_txt.set_text(f'{sky[i]:.2f}° apart, {sep[i]/1e3:.0f},000 km in space')
    msg=''
    for (tm,lab),m in zip(marks,mk):
        j=np.searchsorted(t,tm)
        if i>=j: m.set_offsets([[dx[j],dy[j]]]); msg=lab if i-j<60 else msg
    note.set_text(msg)
k=int(np.argmin(dist[i0:i1]))+i0
draw(k); fig.savefig(out_png,facecolor=BG,dpi=150)
for m in mk: m.set_offsets(np.empty((0,2)))
anim=FuncAnimation(fig,lambda f:draw(i0+f),frames=int(i1-i0),interval=33)
anim.save(out_mp4,writer=FFMpegWriter(fps=30,codec='libx264',extra_args=['-pix_fmt','yuv420p','-crf','23','-movflags','+faststart']),savefig_kwargs={'facecolor':BG})
print('frames',i1-i0,'closest',t[k],round(dist[k]/1e6,1),'Mkm; sky sep range',sky[i0:i1].min().round(2),sky[i0:i1].max().round(2),'space sep km',int(sep[i0:i1].min()),int(sep[i0:i1].max()))
