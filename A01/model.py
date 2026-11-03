
"""Analytical model for Assignment 01."""

from math import pi

import numpy as np


def autocorrelation_m(tau):
    """Return R_m(tau) = max(1 - |tau|, 0)."""
    return np.maximum(1.0 - np.abs(tau), 0.0)


def autocorrelation_z(tau, omega0):
    """Return the autocorrelation of z(t)."""
    return 0.5 * autocorrelation_m(tau) * np.cos(omega0 * tau)


def power_spectral_density_z(f, omega0):
    """Return P_z(f), where f is measured in Hz.

    NumPy's sinc uses the normalized definition:
    sinc(x) = sin(pi*x)/(pi*x).
    """
    f0 = omega0 / (2.0 * pi)

    return 0.25 * (
        np.sinc(f - f0) ** 2
        + np.sinc(f + f0) ** 2
    )


def average_power_z():
    """Return the average power E[z^2(t)] = R_z(0)."""
    return 0.5
