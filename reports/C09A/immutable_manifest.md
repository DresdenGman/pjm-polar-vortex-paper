# C09A — GFS Sample Request Status & Immutable Manifest

## NCEI Request Status
- **Sender:** User (manual send required)
- **Email draft:** `reports/C09A/ncei_order_email_draft.md`
- **Recipient:** ncei.orders@noaa.gov
- **Status:** ⏳ DRAFT — not yet sent
- **Requested dates:**
  - 2014-03-08 06Z → target 2014-03-09
  - 2014-07-14 06Z → target 2014-07-15
  - 2014-11-01 06Z → target 2014-11-02

## Reference Sample (Existing)
- `gfs_4_2014010606.g2.tar` (3.2 GB)
- SHA256: `bb269d71f2cbc96ae01fce91063e33416234ea3676becd14566ee17af59de411`
- Source: NCEI AIRS (HAS012726061)
- Status: ✅ Downloaded, extracted, variables verified

## C09A Pass/Fail Criteria
Each sample must pass: archive integrity → initialization identity → forecast-hour completeness → variable identity → grid homogeneity → decoder parity → DST mapping. All four must match.
