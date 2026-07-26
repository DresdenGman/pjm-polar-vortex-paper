import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'font.size': 9,
})

models = ['PJM\nDay-Ahead', 'Persistence\n1h', 'Naive\n24h', 'Naive\n168h',
          'Linear\nRegr.', 'GBoost', 'QR-GBT\nq50', 'QR-GBT\nq95', 'QR-GBT\nq99']
errors = [2545, 2906, 9973, 30769, 5525, -1388, 5153, 1100, 925]

fig, ax = plt.subplots(figsize=(7.5, 4.5))
colors = ['#888888', '#aaaaaa', '#aaaaaa', '#aaaaaa', '#4472C4', '#ED7D31',
          '#5B9BD5', '#5B9BD5', '#5B9BD5']
bars = ax.bar(range(len(models)), errors, color=colors, edgecolor='white', linewidth=0.5)

for i, (bar, err) in enumerate(zip(bars, errors)):
    sign = '+' if err > 0 else ''
    label = f'{sign}{abs(err):,}'
    if err < 0:
        # GBoost: explicit minus sign
        ax.text(bar.get_x() + bar.get_width()/2, 1000, '-1,388',
                ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#CC5500')
    elif err > 25000:
        ax.text(bar.get_x() + bar.get_width()/2, err - 2000, label,
                ha='center', va='top', fontsize=7.5, fontweight='bold')
    else:
        ax.text(bar.get_x() + bar.get_width()/2, err + 2000, label,
                ha='center', va='bottom', fontsize=7.5, fontweight='bold')

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_xticks(range(len(models)))
ax.set_xticklabels(models, fontsize=7)
ax.set_ylabel('Prediction Error (MW)', fontsize=9)
ax.set_title('Event Peak Prediction Errors, Jan 7 18:00 EPT (Actual = 140,510 MW)', fontsize=10, fontweight='bold')
ax.grid(axis='y', alpha=0.2)

# Overprediction arrow: from above, pointing down toward GBoost
ax.annotate('Overprediction', xy=(5, 2500), fontsize=7, color='#ED7D31',
            ha='center', va='bottom',
            xytext=(5, 7500), textcoords='data',
            arrowprops=dict(arrowstyle='->', color='#ED7D31', lw=0.8))

# Underprediction: small note above positive bars
ax.annotate('Underprediction', xy=(0, 6000), fontsize=7, color='#888888',
            ha='center', va='bottom',
            xytext=(0, 12000), textcoords='data',
            arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))

plt.tight_layout()
plt.savefig('figures/figure6_tail_risk_event_peak.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Done: Figure 6 — GBoost label above bar, Overprediction arrow from above")
