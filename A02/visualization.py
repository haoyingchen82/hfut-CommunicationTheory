"""Plot the candidate DSB bands on the two-path channel response."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from model import (
    normalized_magnitude,
    null_frequencies,
    occupied_band,
    select_carrier,
    worst_case_magnitude,
)


def save_summary_figure(delay_seconds, bandwidth_hz, carriers_hz, output_path):
    """Save aligned response plots for the candidate carrier frequencies."""
    output_path = Path(output_path)
    best_carrier = select_carrier(carriers_hz, bandwidth_hz, delay_seconds)

    padding_hz = bandwidth_hz * 0.2
    low_hz = max(0.0, min(carriers_hz) - bandwidth_hz / 2.0 - padding_hz)
    high_hz = max(carriers_hz) + bandwidth_hz / 2.0 + padding_hz
    nulls_hz = null_frequencies(low_hz, high_hz, delay_seconds)
    frequency_hz = np.sort(
        np.concatenate(
            [
                np.linspace(low_hz, high_hz, 1600),
                nulls_hz,
            ]
        )
    )
    response = normalized_magnitude(frequency_hz, delay_seconds)

    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10}):
        fig, axes = plt.subplots(
            len(carriers_hz),
            1,
            sharex=True,
            sharey=True,
            squeeze=False,
            figsize=(10, 2 + 2.25 * len(carriers_hz)),
            layout="constrained",
        )

        fig.suptitle(
            "Carrier selection in a two-path channel\n"
            f"{bandwidth_hz:g} Hz DSB bandwidth   |   "
            f"{1000 * delay_seconds:g} ms delay difference",
            fontsize=15,
            fontweight="bold",
        )
        fig.supxlabel(
            "Frequency (kHz)\n"
            "Shaded regions show the occupied bands. Dashed guides mark channel nulls.",
            fontsize=10,
        )
        fig.supylabel(r"Normalized channel magnitude $|H(f)|/2$", fontsize=11)

        for ax, carrier_hz in zip(axes[:, 0], carriers_hz):
            left_hz, right_hz = occupied_band(carrier_hz, bandwidth_hz)
            minimum = worst_case_magnitude(carrier_hz, bandwidth_hz, delay_seconds)
            selected = carrier_hz == best_carrier
            color = "#00765e" if selected else "#a14a19"

            ax.axvspan(left_hz / 1000, right_hz / 1000, color=color, alpha=0.09)
            for null_hz in nulls_hz:
                ax.axvline(
                    null_hz / 1000, color="#697480", linestyle="--", linewidth=0.8
                )
            ax.plot(frequency_hz / 1000, response, color="#697480", linewidth=1.25)

            band_nulls_hz = null_frequencies(left_hz, right_hz, delay_seconds)
            band_hz = np.sort(
                np.concatenate(
                    [
                        np.linspace(left_hz, right_hz, 500),
                        band_nulls_hz,
                        [carrier_hz],
                    ]
                )
            )
            ax.plot(
                band_hz / 1000,
                normalized_magnitude(band_hz, delay_seconds),
                color=color,
                linewidth=2.3,
            )

            # The band minimum occurs at an internal null or at a band edge.
            minimum_hz = band_nulls_hz
            if not minimum_hz.size:
                edges_hz = np.array([left_hz, right_hz])
                edge_magnitudes = normalized_magnitude(edges_hz, delay_seconds)
                minimum_hz = edges_hz[np.isclose(edge_magnitudes, minimum, atol=1e-12)]
            ax.scatter(
                minimum_hz / 1000,
                np.full(minimum_hz.shape, minimum),
                color=color,
                edgecolors="white",
                linewidths=0.8,
                s=38,
                zorder=5,
                clip_on=False,
            )

            carrier_title = f"{carrier_hz / 1000:g} kHz carrier"
            if selected:
                carrier_title += " (selected)"
            ax.set_title(carrier_title, loc="left", color=color, fontweight="bold")
            ax.set_title(
                f"{left_hz / 1000:.2f}-{right_hz / 1000:.2f} kHz band   |   "
                f"Min. magnitude {minimum:.3f}",
                loc="right",
                color="#273343",
                fontsize=10,
            )
            ax.set_ylim(-0.055, 1.10)
            ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
            ax.grid(axis="y", color="#dae0e6", linewidth=0.7)
            ax.set_axisbelow(True)
            ax.spines[["top", "right"]].set_visible(False)
            ax.spines[["left", "bottom"]].set_color("#acb6bf")

        axes[-1, 0].set_xlim(low_hz / 1000, high_hz / 1000)
        axes[-1, 0].xaxis.set_major_locator(MaxNLocator(nbins=9))

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output_path, dpi=180, bbox_inches="tight", facecolor="white")
        finally:
            plt.close(fig)

    return output_path
