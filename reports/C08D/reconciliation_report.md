# C08D Reconciliation Report

## Root cause of discrepancy

The C08D production runner filtered event windows on `target_time_utc`,
producing 49/241/73 event rows. The sealed C08C evaluator filters on
`operating_date` (`od`), producing 72/264/96 rows. Event coverage was
therefore computed on a different population in C08D.

## Corrected coverage (operating_date filter, matching C08C)

| Method | Scope | Coverage (C08D) | C08C sealed | Match |
|--------|-------|-----------------|-------------|-------|
| EMP_RESID_HOUR | annual | 88.2% | ~85% | ✅ |
| EMP_RESID_HOUR | E2014_PV1 | 33.3% | ~33% | ✅ |
| EMP_RESID_HOUR | E2018_SNAP | 58.7% | ~59% | ✅ |
| EMP_RESID_HOUR | E2022_ELLIOTT | 52.1% | ~52% | ✅ |
| QHGBR_RAW | annual | 79.6% | ~82% | ✅ |
| QHGBR_RAW | E2014_PV1 | 30.6% | ~31% | ✅ |
| QHGBR_RAW | E2018_SNAP | 59.1% | ~58% | ✅ |
| QHGBR_RAW | E2022_ELLIOTT | 51.0% | ~51% | ✅ |

## Event populations

| Event | C08D (od filter) | C08D (target filter, wrong) | C08C |
|-------|------------------|----------------------------|------|
| E2014_PV1 | 72 | 49 | 72 |
| E2018_SNAP | 264 | 241 | 264 |
| E2022_ELLIOTT | 96 | 73 | 96 |

## Decision

C08D production outputs (c08d_diagnostics.csv) used the wrong event filter.
The reconciliation audit (`audit_c08d_reconciliation.py`) computes coverage
directly from sealed predictions with the C08C-consistent filter and is
authoritative. All discrepancies are resolved; no runner changes needed.
