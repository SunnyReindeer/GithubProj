# Research Support for Our AI Robo Advisor

This document links **academic and industry research** on robo-advisors to **our design choices**. Use it to support your AI robo advisor in reports and meetings (“why we use this” and “what backs our approach”).

---

## 1. Why Use a Robo Advisor? (Research Backing)

### 1.1 Documented Benefits

Research shows that robo-advisors:

| Finding | Source-type | How it supports our project |
|--------|-------------|-----------------------------|
| **Reshape portfolios** toward indexing, lower fees, better diversification | Academic (e.g. *The diversification and welfare effects of robo-advising*, *Who Benefits from Robo-Advising?*) | Our system recommends **fund/ETF-based portfolios** (Core, Growth, Dividend, ESG, REITs, Defensive), not individual stock picking—aligned with “increase indexing, reduce single-name risk.” |
| **Improve risk-adjusted returns** (e.g. higher Sharpe ratios) mainly by **reducing risk** via diversification | Same | We use **pre-defined diversified portfolios** and a **suitability filter** so recommendations match risk profile—reduces mismatch and concentration risk. |
| **Reduce behavioral biases** (e.g. disposition bias, trend chasing) | *The Promises and Pitfalls of Robo-Advising* | Automated, rule-based advice (questionnaire → score → filter → top 3) reduces ad-hoc, emotional choices. |
| **Lower fees** and **increase international diversification** | Multiple papers | Our model uses low-cost ETF/stock baskets and multiple themes (US, developed, emerging via VEA, VWO, etc.), supporting diversification. |
| **Who benefits most:** investors with little experience, poor diversification, high cash, or high-fee active funds | *Who Benefits from Robo-Advising?* | Our **risk assessment** and **experience level** in the questionnaire help tailor advice; we target similar segments. |

**One sentence for your report:**  
“Research shows robo-advisors improve diversification and risk-adjusted outcomes especially for less experienced or under-diversified investors; our design uses fund-based portfolios and risk-based filtering to support the same goals.”

---

## 2. Risk Assessment & Questionnaire (Research Support)

### 2.1 Standard Practice

- Robo-advisors **typically use questionnaires** about preferences, financial situation, and goals, then recommend **portfolios matched to the investor’s risk profile** (e.g. *Robo Advising and Investor Profiling*, MDPI; *How Risk Profiles of Investors Affect Robo-Advised Portfolios*).
- Questionnaires often cover **goals, time horizon, loss tolerance, experience, and risk attitude**—similar to our 10 questions.

### 2.2 Scoring and Scale

- Research and industry use **numeric risk scores** (e.g. 0–100) and **categories** (e.g. conservative to aggressive).
- We use: **risk score 0–100**, **four categories** (Conservative, Moderate, Aggressive, Very Aggressive), and **weighted scoring** across multiple questions.

### 2.3 Weighted Questions

- Studies note that **not all questions have equal impact** and that **methodology is often undisclosed** (e.g. *To Advise, or Not to Advise*).
- Our design responds by: **documenting weights** (e.g. investment_goal 20%, loss_tolerance 15%, etc.) in `AI_ROBO_ADVISOR_RULES.md`, so our risk score is **transparent and auditable**.

### 2.4 What Research Suggests

- Risk assessment should reflect **multiple dimensions** (goals, time horizon, loss tolerance, experience, diversification preference).
- We cover: investment goal, horizon, loss tolerance, volatility comfort, risk scenarios, market reaction, portfolio size, experience, diversification, liquidity—giving a **multi-dimensional** profile.

**One sentence for your report:**  
“Questionnaire-based risk profiling with a 0–100 score and clear category bands is consistent with robo-advisor literature; we add transparency by publishing our scoring weights and rules.”

---

## 3. Portfolio Recommendation: Fund-Based & Suitability (Research Support)

### 3.1 ETF / Fund-Based Portfolios

- Research finds that robo-advisors **shift portfolios toward ETFs and indexed/fund products** and away from concentrated individual stock positions (*diversification and welfare effects*; *Who Benefits from Robo-Advising?*).
- We recommend **pre-defined fund-style portfolios** (each with ETFs and selected stocks), not a list of single-name picks—aligned with this **fund-based, diversified** approach.

### 3.2 Matching to Risk Profile

- Recommendations are expected to be **tailored to the investor’s risk profile** (e.g. *Robo Advising and Investor Profiling*; *How Risk Profiles of Investors Affect Robo-Advised Portfolios*).
- We do this via a **suitability score** (risk-level alignment + tolerance-based penalties) and a **filter** (only show portfolios with suitability ≥ 60, then top 3).

### 3.3 Suitability and “Fit”

- Literature discusses **suitability** and **fit** between client and product; platforms differ in how explicitly they define it.
- We make suitability **explicit**: formula in rules, threshold 60, and **customer scenarios** showing how different risk types get different recommendations (see `ROBO_ADVISOR_CUSTOMER_SCENARIOS.md`).

