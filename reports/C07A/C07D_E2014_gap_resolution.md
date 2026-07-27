# C07D — E2014_PV1 Gap Resolution

## Summary
- Event window: 2014-01-06 to 2014-01-08 (72 hours)
- PJM comparator available: 63 hours
- Missing: 9 hours (3 per operating day)

## Missing Hours
All 9 missing hours are 02:00-04:00 UTC each day.
These correspond to the final 3 hours of each EPT calendar day.

## Cause
All 9 hours ARE present in the raw PJM forecast history, but belong
to evaluation vintages with eval_date = operating_date (not operating_date - 1).
Under the strict one-vintage-per-day protocol, these vintages are excluded
because their eval_date > forecast_origin (12:00 EPT on D-1).

Vintage structure for 2014:
- Each 24h forecast block covers 02:00 UTC D to 01:00 UTC D+1
- EPT operating day D covers 05:00 UTC D to 04:59 UTC D+1
- Hours 02:00-04:59 UTC D+1 belong to EPT day D but forecast vintage D+1

Classification: SOURCE_DATA_STRUCTURE_LIMITATION
The data exists but the 2014 forecast day convention (02:00 boundary)
differs from the EPT calendar day convention (05:00 boundary).

## Verification
- All 9 hours confirmed present in raw data (eval_date = op_date)
- Missing due to protocol exclusion, NOT source absence
- No code error — the selector correctly applies one-vintage-per-day

## Impact
63/72 paired hours for E2014_PV1.
Any PJM benchmark for this event must use 63 paired hours only.
The event-peak hour (2014-01-07 12:00 EPT = 17:00 UTC) IS paired.
