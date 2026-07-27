# C07D — PJM Benchmark Evaluation Policy

**Locked:** 2026-07-26
**Branch:** C07-multievent-pjm

## Complete Events (E2015 anchor, E2018, E2022)
- Calculate metrics over complete registered event window
- All comparator hours available and verified

## 2014 Event (E2014_PV1)
- 63/72 comparator hours available
- 9-hour loss: 3 hours/day at 02:00-04:00 UTC
- Cause: 2014 PJM forecast day convention (02:00 boundary) vs EPT calendar (05:00 boundary)
- Classification: SOURCE_DATA_STRUCTURE_LIMITATION
- Data exists in raw PJM history but excluded by one-vintage-per-day protocol
- Event-peak hour (2014-01-07 17:00 UTC) IS paired ✅

### Rules for 2014 event benchmarking:
1. Report 63/72 prominently
2. Calculate PJM metrics only over 63 paired hours
3. Never label the 2014 PJM event benchmark "complete"
4. List 9 excluded timestamps
5. Report actual event peak even if comparator unavailable
6. State whether event-peak hour is paired

## Cross-Model Comparisons
- Use exact common paired timestamps
- Report model metrics (72h) and model-vs-PJM (63h) separately
- Do not mix denominators

## Annual Results
- 2014: 7623/8760 paired (87%)
- 2015-2022: 69958/70008 paired (99.97%)
- Do not calculate single 2010-2022 PJM error without yearly coverage disclosure
