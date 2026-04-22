import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

vermogen = 100_000
vermogen_min_range = 100_000
vermogen_max_range = 1_000_000

# rendement
dividend_yield = 0.03
growth_rate = 0.07

# belasting
box_3_tarief = 0.36
vpb = 0.19
box_2_tarief = 0.245
vrijstelling = 1800

time_periods = 30


def market(growth, start_kapitaal=1):
    return start_kapitaal
