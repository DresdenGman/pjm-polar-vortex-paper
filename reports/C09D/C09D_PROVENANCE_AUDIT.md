# C09D Provenance Audit

**Status:** PROVISIONAL (30/31) — audit record, not paper prose
**Date:** 2026-08-08
**Audit type:** Integrity-state provenance for C09D GFS acquisition pipeline

---

## 1. Data Source

- Dataset: NCEI GFS Grid 004 (0.5-degree) — GFSGRB24
- Initialization: 06:00 UTC daily
- Forecast leads: f018..f048 (11 leads, 31-hour window)
- Stations: 4 (Baltimore_Washington_MD, Chicago_OHare_IL, Cincinnati_OH, Philadelphia_PA)
- Download route: WSL2 curl → proxy chain → NCEI HAS

## 2. Two-Node Architecture

```
CONTROL:  Mac (192.168.1.15) — git repo, launchd tunnel, decision plane
WORKER:   Windows (192.168.1.13) + WSL2 Ubuntu 24.04 — downloads, verification, derivation
```

Pipeline per cycle: acquisition → verify → derive → publish

## 3. Source Verification Evolution

| Version | Gates |
|---------|-------|
| V1 | Content-Length exact match |
| V2 | Content-Length + SHA256 |
| V3 (FINAL) | transport (CL + bytes + SHA256) + tar structural + GRIB semantic gate (11 leads × 358 msgs × 5/5 vars) |

**Incident that drove V3:** 01-16 f039 corruption passed V2 gates (CL matched, SHA256 recorded) but was scientifically unusable.

## 4. 2014-01-16 Incident Timeline

1. First observed: 01-16 native partition = 40 rows (expected 44)
2. f039 diagnosis: only 65 readable GRIB2 messages (expected 358)
3. Required variables: 0/5 (sp, 2t, 2r, 10u, 10v all absent)
4. ecCodes/grib_api: "Wrong message length" after message 65
5. Two independent HAS orders: HAS012727456 + HAS012729318
6. Both TARs byte-identical (SHA256 F4C08CEFC1A7C8AAF3E8FB30B41AE84C9661E5C9363D2C0D733030E322A9FBA6)
7. Both f039 byte-identical (SHA256 A1148F9BA526638AA21EF64777C21BE81BC22F31C1CAAE4FABEB25F96205C4DD)
8. **Conclusion: upstream archival corruption** (not local transfer — byte-identical across independent orders)
9. NCEI own corrupt/ directory lists 2014-01-16 12Z bad files (same-day corroboration)

## 5. Recovery / Escalation

- NCEI: emailed ncei.orders@noaa.gov 2026-08-07 (full hash evidence + recovery request)
- NCAR: DATAHELP-6009 OPEN (emailed rdahelp@ucar.edu → consolidated to datahelp@ucar.edu)
- Quarantine policy: invalid source moved to `quarantine/source_corrupt_20140116/` (never deleted)
- Evidence package: `quarantine/source_corrupt_20140116/evidence/` (README_CORRUPTION.txt, pygrib diag, hashes)

## 6. Current State

- SOURCE_VERIFIED = 30/31
- Target GRIBs PASS (healthy cycles) = 330/330
- 30C provisional seal: `C09D_30C_PROVISIONAL_SEAL.json`
- 01-16 excluded from all provisional derivatives
- Canonical masters untouched

## 7. Exact Invariants

| Grain | Rows per cycle | 31-cycle final target |
|-------|---------------|----------------------|
| Native (station × lead) | 44 | 1364 |
| Hourly (interpolated 18..48) | 124 | 3844 |
| Trajectory (31 consecutive hours) | 31 | 961 |

## 8. Reproducibility / Hashes

See `C09D_PROVENANCE_MANIFEST.json` for full hash table:
- Seal hashes (30C provisional files)
- Source archive hashes (30 verified + 1 quarantined)
- Code revision: run_c09d_january_batch.py (V3 semantic gate patched)

---

## Integrity-State Taxonomy (Gate Definitions)

| State | Definition |
|-------|-----------|
| TRANSPORT_COMPLETE | Content-Length exact + local bytes exact + SHA256 recorded |
| SOURCE_VERIFIED | TRANSPORT_COMPLETE + TAR structural PASS + GRIB semantic PASS |
| DERIVED_VALID | Partition contract OK (44/124/31 rows, no dup, no NaN) |
| PROVISIONAL_SEALED | 30/31 cycles, explicitly NOT for final analysis |
| FINAL_SEALED | 31/31, canonical masters rebuilt, C09D FINAL — NOT YET ACHIEVED |
