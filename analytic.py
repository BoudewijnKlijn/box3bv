"""Gesloten vorm voor BV/box 3-ratio bij vast jaarlijks rendement."""
import numpy as np

from tax import DEFAULT, Taxes


def ratio(years, growth, dividend_yield: float, taxes: Taxes = DEFAULT) -> np.ndarray:
    """BV/box 3-ratio (netto vermogen belegger) per euro na `years` jaar."""
    v, b, a = taxes.vpb, taxes.box2_rate, taxes.box3_rate
    d = dividend_yield
    T = np.asarray(years, dtype=float)
    g = np.asarray(growth, dtype=float)
    bv_rate = g + d * (1.0 - v)
    bv = 1.0 + (1.0 - b) * (1.0 - v) * (d + g) * ((1.0 + bv_rate) ** T - 1.0) / bv_rate
    box3 = (1.0 + (d + g) * (1.0 - a)) ** T
    return bv / box3


def state_ratio(years, growth, dividend_yield: float,
                taxes: Taxes = DEFAULT) -> np.ndarray:
    """Verhouding staatsopbrengst BV / box 3 per euro na `years` jaar."""
    v, b, a = taxes.vpb, taxes.box2_rate, taxes.box3_rate
    d = dividend_yield
    T = np.asarray(years, dtype=float)
    g = np.asarray(growth, dtype=float)
    r = d + g
    bv_rate = g + d * (1.0 - v)
    factor = (1.0 + bv_rate) ** T
    tax_bv = (factor - 1.0) * r * (v + b * (1.0 - v)) / bv_rate
    tax_box3 = a / (1.0 - a) * ((1.0 + r * (1.0 - a)) ** T - 1.0)
    return tax_bv / tax_box3
