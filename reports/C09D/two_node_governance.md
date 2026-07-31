# Command 039A — Mac–Windows Two-Node Compute Governance

**Status: ACTIVE (approved by Commander 2026-07-31)**

## 1. Node roles

| Node | Role |
|------|------|
| mac-control-01 | Canonical git repo, experiment preregistration, run plans, code review, artifact validation, cross-node aggregation, releases/tags, paper.tex custody |
| win-wsl-worker-01 | NCEI acquisition, rolling GFS archive, GRIB processing, assigned CPU training folds, authorized GPU training, worker-side validation, immutable result packaging |

**Global rule:** One active production campaign at a time. A campaign may use both
machines concurrently. Windows is a managed execution node operating from
Mac-issued immutable run plans — NOT an independent research branch.
`paper.tex` remains frozen and must not appear in any Windows production change set.

## 2. Storage accounting

WSL ext4 and C:\C09D share the same physical Windows drive.
**Physical Windows free space is authoritative** (currently ~431 GB).

| Free space | State | Action |
|-----------|-------|--------|
| >= 300 GB | HEALTHY | normal |
| 200-299 GB | CAUTION | one bounded batch only |
| 150-199 GB | NO NEW DOWNLOADS | finish/clean current transaction |
| < 150 GB | HARD STOP | no acquisition/training starts |

Minimum safety reserve: 150 GB. Working capacity ≈ 290 GB.

## 3. Storage layout

**NTFS (C:\):**
- `C:\C09D\raw\{incoming,verified,monthly}` — compressed GFS archives
- `C:\C09D\transfer` — transfer bundles
- `C:\PJM\artifact-outbox|artifact-archive|environment-exports`

**WSL ext4 (/srv/pjm/, /srv/c09d/):**
- `repo/` git checkouts, `environments/` python envs, `run-plans/`, `runs/<run_id>/`,
  `transactions/`, `datasets/`, `logs/`, `quarantine/`, `transfer/`
- Active GRIB extraction, prepared matrices, training, partitions

Large raw GFS archives must remain on NTFS.

## 4. C09D rolling-archive policy

Windows is a **rolling** archive, not permanent full-history:
download month → verify hashes → process every cycle → validate panels →
package products → transfer to Mac → independently verify hash on Mac →
record raw-source manifest → **explicit monthly deletion authorization** →
reclaim → next month.

Deletion requires: complete URL/metadata ledger, SHA-256 per archive, verified
lead count, accepted row counts, accepted key/missingness checks, package
copied to Mac, hash verified on Mac, explicit authorization.

Full simultaneous retention of all 2014 raw archives is NOT authorized.

## 5. Repository governance

Mac maintains canonical repository and creates production branches.
Windows may: `git fetch`, `git checkout` (read-only on canonical), run from
Mac-issued run plans. All artifacts returned to Mac for validation and commit.
