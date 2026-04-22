"""Belastingparameters voor box 3 en BV/box 2."""
from dataclasses import dataclass

import config


@dataclass(frozen=True)
class Taxes:
    """Nederlandse belastingtarieven (flat). Defaults komen uit .env."""

    box3_rate: float = config.BOX3_RATE
    box3_vrijstelling: float = config.BOX3_VRIJSTELLING
    vpb: float = config.VPB
    box2_rate: float = config.BOX2_RATE


DEFAULT = Taxes()
