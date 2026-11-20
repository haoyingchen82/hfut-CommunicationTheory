"""Analytical model for the two-path channel in Assignment 02."""

from math import ceil, floor

import numpy as np


def normalized_magnitude(frequency_hz, delay_seconds):
    """Return |H(f)| / 2 for two equal-gain, same-polarity paths."""
    phase_cycles = np.asarray(frequency_hz) * delay_seconds
    return np.abs(np.cos(np.pi * phase_cycles))


def occupied_band(carrier_hz, bandwidth_hz):
    """Return the positive-frequency DSB band edges in Hz."""
    half_bandwidth = bandwidth_hz / 2.0
    return carrier_hz - half_bandwidth, carrier_hz + half_bandwidth


def null_frequencies(low_hz, high_hz, delay_seconds):
    """Return all channel nulls in the closed frequency interval."""
    first = ceil(low_hz * delay_seconds - 0.5)
    last = floor(high_hz * delay_seconds - 0.5)
    return (np.arange(first, last + 1) + 0.5) / delay_seconds


def worst_case_magnitude(carrier_hz, bandwidth_hz, delay_seconds):
    """Return the minimum normalized channel magnitude over the DSB band."""
    low_hz, high_hz = occupied_band(carrier_hz, bandwidth_hz)
    if null_frequencies(low_hz, high_hz, delay_seconds).size:
        return 0.0

    # Between consecutive nulls, the only interior extremum is a maximum.
    return float(normalized_magnitude([low_hz, high_hz], delay_seconds).min())


def select_carrier(carriers_hz, bandwidth_hz, delay_seconds):
    """Select the carrier with the largest minimum magnitude in its band."""
    return max(
        carriers_hz,
        key=lambda carrier: worst_case_magnitude(carrier, bandwidth_hz, delay_seconds),
    )
