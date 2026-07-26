import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'font.size': 9,
})

# ══════════════════════════════════════
# Figure 6: Tail-Risk Event Peak Error
# ══════════════════════════════════════
print("Generating Figure 6...")

models = ['PJM\nDay-Ahead', 'Persistence\n1h', 'Naive\n24h', 'Naive\n168h',
          'Linear\nRegr.', 'GBoost', 'QR-GBT\nq50', 'QR-GBT\nq95', 'QR-GBT\nq99']
predictions = [137965, 137604, 130537, 109742, 134985, 141898, 135357, 139410, 139585]
errors = [2545, 2906, 9973, 30769, 5525, -1388, 5153, 1100, 925]
actual = 140510

fig, ax = plt.subplots(figsize=(7.5, 4.5))
colors = ['#888888', '#aaaaaa', '#aaaaaa', '#aaaaaa', '#4472C4', '#ED7D31', 
          '#5B9BD5', '#5B9BD5', '#5B9BD5']
bars = ax.bar(range(len(models)), errors, color=colors, edgecolor='white', linewidth=0.5)

# Add value labels on bars
for i, (bar, err) in enumerate(zip(bars, errors)):
    sign = '+' if err > 0 else ''
    label = f'{sign}{abs(err):,}'
    y_pos = err + (3000 if err > 0 else -3000)
    va = 'bottom' if err > 0 else 'top'
    ax.text(bar.get_x() + bar.get_width()/2, y_pos, label,
            ha='center', va=va, fontsize=7.5, fontweight='bold')

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_xticks(range(len(models)))
ax.set_xticklabels(models, fontsize=7)
ax.set_ylabel('Prediction Error (MW)', fontsize=9)
ax.set_title('Event Peak Prediction Errors, Jan 7 18:00 EPT (Actual = 140,510 MW)', fontsize=10, fontweight='bold')
ax.grid(axis='y', alpha=0.2)

# Legend annotations
ax.text(5, -1388 - 4000, 'Over-\nprediction', ha='center', fontsize=7, color='#ED7D31')
ax.text(0, 2545 + 4000, 'Under-\nprediction', ha='center', fontsize=7, color='#888888')

plt.tight_layout()
plt.savefig('figures/figure6_tail_risk_event_peak.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  Done Figure 6 — labels: +5,153 / +1,100 / +925")

# ══════════════════════════════════════
# Figure 1 fix: panel (b) full Jan 1-15
# ══════════════════════════════════════
print("Regenerating Figure 1 with full Jan 1-15 data...")

import matplotlib.dates as mdates

df = pd.read_csv('data/processed/modeling_features_2010_2014.csv')
df['timestamp_ept'] = pd.to_datetime(df['timestamp_ept'])
df_2014 = df[df['source_year'] == 2014].copy()

df_event = pd.read_csv('figures/data/figure3_jan6_8_data.csv')
df_event['timestamp_ept'] = pd.to_datetime(df_event['timestamp_ept'])

jan7_18 = pd.Timestamp('2014-01-07 18:00:00')
jun17_17 = pd.Timestamp('2014-06-17 17:00:00')

fig, axes = plt.subplots(3, 1, figsize=(7.5, 9), gridspec_kw={'height_ratios': [1.2, 0.9, 1.0]})

# Panel (a): Full-year 2014
ax = axes[0]
ax.plot(df_2014['timestamp_ept'], df_2014['actual_load_mw']/1000, color='steelblue', linewidth=0.5)
ax.axvline(jan7_18, color='crimson', linestyle='--', linewidth=0.8, alpha=0.7)
ax.axvline(jun17_17, color='darkorange', linestyle='--', linewidth=0.8, alpha=0.7)
ax.annotate('Cold-event peak\n140,510 MW\nJan 7 18:00 EPT', xy=(jan7_18, 140.51), fontsize=7, color='crimson',
            ha='left', va='top', xytext=(15, 5), textcoords='offset points')
ax.annotate('Annual peak\n141,678 MW\nJun 17 17:00 EPT', xy=(jun17_17, 141.68), fontsize=7, color='darkorange',
            ha='right', va='bottom', xytext=(-10, 15), textcoords='offset points')
ax.set_ylabel('PJM RTO Load (GW)')
ax.set_title('(a) Full-Year 2014 PJM RTO Hourly Load', fontsize=10, fontweight='bold')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2014-12-31'))
ax.grid(True, alpha=0.2)

# Panel (b): Jan 1-15 — use FULL data from df_2014
ax = axes[1]
mask_jan = (df_2014['timestamp_ept'] >= '2014-01-01') & (df_2014['timestamp_ept'] < '2014-01-16')
df_jan = df_2014[mask_jan]
ax.plot(df_jan['timestamp_ept'], df_jan['actual_load_mw']/1000, color='steelblue', linewidth=0.8)
ax.axvspan(pd.Timestamp('2014-01-06'), pd.Timestamp('2014-01-08 23:59'), alpha=0.1, color='crimson')
ax.axvline(jan7_18, color='crimson', linestyle='--', linewidth=0.8)
ax.annotate('140,510 MW', xy=(jan7_18, 140.51), fontsize=7.5, color='crimson', ha='left', va='bottom')
ax.set_ylabel('PJM RTO Load (GW)')
ax.set_title('(b) January 1-15, 2014', fontsize=10, fontweight='bold')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.set_xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2014-01-15 23:59'))
ax.grid(True, alpha=0.2)

# Panel (c): Jan 6-8 weather
ax = axes[2]
ax2 = ax.twinx()
l1 = ax.plot(df_event['timestamp_ept'], df_event['temperature_f'], color='steelblue', linewidth=0.8, label='Temperature')
l2 = ax.plot(df_event['timestamp_ept'], df_event['wind_chill_f'], color='purple', linewidth=0.8, linestyle='--', label='Wind Chill')
l3 = ax2.plot(df_event['timestamp_ept'], df_event['hdh'], color='darkorange', linewidth=0.8, label='HDH')
ax.set_ylabel('Temperature / Wind Chill (F)', color='steelblue')
ax2.set_ylabel('Heating Degree Hours', color='darkorange')
ax.set_title('(c) ERA5 Weather Conditions, Jan 6-8, 2014', fontsize=10, fontweight='bold')
ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.set_xlim(pd.Timestamp('2014-01-06'), pd.Timestamp('2014-01-08 23:59'))
ax.grid(True, alpha=0.2)
ax.set_ylim(-35, 70)
lns = l1 + l2 + l3
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='upper left', fontsize=7)

plt.tight_layout(pad=2)
plt.savefig('figures/figure1_event_definition.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  Done Figure 1 — full Jan 1-15 data in panel (b)")
print("\nAll corrections applied.")
