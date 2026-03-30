import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PreAudit — Know What Your Auditor Would Flag",
    page_icon="📊",
    layout="wide"
)

# --- HEADER ---
st.title("📊 PreAudit")
st.markdown("### Pre-audit diagnostic tool for small businesses and freelancers")
st.markdown("#### *Know what your auditor would flag — before you're in that room.*")
st.markdown(
    "For freelancers, small businesses, and early-stage startups who want to "
    "understand where they stand financially."
)
st.markdown("*Built using SME financial benchmarks and audit-based frameworks.*")

st.markdown("""
**What this tool does:**
- 🔍 Identify your financial risk position
- 📋 Assess your audit readiness
- 🚩 Highlight what a CA or auditor would flag
""")

st.divider()

# --- MODULE SELECTION ---
st.markdown("#### Select your region to get the right framework")
module = st.radio(
    "",
    ["🇬🇧 UK — Freelancer / Small Business", "🇮🇳 India — SME / Startup"],
    horizontal=True
)
st.divider()

# --- STEP 1: INPUTS ---
st.header("Step 1 — Enter Your Financial Details")
st.markdown("*These are the numbers a CA or auditor would ask for first. You should know them.*")

col1, col2 = st.columns(2)

with col1:
    if "🇬🇧" in module:
        st.markdown("**Revenue & Profitability**")
        revenue = st.number_input("Annual Revenue (£)", min_value=0.0, step=1000.0)
        expenses = st.number_input("Annual Expenses (£)", min_value=0.0, step=1000.0)
        cash = st.number_input("Cash in Bank (£)", min_value=0.0, step=500.0)
    else:
        st.markdown("**Revenue & Profitability**")
        revenue = st.number_input("Annual Revenue (₹)", min_value=0.0, step=10000.0)
        expenses = st.number_input("Annual Expenses (₹)", min_value=0.0, step=10000.0)
        cash = st.number_input("Cash in Bank (₹)", min_value=0.0, step=5000.0)

with col2:
    if "🇬🇧" in module:
        st.markdown("**Debt & Obligations**")
        debt = st.number_input("Total Debt / Liabilities (£)", min_value=0.0, step=500.0)
        fixed_costs = st.number_input("Monthly Fixed Costs (£)", min_value=0.0, step=100.0)
        receivables = st.number_input("Money Owed to You / Receivables (£)", min_value=0.0, step=100.0)
    else:
        st.markdown("**Debt & Obligations**")
        debt = st.number_input("Total Debt / Liabilities (₹)", min_value=0.0, step=5000.0)
        fixed_costs = st.number_input("Monthly Fixed Costs (₹)", min_value=0.0, step=1000.0)
        receivables = st.number_input("Money Owed to You / Receivables (₹)", min_value=0.0, step=1000.0)

st.divider()

# --- STEP 2: AUDIT CHECKLIST ---
st.header("Step 2 — Audit Readiness Check")
st.markdown("*Answer honestly. A CA would ask you exactly these questions in the first ten minutes.*")

if "🇬🇧" in module:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("I have a separate business bank account")
    q3 = st.checkbox("I am registered for VAT — or I know exactly where I stand on the threshold")
    q4 = st.checkbox("I file my self-assessment or company accounts on time, every year")
    q5 = st.checkbox("I have financial records going back at least 2 years")
else:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("I have a separate business bank account")
    q3 = st.checkbox("I am registered for GST — or I know exactly where I stand on the threshold")
    q4 = st.checkbox("I file GST returns quarterly, consistently and on time")
    q5 = st.checkbox("I maintain records that a CA could review without preparation")

st.divider()

