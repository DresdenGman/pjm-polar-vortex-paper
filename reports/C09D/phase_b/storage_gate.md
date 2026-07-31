# C09D Phase B Storage Gate

**Status: C09D_BLOCKED_STORAGE**

## Filesystem inventory (2026-07-30)

| Mount | Size | Available | Capacity | Role |
|-------|------|-----------|----------|------|
| /dev/disk3s5 (Data) | 228 GiB | 5.6 GiB | 98% | main data volume (raw archives here) |
| /dev/disk3s1s1 (/) | 228 GiB | 5.6 GiB | 66% | system |
| /Volumes/Recovery | 228 GiB | 5.6 GiB | 26% | recovery, not usable |
| 闲鱼.app/Wrapper | — | 19 GiB | 91% | sandbox container, not a real volume |

No external volume (USB/SSD), no /media, no /mnt mount exists.

## Gate requirements vs reality

| Requirement | Needed | Available | Pass? |
|-------------|--------|-----------|-------|
| Raw archive location free | ≥ 15 GiB | 5.6 GiB | ❌ |
| Local worktree free per batch | ≥ 3 GiB | ~4 GiB (after cleanup) | ⚠️ |
| Raw/processed separation | uncontrolled tmp | — | ❌ |

## January 2014 volume estimate

31 initializations × ~3.2 GiB per GFS tar = **~99 GiB raw**.
Plus extraction working space. Far beyond current 5.6 GiB free.

## Options requiring Commander/user decision

1. **External drive** — user attaches USB/SSD with ≥ 150 GiB free.
2. **Partial gate** — relax to fewer sample days (e.g. 4 audited dates only,
   already done in C09B) — but that does not prove daily acquisition.
3. **Cloud staging** — download to a cloud VM, extract station values
   there, transfer only small processed outputs back.

No acquisition will begin until a gate passes.
