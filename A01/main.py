
"""Command-line entry point for Assignment 01."""

import argparse
from math import pi
from pathlib import Path

from model import average_power_z
from visualization import save_summary_figure


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Visualize the autocorrelation and PSD "
            "of the modulated process."
        )
    )

    parser.add_argument(
        "--omega0",
        type=float,
        default=2.0 * pi,
        help="Carrier angular frequency in rad/s (default: 2*pi).",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=(
            Path(__file__).resolve().parent
            / "outputs"
            / "a01_visualization.png"
        ),
        help="Path of the generated figure.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    output_path = save_summary_figure(
        args.omega0,
        args.output
    )

    print(f"omega0       : {args.omega0:.6g} rad/s")
    print(f"carrier f0   : {args.omega0 / (2.0 * pi):.6g} Hz")
    print(f"average power: {average_power_z():.6g}")
    print(f"figure saved : {output_path}")


if __name__ == "__main__":
    main()
