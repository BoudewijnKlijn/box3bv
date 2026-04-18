"""BV-route: VPB over dividend en latente winst, box 2 bij uitkeren."""
import numpy as np

from tax import DEFAULT, Taxes


def simulate(start: float, growth: np.ndarray, dividend_yield: float,
             taxes: Taxes = DEFAULT) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Retourneer (wealth, vpb, exit_tax) bij liquidatie in elk jaar.

    - `wealth` (T+1, N): netto vermogen belegger bij liquidatie in jaar t.
    - `vpb` (T, N): jaarlijkse VPB op dividend.
    - `exit_tax` (T+1, N): VPB op latente winst + box 2, betaald bij exit in t.
    """
    years, sims = growth.shape
    wealth = np.empty((years + 1, sims))
    vpb_flow = np.zeros((years, sims))
    exit_tax = np.zeros((years + 1, sims))
    wealth[0] = start

    total = np.full(sims, float(start))
    taxed = np.zeros(sims)
    v, b2 = taxes.vpb, taxes.box2_rate
    net_div = dividend_yield * (1.0 - v)

    for t in range(years):
        vpb_flow[t] = total * dividend_yield * v
        taxed += total * net_div
        total = total * (1.0 + growth[t] + net_div)
        unrealized = total - start - taxed
        exit_vpb = unrealized * v
        withdraw = taxed + unrealized * (1.0 - v)
        exit_tax[t + 1] = exit_vpb + withdraw * b2
        wealth[t + 1] = start + withdraw * (1.0 - b2)
    return wealth, vpb_flow, exit_tax
