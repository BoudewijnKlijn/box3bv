"""Staatsopbrengst en Pareto-kaart BV vs box 3 (analytisch, vaste groei)."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, LogNorm

import analytic


def _annotate(ax, values, fmt, norm=None):
    rows, cols = values.shape
    for i in range(rows):
        for j in range(cols):
            v = values[i, j]
            color = "white" if (norm and norm(v) < 0.5) else "black"
            ax.text(j, i, fmt.format(v), ha="center", va="center",
                    color=color, fontsize=8)


def _ticks(ax, years, growths):
    ax.set_xticks(range(len(years)), years)
    ax.set_yticks(range(len(growths)), [f"{g:.2f}" for g in growths])
    ax.set_xlabel("Jaar in BV")
    ax.set_ylabel("Koers CAGR")


def main() -> None:
    years = np.arange(3, 42, 3)
    growths = np.linspace(0.0, 0.1, 11)
    d = 0.02

    T, G = np.meshgrid(years, growths)
    inv = analytic.ratio(T, G, d)
    st = analytic.state_ratio(T, G, d)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    norm = LogNorm(vmin=st.min(), vmax=st.max())
    ax1.imshow(st, cmap="viridis", norm=norm, origin="lower", aspect="auto")
    _ticks(ax1, years, growths)
    ax1.set_title(f"Staatsopbrengst BV / box 3  (d={d:.2%})")
    _annotate(ax1, st, "{:.2f}", norm)

    # Pareto: 0=niemand, 1=alleen staat, 2=alleen belegger, 3=beide
    cat = (inv > 1.0).astype(int) * 2 + (st > 1.0).astype(int)
    cmap = ListedColormap(["#b00020", "#f4a261", "#2a9d8f", "#1d3557"])
    ax2.imshow(cat, cmap=cmap, vmin=-0.5, vmax=3.5, origin="lower", aspect="auto")
    _ticks(ax2, years, growths)
    ax2.set_title("Wie wint? (belegger | staat)")
    labels = np.array([["niemand", "staat"], ["belegger", "beide"]])
    for i in range(cat.shape[0]):
        for j in range(cat.shape[1]):
            ax2.text(j, i, labels[(inv[i, j] > 1) * 1, (st[i, j] > 1) * 1],
                     ha="center", va="center", color="white", fontsize=7)

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
