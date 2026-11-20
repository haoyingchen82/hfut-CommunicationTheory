"""Command-line entry point for Assignment 02."""

import argparse
from pathlib import Path

from model import occupied_band, select_carrier, worst_case_magnitude
from visualization import save_summary_figure

DELAY_SECONDS = 0.001
BANDWIDTH_HZ = 800.0
CARRIERS_HZ = (1500.0, 2000.0, 2500.0)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare DSB carrier choices in a two-path channel."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs" / "a02_visualization.png",
        help="Path of the generated figure.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = save_summary_figure(
        DELAY_SECONDS, BANDWIDTH_HZ, CARRIERS_HZ, args.output
    )

    print(f"Path delay difference   {DELAY_SECONDS * 1000:g} ms")
    print(f"Total DSB bandwidth     {BANDWIDTH_HZ:g} Hz")
    print()
    print("Carrier (kHz)   DSB band (kHz)   Minimum normalized magnitude")
    for carrier_hz in CARRIERS_HZ:
        low_hz, high_hz = occupied_band(carrier_hz, BANDWIDTH_HZ)
        minimum = worst_case_magnitude(carrier_hz, BANDWIDTH_HZ, DELAY_SECONDS)
        print(
            f"{carrier_hz / 1000:>13.1f}   "
            f"{low_hz / 1000:.1f} to {high_hz / 1000:<8.1f}   {minimum:.6f}"
        )

    selected_hz = select_carrier(CARRIERS_HZ, BANDWIDTH_HZ, DELAY_SECONDS)
    print(f"\nSelected carrier        {selected_hz / 1000:.1f} kHz")
    print(f"Figure saved            {output_path}")


if __name__ == "__main__":
    main()
