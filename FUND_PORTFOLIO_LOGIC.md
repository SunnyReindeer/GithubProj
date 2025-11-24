# Fund Portfolio Recommendation Logic Explanation

## Overview
The fund portfolio recommendation system matches pre-defined portfolios to users based on their risk profile from the questionnaire.

## Step-by-Step Process

### Step 1: User Completes Risk Assessment
- User answers questionnaire (investment goals, time horizon, loss tolerance, etc.)
- System calculates a **Risk Score (0-100)** from answers
- System determines **Risk Tolerance** (Conservative, Moderate, Aggressive, Very Aggressive)

### Step 2: Pre-Defined Portfolios
The system has **6 pre-defined fund portfolios**, each with:
- **Theme**: Core, Growth, Dividend, ESG, REITs, Defensive
- **Risk Level**: 1-10 scale (1 = safest, 10 = riskiest)
- **Expected Return**: Annual percentage
- **Expected Volatility**: Risk measure
- **Holdings**: List of stocks/ETFs with:
  - Symbol (e.g., "SPY", "AAPL")
  - Name
  - AI Labels (sectors, themes, geography, risk)
  - Allocation percentage
  - Asset class (Stock, ETF, Bond)

**Example Portfolios:**
- **Core Portfolio**: Risk Level 5, Balanced mix (SPY 30%, VTI 25%, VEA 20%, etc.)
- **Growth Portfolio**: Risk Level 7, Tech-focused (QQQ 35%, AAPL 15%, MSFT 15%, etc.)
- **Dividend Portfolio**: Risk Level 4, Income-focused (VYM 30%, SCHD 25%, JNJ 15%, etc.)
- **ESG Portfolio**: Risk Level 5, Sustainable investing
- **REITs Portfolio**: Risk Level 5, Real estate focused
- **Defensive Portfolio**: Risk Level 3, Low-risk (TLT 40%, XLP 25%, etc.)

### Step 3: Suitability Scoring Algorithm
For each portfolio, calculate a **Suitability Score (0-100)**:

```python
def _calculate_suitability(portfolio, profile):
    score = 100.0  # Start with perfect score
    
    # 1. Risk Level Matching
    # Compare portfolio risk_level (1-10) with user's risk score (0-100) / 10
    risk_diff = abs(portfolio.risk_level - profile.score / 10)
    score -= risk_diff * 10  # Penalize by 10 points per risk level difference
    
    # 2. Risk Tolerance Matching (Additional penalties)
    if user is CONSERVATIVE and portfolio risk > 5:
        score -= 20  # Too risky for conservative user
    elif user is AGGRESSIVE and portfolio risk < 5:
        score -= 20  # Too safe for aggressive user
    elif user is VERY_AGGRESSIVE and portfolio risk < 7:
        score -= 30  # Way too safe for very aggressive user
    
    return max(0, min(100, score))  # Clamp between 0-100
```

**Example Calculation:**
- User Risk Score: 60 (Moderate-Aggressive)
- User Risk Tolerance: AGGRESSIVE
- Portfolio: Growth Portfolio (Risk Level 7)

```
Initial Score: 100
Risk Level Difference: |7 - 60/10| = |7 - 6| = 1
Penalty: 1 * 10 = 10 points
Score after risk matching: 100 - 10 = 90

Risk Tolerance Check:
- User is AGGRESSIVE, Portfolio risk is 7 (> 5) ✓
- No additional penalty

Final Suitability Score: 90
```

### Step 4: Filtering and Ranking
1. Calculate suitability score for all 6 portfolios
2. **Sort portfolios by suitability score** (highest first)
3. **Filter**: Only show portfolios with score >= 60
4. **Return top 3** portfolios (or fewer if less than 3 meet threshold)

### Step 5: Display Recommendations
Show recommended portfolios with:
- Suitability score
- Expected return and volatility
- Holdings breakdown
- AI labels (sectors, themes, geography)
- Rebalancing frequency

## Key Features

### AI Labeling System
Each holding has AI-generated labels:
- **Sectors**: Technology, Healthcare, Financial, Energy, etc.
- **Themes**: Growth Stock, Value Stock, Dividend Stock, Blue Chip
- **Geography**: US Market, Emerging Market, Developed Market, Asia Pacific, Europe
- **Risk**: Low Risk, Medium Risk, High Risk
- **Style**: ESG Compliant, Sustainable, Income Focused, Defensive

### Portfolio Themes
- **Core**: Balanced, diversified (most users)
- **Growth**: Tech and growth companies (aggressive users)
- **Dividend**: Income-focused (conservative users)
- **ESG**: Sustainable investing (values-based)
- **REITs**: Real estate exposure (diversification)
- **Defensive**: Low-risk, capital preservation (very conservative)

## Example Flow

1. **User completes questionnaire** → Risk Score: 45, Risk Tolerance: MODERATE
2. **System calculates suitability** for all 6 portfolios:
   - Core Portfolio (Risk 5): Score = 95 ✓
   - Dividend Portfolio (Risk 4): Score = 85 ✓
   - ESG Portfolio (Risk 5): Score = 95 ✓
   - Growth Portfolio (Risk 7): Score = 75 ✓
   - REITs Portfolio (Risk 5): Score = 95 ✓
   - Defensive Portfolio (Risk 3): Score = 65 ✓
3. **Filter and sort**: All 6 portfolios have score >= 60
4. **Return top 3**: Core Portfolio (95), ESG Portfolio (95), REITs Portfolio (95)
5. **Display** with holdings, AI labels, and allocation breakdown

## Why This Approach?
- **Pre-defined Portfolios**: Easier to understand and manage
- **AI Labels**: Help users understand what they're investing in
- **Risk Matching**: Ensures portfolios align with user's risk tolerance
- **Diversification**: Each portfolio is already diversified
- **Transparency**: Clear holdings and allocations

