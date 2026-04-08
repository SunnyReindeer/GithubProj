# Meeting Prep: Robo-Advisor – #1 Processes & #2 Filter

Short guide for your professor meeting: what to show for **#1 Processes** (rules + user walkthrough) and **#2 Filter** (customer scenarios, similarity, stable matching).

---

## Part 1: What You Have Ready (#1 – Processes)

### 1.1 Rule (Process / Logic)

**Where:** `AI_ROBO_ADVISOR_RULES.md`

**What to say:**  
“The robo-advisor logic is fully specified: questionnaire → risk score (0–100) → risk category → suitability score per portfolio → filter (≥60) → top 3. All thresholds, formulas, and validation rules are written in one document.”

**What to show:**
- **Section 0 (Visual Summary)** – Mermaid diagrams: step prerequisites, risk score flow, risk tolerance scale, suitability flow, portfolio filter.
- **Section 5 (Risk Tolerance)** – Score ranges 25, 50, 75 → Conservative / Moderate / Aggressive / Very Aggressive.
- **Section 9–10 (Suitability & Filter)** – Suitability formula, threshold 60, max 3 portfolios.

### 1.2 User Walkthrough + Example

**Where:** `AI_ROBO_ADVISOR_USER_WALKTHROUGH.md`

**What to say:**  
“We have a step-by-step user walkthrough: Tab 1 (questionnaire → Analyze) → Tab 2 (Get recommendations) → Tab 3 (Select portfolio, see AI labels) → Tab 4 (Plan + download). Plus a Mermaid flowchart of the same flow.”

**What to show:**
- **Entry → Step 1–4** – Short narrative: what the user sees and does in each tab.
- **Mermaid user walkthrough diagram** – Same flow as a flowchart.
- **Summary table** – Step, tab, user action, outcome.

**Optional live example:**  
Open the app → complete 10 questions → “Analyze My Risk Profile” → go to Fund Portfolios → “Get Fund Portfolio Recommendations” → show the 1–3 portfolios and their match %.

---

## Part 2: Filter – How to Make It Convincing (#2)

#2 is about **filter design**: customer scenarios, **similarity** (how we match), and **stable matching** (research angle). Below: how to design it and what to say.

---

### 2.1 Customer Scenarios (Convincing Examples)

**Problem:** “Scenario of customer” feels 沒說服力 (not convincing) if it’s vague.

**Design approach:** Define **concrete customer personas** with fixed questionnaire answers, then show:
1. Risk score and category  
2. Suitability score for each portfolio  
3. Which portfolios **pass the filter** (≥60)  
4. **Top 3** recommended  

That shows exactly how the filter behaves for different “types” of customers.

**Example scenarios (4 personas):**

| Persona | Profile | Goal / situation |
|--------|---------|-------------------|
| **Sarah (Conservative)** | Near retirement, preserve capital | Low risk, bonds-heavy |
| **Alex (Moderate)** | Mid-career, balanced growth | Medium risk, diversified |
| **Jordan (Aggressive)** | Young, high risk tolerance | Growth, crypto/equity |
| **Sam (Very Aggressive)** | High risk tolerance, long horizon | Max return, highest risk |

**Concrete numbers (example):**

| Persona | Risk score | Category | Portfolios passing filter (≥60) | Top 3 shown |
|---------|------------|----------|----------------------------------|-------------|
| Sarah | 22 | Conservative | Defensive, Dividend, Core, ESG, REITs | Defensive, Dividend, Core |
| Alex | 42 | Moderate | Dividend, Defensive, Core, ESG, REITs, (Growth borderline) | Dividend, Core, ESG |
| Jordan | 64 | Aggressive | Growth, Core, ESG, REITs | Growth, Core, ESG |
| Sam | 82 | Very Aggressive | Growth only (others &lt; 60) | Growth |

So for each scenario you can say: “This customer has this risk score and category; the filter keeps only portfolios with suitability ≥ 60; we show the top 3.” That makes the filter **concrete and verifiable**.

**Where it is:**  
See **`ROBO_ADVISOR_CUSTOMER_SCENARIOS.md`** – four personas (Sarah, Alex, Jordan, Sam) with risk score, category, suitability per portfolio, and top 3 shown. Numbers are consistent with your rules.

---

### 2.2 Similarity & Filter (How We Design It)

**What to say:**  
“We match **customers to portfolios** by **similarity**. Similarity is the **suitability score** (0–100): it measures how well a portfolio’s risk level and style fit the customer’s risk profile.”

**Similarity definition (current design):**
1. **Risk-level fit:**  
   `risk_diff = |portfolio.risk_level - customer.risk_score/10|`  
   Lower difference ⇒ higher similarity.
