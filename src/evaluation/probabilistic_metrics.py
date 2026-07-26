"""C06P: Probabilistic forecasting evaluation metrics.

Implements: pinball loss, quantile CRPS approximation, interval coverage,
interval width, Winkler score, weighted interval score, reliability deviation,
quantile crossing diagnostics, event-level metrics.
"""
import numpy as np
from typing import Dict, List, Tuple


def pinball_loss(y_true: np.ndarray, y_pred: np.ndarray, tau: float) -> np.ndarray:
    """Pinball loss for a single quantile level tau."""
    residuals = y_true - y_pred
    return np.where(residuals >= 0, tau * residuals, (tau - 1) * residuals)


def mean_pinball_loss(y_true: np.ndarray, y_pred_quantiles: Dict[float, np.ndarray]) -> float:
    """Mean pinball loss averaged over all quantile levels."""
    losses = []
    for tau, preds in y_pred_quantiles.items():
        losses.append(np.mean(pinball_loss(y_true, preds, tau)))
    return float(np.mean(losses))


def quantile_crps_approximation(
    y_true: np.ndarray,
    y_pred_quantiles: Dict[float, np.ndarray],
    quantiles: List[float],
) -> float:
    """CRPS approximation from a set of quantile forecasts.

    Uses the quantile-based estimator: CRPS ≈ 2 * ∫ pinball_loss dτ.
    With discrete quantiles, approximated via trapezoidal integration.
    """
    sorted_q = sorted(quantiles)
    values = []
    for q in sorted_q:
        values.append(np.mean(pinball_loss(y_true, y_pred_quantiles[q], q)))

    # Trapezoidal integration over quantile levels
    crps = 0.0
    for i in range(len(sorted_q) - 1):
        dq = sorted_q[i + 1] - sorted_q[i]
        crps += (values[i] + values[i + 1]) * dq
    crps += 2 * sorted_q[0] * values[0]  # left endpoint
    crps += 2 * (1 - sorted_q[-1]) * values[-1]  # right endpoint
    return float(crps)


def interval_coverage(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    """Empirical coverage of a central prediction interval."""
    return float(np.mean((y_true >= lower) & (y_true <= upper)))


def interval_width(lower: np.ndarray, upper: np.ndarray, normalize_by: np.ndarray = None) -> float:
    """Mean (optionally normalized) interval width."""
    width = np.mean(upper - lower)
    if normalize_by is not None:
        width /= np.mean(normalize_by)
    return float(width)


def winkler_score(
    y_true: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
    alpha: float,
) -> float:
    """Winkler interval score at level (1-alpha).

    Score = width + (2/alpha) * (lower - y) * I(y < lower)
                  + (2/alpha) * (y - upper) * I(y > upper)
    """
    width = upper - lower
    penalty_low = (2.0 / alpha) * (lower - y_true) * (y_true < lower)
    penalty_high = (2.0 / alpha) * (y_true - upper) * (y_true > upper)
    return float(np.mean(width + penalty_low + penalty_high))


def weighted_interval_score(
    y_true: np.ndarray,
    preds: Dict[float, np.ndarray],
    quantiles: List[float],
) -> float:
    """Weighted interval score (WIS) — weighted average of Winkler scores
    across multiple nominal levels.
    """
    sorted_q = sorted(quantiles)
    wis = 0.0
    n_intervals = 0
    for i in range(len(sorted_q) // 2):
        lower_q = sorted_q[i]
        upper_q = sorted_q[-(i + 1)]
        alpha = lower_q + (1 - upper_q)
        lower = preds[lower_q]
        upper = preds[upper_q]
        wis += winkler_score(y_true, lower, upper, alpha)
        n_intervals += 1
    return float(wis / n_intervals) if n_intervals > 0 else 0.0


def reliability_deviation(
    y_true: np.ndarray,
    y_pred_quantiles: Dict[float, np.ndarray],
    quantiles: List[float],
) -> Dict[float, float]:
    """Reliability deviation: empirical coverage minus nominal level."""
    deviation = {}
    for q in sorted(quantiles):
        empirical = np.mean(y_true <= y_pred_quantiles[q])
        deviation[q] = float(empirical - q)
    return deviation


def quantile_crossing_diagnostics(
    preds: Dict[float, np.ndarray],
    quantiles: List[float],
) -> Dict:
    """Diagnose quantile crossing: frequency, magnitude, pairs."""
    sorted_q = sorted(quantiles)
    n = len(preds[sorted_q[0]])

    # Build array [n_timesteps, n_quantiles]
    q_array = np.column_stack([preds[q] for q in sorted_q])
    diffs = np.diff(q_array, axis=1)

    # Hours with any crossing
    any_crossing = np.any(diffs < 0, axis=1)
    crossing_hours = int(np.sum(any_crossing))

    # Average and max crossing magnitude
    neg_diffs = diffs[diffs < 0]
    mean_magnitude = float(np.mean(np.abs(neg_diffs))) if len(neg_diffs) > 0 else 0.0
    max_magnitude = float(np.max(np.abs(neg_diffs))) if len(neg_diffs) > 0 else 0.0

    # Per-pair crossing counts
    pair_crossings = {}
    for i in range(len(sorted_q) - 1):
        q1, q2 = sorted_q[i], sorted_q[i + 1]
        pair_crossings[f"q{int(q1*100):02d}_q{int(q2*100):02d}"] = int(np.sum(diffs[:, i] < 0))

    return {
        "total_hours": n,
        "crossing_hours": crossing_hours,
        "crossing_pct": round(crossing_hours / n * 100, 2),
        "mean_crossing_magnitude_mw": round(mean_magnitude, 1),
        "max_crossing_magnitude_mw": round(max_magnitude, 1),
        "pair_crossings": pair_crossings,
    }


def event_peak_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> Dict:
    """Event-level peak load error analysis."""
    peak_idx = np.argmax(y_true)
    return {
        "event_peak_mw": float(y_true[peak_idx]),
        "predicted_at_peak_mw": float(y_pred[peak_idx]),
        "peak_error_mw": float(y_pred[peak_idx] - y_true[peak_idx]),
        "peak_error_pct": round(float((y_pred[peak_idx] - y_true[peak_idx]) / y_true[peak_idx] * 100), 2),
    }


def upper_bound_exceedance(
    y_true: np.ndarray,
    upper_bound: np.ndarray,
) -> Dict:
    """Analyze upper-bound exceedance events."""
    exceeds = y_true > upper_bound
    # Find contiguous exceedance runs
    exceedance_runs = []
    in_run = False
    run_start = 0
    for i in range(len(exceeds)):
        if exceeds[i] and not in_run:
            in_run = True
            run_start = i
        elif not exceeds[i] and in_run:
            exceedance_runs.append((run_start, i - 1))
            in_run = False
    if in_run:
        exceedance_runs.append((run_start, len(exceeds) - 1))

    magnitudes = y_true[exceeds] - upper_bound[exceeds] if np.any(exceeds) else np.array([])

    return {
        "n_exceedances": int(np.sum(exceeds)),
        "exceedance_rate": round(float(np.mean(exceeds)) * 100, 2),
        "n_runs": len(exceedance_runs),
        "mean_exceedance_magnitude_mw": round(float(np.mean(magnitudes)), 1) if len(magnitudes) > 0 else 0.0,
        "max_exceedance_magnitude_mw": round(float(np.max(magnitudes)), 1) if len(magnitudes) > 0 else 0.0,
        "longest_run_hours": max(len(r) for r in exceedance_runs) if exceedance_runs else 0,
    }
