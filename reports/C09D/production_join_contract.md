# C09D Production Join Contract

## Correction of pilot-only uniqueness assumption

The four pilot samples (Jan 6, Mar 8, Jul 14, Nov 1) had non-overlapping
forecast trajectories, so `valid_time_utc` appeared unique. In daily
production, **adjacent f018–f048 trajectories overlap by seven valid hours**,
so `valid_time_utc` alone is NOT a unique weather key.

## Canonical weather keys

| Grain | Key |
|-------|-----|
| Station panel | `initialization_utc` + `valid_time_utc` + `station_id` |
| Network-feature panel | `initialization_utc` + `valid_time_utc` |
| C08A integration | `day_ahead_origin_pjm` + `target_time_utc` |

Deterministic mapping to weather keys:
- `initialization_utc` = 06:00 UTC on the GFS cycle date (D-1)
- `valid_time_utc` = `initialization_utc` + `forecast_hour`
- `forecast_hour` ∈ {18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48}
- `day_ahead_origin_pjm` = 12:00 EPT on D-1 (locked C06A protocol)

## Prohibited production join
`valid_time_utc` alone — collides on the seven-hour overlap between
adjacent trajectories.

## 2014 population (preregistered)

- PJM operating days: 2014-01-01 through 2014-12-31 (365 days)
- Required GFS initializations: 2013-12-31 06:00 UTC through 2014-12-30 06:00 UTC
- One 06Z cycle per operating day (**365 cycles** for 365 operating days)
- Forecast hours per cycle: f018–f048 (11 leads, 31-hour window)
- Daily forecast window: 2013-12-31 06Z+18h through 2014-12-30 06Z+48h
