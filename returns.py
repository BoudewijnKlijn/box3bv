"""Genereer rendementsmatrices met vorm (T, N)."""
import numpy as np


def constant(rate: float, years: int, sims: int = 1) -> np.ndarray:
    """Vast rendement per jaar."""
    return np.full((years, sims), rate)


def normal(mu: float, sigma: float, years: int, sims: int,
           rng: np.random.Generator | None = None) -> np.ndarray:
    """Normaal verdeelde jaarrendementen."""
    rng = rng or np.random.default_rng()
    return rng.normal(mu, sigma, size=(years, sims))


def lognormal(mu: float, sigma: float, years: int, sims: int,
              rng: np.random.Generator | None = None) -> np.ndarray:
    """Lognormaal: sample exp(N(mu, sigma)) - 1."""
    rng = rng or np.random.default_rng()
    return rng.lognormal(mu, sigma, size=(years, sims)) - 1.0
