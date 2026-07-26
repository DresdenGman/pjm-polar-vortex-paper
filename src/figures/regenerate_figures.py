import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# ── Figure 1: Event Definition ──
print("Generating Figure 1...")
df = pd.read_csv('data/processed/modeling_features_2010_2014.csv')
df['timestamp_ept'] = pd.to_datetime(df['timestamp_ept'])
df_2014 = df[df['source_year'] == 2014].copy()
df_zoom = pd.read_csv('figures/data/figure1_jan5_9_data.csv')
df_zoom['timestamp_ept'] = pd.to_datetime(df_zoom['timestamp_ept'])
df_event = pd.read_csv('figures/data/figure3_jan6_8_data.csv')
df_event['timestamp_ept'] = pd.to_datetime(df_event['timestamp_ept'])

fig, axes = plt.subplots(3, 1, figsize=(7.5, 9), gridspec_kw={'height_ratios': [1.2, 0.9, 1.0]})
jan7_18 = pd.Timestamp('2014-01-07 18:00:00')
jun17_17 = pd.Timestamp('2014-06-17 17:00:00')

# Panel (a)
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

# Panel (b)
ax = axes[1]
ax.plot(df_zoom['timestamp_ept'], df_zoom['actual_load_mw']/1000, color='steelblue', linewidth=0.8)
ax.axvspan(pd.Timestamp('2014-01-06'), pd.Timestamp('2014-01-08 23:59'), alpha=0.1, color='crimson')
ax.axvline(jan7_18, color='crimson', linestyle='--', linewidth=0.8)
ax.annotate('140,510 MW', xy=(jan7_18, 140.51), fontsize=7.5, color='crimson', ha='left', va='bottom')
ax.set_ylabel('PJM RTO Load (GW)')
ax.set_title('(b) January 1-15, 2014', fontsize=10, fontweight='bold')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.set_xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2014-01-15 23:59'))
ax.grid(True, alpha=0.2)

# Panel (c)
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
print("  Done Figure 1")

# ── Figure 3: Vortex Quantile Forecast ──
print("Generating Figure 3...")
df_q = pd.read_csv('data/results/quantile_predictions_2014.csv')
df_q['timestamp_ept'] = pd.to_datetime(df_q['timestamp_ept'])
mask = (df_q['timestamp_ept'] >= '2014-01-06') & (df_q['timestamp_ept'] < '2014-01-09')
df_v = df_q[mask].copy()

fig, axes = plt.subplots(3, 1, figsize=(7.5, 8.5), gridspec_kw={'height_ratios': [1.1, 1.1, 0.9]})

# Panel (a)
ax = axes[0]
ax.plot(df_v['timestamp_ept'], df_v['actual_load_mw']/1000, 'k-', linewidth=0.9, label='Actual')
ax.plot(df_v['timestamp_ept'], df_v['qr_gbt_q50_mw']/1000, '--', color='crimson', linewidth=0.9, label='QR-GBT q50')
ax.plot(df_v['timestamp_ept'], df_v['pjm_day_ahead_mw']/1000, ':', color='grey', linewidth=0.8, label='PJM Day-Ahead')
ax.set_ylabel('Load (GW)')
ax.set_title('(a) Actual Load vs Forecasts, Jan 6-8, 2014', fontsize=10, fontweight='bold')
ax.legend(fontsize=7, loc='upper left')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
ax.grid(True, alpha=0.2)

# Panel (b)
ax = axes[1]
ax.fill_between(df_v['timestamp_ept'], df_v['qr_gbt_q01_mw']/1000, df_v['qr_gbt_q99_mw']/1000,
                alpha=0.15, color='steelblue', label='98% PI')
ax.fill_between(df_v['timestamp_ept'], df_v['qr_gbt_q05_mw']/1000, df_v['qr_gbt_q95_mw']/1000,
                alpha=0.2, color='steelblue', label='90% PI')
ax.plot(df_v['timestamp_ept'], df_v['actual_load_mw']/1000, 'k-', linewidth=0.9, label='Actual')
ax.set_ylabel('Load (GW)')
ax.set_title('(b) Prediction Intervals, Jan 6-8, 2014', fontsize=10, fontweight='bold')
ax.legend(fontsize=7, loc='upper left')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
ax.grid(True, alpha=0.2)

# Panel (c)
ax = axes[2]
mask_pk = (df_v['timestamp_ept'] >= '2014-01-07 12:00') & (df_v['timestamp_ept'] <= '2014-01-08 00:00')
df_pk = df_v[mask_pk]
ax.fill_between(df_pk['timestamp_ept'], df_pk['qr_gbt_q01_mw']/1000, df_pk['qr_gbt_q99_mw']/1000,
                alpha=0.15, color='steelblue')