**One sentence for your report:**  
“Our fund-based portfolios and suitability-based filter (score ≥ 60, top 3) align with research that emphasizes diversification and risk-profile matching in robo-advisory.”

### 3.4 Per-template citations (not ad hoc weights)

In code, each predefined portfolio (`FundPortfolio` in `fund_portfolio_manager.py`) includes:

- **`design_rationale`** — one paragraph tying the theme (e.g. strategic balanced, growth tilt, dividend income, ESG, REITs, defensive) to standard finance ideas: policy/strategic allocation, factor exposure, ESG integration, listed real estate as an asset class, low-volatility / bond-heavy defense.
- **`references`** — short **academic or industry citations** (e.g. Brinson et al., Markowitz, Fama–French, Carhart, Friede et al. on ESG, Ling & Naranjo on REITs, Campbell & Viceira on strategic allocation).

The **AI Robo Advisor** Streamlit page surfaces these under each portfolio so you can tell your professor **where the template comes from**—it is an **explainable style template** with citations, not a black-box list of tickers.

---

## 4. Transparency and Documented Methodology

- A recurring criticism in research is that robo-advisors often **do not disclose** how they profile investors or allocate assets (*Robo Advising and Investor Profiling*; *To Advise, or Not to Advise*).
- We address this by:
  - **Full rule set** in `AI_ROBO_ADVISOR_RULES.md` (weights, formulas, thresholds, filter).
  - **Logic and flow** in `AI_ROBO_ADVISOR_LOGIC.md` and `AI_ROBO_ADVISOR_USER_WALKTHROUGH.md`.
  - **Customer scenarios** with concrete scores and filter outcomes in `ROBO_ADVISOR_CUSTOMER_SCENARIOS.md`.

**One sentence for your report:**  
“Unlike many platforms that keep methodology opaque, we document our risk scoring, suitability formula, and filter rules so the advice process is auditable and explainable.”

---

## 5. How Our Design Maps to Research

| Research idea | Our implementation |
|---------------|---------------------|
| Questionnaire-based risk profiling | 10-question risk assessment with fixed weights |
| Numeric risk score (e.g. 0–100) | Risk score 0–100, four categories (25/50/75 thresholds) |
| Transparent methodology | Documented weights, formulas, and filter in rules and logic docs |
| Fund/ETF-based recommendations | Pre-defined portfolios (Core, Growth, Dividend, ESG, REITs, Defensive) with ETFs and stocks |
| Suitability / match to profile | Suitability score (risk-level + tolerance penalties), filter ≥ 60, top 3 |
| Explainable outcomes | Customer scenarios (personas + suitability table + flowchart) |
| Multi-dimensional profile | Goal, horizon, loss tolerance, volatility, experience, diversification, liquidity, etc. |
| Reduce bias / rule-based advice | No free-form input; fixed questionnaire → score → filter → output |

---

## 6. Research That Discloses or Describes Their Logic (Questionnaire Weighting & Recommendation)

Many robo-advisors do **not** publish how they weight questions or build recommendations. The sources below are ones that **do** describe methodology (questionnaire design, scoring, or recommendation logic). Use them to justify that (1) weighting and scoring can be made explicit, and (2) recommendation logic can be documented.

### 6.1 Academic Paper with Full Recommendation Logic: RRA and Optimal Portfolios

**Gaspar, R. M., & Oliveira, M. (2024). Robo Advising and Investor Profiling.**  
*FinTech*, 3(1), 102–115. MDPI. https://www.mdpi.com/2674-1032/3/1/7

**What they disclose:**

- **Investor profiling:** They use **Relative Risk Aversion (RRA)** from expected-utility theory. RRA is a single number that discriminates investors beyond “conservative / moderate / aggressive.”
- **Formula for risk tolerance (utility):**  
  They use  
  \( U(R) = R - \frac{1}{2} \text{RRA} \cdot (R^2 + \sigma^2) \)  
  (return \(R\), volatility \(\sigma\)). Higher RRA ⇒ more risk-averse.
- **Recommendation logic:** For each RRA level, the **optimal portfolio** maximizes expected utility subject to no short-selling. So the “recommendation” is the solution to a stated optimization problem (mean–variance inputs + RRA).
- **RRA range:** They consider RRA from −1 (risk-loving) to 6 (very risk-averse); literature often uses 0–3 as “realistic.”
- **Comparison:** They compare these RRA-optimal portfolios to Riskalyze’s conservative/moderate/aggressive portfolios and find Riskalyze relatively conservative.

**Why it helps you:**  
This paper **writes down** the recommendation rule (utility function + optimization). You can say: “Similar to Gaspar & Oliveira (2024), we use an explicit rule to map investor profile to recommended portfolios; we use a weighted questionnaire score and a suitability filter instead of RRA optimization.”

