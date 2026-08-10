# C09D Full-Year Acquisition Plan

**Status:** DESIGN PREFLIGHT (Command 050) — no orders submitted
**Date:** 2026-08-08

## Scope (050-A)

- Operating days: 2014-01-01 → 2014-12-31 (365)
- GFS initializations: 2013-12-31 06Z → 2014-12-30 06Z (365 cycles)
- January: 31 cycles (30 SOURCE_VERIFIED, 1 INVALID [2014-01-16 06Z f039])
- **NOT YET ACQUIRED: 334 cycles** (2014-01-31 06Z → 2014-12-30 06Z)
- This phase: NO orders, NO production fitting, NO canonical full-year master

## Source Retention Policy (050-B)

**ORIGINAL VERIFIED SOURCE = RETAINED** (never verify→derive→delete)
- Retained at least until C09D_2014_FINAL_SEAL + C10/C11 primary artifacts frozen
- Deletion/archival only by Commander decision afterwards
- Rationale: 01-16 incident proved historical archives may not be re-acquirable

## Storage Architecture — Capacity Gate

| Item | Value |
|------|-------|
| January 30 archives total | 94,365,286,400 B (94.4 GB) |
| January mean | 3,145,509,546 B |
| January p95 | 3,428,628,480 B |
| Remaining 334 mean projection | 1,050,600,188,586 B (1.05 TB) |
| Remaining 334 p95 conservative | 1,145,161,912,320 B (1.15 TB) |
| 365-cycle conservative total | 1,251,449,395,200 B (1.25 TB) |
| Windows C: free | 349,533,265,920 B (349 GB) |
| Windows C: total | 1,022,237,866,496 B (1.02 TB) |
| Second disk / NAS / SMB | NONE detected |

**Mode A (Local Retention)** — NOT FEASIBLE (free 349 GB < 1.15 TB conservative + 15% + 100 GB reserve)

**Mode B (Verified Cold Migration)** — requires cold storage. Candidates:
1. **UGREEN NAS (1 TB, 闲鱼)** — user-owned, network-accessible; attach via SMB
2. External USB drive (if available)
3. NOT FEASIBLE on current C: only

**RECOMMENDED RETENTION MODE: BLOCKED_NO_CAPACITY until cold storage attached** (or Commander decides otherwise)

## Batch Strategy (050-C)

NCEI request cap 250 GB/order; OUR INTERNAL HARD CAP = **120 GB/order**; MAX_OUTSTANDING_ORDERS = 1.

| Batch | Month | Init range | Cycles | Est bytes (p95) |
|-------|-------|-----------|--------|-----------------|
| FY02 | Feb | 2014-01-31 → 2014-02-27 | 28 | ~96.0 GB |
| FY03 | Mar | 2014-02-28 → 2014-03-30 | 31 | ~106.3 GB |
| FY04 | Apr | 2014-03-31 → 2014-04-29 | 30 | ~102.9 GB |
| FY05 | May | 2014-04-30 → 2014-05-30 | 31 | ~106.3 GB |
| FY06 | Jun | 2014-05-31 → 2014-06-29 | 30 | ~102.9 GB |
| FY07 | Jul | 2014-06-30 → 2014-07-30 | 31 | ~106.3 GB |
| FY08 | Aug | 2014-07-31 → 2014-08-30 | 31 | ~106.3 GB |
| FY09 | Sep | 2014-08-31 → 2014-09-29 | 30 | ~102.9 GB |
| FY10 | Oct | 2014-09-30 → 2014-10-30 | 31 | ~106.3 GB |
| FY11 | Nov | 2014-10-31 → 2014-11-29 | 30 | ~102.9 GB |
| FY12 | Dec | 2014-11-30 → 2014-12-30 | 31 | ~106.3 GB |

All batches ≤ 120 GB → no splits required.

## Order Lifecycle (050-D)

SUBMIT → WAIT READY → DOWNLOAD ALL → SOURCE AUDIT ALL → DERIVE ALL → BATCH SEAL → NEXT ORDER

State machine: PLANNED → ORDER_SUBMITTED → ORDER_READY → DOWNLOADING → TRANSPORT_COMPLETE → SOURCE_AUDITING → SOURCE_VERIFIED → DERIVING → BATCH_QA → BATCH_SEALED

## Per-Cycle Contract (050-E)

1. download → .part
2. exact Content-Length
3. SHA256
4. tar structural test
5. target GRIB semantic gate (leads 18,21,24,27,30,33,36,39,42,45,48; vars sp,2t,2r,10u,10v)
6. native 44-row derivation
7. archive retention/migration
8. manifest publication

## Semantic Gate v4 (050-F)

- **Tier 1 (HARD):** member exists, strict parse to clean EOF, 0 parser errors, 5/5 required vars → else SOURCE_INVALID → quarantine
- **Tier 2 (signature):** count != locked signature BUT parse PASS + 5/5 vars → **SCHEMA_DRIFT_CANDIDATE** (NOT corrupt — GFS evolves); STOP cycle, check ±3 cycles, Commander defines new epoch
- Signature epochs: `reports/C09D/grib_signature_epochs.json` (epoch_001: 2013-12-31T06:00:00Z, 358 msgs, LOCKED_FROM_JANUARY_AUDIT)

## Native Partition Contract (050-G)

44 rows, 4 stations, 11 leads, key (init_date, forecast_hour, station_id), dup=0, NaN=0, 11 rows/station, 4 rows/lead. NO existence-only resume.

## Batch Seal (050-H)

`reports/C09D/batches/FYXX_BATCH_SEAL.json`: batch_id, month, init range, expected/source_verified/source_invalid/schema_drift cycles, archive bytes, SHA256 manifest hash, native rows/dup/nan, code_commit, semantic_gate_version, status. BATCH_SEALED only if: verified==expected, invalid==0, drift==0, native==N×44.

## Manifest Schema (050-J)

`C09D_FULL_YEAR_BATCH_MANIFEST.csv` fields: initialization_utc, operating_day, batch_id, archive_filename, archive_bytes, archive_sha256, transport_pass, tar_structural_pass, semantic_status, signature_epoch, target_gribs_pass, native_rows, storage_location, cold_copy_sha256, cold_copy_verified, status, notes.

Status vocabulary: PLANNED, ORDERED, TRANSPORT_COMPLETE, SOURCE_VERIFIED, SCHEMA_DRIFT_CANDIDATE, SOURCE_INVALID_QUARANTINED, DERIVED_VALID, BATCH_SEALED

## Crash Safety (050-K)

.part resumable; verified never overwritten; manifest tmp→fsync→atomic replace; partition candidate→validate→atomic publish; batch seal last object. FILESYSTEM + VALIDATION = source of truth; checkpoint never authorizes skip.