ax.fill_between(df_pk['timestamp_ept'], df_pk['qr_gbt_q05_mw']/1000, df_pk['qr_gbt_q95_mw']/1000,
                alpha=0.2, color='steelblue')
ax.plot(df_pk['timestamp_ept'], df_pk['actual_load_mw']/1000, 'k-', linewidth=1.0)
ax.plot(df_pk['timestamp_ept'], df_pk['qr_gbt_q50_mw']/1000, '--', color='crimson', linewidth=0.9)
peak_time = pd.Timestamp('2014-01-07 18:00:00')
ax.axhline(140.51, color='red', linestyle=':', linewidth=0.8, alpha=0.5)
ax.annotate('Event peak 140,510 MW\n(outside 98% PI)', xy=(peak_time, 140.51),
            fontsize=7.5, color='red', ha='left', va='bottom',
            xytext=(30, -12), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
ax.set_ylabel('Load (GW)')
ax.set_xlabel('Time (EPT)')
ax.set_title('(c) Peak Zoom, Jan 7, 2014', fontsize=10, fontweight='bold')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax.grid(True, alpha=0.2)

plt.tight_layout(pad=2)
plt.savefig('figures/figure3_vortex_quantile_forecast.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  Done Figure 3")

# ── Figure 5: Winter vs Summer ──
print("Generating Figure 5...")
mask_s = (df_q['timestamp_ept'] >= '2014-06-16') & (df_q['timestamp_ept'] < '2014-06-19')
df_summer = df_q[mask_s].copy()
mask_w = (df_q['timestamp_ept'] >= '2014-01-06') & (df_q['timestamp_ept'] < '2014-01-09')
df_winter = df_q[mask_w].copy()

fig, axes = plt.subplots(2, 2, figsize=(7.5, 6.5))

# Winter actual vs q50
ax = axes[0, 0]
ax.plot(df_winter['timestamp_ept'], df_winter['actual_load_mw']/1000, 'k-', linewidth=0.8, label='Actual')
ax.plot(df_winter['timestamp_ept'], df_winter['qr_gbt_q50_mw']/1000, '--', color='crimson', linewidth=0.8, label='QR-GBT q50')
ax.set_title('Winter Vortex (Jan 6-8)', fontsize=9, fontweight='bold')
ax.set_ylabel('Load (GW)')
ax.legend(fontsize=6.5)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax.grid(True, alpha=0.2)
ax.text(0.98, 0.05, 'q50 MAE = 2,130 MW', transform=ax.transAxes, fontsize=7, ha='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Summer actual vs q50
ax = axes[0, 1]
ax.plot(df_summer['timestamp_ept'], df_summer['actual_load_mw']/1000, 'k-', linewidth=0.8, label='Actual')
ax.plot(df_summer['timestamp_ept'], df_summer['qr_gbt_q50_mw']/1000, '--', color='darkgreen', linewidth=0.8, label='QR-GBT q50')
ax.set_title('Summer Near-Peak (Jun 16-18)', fontsize=9, fontweight='bold')
ax.set_ylabel('Load (GW)')
ax.legend(fontsize=6.5)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax.grid(True, alpha=0.2)
ax.text(0.98, 0.05, 'q50 MAE = 1,060 MW', transform=ax.transAxes, fontsize=7, ha='right',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# Winter PI coverage
ax = axes[1, 0]
ax.fill_between(df_winter['timestamp_ept'], df_winter['qr_gbt_q05_mw']/1000, df_winter['qr_gbt_q95_mw']/1000,
                alpha=0.25, color='steelblue')
ax.plot(df_winter['timestamp_ept'], df_winter['actual_load_mw']/1000, 'k-', linewidth=0.8)
ax.set_ylabel('Load (GW)')
ax.set_xlabel('Time')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax.grid(True, alpha=0.2)
ax.text(0.98, 0.05, '90% PI Cov. = 66.7%', transform=ax.transAxes, fontsize=7, ha='right',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))

# Summer PI coverage
ax = axes[1, 1]
ax.fill_between(df_summer['timestamp_ept'], df_summer['qr_gbt_q05_mw']/1000, df_summer['qr_gbt_q95_mw']/1000,
                alpha=0.25, color='darkgreen')
ax.plot(df_summer['timestamp_ept'], df_summer['actual_load_mw']/1000, 'k-', linewidth=0.8)
ax.set_ylabel('Load (GW)')
ax.set_xlabel('Time')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:00'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
ax.grid(True, alpha=0.2)
ax.text(0.98, 0.05, '90% PI Cov. = 86.1%', transform=ax.transAxes, fontsize=7, ha='right',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.tight_layout(pad=2)
plt.savefig('figures/figure5_winter_vs_summer.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  Done Figure 5")
print("\nAll figures regenerated successfully.")
