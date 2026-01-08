# AI Robo Advisor Logic - Complete Documentation

This document provides a comprehensive explanation of the AI Robo Advisor system logic, including risk assessment, portfolio matching algorithm, and AI labeling system.

## Table of Contents

1. [Overview](#overview)
2. [Risk Assessment Engine](#risk-assessment-engine)
3. [Portfolio Matching Algorithm](#portfolio-matching-algorithm)
4. [AI Labeling System](#ai-labeling-system)
5. [Complete Flow Example](#complete-flow-example)
6. [Mathematical Formulas](#mathematical-formulas)

---

## Overview

The AI Robo Advisor system uses a **fund-based portfolio recommendation model** (similar to robo-advisors like Betterment or Wealthfront) rather than individual stock picking. The system:

1. **Assesses user risk profile** through a 10-question questionnaire
2. **Calculates risk score** (0-100) using weighted scoring
3. **Matches pre-defined portfolios** to user risk profile using suitability scoring
4. **Labels investments** with AI-generated tags (sectors, themes, geography, risk, style)
5. **Generates personalized investment plans** based on selected portfolios

---

## Risk Assessment Engine

### 1. Questionnaire Structure

The system uses **10 questions** covering:

| Question ID | Question | Weight | Impact |
|------------|----------|--------|--------|
| `investment_goal` | Primary investment goal | 20% | Highest impact on risk score |
| `loss_tolerance` | Reaction to 20% decline | 15% | Critical for risk matching |
| `volatility_comfort` | Comfort with daily fluctuations | 15% | Affects portfolio selection |
| `risk_scenarios` | Risk preference scenario | 15% | Direct risk indicator |
| `market_conditions` | Reaction to downturns | 10% | Behavioral risk factor |
| `portfolio_size` | Percentage of total wealth | 10% | Concentration risk |
| `experience_level` | Trading experience | 10% | Knowledge factor |
| `diversification_preference` | Importance of diversification | 5% | Portfolio structure |
| `investment_horizon` | Time horizon | - | Used for allocation, not scoring |
| `liquidity_needs` | Access to funds | - | Used for allocation, not scoring |

### 2. Scoring Weights

Each question has a **weight** that determines its importance in the final risk score:

```python
scoring_weights = {
    "investment_goal": 0.20,      # 20% - Most important
    "loss_tolerance": 0.15,       # 15%
    "volatility_comfort": 0.15,   # 15%
    "risk_scenarios": 0.15,       # 15%
    "market_conditions": 0.10,    # 10%
    "portfolio_size": 0.10,       # 10%
    "experience_level": 0.10,     # 10%
    "diversification_preference": 0.05  # 5% - Least important
}
```

**Total weight = 1.0 (100%)**

### 3. Risk Score Calculation

**Formula:**
```
Risk Score = (Σ(answer × weight) / (4 × total_weight)) × 100
```

Where:
- `answer` = Selected option score (1-4)
- `weight` = Question weight (0.05-0.20)
- `4` = Maximum possible answer score
- Result is normalized to **0-100 scale**

**Example Calculation:**

User answers:
- Investment Goal: 3 (Aggressive growth) → 3 × 0.20 = 0.60
- Loss Tolerance: 2 (Sell some) → 2 × 0.15 = 0.30
- Volatility Comfort: 3 (Moderate) → 3 × 0.15 = 0.45
- Risk Scenarios: 3 (Higher returns) → 3 × 0.15 = 0.45
- Market Conditions: 3 (Hold) → 3 × 0.10 = 0.30
- Portfolio Size: 2 (25-50%) → 2 × 0.10 = 0.20
- Experience: 2 (Some experience) → 2 × 0.10 = 0.20
- Diversification: 3 (Important) → 3 × 0.05 = 0.15

**Total Score:**
```
Total = 0.60 + 0.30 + 0.45 + 0.45 + 0.30 + 0.20 + 0.20 + 0.15 = 2.65
Normalized = (2.65 / (4 × 1.0)) × 100 = 66.25
```

**Risk Score: 66.25** → **Risk Tolerance: AGGRESSIVE** (50-75 range)

### 4. Risk Tolerance Categories

| Score Range | Risk Tolerance | Characteristics |
|-------------|----------------|-----------------|
| 0-25 | **Conservative** | Capital preservation, low volatility, bonds-heavy |
| 26-50 | **Moderate** | Balanced growth, moderate risk, diversified |
| 51-75 | **Aggressive** | Growth-focused, higher risk, equity-heavy |
| 76-100 | **Very Aggressive** | Maximum returns, highest risk, crypto/volatile assets |

### 5. Risk Metrics Calculation

The system calculates additional risk metrics:

**Max Drawdown Tolerance:**
```python
base_drawdown = {
    CONSERVATIVE: 0.10,      # 10% max loss
    MODERATE: 0.20,          # 20% max loss
    AGGRESSIVE: 0.35,        # 35% max loss
    VERY_AGGRESSIVE: 0.50    # 50% max loss
}
max_drawdown = base_drawdown[risk_tolerance] × (loss_tolerance / 4)
```

**Volatility Tolerance:**
```python
volatility_tolerance = (volatility_comfort / 4) × 0.5  # 0-0.5 scale
```

**Diversification Preference:**
```python
diversification_preference = diversification_answer / 4  # 0-1 scale
```

**Liquidity Needs:**
```python
liquidity_needs = (5 - liquidity_answer) / 4  # Inverted: 0-1 scale
# Higher answer = lower liquidity needs
```

### 6. Recommended Asset Allocation

Based on risk tolerance, the system recommends asset allocation:

| Risk Tolerance | Stocks | ETFs | Bonds | Crypto | Commodities | Forex |
|----------------|--------|------|-------|--------|-------------|-------|
| **Conservative** | 20% | 30% | 35% | 5% | 10% | 0% |
| **Moderate** | 35% | 25% | 5% | 20% | 15% | 0% |
| **Aggressive** | 30% | 10% | 0% | 35% | 20% | 5% |
| **Very Aggressive** | 25% | 0% | 0% | 45% | 20% | 10% |

---

## Portfolio Matching Algorithm

### 1. Pre-Defined Portfolios

The system maintains **6 pre-defined fund portfolios**, each with:

- **Theme**: Core, Growth, Dividend, ESG, REITs, Defensive
- **Risk Level**: 1-10 scale (1 = safest, 10 = riskiest)
- **Expected Return**: Annual percentage
- **Expected Volatility**: Risk measure
- **Holdings**: List of stocks/ETFs with allocations
- **Rebalancing Frequency**: Monthly, Quarterly, Semi-Annually

**Portfolio Details:**

| Portfolio | Risk Level | Expected Return | Volatility | Theme |
|-----------|------------|-----------------|------------|-------|
| **Core** | 5 | 8.5% | 12.0% | Balanced, diversified |
| **Growth** | 7 | 12.0% | 18.0% | Tech and growth stocks |
| **Dividend** | 4 | 6.5% | 10.0% | Income-focused |
| **ESG** | 5 | 9.0% | 13.0% | Sustainable investing |
| **REITs** | 5 | 7.5% | 14.0% | Real estate exposure |
| **Defensive** | 3 | 5.5% | 8.0% | Low-risk, capital preservation |

### 2. Suitability Scoring Algorithm

For each portfolio, calculate a **Suitability Score (0-100)**:

**Step 1: Risk Level Matching**
```python
risk_diff = abs(portfolio.risk_level - (user_risk_score / 10))
penalty = risk_diff × 10
score = 100 - penalty
```

**Step 2: Risk Tolerance Matching (Additional Penalties)**
```python
if user is CONSERVATIVE and portfolio.risk_level > 5:
    score -= 20  # Too risky for conservative user
elif user is AGGRESSIVE and portfolio.risk_level < 5:
    score -= 20  # Too safe for aggressive user
elif user is VERY_AGGRESSIVE and portfolio.risk_level < 7:
    score -= 30  # Way too safe for very aggressive user
```

**Step 3: Final Score**
```python
final_score = max(0, min(100, score))  # Clamp between 0-100
```

### 3. Example Suitability Calculation

**User Profile:**
- Risk Score: 60 (Moderate-Aggressive)
- Risk Tolerance: AGGRESSIVE
- Risk Score / 10 = 6.0

**Growth Portfolio (Risk Level 7):**

```
Step 1: Risk Level Matching
risk_diff = |7 - 6.0| = 1.0
penalty = 1.0 × 10 = 10
score = 100 - 10 = 90

Step 2: Risk Tolerance Matching
User is AGGRESSIVE, Portfolio risk is 7 (> 5) ✓
No additional penalty

Final Suitability Score: 90
```

**Defensive Portfolio (Risk Level 3):**

```
Step 1: Risk Level Matching
risk_diff = |3 - 6.0| = 3.0
penalty = 3.0 × 10 = 30
score = 100 - 30 = 70

Step 2: Risk Tolerance Matching
User is AGGRESSIVE, Portfolio risk is 3 (< 5) ✗
score -= 20
score = 70 - 20 = 50

Final Suitability Score: 50 (Below threshold)
```

### 4. Portfolio Filtering and Selection

**Process:**
1. Calculate suitability score for all 6 portfolios
2. **Filter**: Only portfolios with score >= 60
3. **Sort**: By suitability score (highest first)
4. **Return**: Top 3 portfolios (or fewer if < 3 meet threshold)

**Example Results:**

| Portfolio | Suitability Score | Status |
|-----------|-------------------|--------|
| Growth | 90 | ✅ Selected |
| Core | 85 | ✅ Selected |
| ESG | 80 | ✅ Selected |
| REITs | 75 | ✅ Selected (if showing 4) |
| Dividend | 65 | ✅ Selected (if showing 5) |
| Defensive | 50 | ❌ Filtered out (< 60) |

---

## AI Labeling System

### 1. Label Categories

The AI labeling system categorizes investments using **5 label types**:

#### A. Sector Labels
- Technology, Healthcare, Financial Services, Energy, Consumer Goods, Industrial, Materials, Utilities, Real Estate, Communication Services

#### B. Theme Labels
- Growth Stock, Value Stock, Dividend Stock, Blue Chip, Small Cap, Mid Cap, Large Cap

#### C. Geographic Labels
- US Market, Emerging Market, Developed Market, Asia Pacific, Europe

#### D. Risk Labels
- Low Risk, Medium Risk, High Risk

#### E. Style Labels
- ESG Compliant, Sustainable, Income Focused, Capital Appreciation, Defensive, Cyclical

### 2. Labeling Logic

**For Stocks:**
```python
if symbol in SECTOR_MAP:
    sector = SECTOR_MAP[symbol]  # e.g., "AAPL" → "Technology"
    labels.append(sector_label)
    
# Add risk label based on asset class
if asset_class == "Crypto":
    labels.append(HIGH_RISK)
elif asset_class == "Bond":
    labels.append(LOW_RISK)
else:
    labels.append(MEDIUM_RISK)
```

**For ETFs:**
```python
if symbol in ETF_THEMES:
    themes = ETF_THEMES[symbol]  # e.g., "QQQ" → ["Technology", "Growth Stock", "US Market"]
    for theme in themes:
        labels.append(theme_label)
```

**Example Labeling:**

**Apple (AAPL):**
- Sector: Technology
- Theme: Large Cap, Growth Stock
- Geography: US Market
- Risk: Medium Risk
- Style: Capital Appreciation

**S&P 500 ETF (SPY):**
- Sector: (Broad Market)
- Theme: Large Cap
- Geography: US Market
- Risk: Medium Risk
- Style: Diversified

**20+ Year Treasury Bond ETF (TLT):**
- Sector: (Bond)
- Theme: (Fixed Income)
- Geography: US Market
- Risk: Low Risk
- Style: Income Focused

### 3. Sector Mapping

The system uses predefined mappings:

**Technology Stocks:**
- AAPL, MSFT, GOOGL, META, NVDA, AMD, INTC, CRM, ORCL, TSM, ASML

**Healthcare Stocks:**
- JNJ, PFE, UNH, ABBV, TMO, ABT, DHR, BMY

**Financial Services:**
- JPM, BAC, WFC, GS, MS, C, V, MA

**Energy:**
- XOM, CVX, SLB, COP, EOG

**Consumer:**
- AMZN, TSLA, HD, NKE, SBUX (Discretionary)
- MCD, KO, PEP, WMT, PG (Staples)

### 4. ETF Theme Mapping

**Broad Market ETFs:**
- SPY: US Market, Large Cap, Broad Market
- VTI: US Market, Total Market, Diversified
- QQQ: Technology, Growth Stock, US Market

**Sector ETFs:**
- XLK: Technology, Sector, Growth Stock
- XLV: Healthcare, Sector, Defensive
- XLF: Financial Services, Sector, Value Stock
- XLE: Energy, Sector, Cyclical

**Income ETFs:**
- VYM: Dividend Stock, Value Stock, Income Focused
- SCHD: Dividend Stock, Value Stock, Income Focused
- VNQ: Real Estate, REITs, Income Focused

---

## Complete Flow Example

### Scenario: Moderate-Aggressive Investor

**Step 1: User Completes Questionnaire**

Answers:
- Investment Goal: "Aggressive growth with higher risk" (Score: 3)
- Time Horizon: "3-5 years" (Score: 3)
- Loss Tolerance: "Hold and wait for recovery" (Score: 3)
- Experience: "Some experience with basic strategies" (Score: 2)
- Portfolio Size: "25-50%" (Score: 2)
- Volatility Comfort: "Comfortable with moderate volatility" (Score: 3)
- Diversification: "Important - some diversification" (Score: 3)
- Liquidity Needs: "Within a year" (Score: 3)
- Risk Scenarios: "I prefer higher returns with higher risk" (Score: 3)
- Market Conditions: "Hold current positions" (Score: 3)

**Step 2: Calculate Risk Score**

```
Weighted Scores:
- investment_goal: 3 × 0.20 = 0.60
- loss_tolerance: 3 × 0.15 = 0.45
- volatility_comfort: 3 × 0.15 = 0.45
- risk_scenarios: 3 × 0.15 = 0.45
- market_conditions: 3 × 0.10 = 0.30
- portfolio_size: 2 × 0.10 = 0.20
- experience_level: 2 × 0.10 = 0.20
- diversification_preference: 3 × 0.05 = 0.15

Total: 2.80
Risk Score: (2.80 / (4 × 1.0)) × 100 = 70.0
```

**Step 3: Determine Risk Profile**

- **Risk Score**: 70.0
- **Risk Tolerance**: AGGRESSIVE (51-75 range)
- **Investment Horizon**: MEDIUM_TERM (3-5 years)
- **Experience Level**: INTERMEDIATE
- **Max Drawdown Tolerance**: 0.35 × (3/4) = 0.2625 (26.25%)
- **Volatility Tolerance**: (3/4) × 0.5 = 0.375
- **Diversification Preference**: 3/4 = 0.75
- **Liquidity Needs**: (5-3)/4 = 0.5

**Step 4: Calculate Suitability Scores**

| Portfolio | Risk Level | Risk Diff | Penalty | Tolerance Check | Final Score |
|-----------|------------|-----------|---------|-----------------|-------------|
| Growth | 7 | \|7-7\| = 0 | 0 | ✓ (7 > 5) | **100** |
| Core | 5 | \|5-7\| = 2 | 20 | ✗ (5 < 5) | **80** |
| ESG | 5 | \|5-7\| = 2 | 20 | ✗ (5 < 5) | **80** |
| REITs | 5 | \|5-7\| = 2 | 20 | ✗ (5 < 5) | **80** |
| Dividend | 4 | \|4-7\| = 3 | 30 | ✗ (4 < 5) | **50** |
| Defensive | 3 | \|3-7\| = 4 | 40 | ✗ (3 < 5) | **40** |

**Step 5: Filter and Select**

- Filter: Scores >= 60
- Selected: Growth (100), Core (80), ESG (80), REITs (80)
- Display: Top 3 → Growth, Core, ESG

**Step 6: User Selects Growth Portfolio**

**Portfolio Holdings:**
- QQQ (35%): Technology, Growth Stock, US Market
- AAPL (15%): Technology, Large Cap, Growth Stock
- MSFT (15%): Technology, Large Cap, Growth Stock
- NVDA (15%): Technology, Growth Stock, High Risk
- TSLA (10%): Consumer, Growth Stock, High Risk
- AMZN (10%): Consumer, Growth Stock, Large Cap

**AI Label Breakdown:**
- **Sectors**: Technology (75%), Consumer (20%)
- **Themes**: Growth Stock (100%), Large Cap (50%)
- **Geography**: US Market (100%)
- **Risk**: High Risk (25%), Medium Risk (75%)
- **Style**: Capital Appreciation (100%)

**Step 7: Generate Investment Plan**

- Portfolio Summary: Growth Portfolio, Risk Level 7, Expected Return 12%
- Implementation Steps: Monthly rebalancing, focus on tech sector
- Recommendations: Suitable for aggressive investors with 3-5 year horizon

---

## Mathematical Formulas

### Risk Score Formula

```
Risk Score = (Σ(answer_i × weight_i) / (max_answer × total_weight)) × 100

Where:
- answer_i = Selected option score (1-4)
- weight_i = Question weight (0.05-0.20)
- max_answer = 4 (maximum possible score)
- total_weight = 1.0 (sum of all weights)
```

### Suitability Score Formula

```
Suitability Score = 100 - (risk_level_penalty + tolerance_penalty)

Where:
risk_level_penalty = |portfolio_risk_level - (user_risk_score / 10)| × 10

tolerance_penalty = {
    20 if (conservative & portfolio_risk > 5) or (aggressive & portfolio_risk < 5)
    30 if (very_aggressive & portfolio_risk < 7)
    0 otherwise
}
```

### Normalization Formula

```
Normalized Score = max(0, min(100, raw_score))
```

This ensures all scores are clamped between 0-100.

---

## Key Features

### 1. Weighted Scoring System
- Different questions have different importance
- Investment goal has highest weight (20%)
- Diversification has lowest weight (5%)

### 2. Multi-Factor Risk Assessment
- Not just risk score, but also:
  - Max drawdown tolerance
  - Volatility tolerance
  - Diversification preference
  - Liquidity needs

### 3. Intelligent Portfolio Matching
- Considers both risk level and risk tolerance
- Applies penalties for mismatches
- Filters out unsuitable portfolios

### 4. AI-Powered Labeling
- Automatic categorization of investments
- Multiple label dimensions (sector, theme, geography, risk, style)
- Helps users understand what they're investing in

### 5. Personalized Recommendations
- Based on comprehensive risk profile
- Multiple portfolio options (up to 3)
- Detailed breakdowns and explanations

---

## Conclusion

The AI Robo Advisor system uses a sophisticated multi-step process:

1. **Comprehensive Risk Assessment** → 10-question weighted questionnaire
2. **Precise Risk Scoring** → Weighted algorithm producing 0-100 score
3. **Intelligent Matching** → Suitability scoring with penalty system
4. **AI Labeling** → Automatic investment categorization
5. **Personalized Plans** → Tailored recommendations based on profile

This approach ensures that users receive portfolio recommendations that truly match their risk preferences, investment goals, and financial situation.


