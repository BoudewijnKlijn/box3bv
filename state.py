"""Aggregeer belastingkasstroom tot totale staatsopbrengst."""
import numpy as np


def box3_cum_tax(tax: np.ndarray) -> np.ndarray:
    """Cumulatieve box 3-opbrengst per jaar, vorm (T+1, N)."""
    years, sims = tax.shape
    out = np.zeros((years + 1, sims))
    out[1:] = tax.cumsum(axis=0)
    return out


def bv_cum_tax(vpb: np.ndarray, exit_tax: np.ndarray) -> np.ndarray:
    """Totale staatsopbrengst bij liquidatie in elk jaar, vorm (T+1, N)."""
    years, sims = vpb.shape
    cum_vpb = np.zeros((years + 1, sims))
    cum_vpb[1:] = vpb.cumsum(axis=0)
    return cum_vpb + exit_tax


def future_value(flow: np.ndarray, rate: float = 0.0) -> np.ndarray:
    """FV per jaar van een jaarlijkse kasstroom (T, N) bij rente `rate`."""
    years, sims = flow.shape
    out = np.zeros((years + 1, sims))
    for t in range(years):
        out[t + 1] = out[t] * (1.0 + rate) + flow[t]
    return out
