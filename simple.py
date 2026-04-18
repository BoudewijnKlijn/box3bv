import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

vermogen = 100_000
vermogen_min_range = 100_000
vermogen_max_range = 1_000_000

# rendement
dividend_yield = 0.03
growth_rate = 0.07

# belasting
box_3_tarief = 0.36
vpb = 0.19
box_2_tarief = 0.245
vrijstelling = 1800

# simulatie
n = 30


def get_market():
    data = pd.DataFrame(columns=["vermogen"])
    data.loc[0, "vermogen"] = vermogen

    for t in range(1, n + 1):
        data.loc[t, "vermogen"] = data.loc[t - 1, "vermogen"] * (
            1 + dividend_yield + growth_rate
        )
    return data


def get_box3():
    data = pd.DataFrame(columns=["vermogen", "bruto", "belasting", "netto"])
    data.loc[0, "vermogen"] = vermogen

    for t in range(1, n + 1):
        data.loc[t, "bruto"] = data.loc[t - 1, "vermogen"] * (
            dividend_yield + growth_rate
        )
        data.loc[t, "belasting"] = max(
            0, data.loc[t, "bruto"] * box_3_tarief - vrijstelling
        )
        data.loc[t, "netto"] = data.loc[t, "bruto"] - data.loc[t, "belasting"]

        data.loc[t, "vermogen"] = data.loc[t - 1, "vermogen"] + data.loc[t, "netto"]
    return data


def get_box2_optimaal():
    """Aannames:
    - Geen verlies door liquideren en aankopen.
    - Geen oprichtingskosten.
    - Geen jaarlijkse kosten.
    - Wel jaarlijks vpb over dividend.
    - Bij opheffen:
        - vpb over ongerealiseerde koerswinst (niet over betaalde dividend yield)
        - box 2 belasting over totale BV winst"""
    data = pd.DataFrame(columns=["vermogen"])
    data.loc[0, "vermogen"] = vermogen
    total = vermogen
    taxed_already = 0
    for t in range(1, n + 1):
        taxed_already = taxed_already + total * dividend_yield * (1 - vpb)
        total = total * (1 + growth_rate + dividend_yield * (1 - vpb))
        after_tax = (total - vermogen - taxed_already) * (1 - vpb)
        data.loc[t, "vermogen"] = vermogen + (taxed_already + after_tax) * (
            1 - box_2_tarief
        )
    return data


colors = {
    "tab:blue": "#1f77b4",
    "tab:orange": "#ff7f0e",
    "tab:green": "#2ca02c",
    "tab:red": "#d62728",
    "tab:purple": "#9467bd",
    "tab:brown": "#8c564b",
    "tab:pink": "#e377c2",
    "tab:gray": "#7f7f7f",
    "tab:olive": "#bcbd22",
    "tab:cyan": "#17becf",
}

for color, vermogen in zip(
    colors, np.linspace(vermogen_min_range, vermogen_max_range, 4)
):
    box3 = get_box3()
    box2 = get_box2_optimaal()
    relatief = box2.vermogen / box3.vermogen
    plt.plot(relatief, label=f"{vermogen:.0f}", linestyle="--", c=color)

plt.ylabel("Box 2 / Box 3")
plt.xlabel("Jaar")
plt.axhline(1.0, color="grey", linestyle=":")
plt.xlim([0, n])
plt.legend(title="Startkapitaal")
plt.show()
