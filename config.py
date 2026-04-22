"""Centrale configuratie — alle tuneable parameters uit .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


def _f(key: str) -> float:
    return float(os.environ[key])


def _i(key: str) -> int:
    return int(os.environ[key])


BOX3_RATE = _f("BOX3_RATE")
BOX3_VRIJSTELLING = _f("BOX3_VRIJSTELLING")
VPB = _f("VPB")
BOX2_RATE = _f("BOX2_RATE")

STATE_RATE = _f("STATE_RATE")

DIVIDEND_YIELD = _f("DIVIDEND_YIELD")
MEAN = _f("MEAN")
STD = _f("STD")

YEARS = _i("YEARS")
SIMS = _i("SIMS")
START = _f("START")
SEED = _i("SEED")
