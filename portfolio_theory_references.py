"""
Literature-backed rationale for strategic asset allocation used by the robo advisor.

The weights in ``RiskAssessmentEngine._initialize_asset_allocations`` are **policy
templates**: they encode higher fixed-income and broad-market index exposure for
lower risk scores and more equity / alternative sleeves for higher scores, in line
with textbook strategic allocation and robo-advisory practice. They are **not**
outputs of a live mean–variance optimization (which would require estimated
expected returns, a covariance matrix, and constraints).
"""
from __future__ import annotations

from typing import Dict

from risk_assessment_engine import RiskTolerance

# --- Core citations (use in UI / reports; verify pages for your bibliography style) ---

MARKOWITZ_1952 = (
    "Markowitz, H. (1952). Portfolio selection. *The Journal of Finance*, 7(1), 77–91."
)
BRINSON_1986 = (
    "Brinson, G. P., Hood, L. R., & Beebower, G. L. (1986). Determinants of portfolio "
    "performance. *Financial Analysts Journal*, 42(4), 39–44."
)
CAMPBELL_VICEIRA_2002 = (
    "Campbell, J. Y., & Viceira, L. M. (2002). *Strategic Asset Allocation*. Oxford University Press."
)
ANG_2014 = (
    "Ang, A. (2014). *Asset Management: A Systematic Approach to Factor Investing*. Oxford University Press."
)
GASPAR_OLIVEIRA_2024 = (
    "Gaspar, R. M., & Oliveira, M. (2024). Robo advising and investor profiling. "
    "*FinTech*, 3(1), 7. https://doi.org/10.3390/fintech3010007"
)
REHER_SOKOLINSKI_2024 = (
    "Reher, M., & Sokolinski, S. (2024). Robo advisors and access to wealth management. "
    "*Journal of Financial Economics*, 155, 103829. https://doi.org/10.1016/j.jfineco.2024.103829"
)
LIU_TSYVINSKI_2021 = (
    "Liu, Y., & Tsyvinski, A. (2021). Risks and returns of cryptocurrency. *The Review of Financial Studies*, 34(6), 2689–2727."
)

BIBLIOGRAPHY_MARKDOWN = f"""
**Foundations**
- {MARKOWITZ_1952} — Mean–variance intuition and the benefit of **diversification** across imperfectly correlated assets.
- {BRINSON_1986} — Strategic **asset allocation** explains much of long-run portfolio variation; motivates explicit policy weights by risk objective.
- {CAMPBELL_VICEIRA_2002} — Long-horizon investors often hold more **equity** when risk tolerance and horizon allow; more **fixed income** when stabilizing consumption matters.

**Multi-asset & risk budgeting**
- {ANG_2014} — Factor and multi-asset framing: risk tolerance maps to **risk budgets** across equity, rates, commodities, and alternatives.

**Robo-advisory & diversification**
- {GASPAR_OLIVEIRA_2024} — Robo platforms typically map investor profiles to **indexed / fund-based** portfolios.
- {REHER_SOKOLINSKI_2024} — Quasi-experimental evidence on access to robo-advisors, **diversification**, and welfare for middle-class investors.

**Alternatives (e.g. crypto in high-risk bands)**
- {LIU_TSYVINSKI_2021} — Academic risk–return evidence on crypto as a **volatile** alternative; suitable only for **small sleeves** in aggressive educational simulations, not a recommendation to concentrate wealth.
"""

RATIONALE_BY_RISK: Dict[RiskTolerance, str] = {
    RiskTolerance.CONSERVATIVE: (
        "**Conservative band:** Higher weights on **bonds** and **broad ETFs** follow the standard idea that "
        "fixed income and diversified index funds dampen portfolio volatility when capital preservation is primary "
        f"({BRINSON_1986}; {CAMPBELL_VICEIRA_2002}). Smaller sleeves in commodities and crypto reflect **limited** "
        "alternative exposure for diversification, not a bet on any single asset class ({MARKOWITZ_1952})."
    ),
    RiskTolerance.MODERATE: (
        "**Moderate band:** A **balanced** mix (meaningful equities and ETFs, some bonds, commodities, and crypto) "
        f"matches textbook **strategic** blends between capital preservation and growth ({ANG_2014}). "
        "Weights are a transparent policy template—not a covariance-optimized portfolio."
    ),
    RiskTolerance.AGGRESSIVE: (
        "**Aggressive band:** Larger sleeves in **equities**, **crypto**, and **commodities** express a higher "
        f"**risk budget** consistent with multi-asset theory ({ANG_2014}). Forex is a small sleeve illustrating "
        "currency exposure; in practice this is often accessed via funds rather than spot FX."
    ),
    RiskTolerance.VERY_AGGRESSIVE: (
        "**Very aggressive band:** The largest allocation to **crypto** and volatile sleeves is an **educational** "
        "illustration of high risk tolerance only. Empirical work documents crypto’s large volatility and role as a "
        f"debated diversifier ({LIU_TSYVINSKI_2021}); it should be interpreted as a **small, experimental** share of "
        "wealth in real life, not maximum concentration."
    ),
}

FUND_BASED_ROBO_RATIONALE = (
    "**Why fund/ETF portfolios?** Research on robo-advisory emphasizes **low-cost indexing**, "
    "**diversification**, and mapping questionnaire-based profiles to a small set of portfolios "
    f"({GASPAR_OLIVEIRA_2024}; {REHER_SOKOLINSKI_2024}). Our themed fund portfolios (Core, Growth, ESG, etc.) "
    "implement that pattern: holdings are **pre-specified baskets** with stated risk/return assumptions, then "
    "**filtered** by suitability to your score—mirroring transparent, rules-based robo design rather than opaque stock picking."
)


def allocation_rationale_markdown(risk_tolerance: RiskTolerance) -> str:
    """Narrative tying this user's risk band to cited theory (for Streamlit markdown)."""
    return RATIONALE_BY_RISK.get(
        risk_tolerance,
        RATIONALE_BY_RISK[RiskTolerance.MODERATE],
    )


def full_portfolio_references_markdown(risk_tolerance: RiskTolerance) -> str:
    """Expander content: band-specific rationale plus bibliography."""
    return (
        allocation_rationale_markdown(risk_tolerance)
        + "\n\n---\n\n"
        + BIBLIOGRAPHY_MARKDOWN.strip()
    )
