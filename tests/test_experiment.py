import numpy as np
import pandas as pd

from src.experiment import cuped_adjust, difference_in_differences, minimum_sample_size, two_proportion_test


def test_minimum_sample_size_positive():
    assert minimum_sample_size(0.10, 0.01) > 0


def test_two_proportion_direction():
    result = two_proportion_test(100, 1000, 130, 1000)
    assert result.absolute_lift > 0
    assert result.treatment_rate == 0.13


def test_cuped_preserves_mean_approximately():
    rng = np.random.default_rng(7)
    x = pd.Series(rng.normal(size=1000))
    y = pd.Series(2 * x + rng.normal(scale=0.5, size=1000))
    adjusted = cuped_adjust(y, x)
    assert abs(adjusted.mean() - y.mean()) < 1e-10
    assert adjusted.var() < y.var()


def test_did():
    df = pd.DataFrame({
        "group": [0, 0, 1, 1],
        "period": [0, 1, 0, 1],
        "y": [10.0, 11.0, 10.0, 14.0],
    })
    assert difference_in_differences(df, "y", "group", "period") == 3.0
