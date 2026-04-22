"""Simpele sanity checks voor bv.simulate."""
import numpy as np

import analytic
import box3
import bv
import returns
import state
from tax import Taxes


def test_geen_groei_geen_dividend():
    """Zonder rendement en dividend verandert er niets en is er geen belasting."""
    growth = np.zeros((5, 1))
    wealth, vpb, exit_tax = bv.simulate(100.0, growth, dividend_yield=0.0)
    assert np.allclose(wealth, 100.0)
    assert np.allclose(vpb, 0.0)
    assert np.allclose(exit_tax, 0.0)


def test_geen_belasting_is_pure_compounding():
    """Met vpb=0 en box2=0 volgt de BV zuivere samengestelde groei."""
    taxes = Taxes(box3_rate=0.0, box3_vrijstelling=0.0, vpb=0.0, box2_rate=0.0)
    growth = np.array([[0.05], [0.10], [-0.02]])
    d = 0.03
    wealth, _, _ = bv.simulate(100.0, growth, d, taxes)
    expected = 100.0 * np.cumprod(1.0 + growth[:, 0] + d)
    assert np.allclose(wealth[1:, 0], expected)


def test_een_jaar_alleen_dividend_handmatig():
    """Handmatig uitgerekend: 1 jaar, 5% div, 0% groei, vpb 20%, box2 25%."""
    taxes = Taxes(box3_rate=0.36, box3_vrijstelling=0.0, vpb=0.20, box2_rate=0.25)
    growth = np.zeros((1, 1))
    wealth, vpb, exit_tax = bv.simulate(100.0, growth, dividend_yield=0.05, taxes=taxes)
    # VPB over brutodividend: 100 * 0.05 * 0.20 = 1.0
    assert np.isclose(vpb[0, 0], 1.0)
    # Netto dividend 4 blijft in BV, geen latente winst.
    # Box 2 over 4: 1.0. Totaal exit_tax: 0 + 1.0 = 1.0.
    assert np.isclose(exit_tax[1, 0], 1.0)
    # Belegger houdt 100 + 4*0.75 = 103 over.
    assert np.isclose(wealth[1, 0], 103.0)


def test_komt_overeen_met_analytic_ratio():
    """Monte-Carlo met constant rendement moet de gesloten vorm reproduceren."""
    taxes = Taxes(box3_rate=0.36, box3_vrijstelling=0.0, vpb=0.19, box2_rate=0.245)
    years, g, d = 10, 0.05, 0.02
    growth = np.full((years, 1), g)
    total = np.full((years, 1), g + d)

    wbv, _, _ = bv.simulate(1.0, growth, d, taxes)
    w3, _ = box3.simulate(1.0, total, taxes)
    ratio_sim = wbv[-1, 0] / w3[-1, 0]
    ratio_ana = float(analytic.ratio(years, g, d, taxes))
    assert np.isclose(ratio_sim, ratio_ana, rtol=1e-10)


def test_box3_cum_tax_zonder_rente_is_cumsum():
    """Met rate=0 reproduceert box3_cum_tax het oude cumsum-gedrag."""
    tax = np.array([[1.0], [2.0], [3.0]])
    out = state.box3_cum_tax(tax, rate=0.0)
    expected = np.array([[0.0], [1.0], [3.0], [6.0]])
    assert np.allclose(out, expected)


def test_future_value_handmatig():
    """Jaarlijkse stroom 10 bij 10% rente: 0, 10, 21, 33.1."""
    flow = np.array([[10.0], [10.0], [10.0]])
    out = state.future_value(flow, rate=0.1)
    expected = np.array([[0.0], [10.0], [21.0], [33.1]])
    assert np.allclose(out, expected)


def test_lognormal_kalibratie_matcht_target():
    """Sample mean/std van gekalibreerde lognormaal komt op target uit."""
    rng = np.random.default_rng(0)
    mean, std = 0.085, 0.15
    r = returns.lognormal_from_mean_std(mean, std, years=1, sims=500_000, rng=rng)
    assert np.isclose(r.mean(), mean, atol=5e-4)
    assert np.isclose(r.std(), std, atol=5e-4)


def test_bv_cum_tax_exit_tax_niet_gecompound():
    """Exit_tax valt op liquidatiedatum — wordt puur opgeteld, niet opgerent."""
    vpb = np.zeros((3, 1))
    exit_tax = np.array([[0.0], [5.0], [5.0], [5.0]])
    out = state.bv_cum_tax(vpb, exit_tax, rate=0.1)
    assert np.allclose(out, exit_tax)


