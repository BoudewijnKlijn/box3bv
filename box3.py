"""Box 3 simulatie onder belasting op werkelijk rendement."""
import numpy as np

from tax import DEFAULT, Taxes


def simulate(start: float, returns: np.ndarray,
             taxes: Taxes = DEFAULT) -> tuple[np.ndarray, np.ndarray]:
    """Retourneer (wealth (T+1, N), tax (T, N)) per jaar per simulatie.

    `returns` (T, N) = bruto jaarrendement (dividend + koers).
    """
    years, sims = returns.shape
    wealth = np.empty((years + 1, sims))
    wealth[0] = start
    tax = np.empty((years, sims))
    rate, vrij = taxes.box3_rate, taxes.box3_vrijstelling
    for t in range(years):
        gross = wealth[t] * returns[t]
        tax[t] = np.maximum(0.0, gross * rate - vrij)
        wealth[t + 1] = wealth[t] + gross - tax[t]
    return wealth, tax
