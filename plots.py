"""Genereer alle plots met default-waarden en sla ze op in plots/.

Run met:  uv run python plots.py

Bedoeld om plots in de repo te checken zodat ze op GitHub direct zichtbaar zijn.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import heatmap
import run
import state_view

OUT = Path(__file__).parent / "plots"
OUT.mkdir(exist_ok=True)

# De scripts roepen intern plt.show() aan; we willen saven i.p.v. tonen.
plt.show = lambda *a, **k: None


def save(name: str) -> None:
    path = OUT / f"{name}.png"
    plt.gcf().savefig(path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"saved {path}")


def main() -> None:
    run.main()
    save("run")

    heatmap.main()
    save("heatmap")

    state_view.plot_state_heatmap()
    save("state_heatmap")

    state_view.plot_pareto()
    save("state_pareto")


if __name__ == "__main__":
    main()
