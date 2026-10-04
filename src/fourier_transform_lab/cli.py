"""Command line entry point for the demo figure."""

from __future__ import annotations

import argparse
from pathlib import Path

from .demo import generate_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Fourier transform demo figure.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/figures/demo_spectrum.png"),
        help="Path for the generated figure.",
    )
    args = parser.parse_args()
    path = generate_demo(args.output)
    print(path)


if __name__ == "__main__":
    main()
