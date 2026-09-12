"""Statistical utilities for product experimentation.

The functions are intentionally small and testable so the project can be used to
explain the mechanics of experimentation in interviews rather than hiding them
behind a notebook.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


@dataclass(frozen=True)
class ExperimentResult:
    control_rate: float
    treatment_rate: float
    absolute_lift: float
    relative_lift: float
    z_stat: float
    p_value: float
    ci_low: float
    ci_high: float


def minimum_sample_size(control_rate: float, mde: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Return per-arm sample size for a two-sided proportions test.

    Args:
        control_rate: Baseline conversion probability.
        mde: Minimum detectable *absolute* effect, e.g. 0.01 for +1pp.
    """
    treatment_rate = control_rate + mde
    if not (0 < control_rate < 1 and 0 < treatment_rate < 1):
        raise ValueError("control_rate and control_rate + mde must lie in (0, 1)")
    effect = proportion_effectsize(control_rate, treatment_rate)
    n = NormalIndPower().solve_power(effect_size=effect, alpha=alpha, power=power, ratio=1.0)
    return ceil(n)


def two_proportion_test(control_success: int, control_n: int, treatment_success: int, treatment_n: int, alpha: float = 0.05) -> ExperimentResult:
    """Two-sample z test with a Wald CI for the difference in proportions."""
    if min(control_n, treatment_n) <= 0:
        raise ValueError("sample sizes must be positive")
    p_c = control_success / control_n
    p_t = treatment_success / treatment_n
    diff = p_t - p_c
    pooled = (control_success + treatment_success) / (control_n + treatment_n)
    se_null = np.sqrt(pooled * (1 - pooled) * (1 / control_n + 1 / treatment_n))
    z = diff / se_null if se_null > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    se_diff = np.sqrt(p_c * (1 - p_c) / control_n + p_t * (1 - p_t) / treatment_n)
    critical = stats.norm.ppf(1 - alpha / 2)
    relative = diff / p_c if p_c else np.nan
    return ExperimentResult(p_c, p_t, diff, relative, z, p_value, diff - critical * se_diff, diff + critical * se_diff)


def sample_ratio_mismatch(assignments: pd.Series, expected_treatment_share: float = 0.5) -> tuple[float, float]:
    """Chi-square SRM diagnostic. Returns statistic and p-value."""
    counts = assignments.value_counts()
    n = counts.sum()
    observed = np.array([counts.get("control", 0), counts.get("treatment", 0)], dtype=float)
    expected = np.array([n * (1 - expected_treatment_share), n * expected_treatment_share])
    stat, p_value = stats.chisquare(observed, f_exp=expected)
    return float(stat), float(p_value)


def cuped_adjust(outcome: pd.Series, pre_period_covariate: pd.Series) -> pd.Series:
    """Variance-reduce an outcome using a pre-treatment covariate.

    CUPED coefficient theta = Cov(Y, X) / Var(X). The centered adjustment
    preserves the outcome mean while reducing variance when X predicts Y.
    """
    frame = pd.DataFrame({"y": outcome, "x": pre_period_covariate}).dropna()
    if frame.empty or frame["x"].var(ddof=1) == 0:
        return outcome.astype(float)
    theta = frame["y"].cov(frame["x"]) / frame["x"].var(ddof=1)
    adjusted = outcome.astype(float) - theta * (pre_period_covariate - pre_period_covariate.mean())
    return adjusted


def difference_in_differences(df: pd.DataFrame, outcome: str, group: str, period: str) -> float:
    """Compute the canonical 2x2 Difference-in-Differences estimate.

    group and period must be binary 0/1 indicators.
    """
    means = df.groupby([group, period])[outcome].mean()
    return float((means.loc[(1, 1)] - means.loc[(1, 0)]) - (means.loc[(0, 1)] - means.loc[(0, 0)]))