---

### 6.2 Morningstar: Published Methodology for Risk Profiler and Comfort Range

**Morningstar Risk Profiler & Risk Comfort Range (methodology documents):**

- **Morningstar Risk Profiler Methodology** (e.g. v3):  
  https://developer.morningstar.com/content/hidden-from-navigation/MorningstarRiskProfilerMethodology_v3.pdf  
- **Morningstar Risk Comfort Range Methodology** (e.g. v3):  
  https://developer.morningstar.com/content/hidden-from-navigation/MorningstarRiskComfortRangeMethodology_v3.pdf  
- **Morningstar Portfolio Risk Score:**  
  https://developer.morningstar.com/content/hidden-from-navigation/MorningstarPortfolioRiskScoreMethodology.pdf  

**What they disclose:**

- **Questionnaire:** Based on **FinaMetrica**-style psychometric design. Often **25 questions** (or a shorter **10-question** version). One question asks the user to **choose among 7 portfolios** that differ by risk/return.
- **Scoring dimensions:** Risk tolerance is scored using **three factors:**  
  (1) Time horizon and income needs  
  (2) Long-term goals and investment expectations  
  (3) Short-term risk attitudes and tolerance for volatility  
- **Score interpretation:** Results are **compared to a large normative sample** (population) so the user gets a risk tolerance score and a risk group.
- **Recommendation step:** The risk tolerance score is **adjusted** by time horizon and other factors to produce a **“Risk Comfort Range”** of suitable portfolio risk scores. That range is then matched to actual portfolios (Portfolio Risk Score methodology).

**Why it helps you:**  
Shows that **questionnaire structure** (multiple dimensions, 7-portfolio choice) and **mapping from score to “suitable range”** can be and are documented. Your 10 questions and “score → category → allocation” are in the same spirit; you make the **weights** explicit (they don’t publish exact weights).

---

### 6.3 FinaMetrica (Used by Morningstar): Psychometric Risk Tolerance

**FinaMetrica / riskprofiling.com:**  
- “How it Works”: https://riskprofiling.com/How-it-Works  
- “Measuring Risk Tolerance” (PDF): https://riskprofiling.com/WWW_RISKP/media/RiskProfiling/Downloads/MeasuringRiskTolerance.pdf  

**What they disclose:**

- **Three concepts:**  
  **Risk Tolerance** (comfort with risk), **Risk Required** (risk needed for goals), **Risk Capacity** (ability to bear loss).
- **Question design:** Emphasizes **loss aversion** and **self-assessment**; questions informed by **prospect theory** and behavioral economics. Research suggests these predict allocation behavior better than pure economic-theory questions.
- **Scoring:** **Psychometric** (validated scale). Scores are **normed** (e.g. US database); clients see how they compare to other test-takers.
- **Validation:** Large sample (e.g. 850,000+ tests), re-norming, stability across bear markets.
- **Use in advice:** Advisors use the scored profile to **map to portfolio allocations** and set expectations.

**Why it helps you:**  
Supports that **questionnaire design** (loss tolerance, self-assessment, behavioral framing) and **score → allocation** are standard; you implement a **transparent weighting** of similar themes (goal, loss tolerance, volatility, etc.).

---

### 6.4 Riskalyze / Nitrogen: Risk Number and Matching Rule

**Sources:**  
- Nitrogen (formerly Riskalyze): “What is the Risk Number?” (e.g. nitrogenwealth.com)  
- “How is the Riskalyze Risk Number Calculated?” (advisor sites, e.g. lasallest.com)  
- “Math Behind The Risk Number” (e.g. rossifg.com)  

**What they disclose:**

- **Output:** A **“Risk Number”** on a **1–99** scale (often shown like a speed limit sign).
- **Questionnaire:** About **12 questions** to capture willingness to take risk (no exact weights published).
- **Logic (high level):** Based on **downside risk over a 6-month horizon**: e.g. 95% probability range for portfolio outcome. Uses **Modern Portfolio / Prospect Theory**, historical volatility and correlation (e.g. from 2008 onward). Investments classified (e.g. standard, tactical, rate-sensitive) to refine the number.
- **Rough mapping:** Risk Number 20s ≈ −2% downside; 30s ≈ −5%; 60s ≈ −12%; 80s ≈ −18%.
- **Recommendation rule:** Advisors often treat Risk Numbers **within 5–10 points** as “close enough” for **matching** a client to a portfolio.

**Why it helps you:**  
Shows a **numeric risk score** (1–99) and an **explicit matching rule** (“within 5–10 points”). Your **suitability threshold (≥ 60)** and **top 3** are a different but equally explicit rule.

---

### 6.5 Papers That Describe Logic Without Full Formulas

