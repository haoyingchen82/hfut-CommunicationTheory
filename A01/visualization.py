
"""Plot the autocorrelation and power spectrum for Assignment 01."""

from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from model import (
    autocorrelation_m,
    autocorrelation_z,
    average_power_z,
    power_spectral_density_z,
)


def save_summary_figure(omega0, output_path):
    """Save a three-panel figure: R_m(tau), R_z(tau), and P_z(f)."""

    output_path = Path(output_path)

    # Time-delay axis
    tau = np.linspace(-1.5, 1.5, 2400)

    # Carrier frequency
    f0 = omega0 / (2.0 * pi)

    # Frequency axis
    frequency_limit = max(5.0, abs(f0) + 4.0)
    frequency = np.linspace(-frequency_limit, frequency_limit, 4000)

    # Calculate statistical characteristics
    rm = autocorrelation_m(tau)
    rz = autocorrelation_z(tau, omega0)
    pz = power_spectral_density_z(frequency, omega0)

    # Plot configuration
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(10, 11),
        constrained_layout=True
    )

    # 1. Original autocorrelation function
    axes[0].plot(tau, rm, linewidth=2)

    axes[0].set_title(
        r"Autocorrelation of $m(t)$: $R_m(\tau)$"
    )
    axes[0].set_xlabel(r"$\tau$ (s)")
    axes[0].set_ylabel(r"$R_m(\tau)$")
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(-1.5, 1.5)

    # 2. Modulated autocorrelation function
    axes[1].plot(
        tau,
        rz,
        linewidth=2,
        label=r"$R_z(\tau)$"
    )

    # Upper envelope
    axes[1].plot(
        tau,
        0.5 * rm,
        linestyle="--",
        linewidth=1.2,
        label=r"Envelope $\frac{1}{2}R_m(\tau)$"
    )

    # Lower envelope
    axes[1].plot(
        tau,
        -0.5 * rm,
        linestyle="--",
        linewidth=1.2
    )

    axes[1].axhline(0, linewidth=0.8)

    axes[1].set_title(
        rf"Modulated autocorrelation $R_z(\tau)$ "
        rf"($\omega_0={omega0:.3g}$ rad/s)"
    )

    axes[1].set_xlabel(r"$\tau$ (s)")
    axes[1].set_ylabel(r"$R_z(\tau)$")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(-1.5, 1.5)

    # 3. Power spectral density
    axes[2].plot(
        frequency,
        pz,
        linewidth=2,
        label=r"$P_z(f)$"
    )

    axes[2].axvline(
        f0,
        linestyle="--",
        linewidth=1,
        label=rf"$f_0={f0:.3g}$ Hz"
    )

    axes[2].axvline(
        -f0,
        linestyle="--",
        linewidth=1,
        label=rf"$-f_0={-f0:.3g}$ Hz"
    )

    axes[2].set_title(
        r"Power spectral density $P_z(f)$"
    )

    axes[2].set_xlabel("$f$ (Hz)")
    axes[2].set_ylabel(r"$P_z(f)$")
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    # Overall title
    fig.suptitle(
        rf"Random-process modulation: "
        rf"$\omega_0={omega0:.3g}$ rad/s, "
        rf"average power $S={average_power_z():.2f}$",
        fontsize=14
    )

    # Save figure
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fig.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    return output_path
