# C09A — GFS Source Audit Summary

## Existing Sample (2014-01-07)
- ✅ File: `gfs_4_2014010606.g2.tar` (3.2GB)
- ✅ SHA256: bb269d71f2cbc96ae01fce91063e33416234ea3676becd14566ee17af59de411
- ✅ Cycle: 2014-01-06 06Z, f000-f192
- ✅ Variables: t2m, r2, u10, v10 (verified via cfgrib + pygrib)
- ✅ 0.5° grid covers PJM (35-44°N)

## Route A: NCEI DSI 6182 (2010-2014, 0.5°)
- ✅ Primary source established
- ✅ AIRS workflow: proven (HAS012726061)
- ❌ Missing 3 sample dates: Mar 9, Jul 15, Nov 2
- ⏳ Email draft saved, needs manual send

## Route B: AWS (noaa-gfs-bdp-pds)
- ❌ Rolling 30-day window only — not suitable for historical archive

## Route C: NCAR GDEX d084001 (2015-2022, 0.25°)
- ⚠️ 0.25° resolution (1057×2103 grid) — NOT 0.5° like DSI 6182
- ⚠️ Requires free registration/login to download
- ⚠️ Dataset being discontinued (stopping updates early 2026)
- ⚠️ Mixing 0.5° (2010-2014, DSI 6182) with 0.25° (2015-2022, GDEX) creates homogeneity risk
- ❌ Would need version adapter, resolution harmonization, and variable crosswalk

## Recommendation
- Stick with NCEI DSI 6182 as the single unified source
- Order full 2010-2014 via AIRS (tape order)
- For 2015-2022: DSI 6182 may also work (same product), but delivery method unknown for recent years
- NCAR GDEX as fallback only if DSI 6182 fails for 2015-2022