2. **Tolerance fit:**  
   Extra penalty if the portfolio is “too risky” for a Conservative customer, or “too safe” for an Aggressive / Very Aggressive customer.
3. **Suitability score:**  
   `score = 100 - (risk_diff × 10) - tolerance_penalty`, clamped to 0–100.

**Filter design:**
- **Step 1:** Compute similarity (suitability) for all 6 portfolios.
- **Step 2:** **Filter** – keep only portfolios with similarity **≥ 60** (threshold).
- **Step 3:** **Sort** by similarity descending.
- **Step 4:** **Return top 3** (or fewer if fewer pass).

So: **“Similarity” = suitability score; “filter” = threshold 60 + cap of 3.** You can say: “We use a similarity-based filter: only sufficiently similar portfolios are shown, and we limit to the top 3 to avoid overload.”

**One sentence for professor:**  
“We define similarity between customer and portfolio by risk alignment and tolerance fit; the filter keeps only portfolios above a similarity threshold (60) and returns the top 3.”

---

### 2.3 Stable Matching (Research Angle – Hard)

**What it is:**  
**Stable matching** (e.g. **Gale–Shapley**) assigns two sides (e.g. customers and portfolios) so that no **blocking pair** exists: no customer and no portfolio would both prefer each other over their current match.

**How it relates to this project:**
- **Customers** have a **preference order** over portfolios (e.g. by suitability score: best match first).
- **Portfolios** can be given a **preference order** over customers (e.g. by “fit” or by capacity rules).
- **Stable matching** would assign each customer to (e.g.) one portfolio, or each portfolio to a set of customers, so the assignment is **stable**.

**What we do now vs stable matching:**

| Aspect | Current design | Stable matching (research) |
|--------|----------------|----------------------------|
| Output | Top 3 portfolios per customer (no single “match”) | One-to-one or many-to-one assignment |
| Preference | Customer → portfolio similarity only | Two-sided: customer preferences + portfolio preferences (or capacity) |
| Goal | “Show best options” | “Assign so no pair wants to switch” |
| Use case | Single customer, many portfolios | Many customers, limited slots/capacity |

**When stable matching is useful:**  
When there are **many customers** and **limited capacity** (e.g. each portfolio can only “take” a limited number of customers). Then you need a clear rule for who gets which portfolio; Gale–Shapley gives a stable assignment.

**What you can say in the meeting:**
1. “Right now we use **similarity-based filtering**: we rank portfolios by suitability and show the top 3 above a threshold. That’s our ‘matching’.”
2. “A **research extension** would be **stable matching** (Gale–Shapley): if we had many customers and limited capacity per portfolio, we could define preferences on both sides and compute a stable assignment. That would align with matching theory and make the design more rigorous.”

**If professor asks “How would you do stable matching?”**  
- **Customers’ preference list:** Order portfolios by suitability score (descending).  
- **Portfolios’ preference list:** Order customers by suitability score (descending) or by “fit” (e.g. risk alignment).  
- **Algorithm:** Run Gale–Shapley (e.g. customers propose to portfolios in order of preference; portfolios accept or reject).  
- **Result:** Each customer assigned to at most one portfolio, each portfolio to a set of customers (if many-to-one), and the assignment is stable.

**Reference:**  
- Gale–Shapley: e.g. Wikipedia “Gale–Shapley algorithm”, or “Stable matching algorithm”.  
- Robo-advisory context: research on “customer–advisor assignment” or “portfolio assignment” in robo-advisory; our current filter is similarity-based; stable matching would be an added theoretical layer.

---

## Quick Checklist for the Meeting

**#1 Processes**
- [ ] Show **rules**: `AI_ROBO_ADVISOR_RULES.md` – Section 0 (visuals) + suitability/filter sections.
- [ ] Show **user walkthrough**: `AI_ROBO_ADVISOR_USER_WALKTHROUGH.md` – steps + Mermaid diagram.
- [ ] (Optional) Live demo: one full flow (questionnaire → analyze → recommendations).

**#2 Filter**
- [ ] **Customer scenarios:** 4 personas (e.g. Sarah, Alex, Jordan, Sam) with risk score, category, which portfolios pass filter, top 3.
- [ ] **Similarity:** “Similarity = suitability score (risk + tolerance fit); filter = keep ≥60, show top 3.”
- [ ] **Stable matching:** “Current design is similarity-based; a research extension is stable matching (Gale–Shapley) for many customers and limited capacity.”

If you want, next step can be: (1) a separate `ROBO_ADVISOR_CUSTOMER_SCENARIOS.md` with the 4 personas and exact suitability numbers computed from your code, or (2) one more page that only explains “Similarity & Filter” and “Stable matching” for handing to the professor.
