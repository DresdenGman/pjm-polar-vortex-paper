# C05B — Environment Provenance

**Status**: The original C04S execution environment was NOT preserved (no requirements.txt, environment.yml, or container image was archived).

This is the **recovery environment**, NOT necessarily the original environment. Any reproduction discrepancies that can reasonably be attributed to package-version differences are expected and should be documented rather than treated as errors.

## Recovery Environment

- Python: 3.11.15
- Platform: macOS 15.3, arm64 (Apple Silicon)
- venv: ~/Documents/Essays/venv/
- 89 installed packages (see recovery_environment_freeze.txt)

## Key Packages (recovered venv)

| Package | Version |
|---------|---------|
| scikit-learn | 1.7.2 |
| numpy | 2.2.6 |
| pandas | 2.2.3 |
| scipy | 1.15.2 |
| matplotlib | 3.10.3 |
| lightgbm | 4.6.0 |

## Known Version-Sensitive Differences

### scikit-learn HistGradientBoostingRegressor
Version 1.7.2 was released after the C04S experiments were conducted. The C04S version is unknown. Known behavioral changes between 1.x releases include:
- Default `max_bins` changed in 1.4+
- `scoring` parameter semantics adjusted in 1.3+

### lightgbm
Present in environment but NOT used in C04S models (paper.tex uses sklearn HistGradientBoostingRegressor only).

## Reproduction Caveats

Any differences between recovered and original predictions that fall within floating-point tolerance should be attributed to:
1. Unknown sklearn version mismatch
2. Potential missing random_state settings
3. Platform-dependent numerical differences (BLAS/LAPACK backend)

Exact bit-for-bit reproduction cannot be expected in this recovery environment.