# --- RUN BUTTON ---
if st.button("Run Pre-Audit Check", type="primary", use_container_width=True):

    if revenue == 0:
        st.error("Please enter your annual revenue to run the diagnostic.")

    else:
        # --- CALCULATIONS ---
        currency = "£" if "🇬🇧" in module else "₹"
        profit = revenue - expenses
        profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
        expense_ratio = (expenses / revenue) * 100 if revenue > 0 else 0
        debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
        current_ratio = (cash + receivables) / (debt if debt > 0 else 1)

        checklist = [q1, q2, q3, q4, q5]
        audit_score = (sum(checklist) / len(checklist)) * 100

        # --- RISK SCORING ---
        risk_points = 0

        if "🇬🇧" in module:
            if profit_margin >= 20:
                risk_points += 0
            elif profit_margin >= 10:
                risk_points += 15
            else:
                risk_points += 30
        else:
            if profit_margin >= 15:
                risk_points += 0
            elif profit_margin >= 8:
                risk_points += 15
            else:
                risk_points += 30

        if current_ratio >= 2:
            risk_points += 0
        elif current_ratio >= 1:
            risk_points += 15
        else:
            risk_points += 30

        if debt_to_revenue <= 30:
            risk_points += 0
        elif debt_to_revenue <= 60:
            risk_points += 20
        else:
            risk_points += 40

        overall_risk = max(0, 100 - risk_points)

        # --- GOVERNANCE SCORE ---
        governance_score = min(audit_score * 0.6 + (20 if q2 else 0) + (20 if q1 else 0), 100)

        # --- RED FLAGS ---
        red_flags = []
        if profit_margin < 0:
            red_flags.append("🚨 Your business is operating at a loss — expenses exceed revenue.")
        if expense_ratio > 85:
            red_flags.append("⚠️ Expenses are consuming more than 85% of revenue — very little financial buffer.")
        if cash < (fixed_costs * 2):
            red_flags.append("⚠️ Cash reserves below 2 months of fixed costs — liquidity risk.")
        if debt_to_revenue > 60:
            red_flags.append("🚨 Debt is high relative to revenue — significant leverage risk.")
        if current_ratio < 1:
            red_flags.append("🚨 Current ratio below 1 — may struggle to meet short-term obligations.")
        if "🇬🇧" in module and revenue > 85000 and not q3:
            red_flags.append("⚠️ Revenue may be above the VAT threshold (£85,000). Verify your registration status immediately.")
        if "🇮🇳" in module and revenue > 2000000 and not q3:
            red_flags.append("⚠️ Revenue may be above the GST threshold (₹20 Lakhs). Verify your registration status immediately.")

        # --- TOP 3 ACTIONS ---
        actions = []
        if profit_margin < 0:
            actions.append("🔴 Your business is loss-making. Review your expense structure immediately and identify what can be reduced or eliminated.")
        if expense_ratio > 85:
            actions.append("🔴 Reduce your expense ratio below 80% — identify your top 3 costs and assess whether each is necessary at its current level.")
        if cash < fixed_costs * 2:
            actions.append("🟠 Build at least 2 months of fixed cost coverage in cash reserves before taking on new commitments.")
        if debt_to_revenue > 60:
            actions.append("🟠 Reduce debt exposure before taking on additional financial commitments or applying for further credit.")
        if audit_score < 60:
            actions.append("🟡 Address your missing compliance checklist items before any CA or audit review — these are the first things an auditor checks.")
        if current_ratio < 1:
            actions.append("🔴 Your liquidity position is critical. Prioritise converting receivables to cash and review your short-term debt obligations.")
        if not actions:
            actions.append("✅ No immediate corrective action required. Maintain your current financial discipline and revisit this tool quarterly.")

        # --- STEP 3: RESULTS ---
        st.header("Step 3 — Your Pre-Audit Diagnostic Results")
        st.markdown("*Here is how your business looks through an auditor's lens.*")
        st.divider()

        # THREE SCORES
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Overall Financial Risk**")
            if overall_risk >= 70:
                st.success(f"## {overall_risk:.0f} / 100\n**Low Risk** ✅\n\nYour financial position is stable. Focus on maintaining controls and improving audit readiness.")
            elif overall_risk >= 45:
                st.warning(f"## {overall_risk:.0f} / 100\n**Moderate Risk** ⚠️\n\nThere are areas that need attention. Review the audit flags and priority actions below.")
            else:
                st.error(f"## {overall_risk:.0f} / 100\n**High Risk** 🚨\n\nImmediate attention needed. Do not wait for a CA review to surface these issues.")

        with col2:
            st.markdown("**Audit Readiness**")
            if audit_score >= 80:
                st.success(f"## {audit_score:.0f}%\n**Well Prepared** ✅\n\nYour compliance foundations are solid. You are ready for a CA review.")
            elif audit_score >= 50:
                st.warning(f"## {audit_score:.0f}%\n**Partially Prepared** ⚠️\n\nSome compliance gaps exist. Address these before any formal review.")
            else:
                st.error(f"## {audit_score:.0f}%\n**Not Audit Ready** 🚨\n\nSignificant compliance gaps. A CA review right now would surface multiple issues.")

        with col3:
            st.markdown("**Governance Score**")
            if governance_score >= 70:
                st.success(f"## {governance_score:.0f}%\n**Strong Controls** ✅\n\nGood internal controls and documentation practices in place.")
            elif governance_score >= 40:
                st.warning(f"## {governance_score:.0f}%\n**Needs Attention** ⚠️\n\nSome governance gaps. Focus on documentation and separation of finances.")
            else:
                st.error(f"## {governance_score:.0f}%\n**Weak Governance** 🚨\n\nSignificant control weaknesses. Priority: separate business banking and proper record keeping.")

        st.divider()

        # KEY FINANCIAL RATIOS
        st.subheader("Key Financial Ratios")
        st.markdown("*The ratios a CA calculates in the first pass of your accounts — benchmarked against SME standards.*")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Net Profit Margin",
                f"{profit_margin:.1f}%",
                help="Benchmark: ≥20% healthy (UK), ≥15% healthy (India). Below 10%/8% is high risk."
            )
            st.metric(
                "Expense Ratio",
                f"{expense_ratio:.1f}%",
                help="Expenses as % of revenue. Below 80% healthy. Above 85% is a warning signal."
            )
        with col2:
            st.metric(
                "Debt-to-Revenue Ratio",
                f"{debt_to_revenue:.1f}%",
                help="Total debt relative to annual revenue. Below 30% low risk. Above 60% high risk."
            )
            st.metric(
                "Current Ratio",
                f"{current_ratio:.2f}",
                help="Liquidity: (cash + receivables) / debt. Above 2.0 healthy. Below 1.0 is a risk signal."
            )

        st.divider()

        # AUDIT FLAGS
        st.subheader("Audit Flags")
        st.markdown("*These are the issues a CA would flag immediately in an initial review.*")
        if red_flags:
            for flag in red_flags:
                st.markdown(flag)
        else:
            st.success("✅ No audit flags detected. Your numbers are telling a clean story.")

        st.divider()

        # TOP PRIORITY ACTIONS
        st.subheader("Top Priority Actions")
        st.markdown("*Based on your results, these are the most important steps to take next.*")
        for action in actions[:3]:
            st.markdown(f"- {action}")

        st.divider()

        # OVERALL ASSESSMENT
        st.subheader("Overall Assessment")
        if overall_risk >= 70:
            summary = (
                f"Your business is in a relatively healthy position — risk score {overall_risk:.0f}/100. "
                f"Profit margins and liquidity look stable. "
                f"Your audit readiness sits at {audit_score:.0f}% — "
                f"{'focus on the checklist gaps before your next CA review.' if audit_score < 100 else 'you are well prepared for a CA review.'}"
            )
        elif overall_risk >= 45:
            weak_area = (
                "cash reserves" if cash < fixed_costs * 2
                else "debt levels" if debt_to_revenue > 60
                else "profit margins"
            )
            summary = (
                f"Your business shows moderate risk — score {overall_risk:.0f}/100. "
                f"The main area of concern is your {weak_area}. "
                f"This is manageable now but needs attention before it becomes critical. "
                f"Audit readiness at {audit_score:.0f}% — address the checklist gaps before any CA review."
            )
        else:
            summary = (
                f"Your business is showing high risk signals — score {overall_risk:.0f}/100. "
                f"Immediate attention is needed. "
                f"Use this report as a starting point for an urgent conversation with your accountant or CA. "
                f"Do not wait for a formal audit to surface these issues."
            )
        st.info(f"💡 {summary}")

        st.divider()

        # SCENARIO / STRESS TEST
        st.subheader("Stress Test — What If?")
        st.markdown("*See how your business holds up under pressure. This is what auditors and investors model.*")

        scenario_drop = st.slider("Revenue drops by:", 0, 50, 20, format="%d%%")
        new_revenue = revenue * (1 - scenario_drop / 100)
        new_profit = new_revenue - expenses
        new_margin = (new_profit / new_revenue) * 100 if new_revenue > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Revenue After Drop",
                f"{currency}{new_revenue:,.0f}",
                delta=f"-{scenario_drop}%"
            )
        with col2:
            st.metric(
                "New Profit / Loss",
                f"{currency}{new_profit:,.0f}",
                delta=f"{currency}{new_profit - profit:,.0f}"
            )
        with col3:
            st.metric(
                "New Profit Margin",
                f"{new_margin:.1f}%",
                delta=f"{new_margin - profit_margin:.1f}%"
            )

        if new_profit < 0:
            st.error(f"🚨 A {scenario_drop}% revenue drop would push your business into a loss. Your current cost base is not sustainable at lower revenue.")
        elif new_margin < 10:
            st.warning(f"⚠️ A {scenario_drop}% revenue drop leaves your margin dangerously thin at {new_margin:.1f}%. Limited room for unexpected costs.")
        else:
            st.success(f"✅ Your business remains profitable under a {scenario_drop}% revenue drop — margin holds at {new_margin:.1f}%.")

        st.divider()

        # DOWNLOAD BUTTON (placeholder)
        st.button("📄 Download Full Pre-Audit Report (PDF) — Coming Soon", disabled=True)

        st.divider()

        # FOOTER
        st.markdown(
            "*PreAudit is a diagnostic tool, not financial advice. "
            "It does not replace your accountant, CA, or auditor. "
            "It helps you walk into that conversation better prepared.*"
        )
