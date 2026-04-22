"""Staatsopbrengst (numeriek) en Pareto-kaart (binair, fijnmazig)."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, LogNorm
from matplotlib.patches import Patch

import analytic
import box3
import bv
import config
import state
from tax import DEFAULT, Taxes


def _pareto_grid(
    years: np.ndarray, growths: np.ndarray, d: float, taxes: Taxes, state_rate: float
) -> tuple[np.ndarray, np.ndarray]:
    """Simulatie-gebaseerde winnaars-matrix (len(growths), len(years))."""
    per_euro = Taxes(
        box3_rate=taxes.box3_rate,
        box3_vrijstelling=0.0,
        vpb=taxes.vpb,
        box2_rate=taxes.box2_rate,
    )
    t_max = int(years.max())
    total = np.broadcast_to(growths + d, (t_max, len(growths))).copy()
    grow = np.broadcast_to(growths, (t_max, len(growths))).copy()
    w3, tax3 = box3.simulate(1.0, total, per_euro)
    wb, vpb_flow, exit_tax = bv.simulate(1.0, grow, d, per_euro)
    cum3 = state.box3_cum_tax(tax3, state_rate)
    cumbv = state.bv_cum_tax(vpb_flow, exit_tax, state_rate)
    idx = years.astype(int)
    inv = (wb[idx] > w3[idx]).T
    st = (cumbv[idx] > cum3[idx]).T
    return inv, st


def _ticks(ax, xvals, yvals, yfmt="{:.2%}"):
    xstep = max(1, len(xvals) // 10)
    ystep = max(1, len(yvals) // 10)
    ax.set_xticks(range(0, len(xvals), xstep), xvals[::xstep])
    ax.set_yticks(range(0, len(yvals), ystep), [yfmt.format(y) for y in yvals[::ystep]])
    ax.set_xlabel("Jaar in BV")
    ax.set_ylabel("Koers CAGR")


def plot_state_heatmap(d: float = config.DIVIDEND_YIELD,
                       taxes: Taxes = DEFAULT) -> None:
    """Heatmap van staats-ratio (analytisch, YEARS jaar × 1 jaar)."""
    years = np.arange(1, config.YEARS + 1)
    growths = np.linspace(0.0, 0.1, 11)
    T, G = np.meshgrid(years, growths)
    st = analytic.state_ratio(T, G, d, taxes)

    fig, ax = plt.subplots(figsize=(9, 6))
    norm = LogNorm(vmin=st.min(), vmax=st.max())
    ax.imshow(st, cmap="viridis", norm=norm, origin="lower", aspect="auto")
    ax.set_xticks(range(len(years)), years)
    ax.set_yticks(range(len(growths)), [f"{g:.2f}" for g in growths])
    ax.set_xlabel("Jaar in BV")
    ax.set_ylabel("Koers CAGR")
    ax.set_title(
        f"Staatsopbrengst BV / box 3 × 100 (d={d:.2%}, analytisch: geen staatsrente)"
    )
    for i in range(st.shape[0]):
        for j in range(st.shape[1]):
            c = "white" if norm(st[i, j]) < 0.5 else "black"
            ax.text(
                j,
                i,
                f"{st[i, j] * 100:.0f}",
                ha="center",
                va="center",
                color=c,
                fontsize=7,
            )
    fig.tight_layout()


def plot_pareto(
    d: float = config.DIVIDEND_YIELD,
    taxes: Taxes = DEFAULT,
    state_rate: float = config.STATE_RATE,
) -> None:
    """Fijnmazige Pareto-kaart inclusief negatieve groei."""
    years = np.arange(1, config.YEARS + 1)
    growths = np.linspace(0, 0.15, 51)
    inv, st = _pareto_grid(years, growths, d, taxes, state_rate)
    cat = inv.astype(int) * 2 + st.astype(int)

    cmap = ListedColormap(["#b00020", "#f4a261", "#2a9d8f", "#1d3557"])
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.imshow(cat, cmap=cmap, vmin=-0.5, vmax=3.5, origin="lower", aspect="auto")
    _ticks(ax, years, growths)
    ax.axhline(np.argmin(np.abs(growths)), color="white", lw=0.5, ls=":")
    ax.set_title(f"Wie wint met BV? (d={d:.2%}, staatsrente={state_rate:.2%})")
    legend = [
        Patch(color="#b00020", label="niemand"),
        Patch(color="#f4a261", label="alleen staat"),
        Patch(color="#2a9d8f", label="alleen belegger"),
        Patch(color="#1d3557", label="beide"),
    ]
    ax.legend(handles=legend, loc="lower right", framealpha=0.9)
    fig.tight_layout()


def main() -> None:
    plot_state_heatmap()
    plot_pareto()
    plt.show()


if __name__ == "__main__":
    main()
