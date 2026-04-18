"""Vergelijk BV-route met box 3 over N simulaties (belegger + staat)."""
import numpy as np

import box3
import bv
import state
from tax import DEFAULT, Taxes


def run(start: float, growth: np.ndarray, dividend_yield: float,
        taxes: Taxes = DEFAULT) -> dict[str, np.ndarray]:
    """Simuleer beide routes; retourneer vermogen, belasting en ratio's."""
    total_return = growth + dividend_yield
    w3, tax3 = box3.simulate(start, total_return, taxes)
    wbv, vpb_flow, exit_tax = bv.simulate(start, growth, dividend_yield, taxes)
    cum3 = state.box3_cum_tax(tax3)
    cumbv = state.bv_cum_tax(vpb_flow, exit_tax)
    return {
        "box3": w3, "bv": wbv, "ratio": wbv / w3,
        "tax_box3": cum3, "tax_bv": cumbv,
        "tax_ratio": np.divide(cumbv, cum3, out=np.ones_like(cum3), where=cum3 > 0),
    }


def summary(result: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Mediaan/percentielen per jaar voor belegger- en staatsratio."""
    r, tr = result["ratio"], result["tax_ratio"]
    return {
        "median": np.median(r, axis=1),
        "p5": np.percentile(r, 5, axis=1),
        "p95": np.percentile(r, 95, axis=1),
        "p_bv_wins": (r > 1.0).mean(axis=1),
        "tax_median": np.median(tr, axis=1),
        "tax_p5": np.percentile(tr, 5, axis=1),
        "tax_p95": np.percentile(tr, 95, axis=1),
        "p_state_wins": (tr > 1.0).mean(axis=1),
    }
