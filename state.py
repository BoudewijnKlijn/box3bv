"""Aggregeer belastingkasstroom tot totale staatsopbrengst."""
import numpy as np


def future_value(flow: np.ndarray, rate: float = 0.0) -> np.ndarray:
    """FV per jaar van een jaarlijkse kasstroom (T, N) bij rente `rate`."""
    years, sims = flow.shape
    out = np.zeros((years + 1, sims))
    for t in range(years):
        out[t + 1] = out[t] * (1.0 + rate) + flow[t]
    return out


def box3_cum_tax(tax: np.ndarray, rate: float = 0.02) -> np.ndarray:
    """Opgerolde box 3-opbrengst per jaar, vorm (T+1, N), met staatsrente."""
    return future_value(tax, rate)


def bv_cum_tax(vpb: np.ndarray, exit_tax: np.ndarray,
               rate: float = 0.02) -> np.ndarray:
    """Totale staatsopbrengst bij liquidatie in elk jaar, vorm (T+1, N).

    VPB-stromen compounden met `rate` tot de liquidatiedatum; `exit_tax`
    valt per definitie op die datum en wordt er nominaal bij opgeteld.
    """
    return future_value(vpb, rate) + exit_tax
