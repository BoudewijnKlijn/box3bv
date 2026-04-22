"""Heatmap BV/box 3-ratio over (jaren in BV, koers CAGR)."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

import analytic


def plot(years: np.ndarray, growths: np.ndarray, dividend_yield: float = 0.02) -> None:
    """Plot ratio-matrix met annotaties per cel."""
    T, G = np.meshgrid(years, growths)
    r = analytic.ratio(T, G, dividend_yield)

    fig, ax = plt.subplots(figsize=(9, 6))
    norm = LogNorm(vmin=r.min(), vmax=r.max())
    ax.imshow(r, cmap="viridis", norm=norm, origin="lower", aspect="auto")

    ax.set_xticks(range(len(years)), years)
    ax.set_yticks(range(len(growths)), [f"{g:.2f}" for g in growths])
    ax.set_xlabel("Jaar in BV")
    ax.set_ylabel("Koers CAGR")
    ax.set_title(f"BV / box 3 × 100  (dividend yield = {dividend_yield:.2%})")

    for i in range(len(growths)):
        for j in range(len(years)):
            c = "white" if norm(r[i, j]) < 0.5 else "black"
            ax.text(
                j, i, f"{r[i, j] * 100:.0f}", ha="center", va="center", color=c, fontsize=7
            )
    fig.tight_layout()
    plt.show()


def main() -> None:
    years = np.arange(0, 30, 1)
    growths = np.linspace(0.0, 0.1, 11)
    plot(years, growths, dividend_yield=0.02)


if __name__ == "__main__":
    main()