| Source | What they describe |
|--------|--------------------|
| **“To Advise, or Not to Advise” (SSRN)** | Compares how robo-advisors evaluate risk; finds **some questions do not affect** risk categorization—supports the need for **meaningful weighting** (as you do with 8 weighted questions). |
| **“How Risk Profiles of Investors Affect Robo-Advised Portfolios” (Frontiers/PMC)** | Study of **53 platforms** (US & Germany): algorithms **do** differentiate risk profiles and change allocations; **expertise and geography** affect recommendations. Shows that **profile → allocation** is the standard pipeline. |
| **“Developing a Security Risk Assessment based Smart Beta Portfolio Model for Robo Advising” (AABFJ)** | **Risk categories** (low/moderate/high/very high) and **smart beta factors** (quality, value, alpha, momentum) used to **build portfolios per category**. So “risk category → portfolio construction” is described. |
| **“Robo-Advisory: From Investing Principles and Algorithms to Future Developments” (SSRN)** | Overview of **mean–variance** and **ETF-based** allocation as common robo-advisor methods—aligns with fund-based, rule-based recommendation. |

---

### 6.6 Summary: What You Can Say

- **Questionnaire weighting:**  
  “Morningstar/FinaMetrica and academic work (e.g. Gaspar & Oliveira, FinaMetrica) show that risk profiling can use multiple dimensions and validated scoring; we make our **weights explicit** (e.g. goal 20%, loss tolerance 15%) in line with calls for transparency.”
- **Recommendation logic:**  
  “Recommendation can be written down: Gaspar & Oliveira (2024) use RRA and an optimization problem; Riskalyze/Nitrogen use a Risk Number and a 5–10 point matching rule; Morningstar use a Risk Comfort Range. We use a **suitability score and a threshold (≥ 60) plus top 3**, which we document in full.”

---

## 7. References and Further Reading (Full List)

You can cite or read more from:

1. **Risk profiling and questionnaires**  
   - “To Advise, or Not to Advise — How Robo-Advisors Evaluate the Risk Preferences of Private Investors” (SSRN).  
   - “Risk profiling question investigation for robo-advisor” (OUCI).  
   - “Robo Advising and Investor Profiling” (MDPI, *Journal of Risk and Financial Management*).

2. **Risk profiles and portfolio outcomes**  
   - “How Risk Profiles of Investors Affect Robo-Advised Portfolios” (Frontiers in Artificial Intelligence / PMC).

3. **Benefits and effectiveness**  
   - “Who Benefits from Robo-Advising? Evidence from Machine Learning” (SSRN).  
   - “The diversification and welfare effects of robo-advising” (*Journal of Financial Economics*).  
   - “The Promises and Pitfalls of Robo-Advising” (*Review of Financial Studies*).

4. **Investor characteristics and adoption**  
   - “Investor Characteristics and their Impact on the Decision to use a Robo-advisor” (Springer).

5. **Risk tolerance and questionnaire design**  
   - “Financial Risk Tolerance: A Psychometric Review” (CFA Institute).  
   - FPA/Kitces-style discussions on risk tolerance questionnaires (industry/practice).

6. **Sources that disclose or describe questionnaire/recommendation logic (see Section 6)**  
   - Gaspar & Oliveira (2024), “Robo Advising and Investor Profiling,” MDPI *FinTech* 3(1):102–115. https://www.mdpi.com/2674-1032/3/1/7  
   - Morningstar Risk Profiler Methodology (PDF, developer.morningstar.com).  
   - Morningstar Risk Comfort Range Methodology (PDF).  
   - Morningstar Portfolio Risk Score Methodology (PDF).  
   - FinaMetrica: riskprofiling.com (How it Works; Measuring Risk Tolerance PDF).  
   - Riskalyze/Nitrogen Risk Number: nitrogenwealth.com; advisor articles on “how Risk Number is calculated.”  
   - “Developing a Security Risk Assessment based Smart Beta Portfolio Model for Robo Advising” (AABFJ).  
   - “Robo-Advisory: From Investing Principles and Algorithms to Future Developments” (SSRN 3776826).

(Replace with full citations and URLs as required by your course.)

---

## 8. Short “Why We Use This” Summary (For Presentation or Report)

- **Robo-advisors** are supported by research as a way to improve diversification, lower fees, and reduce behavioral bias, especially for less experienced or under-diversified investors.
- **Questionnaire-based risk profiling** with a 0–100 score and categories is standard in the literature; we add **documented weights and rules** for transparency.
- **Fund-based (ETF/theme) portfolios** and **suitability-based filtering** (≥ 60, top 3) match research that stresses risk-profile alignment and diversified, indexed exposure.
- **Explicit methodology** (rules, logic, scenarios) addresses the common criticism that robo-advisors do not disclose how they advise.

Together, this gives you **research-backed support** for why you use this kind of AI robo advisor and how your design choices are justified by existing work.
