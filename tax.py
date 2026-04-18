"""Belastingparameters voor box 3 en BV/box 2."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Taxes:
    """Nederlandse belastingtarieven (flat)."""

    box3_rate: float = 0.36
    box3_vrijstelling: float = 1_800.0
    vpb: float = 0.19
    box2_rate: float = 0.245


DEFAULT = Taxes()
