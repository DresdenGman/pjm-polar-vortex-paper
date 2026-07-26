"""C06P: Moving-block bootstrap for serially dependent forecast evaluation.

Provides confidence intervals for point and probabilistic metrics
under temporal dependence. Uses fixed sensitivity block lengths:
24h, 48h, 72h — no selection based on which yields significance.
"""
import numpy as np
from typing import Callable, Dict, List


def block_bootstrap_ci(
    data: np.ndarray,
    statistic: Callable[[np.ndarray], float],
    block_lengths: List[int] = None,
    n_bootstrap: int = 1000,
    alpha: float = 0.05,
    seed: int = 42,
) -> Dict[int, Dict]:
    """Compute moving-block bootstrap confidence intervals.

    Args:
        data: 1D array of hourly values (e.g., errors, losses).
        statistic: Function mapping array → scalar.
        block_lengths: List of block sizes in hours. Default: [24, 48, 72].
        n_bootstrap: Number of bootstrap replicates.
        alpha: Significance level (default 0.05 for 95% CI).
        seed: Random seed for reproducibility.

    Returns:
        Dict mapping block_length → {lower, upper, mean, std, ci_width}.
    """
    if block_lengths is None:
        block_lengths = [24, 48, 72]

    rng = np.random.default_rng(seed)
    n = len(data)
    results = {}

    for L in block_lengths:
        if L > n:
            results[L] = {"error": f"Block length {L} exceeds data length {n}"}
            continue

        n_blocks = n // L
        replicates = np.zeros(n_bootstrap)

        for b in range(n_bootstrap):
            # Sample blocks with replacement
            block_indices = rng.integers(0, n - L + 1, size=n_blocks)
            bootstrap_sample = np.concatenate([data[i:i + L] for i in block_indices])
            replicates[b] = statistic(bootstrap_sample[:n])  # truncate to original length

        lower = np.percentile(replicates, alpha / 2 * 100)
        upper = np.percentile(replicates, (1 - alpha / 2) * 100)

        results[L] = {
            "lower": float(lower),
            "upper": float(upper),
            "mean": float(np.mean(replicates)),
            "std": float(np.std(replicates, ddof=1)),
            "ci_width": float(upper - lower),
        }

    return results


def block_bootstrap_compare(
    data_a: np.ndarray,
    data_b: np.ndarray,
    statistic: Callable[[np.ndarray], float],
    block_length: int = 48,
    n_bootstrap: int = 1000,
    seed: int = 42,
) -> Dict:
    """Bootstrap comparison test for two dependent samples.

    Tests H0: statistic(data_a) == statistic(data_b).

    Returns proportion of bootstrap replicates where diff <= 0.
    """
    rng = np.random.default_rng(seed)
    n = min(len(data_a), len(data_b))
    n_blocks = n // block_length

    diffs = np.zeros(n_bootstrap)
    for b in range(n_bootstrap):
        indices = rng.integers(0, n - block_length + 1, size=n_blocks)
        sample_a = np.concatenate([data_a[i:i + block_length] for i in indices])[:n]
        sample_b = np.concatenate([data_b[i:i + block_length] for i in indices])[:n]
        diffs[b] = statistic(sample_a) - statistic(sample_b)

    return {
        "mean_diff": float(np.mean(diffs)),
        "std_diff": float(np.std(diffs, ddof=1)),
        "ci_lower": float(np.percentile(diffs, 2.5)),
        "ci_upper": float(np.percentile(diffs, 97.5)),
        "p_value_approx": float(np.mean(diffs <= 0)),
        "block_length_hours": block_length,
        "n_bootstrap": n_bootstrap,
    }
