import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import scienceplots
plt.style.use(['science', 'ieee'])
plt.rcParams.update({'font.size': 8, 'figure.dpi': 300, 'text.usetex': False})

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')

C = {'data':'#F0F4F8','weather':'#EBF5FB','bench':'#FEF9E7','feat':'#F5F5F5',
     'point':'#EAFAF1','qr':'#EBF5FB','eval':'#FFF8E1','stress':'#FDEDEC'}
BORDER = '#999999'
TEXT = '#222222'
ARROW = '#888888'
LAB = '#777777'

def box(ax, x, y, w, h, txt, c, fs=7.5):
    b = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.15",
                        facecolor=c, edgecolor=BORDER, linewidth=0.8)
    ax.add_patch(b)
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs, color=TEXT, linespacing=1.3)

def arr(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=ARROW, lw=0.8))

def lbl(ax, x, y, t):
    ax.text(x, y, t, fontsize=6.5, color=LAB, fontweight='bold', ha='center', va='bottom')

# Row 1
y1=6.8
box(ax,2.2,y1,2.8,1.0,'PJM RTO Load\n2010--2014',C['data'])
box(ax,5.0,y1,2.8,1.0,'ERA5 Weather\nReanalysis',C['weather'])
box(ax,7.8,y1,2.8,1.0,'PJM Day-Ahead\nForecast 2014',C['bench'])
lbl(ax,5.0,y1+0.7,'DATA SOURCES')

# Row 2
y2=5.2
box(ax,3.6,y2,4.0,0.9,'Feature Engineering: Calendar + Lags + Weather',C['feat'])
lbl(ax,5.0,y2+0.65,'PROCESSING')

# Row 3
y3=3.5
box(ax,2.2,y3,2.8,1.1,'Point Baselines\nPersist, Naive,\nLinear, GBoost',C['point'])
box(ax,5.0,y3,2.8,1.1,'QR-GBT Quantile\nq01,q05,q10,q50,\nq90,q95,q99',C['qr'])
box(ax,7.8,y3,2.8,1.1,'PJM Day-Ahead\nBenchmark',C['bench'])
lbl(ax,5.0,y3+0.8,'MODELING')

# Row 4
y4=1.8
box(ax,5.0,y4,4.2,0.9,'Calibration and Coverage Analysis',C['eval'])
y5=0.8
box(ax,5.0,y5,4.2,0.9,'Winter Vortex vs Summer Peak Stress Test',C['stress'])
lbl(ax,5.0,y4+0.65,'EVALUATION')

# Arrows
arr(ax,2.2,y1-0.5,3.0,y2+0.45); arr(ax,5.0,y1-0.5,4.2,y2+0.45)
arr(ax,7.8,y1-0.5,7.8,y3+0.55)
arr(ax,2.8,y2-0.45,2.2,y3+0.55); arr(ax,4.4,y2-0.45,5.0,y3+0.55)
arr(ax,2.2,y3-0.55,3.8,y4+0.45); arr(ax,5.0,y3-0.55,5.0,y4+0.45)
arr(ax,7.8,y3-0.55,6.2,y4+0.45)
arr(ax,5.0,y4-0.45,5.0,y5+0.45)

plt.tight_layout(pad=0.5)
plt.savefig('figures/figure2_workflow.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Done: Figure 2 — SciencePlots IEEE style")
