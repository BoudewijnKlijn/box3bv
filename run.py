"""Voorbeeldrun: plot BV/box 3-ratio over tijd met onzekerheidsband."""
import matplotlib.pyplot as plt
import numpy as np

import compare
import returns


def main() -> None:
    years, sims = 30, 20_000
    start = 100_000.0
    # SPY-kalibratie (1993-heden): total return ~10.3%, stdev ~15%,
    # dividend yield ~1.8% → koerswinst ~8.5%.
    dividend_yield = 0.018
    mean, std = 0.085, 0.15

    rng = np.random.default_rng(42)
    growth = returns.lognormal_from_mean_std(mean, std, years, sims, rng)

    result = compare.run(start, growth, dividend_yield)
    stats = compare.summary(result)

    x = np.arange(years + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(x, stats["median"], label="mediaan")
    ax1.fill_between(x, stats["p5"], stats["p95"], alpha=0.2, label="P5-P95")
    ax1.axhline(1.0, color="grey", linestyle=":")
    ax1.set_xlabel("jaar")
    ax1.set_ylabel("BV / box 3")
    ax1.legend()

    ax2.plot(x, stats["p_bv_wins"])
    ax2.axhline(0.5, color="grey", linestyle=":")
    ax2.set_xlabel("jaar")
    ax2.set_ylabel("P(BV > box 3)")
    ax2.set_ylim(0, 1)

    fig.suptitle(f"start=€{start:,.0f}, mean={mean}, std={std}, div={dividend_yield} (SPY-like, lognormaal)")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
