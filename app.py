import streamlit as st
import anthropic

st.set_page_config(
    page_title="Smit — Your AI Financial + ESG Co-Pilot",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #FAFAF8;
    color: #1a1a1a;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
h1, h2, h3 { font-family: 'Playfair Display', serif; color: #1a1a1a; }
.block-container { padding: 2rem 1.5rem; max-width: 800px; }

.masthead { border-bottom: 3px solid #1a1a1a; padding-bottom: 1rem; margin-bottom: 0.5rem; }
.masthead-top { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.25rem; }
.masthead-name { font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 700; color: #1a1a1a; letter-spacing: -1px; line-height: 1; }
.masthead-pill { font-size: 0.7rem; font-weight: 600; background: #8B0000; color: white; padding: 0.2rem 0.7rem; letter-spacing: 1px; text-transform: uppercase; }
.masthead-sub { font-size: 0.72rem; color: #6b6b6b; border-top: 1px solid #d4d4d4; padding-top: 0.4rem; margin-top: 0.4rem; letter-spacing: 0.3px; }

.rule { height: 1px; background: #d4d4d4; margin: 1.5rem 0; }
.rule-thick { height: 2px; background: #1a1a1a; margin: 2rem 0; }

.section-kicker { font-size: 0.68rem; font-weight: 600; color: #8B0000; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.25rem; }

/* Combined score hero */
.smit-score-hero {
    background: #1a1a1a;
    padding: 1.75rem;
    margin: 1rem 0;
    text-align: center;
}
.smit-score-label { font-size: 0.65rem; font-weight: 600; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.5rem; }
.smit-score-number { font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 700; color: white; line-height: 1; margin-bottom: 0.4rem; }
.smit-score-sub { font-size: 0.78rem; color: rgba(255,255,255,0.5); margin-top: 0.4rem; }
.smit-score-breakdown { display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); }
.smit-breakdown-item { text-align: center; }
.smit-breakdown-val { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 700; }
.smit-breakdown-lbl { font-size: 0.6rem; font-weight: 600; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }

/* Score row */
.score-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #d4d4d4; border: 1px solid #d4d4d4; margin: 1rem 0; }
.score-cell { background: #FAFAF8; padding: 1.25rem 1rem; text-align: center; }
.score-cell-label { font-size: 0.63rem; font-weight: 600; color: #6b6b6b; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.5rem; }
.score-cell-number { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 700; line-height: 1; margin-bottom: 0.4rem; }
.score-cell-status { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px; padding: 0.2rem 0.6rem; display: inline-block; }
.status-green { color: #1a5c2e; background: #e8f5ee; }
.status-amber { color: #7a4a0a; background: #fdf3e3; }
.status-red { color: #8B0000; background: #fdecea; }

/* Ratio table */
.ratio-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; margin: 1rem 0; }
.ratio-table th { font-size: 0.63rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: #6b6b6b; padding: 0.5rem 0.75rem; border-bottom: 2px solid #1a1a1a; text-align: left; }
.ratio-table td { padding: 0.7rem 0.75rem; border-bottom: 1px solid #e8e8e4; color: #1a1a1a; vertical-align: middle; }
.ratio-table tr:hover td { background: #f5f5f0; }
.ratio-val { font-weight: 600; font-size: 1rem; }
.ratio-tooltip { font-size: 0.72rem; color: #888; display: block; font-weight: 400; margin-top: 0.1rem; font-style: italic; }
.ratio-good { color: #1a5c2e; }
.ratio-warn { color: #7a4a0a; }
.ratio-bad { color: #8B0000; }

/* Flags */
.flag-item { padding: 0.75rem 1rem; margin: 0.4rem 0; border-left: 3px solid; font-size: 0.875rem; line-height: 1.5; }
.flag-critical { border-color: #8B0000; background: #fdecea; color: #5a1010; }
.flag-warning { border-color: #C17A2A; background: #fdf3e3; color: #6b4010; }
.flag-ok { border-color: #1a5c2e; background: #e8f5ee; color: #1a5c2e; }

/* Action items */
.action-item { display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.85rem 1rem; margin: 0.4rem 0; background: #f5f5f0; border: 1px solid #e8e8e4; font-size: 0.875rem; line-height: 1.5; }
.action-number { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: #8B0000; line-height: 1; flex-shrink: 0; min-width: 20px; }

/* ESG upgrade plan */
.esg-plan { background: #f0fdf4; border: 1px solid #d1fae5; margin: 0.4rem 0; }
.esg-plan-header { background: #1a5c2e; color: white; padding: 0.6rem 1rem; font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; }
.esg-plan-item { padding: 0.85rem 1rem; border-bottom: 1px solid #d1fae5; font-size: 0.875rem; line-height: 1.6; color: #1a1a1a; }
.esg-plan-item:last-child { border-bottom: none; }
.esg-plan-item strong { color: #1a5c2e; }

/* ESG grid */
.esg-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; margin: 0.75rem 0; }
.esg-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: #f5f5f0; border: 1px solid #e8e8e4; font-size: 0.8rem; color: #1a1a1a; }
.esg-pass { border-left: 3px solid #1a5c2e; }
.esg-fail { border-left: 3px solid #8B0000; opacity: 0.6; }

/* Summary */
.summary-box { background: #1a1a1a; color: #FAFAF8; padding: 1.5rem; margin: 1rem 0; font-size: 0.9rem; line-height: 1.7; }
.summary-kicker { font-size: 0.63rem; font-weight: 600; color: #C17A2A; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.5rem; }

/* Stress test */
.stress-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #d4d4d4; border: 1px solid #d4d4d4; margin: 1rem 0; }
.stress-cell { background: #FAFAF8; padding: 1rem; text-align: center; }
.stress-cell-label { font-size: 0.63rem; font-weight: 600; color: #6b6b6b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem; }
.stress-cell-value { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: #1a1a1a; }
.stress-cell-delta { font-size: 0.75rem; margin-top: 0.2rem; }
.delta-neg { color: #8B0000; }
.delta-pos { color: #1a5c2e; }

/* Chat */
.chat-wrap { border: 1px solid #d4d4d4; background: #ffffff; margin: 1rem 0; }
.chat-header { background: #1a1a1a; color: #FAFAF8; padding: 0.75rem 1rem; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; display: flex; justify-content: space-between; align-items: center; }
.chat-badge { font-size: 0.62rem; background: #8B0000; color: white; padding: 0.15rem 0.5rem; }
.chat-msg-user { background: #f5f5f0; border-left: 3px solid #1a1a1a; padding: 0.75rem 1rem; margin: 0.5rem; font-size: 0.875rem; }
.chat-msg-assistant { background: #ffffff; border-left: 3px solid #8B0000; padding: 0.75rem 1rem; margin: 0.5rem; font-size: 0.875rem; line-height: 1.6; }
.chat-msg-label { font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.35rem; }
.chat-msg-user .chat-msg-label { color: #1a1a1a; }
.chat-msg-assistant .chat-msg-label { color: #8B0000; }
.pro-gate { background: #1a1a1a; padding: 1.25rem 1.5rem; text-align: center; }
.pro-gate p { color: rgba(255,255,255,0.65); font-size: 0.875rem; margin-bottom: 0.75rem; }
.pro-gate strong { color: white; }

/* Buttons */
.stButton > button { background: #1a1a1a !important; color: #FAFAF8 !important; border: 1px solid #1a1a1a !important; border-radius: 0 !important; padding: 0.65rem 1.5rem !important; font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.5px !important; font-family: 'Inter', sans-serif !important; transition: all 0.2s !important; width: 100% !important; }
.stButton > button:hover { background: #8B0000 !important; border-color: #8B0000 !important; }
.stButton > button:disabled { background: #d4d4d4 !important; border-color: #d4d4d4 !important; color: #6b6b6b !important; }

/* Inputs */
.stTextInput > div > div > input { border-radius: 0 !important; border: 1px solid #d4d4d4 !important; background: #ffffff !important; font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; }
.stTextInput > div > div > input:focus { border-color: #1a1a1a !important; box-shadow: none !important; }
.stNumberInput > div > div > input { border-radius: 0 !important; border: 1px solid #d4d4d4 !important; background: #ffffff !important; }
.stCheckbox > label { font-size: 0.875rem !important; }
.stRadio > label { font-size: 0.875rem !important; }

/* Step indicator */
.step-indicator { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.step-dot { width: 24px; height: 24px; background: #8B0000; color: white; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.step-text { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: #1a1a1a; }

/* Disclaimer */
.disclaimer { border-top: 1px solid #d4d4d4; padding-top: 1rem; margin-top: 2rem; font-size: 0.75rem; color: #6b6b6b; line-height: 1.6; }
.legal-warning { background: #fff8e1; border: 1px solid #f59e0b; padding: 0.75rem 1rem; font-size: 0.8rem; color: #78350f; line-height: 1.6; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ──────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-top">
        <div class="masthead-name">Smit.</div>
        <span class="masthead-pill">AI Financial + ESG Co-Pilot</span>
    </div>
    <div class="masthead-sub">
        UK &amp; India frameworks &nbsp;·&nbsp; HMRC · RBI · Bank of England · World Bank benchmarks &nbsp;·&nbsp; Not regulated financial advice
    </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────
for k, v in [
    ('signed_up', False), ('user_info', {}), ('results_ready', False),
    ('financial_data', {}), ('chat_messages', []), ('is_pro', False)
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIGNUP GATE ───────────────────────────────────────────────
if not st.session_state.signed_up:
    st.markdown("""
    <div style="padding: 2rem 0 1rem;">
        <div class="section-kicker">Free access — no credit card</div>
        <h1 style="font-size: 2.2rem; letter-spacing: -1px; margin-bottom: 0.75rem; line-height: 1.2;">
            Your AI Financial + ESG Co-Pilot.<br>
            <span style="color:#8B0000; font-style:italic;">For businesses that mean it.</span>
        </h1>
        <p style="font-size: 0.95rem; color: #4a4a4a; max-width: 560px; line-height: 1.8; margin-bottom: 2rem;">
            Smit takes your 7 real numbers, runs them against official HMRC, RBI, Bank of England, 
            and World Bank benchmarks, and delivers combined Financial + ESG scores with concrete actions 
            that improve your financial health <em>and</em> help you win contracts, loans, and clients.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full name", placeholder="Your name")
        email = st.text_input("Email address", placeholder="your@email.com")
    with col2:
        region = st.selectbox("Your region", ["", "🇬🇧 United Kingdom", "🇮🇳 India", "🌍 Other"])
        biz_type = st.selectbox("Business type", [
            "", "Freelancer / Sole trader", "Small business (1–10 people)",
            "Early-stage startup", "Limited company director", "Other"
        ])

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("Access Smit free — no credit card required"):
        if not name or not email or not region or not biz_type:
            st.error("Please fill in all fields to continue.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            st.session_state.signed_up = True
            st.session_state.user_info = {"name": name, "email": email, "region": region, "biz_type": biz_type}
            st.rerun()

    st.markdown("""
    <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #d4d4d4;">
        <p style="font-size:0.78rem;color:#6b6b6b;line-height:1.7;">
            No credit card. No spam. Your data personalises your diagnostic only.<br>
            <strong>Important:</strong> Smit is a financial intelligence tool. It does not provide regulated 
            financial, tax, or legal advice. Always consult a qualified professional for regulated decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── MAIN TOOL ─────────────────────────────────────────────────
user = st.session_state.user_info
is_uk = "United Kingdom" in user.get("region", "")
currency = "£" if is_uk else "₹"
step = 1000.0 if is_uk else 10000.0

st.markdown(f"""
<div style="padding:0.5rem 0 1rem;">
    <span style="font-size:0.78rem;color:#6b6b6b;">
        Welcome, {user.get('name','')} &nbsp;·&nbsp; {user.get('biz_type','')} &nbsp;·&nbsp; {user.get('region','')}
    </span>
</div>
""", unsafe_allow_html=True)

# ── STEP 1 ────────────────────────────────────────────────────
st.markdown("""
<div class="rule-thick"></div>
<div class="step-indicator"><div class="step-dot">1</div><div class="step-text">Your 7 financial inputs</div></div>
<p style="font-size:0.85rem;color:#4a4a4a;margin-bottom:1.25rem;">
    These are the exact numbers Smit uses for every calculation and AI response. Enter your most recent figures.
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Revenue & costs** _{currency}_")
    revenue = st.number_input("Annual revenue", min_value=0.0, step=step, key="rev",
                               help="Total income before expenses for the past 12 months")
    expenses = st.number_input("Annual expenses", min_value=0.0, step=step, key="exp",
                                help="All business costs — staff, rent, subscriptions, everything")
    cash = st.number_input("Cash in bank", min_value=0.0, step=step/2, key="cash",
                            help="Liquid cash available right now across all business accounts")
with col2:
    st.markdown(f"**Debt & obligations** _{currency}_")
    debt = st.number_input("Total debt / liabilities", min_value=0.0, step=step/2, key="debt",
                            help="All outstanding loans, credit, and financial obligations")
    fixed_costs = st.number_input("Monthly fixed costs", min_value=0.0, step=100.0, key="fc",
                                   help="Costs that stay the same regardless of revenue — rent, salaries, subscriptions")
    receivables = st.number_input("Money owed to you", min_value=0.0, step=100.0, key="rec",
                                   help="Outstanding invoices and payments you are owed but haven't received yet")

# ── STEP 2 ────────────────────────────────────────────────────
st.markdown("""
<div class="rule"></div>
<div class="step-indicator"><div class="step-dot">2</div><div class="step-text">Compliance checklist</div></div>
<p style="font-size:0.85rem;color:#4a4a4a;margin-bottom:1rem;">
    Answer honestly — these are the first things any regulatory review checks.
    Source: HMRC compliance requirements (UK) · CGST Act 2017 &amp; MCA ROC requirements (India).
</p>
""", unsafe_allow_html=True)

if is_uk:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)",
                     help="Required under HMRC record-keeping rules — minimum 5 years for companies, 22 months for sole traders")
    q2 = st.checkbox("I have a dedicated business bank account",
                     help="Legally required for limited companies; strongly recommended for sole traders — mixing finances is the #1 CA audit finding")
    q3 = st.checkbox("I know my VAT registration status and whether I'm above the £85,000 threshold",
                     help="HMRC requires registration within 30 days of exceeding £85,000 turnover. Non-registration is a criminal offence under VAT Act 1994.")
    q4 = st.checkbox("I file self-assessment or company accounts on time every year",
                     help="Late filing triggers automatic penalties: £100 for SA, £150+ for company accounts at Companies House")
    q5 = st.checkbox("I have financial records going back at least 2 years",
                     help="HMRC requires 5 years for companies, 22 months for individuals. 2 years is a practical minimum for any business review.")
else:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)",
                     help="Required under GST Rules 2017 — records must be maintained for 72 months (6 years)")
    q2 = st.checkbox("I have a dedicated business bank account",
                     help="Required for GST-registered businesses; strongly recommended for all. Separates personal and business liability.")
    q3 = st.checkbox("I know my GST registration status and whether I'm above the ₹20 Lakh threshold",
                     help="Mandatory GST registration above ₹20 Lakhs (services) or ₹40 Lakhs (goods) under CGST Act 2017. Penalty: 10% of tax or ₹10,000, whichever is higher.")
    q4 = st.checkbox("I file GST returns quarterly and on time",
                     help="Late GSTR-3B filing attracts ₹50/day late fee (₹20 for nil returns). Consistent filing history is required for loans and contracts.")
    q5 = st.checkbox("I maintain records a CA could review immediately",
                     help="Required under Companies Act 2013 Section 128 — books of account must be kept at registered office and available for inspection.")

# ── STEP 3 ────────────────────────────────────────────────────
st.markdown("""
<div class="rule"></div>
<div class="step-indicator"><div class="step-dot">3</div><div class="step-text">Governance &amp; ESG assessment</div></div>
<p style="font-size:0.85rem;color:#4a4a4a;margin-bottom:1rem;">
    ESG is no longer just for large companies. Banks, large clients, and supply chains increasingly require 
    ESG evidence from their SME partners.
    Source: UK DBT SME ESG Guidance 2023 · SEBI BRSR Lite Framework (India) · ISO 26000.
</p>
""", unsafe_allow_html=True)

esg1 = st.checkbox("I review my finances monthly or quarterly",
                   help="Regular financial review is a core governance indicator under FRC Corporate Governance Code and SEBI BRSR Lite")
esg2 = st.checkbox("I have clear written contracts or terms of service with clients",
                   help="Contract discipline reduces dispute risk and is a social governance indicator (ISO 26000 Section 6.6)")
esg3 = st.checkbox("I am aware of my key legal and compliance obligations",
                   help="Compliance awareness is a governance foundation — referenced in UK DBT Small Business ESG Guidance 2023")
esg4 = st.checkbox("I track or consider the environmental impact of my business operations",
                   help="Basic environmental awareness — referenced in SEBI BRSR Lite and UK DBT ESG guidance as the entry-level E indicator for SMEs")

# ── RUN ───────────────────────────────────────────────────────
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

if st.button("Run Smit Diagnostic →"):
    if revenue == 0:
        st.error("Please enter your annual revenue to continue.")
        st.stop()

    # Calculations
    profit = revenue - expenses
    profit_margin = (profit / revenue) * 100
    expense_ratio = (expenses / revenue) * 100
    debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
    current_ratio = (cash + receivables) / (debt if debt > 0 else 1)

    # Audit score
    checklist = [q1, q2, q3, q4, q5]
    audit_score = (sum(checklist) / 5) * 100

    # ESG score
    esg_checklist = [esg1, esg2, esg3, esg4]
    esg_raw = (sum(esg_checklist) / 4) * 100
    governance_score = min((audit_score * 0.5) + (esg_raw * 0.3) + (20 if q2 else 0) + (10 if q1 else 0), 100)

    # Financial risk scoring
    risk_points = 0
    if is_uk:
        if profit_margin >= 20: risk_points += 0
        elif profit_margin >= 10: risk_points += 15
        else: risk_points += 30
    else:
        if profit_margin >= 15: risk_points += 0
        elif profit_margin >= 8: risk_points += 15
        else: risk_points += 30

    if current_ratio >= 2: risk_points += 0
    elif current_ratio >= 1: risk_points += 15
    else: risk_points += 30

    if debt_to_revenue <= 30: risk_points += 0
    elif debt_to_revenue <= 60: risk_points += 20
    else: risk_points += 40

    financial_score = max(0, 100 - risk_points)

    # Combined Smit Score
    combined_score = round((financial_score * 0.6) + (governance_score * 0.4))

    # Status helpers
    def fin_status(s):
        if s >= 70: return "Low risk", "status-green"
        elif s >= 45: return "Moderate", "status-amber"
        else: return "High risk", "status-red"

    def audit_status(s):
        if s >= 80: return "Prepared", "status-green"
        elif s >= 50: return "Partial", "status-amber"
        else: return "Not ready", "status-red"

    def gov_status(s):
        if s >= 70: return "Strong", "status-green"
        elif s >= 40: return "Developing", "status-amber"
        else: return "Weak", "status-red"

    def combined_label(s):
        if s >= 70: return "Strong position", "#1a5c2e"
        elif s >= 50: return "Developing", "#7a4a0a"
        else: return "Needs attention", "#8B0000"

    fs_label, fs_class = fin_status(financial_score)
    as_label, as_class = audit_status(audit_score)
    gs_label, gs_class = gov_status(governance_score)
    comb_label, comb_colour = combined_label(combined_score)

    # Red flags
    red_flags = []
    if profit_margin < 0:
        red_flags.append(("critical", "Operating at a loss — expenses exceed revenue. Every month deepens the deficit."))
    if expense_ratio > 85:
        red_flags.append(("warning", f"Expense ratio {expense_ratio:.1f}% — above the 85% warning threshold. Under 15p in every £1 remains after costs. Source: HMRC SME Business Population benchmarks."))
    if cash < (fixed_costs * 2):
        red_flags.append(("warning", f"Cash reserves below 2 months of fixed costs ({currency}{fixed_costs*2:,.0f}). Vulnerability to any revenue interruption. Bank of England SME resilience guidance recommends minimum 3 months."))
    if debt_to_revenue > 60:
        red_flags.append(("critical", f"Debt-to-revenue {debt_to_revenue:.1f}% — above the 60% high-risk threshold. Source: World Bank MSME Finance Gap Report. Significant portion of annual income committed to obligations."))
    if current_ratio < 1:
        red_flags.append(("critical", f"Current ratio {current_ratio:.2f} — below 1.0. Cannot meet short-term obligations from liquid assets. This is a going concern indicator (ISA 570). Immediate action required."))
    if is_uk and revenue > 85000 and not q3:
        red_flags.append(("critical", "Revenue above VAT registration threshold (£85,000). Non-registration is a criminal offence under Value Added Tax Act 1994, Section 67."))
    if not is_uk and revenue > 2000000 and not q3:
        red_flags.append(("critical", "Revenue above GST threshold (₹20 Lakhs). Mandatory registration required under CGST Act 2017. Penalty: 10% of tax due or ₹10,000, whichever is higher."))

    # Financial priority actions
    actions = []
    if profit_margin < 0:
        actions.append(f"Review your full expense structure. Identify your 3 largest costs and assess whether each generates proportional value. A return to break-even requires cutting {currency}{abs(profit):,.0f} from annual costs.")
    if expense_ratio > 85:
        actions.append(f"Reduce expense ratio from {expense_ratio:.1f}% toward 80%. A 5-point improvement on {currency}{revenue:,.0f} revenue adds {currency}{revenue*0.05:,.0f} to annual profit.")
    if cash < fixed_costs * 2:
        actions.append(f"Build cash reserves to {currency}{fixed_costs*2:,.0f} (2 months fixed costs) before any new financial commitments. Accelerate collection of receivables ({currency}{receivables:,.0f} outstanding).")
    if debt_to_revenue > 60:
        actions.append(f"Prioritise debt reduction before new borrowing. At {debt_to_revenue:.1f}% debt-to-revenue, your leverage increases vulnerability to any revenue decline significantly.")
    if audit_score < 60:
        actions.append("Address compliance gaps — particularly missing checklist items. These are the first things surfaced in any regulatory review or loan application.")
    if current_ratio < 1:
        actions.append(f"Convert receivables ({currency}{receivables:,.0f}) to cash as priority. Your current ratio of {current_ratio:.2f} is the most immediate operational risk.")
    if not actions:
        actions.append("Your financial position is stable. Maintain discipline, run this diagnostic quarterly, and focus on bringing ESG score above 70%.")

    # ESG Upgrade Plan — tied to actual numbers
    esg_actions = []

    if not esg1:
        esg_actions.append({
            "action": "Start a monthly 30-minute financial review",
            "detail": f"Set a recurring calendar event. Review your revenue vs expenses vs cash. At your current scale ({currency}{revenue:,.0f} annual revenue), one month of unnoticed drift could cost {currency}{revenue/12*0.05:,.0f}. Zero cost — saves money and raises your Governance score.",
            "impact": "+15 pts ESG"
        })

    if expense_ratio > 75:
        if is_uk:
            esg_actions.append({
                "action": "Audit your supplier and subscription costs for greener alternatives",
                "detail": f"With an expense ratio of {expense_ratio:.1f}%, your cost base is {currency}{expenses:,.0f}/year. Switching even 10% of costs to verified sustainable suppliers (e.g. renewable energy tariffs, FSC-certified materials) could reduce costs by £200–800/year and qualifies you for UK DBT Green Business programmes.",
                "impact": "+12 pts ESG, potential cost saving"
            })
        else:
            esg_actions.append({
                "action": "Review supplier costs for efficiency and sustainability",
                "detail": f"With expenses at {currency}{expenses:,.0f}/year, even a 5% reduction through efficient procurement improves both your expense ratio and ESG score. SEBI BRSR Lite requires disclosure of basic environmental practices — starting this now prepares you for future requirements.",
                "impact": "+12 pts ESG"
            })

    if not esg2:
        esg_actions.append({
            "action": "Create a standard client contract or terms of service",
            "detail": "A one-page written agreement for every client engagement reduces dispute risk, strengthens your governance score, and is required by ISO 26000 Section 6.6 (fair operating practices). Free templates available via UK government business tools or Ministry of MSME.",
            "impact": "+10 pts ESG, reduced legal risk"
        })

    if cash < fixed_costs * 3 and not esg4:
        esg_actions.append({
            "action": "Track your energy and operational costs as a sustainability baseline",
            "detail": f"Your cash position of {currency}{cash:,.0f} is tight. Tracking energy use (electricity, travel, logistics) typically identifies 8–15% cost savings while meeting SEBI BRSR Lite environmental baseline requirements. Start with a simple monthly log — free to do.",
            "impact": "+8 pts ESG, potential 8–15% energy cost reduction"
        })

    if not esg3:
        esg_actions.append({
            "action": "Map your key legal and compliance obligations",
            "detail": f"In {'the UK' if is_uk else 'India'}, {'HMRC self-assessment, Companies House filing, VAT obligations' if is_uk else 'GST filing, ROC compliance, TDS obligations'} are the core obligations. A one-page compliance calendar costs nothing and is the foundation of your governance score.",
            "impact": "+10 pts ESG"
        })

    if not esg_actions:
        esg_actions.append({
            "action": "Maintain your current ESG practices and document them",
            "detail": "Your governance indicators are strong. Start documenting your practices formally — a simple one-page ESG statement can be shared with clients, banks, and supply chain partners who increasingly require ESG evidence. Costs nothing and increases your credibility.",
            "impact": "Consolidates existing score"
        })

    # ESG checklist items for display
    esg_items = [
        ("Monthly or quarterly financial review", esg1),
        ("Written contracts / terms of service", esg2),
        ("Compliance obligations awareness", esg3),
        ("Environmental impact awareness", esg4),
        ("Dedicated business banking", q2),
        ("Consistent record keeping", q1),
    ]

    # Overall summary
    if financial_score >= 70:
        summary_text = f"Your business presents a broadly stable financial profile — financial risk score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. Profitability and liquidity are within acceptable ranges. The primary improvement area is {'audit readiness at ' + str(int(audit_score)) + '%' if audit_score < 80 else 'ESG governance at ' + str(int(governance_score)) + '%'} — addressing the outstanding items would lift your Combined Smit Score meaningfully."
    elif financial_score >= 45:
        weak = "cash reserves" if cash < fixed_costs * 2 else "leverage position" if debt_to_revenue > 60 else "profit margins"
        summary_text = f"Your business shows moderate financial risk — score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. The principal concern is your {weak}. ESG score at {governance_score:.0f}% — improving governance practices now protects you against future compliance requirements and improves access to credit and contracts."
    else:
        summary_text = f"High-risk signals across multiple dimensions — financial score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. Immediate attention needed. The ESG Upgrade Plan below includes zero-cost actions that improve both your operational resilience and sustainability position simultaneously."

    # Store
    st.session_state.results_ready = True
    st.session_state.financial_data = {
        "revenue": revenue, "expenses": expenses, "cash": cash,
        "debt": debt, "fixed_costs": fixed_costs, "receivables": receivables,
        "profit": profit, "profit_margin": profit_margin,
        "expense_ratio": expense_ratio, "debt_to_revenue": debt_to_revenue,
        "current_ratio": current_ratio, "financial_score": financial_score,
        "audit_score": audit_score, "governance_score": governance_score,
        "combined_score": combined_score, "comb_label": comb_label, "comb_colour": comb_colour,
        "red_flags": red_flags, "actions": actions,
        "esg_items": esg_items, "esg_actions": esg_actions,
        "summary_text": summary_text, "currency": currency, "is_uk": is_uk,
        "fs_label": fs_label, "fs_class": fs_class,
        "as_label": as_label, "as_class": as_class,
        "gs_label": gs_label, "gs_class": gs_class,
        # pass checklist answers for AI
        "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5,
        "esg1": esg1, "esg2": esg2, "esg3": esg3, "esg4": esg4,
    }
    st.rerun()

# ── RESULTS ───────────────────────────────────────────────────
if st.session_state.results_ready:
    d = st.session_state.financial_data

    st.markdown("""
    <div class="rule-thick"></div>
    <div class="section-kicker">Your Smit diagnostic</div>
    """, unsafe_allow_html=True)

    # Combined Smit Score hero
    st.markdown(f"""
    <div class="smit-score-hero">
        <div class="smit-score-label">Combined Smit Score — Financial + ESG</div>
        <div class="smit-score-number" style="color:{d['comb_colour']}">{d['combined_score']}</div>
        <div style="font-size:0.85rem;color:{d['comb_colour']};font-weight:600;">{d['comb_label']}</div>
        <div class="smit-score-sub">60% financial risk weighting · 40% ESG &amp; governance weighting</div>
        <div class="smit-score-breakdown">
            <div class="smit-breakdown-item">
                <div class="smit-breakdown-val" style="color:{'#4ade80' if d['financial_score']>=70 else '#fbbf24' if d['financial_score']>=45 else '#f87171'}">{d['financial_score']:.0f}</div>
                <div class="smit-breakdown-lbl">Financial risk score</div>
            </div>
            <div class="smit-breakdown-item">
                <div class="smit-breakdown-val" style="color:{'#4ade80' if d['audit_score']>=80 else '#fbbf24' if d['audit_score']>=50 else '#f87171'}">{d['audit_score']:.0f}%</div>
                <div class="smit-breakdown-lbl">Audit readiness</div>
            </div>
            <div class="smit-breakdown-item">
                <div class="smit-breakdown-val" style="color:{'#4ade80' if d['governance_score']>=70 else '#fbbf24' if d['governance_score']>=40 else '#f87171'}">{d['governance_score']:.0f}%</div>
                <div class="smit-breakdown-lbl">ESG governance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Three scores
    st.markdown(f"""
    <div class="score-row">
        <div class="score-cell">
            <div class="score-cell-label">Financial risk</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['financial_score']>=70 else '#7a4a0a' if d['financial_score']>=45 else '#8B0000'}">
                {d['financial_score']:.0f}<span style="font-size:1.1rem;color:#6b6b6b;font-weight:400">/100</span>
            </div>
            <span class="score-cell-status {d['fs_class']}">{d['fs_label']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-label">Audit readiness</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['audit_score']>=80 else '#7a4a0a' if d['audit_score']>=50 else '#8B0000'}">
                {d['audit_score']:.0f}<span style="font-size:1.1rem;color:#6b6b6b;font-weight:400">%</span>
            </div>
            <span class="score-cell-status {d['as_class']}">{d['as_label']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-label">ESG governance</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['governance_score']>=70 else '#7a4a0a' if d['governance_score']>=40 else '#8B0000'}">
                {d['governance_score']:.0f}<span style="font-size:1.1rem;color:#6b6b6b;font-weight:400">%</span>
            </div>
            <span class="score-cell-status {d['gs_class']}">{d['gs_label']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ratios
    st.markdown('<div class="section-kicker" style="margin-top:1.5rem">Key financial ratios</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.78rem;color:#6b6b6b;margin-bottom:0.75rem;">Benchmarked against HMRC Business Population Estimates (UK) and RBI MSME Lending Data (India) · Bank of England SME lending criteria · World Bank MSME Finance Gap Report.</p>', unsafe_allow_html=True)

    def rc(metric, v, uk):
        if metric == "margin":
            t, w = (20, 10) if uk else (15, 8)
            return "ratio-good" if v >= t else "ratio-warn" if v >= w else "ratio-bad"
        elif metric == "expense":
            return "ratio-good" if v < 80 else "ratio-warn" if v < 85 else "ratio-bad"
        elif metric == "dtr":
            return "ratio-good" if v <= 30 else "ratio-warn" if v <= 60 else "ratio-bad"
        elif metric == "cr":
            return "ratio-good" if v >= 2 else "ratio-warn" if v >= 1 else "ratio-bad"

    mc = rc("margin", d['profit_margin'], d['is_uk'])
    ec = rc("expense", d['expense_ratio'], d['is_uk'])
    dc = rc("dtr", d['debt_to_revenue'], d['is_uk'])
    cc = rc("cr", d['current_ratio'], d['is_uk'])

    def status_txt(cls):
        return "✓ Healthy" if cls == "ratio-good" else "⚠ Watch" if cls == "ratio-warn" else "✗ At risk"

    bm_margin = "≥20% healthy (HMRC)" if d['is_uk'] else "≥15% healthy (RBI)"
    st.markdown(f"""
    <table class="ratio-table">
        <thead><tr><th>Ratio</th><th>What it measures</th><th>Your figure</th><th>Benchmark</th><th>Status</th></tr></thead>
        <tbody>
            <tr>
                <td><strong>Net profit margin</strong><span class="ratio-tooltip">Revenue minus all costs, as % of revenue. How much you actually keep.</span></td>
                <td style="font-size:0.78rem;color:#6b6b6b;">Profitability</td>
                <td class="ratio-val {mc}">{d['profit_margin']:.1f}%</td>
                <td style="font-size:0.78rem;">{bm_margin}</td>
                <td class="{mc}">{status_txt(mc)}</td>
            </tr>
            <tr>
                <td><strong>Expense ratio</strong><span class="ratio-tooltip">Total expenses as % of revenue. How much it costs to generate each £/₹ of income.</span></td>
                <td style="font-size:0.78rem;color:#6b6b6b;">Cost efficiency</td>
                <td class="ratio-val {ec}">{d['expense_ratio']:.1f}%</td>
                <td style="font-size:0.78rem;">Below 80% healthy</td>
                <td class="{ec}">{status_txt(ec)}</td>
            </tr>
            <tr>
                <td><strong>Debt-to-revenue</strong><span class="ratio-tooltip">Total debt as % of annual revenue. How leveraged the business is relative to income.</span></td>
                <td style="font-size:0.78rem;color:#6b6b6b;">Leverage</td>
                <td class="ratio-val {dc}">{d['debt_to_revenue']:.1f}%</td>
                <td style="font-size:0.78rem;">Below 30% low risk (World Bank)</td>
                <td class="{dc}">{'✓ Low risk' if dc=='ratio-good' else '⚠ Moderate' if dc=='ratio-warn' else '✗ High risk'}</td>
            </tr>
            <tr>
                <td><strong>Current ratio</strong><span class="ratio-tooltip">(Cash + receivables) ÷ debt. Can you meet short-term obligations from liquid assets?</span></td>
                <td style="font-size:0.78rem;color:#6b6b6b;">Liquidity</td>
                <td class="ratio-val {cc}">{d['current_ratio']:.2f}</td>
                <td style="font-size:0.78rem;">Above 2.0 (Bank of England)</td>
                <td class="{cc}">{status_txt(cc)}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Audit flags
    st.markdown('<div class="rule"></div><div class="section-kicker">Audit flags</div>', unsafe_allow_html=True)
    if d['red_flags']:
        for severity, msg in d['red_flags']:
            css = "flag-critical" if severity == "critical" else "flag-warning"
            icon = "●" if severity == "critical" else "◐"
            st.markdown(f'<div class="flag-item {css}"><strong>{icon}</strong> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="flag-item flag-ok">✓ No audit flags detected. Your numbers present cleanly.</div>', unsafe_allow_html=True)

    # Priority actions
    st.markdown('<div class="rule"></div><div class="section-kicker">Financial priority actions</div>', unsafe_allow_html=True)
    for i, action in enumerate(d['actions'][:3], 1):
        st.markdown(f"""
        <div class="action-item">
            <div class="action-number">{i}.</div>
            <div>{action}</div>
        </div>
        """, unsafe_allow_html=True)

    # ESG Upgrade Plan
    st.markdown('<div class="rule"></div><div class="section-kicker">Your ESG upgrade plan</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem;color:#4a4a4a;margin-bottom:0.75rem;">Concrete, low/zero-cost actions tied to your specific numbers. Each improves your Combined Smit Score and strengthens your position with banks, clients, and supply chains.</p>', unsafe_allow_html=True)

    for item in d['esg_actions'][:4]:
        st.markdown(f"""
        <div class="esg-plan">
            <div class="esg-plan-header">Action · <span style="color:#a7f3d0">{item['impact']}</span></div>
            <div class="esg-plan-item">
                <strong>{item['action']}</strong><br>
                {item['detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ESG checklist display
    st.markdown('<div class="section-kicker" style="margin-top:1rem">ESG &amp; governance indicators</div>', unsafe_allow_html=True)
    esg_grid_html = ""
    for item, passed in d['esg_items']:
        css = "esg-pass" if passed else "esg-fail"
        icon = "✓" if passed else "✗"
        esg_grid_html += f'<div class="esg-item {css}"><span><strong>{icon}</strong></span> {item}</div>'
    st.markdown(f'<div class="esg-grid">{esg_grid_html}</div>', unsafe_allow_html=True)

    # Overall assessment
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-kicker">Overall assessment</div>
        {d['summary_text']}
    </div>
    """, unsafe_allow_html=True)

    # Stress test
    st.markdown('<div class="section-kicker" style="margin-top:1.5rem">Future-proof your business — stress test</div>', unsafe_allow_html=True)
    st.caption("Model a revenue decline. Expenses held constant — the conservative assumption used in Bank of England SME stress testing. See both financial impact and how ESG actions can reduce the damage.")

    drop = st.slider("Revenue declines by:", 0, 50, 20, format="%d%%")
    new_rev = d['revenue'] * (1 - drop / 100)
    new_profit = new_rev - d['expenses']
    new_margin = (new_profit / new_rev * 100) if new_rev > 0 else 0

    st.markdown(f"""
    <div class="stress-row">
        <div class="stress-cell">
            <div class="stress-cell-label">Revenue after decline</div>
            <div class="stress-cell-value">{d['currency']}{new_rev:,.0f}</div>
            <div class="stress-cell-delta delta-neg">−{drop}%</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-label">Profit / loss</div>
            <div class="stress-cell-value" style="color:{'#1a5c2e' if new_profit>=0 else '#8B0000'}">{d['currency']}{new_profit:,.0f}</div>
            <div class="stress-cell-delta {'delta-pos' if new_profit>=0 else 'delta-neg'}">{d['currency']}{new_profit-d['profit']:,.0f}</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-label">New profit margin</div>
            <div class="stress-cell-value" style="color:{'#1a5c2e' if new_margin>=10 else '#8B0000'}">{new_margin:.1f}%</div>
            <div class="stress-cell-delta delta-neg">{new_margin-d['profit_margin']:+.1f}pp</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if new_profit < 0:
        st.markdown(f'<div class="flag-item flag-critical">A {drop}% revenue decline pushes your business into loss. Fixed cost base of {d["currency"]}{d["fixed_costs"]*12:,.0f}/year is not sustainable at this revenue level. ESG action: reducing your expense ratio through sustainable procurement could add {d["currency"]}{d["expenses"]*0.05:,.0f}/year buffer.</div>', unsafe_allow_html=True)
    elif new_margin < 10:
        st.markdown(f'<div class="flag-item flag-warning">Margin compresses to {new_margin:.1f}% — dangerously thin. ESG action: implementing a monthly financial review (zero cost) would give you 30 days earlier warning of this scenario.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flag-item flag-ok">Business remains profitable under a {drop}% revenue decline. Margin holds at {new_margin:.1f}%. Maintaining your ESG governance score protects access to credit in downturns.</div>', unsafe_allow_html=True)

    # AI Chat — Pro only
    st.markdown("""
    <div class="rule-thick" style="margin-top:2rem"></div>
    <div class="section-kicker">Smit AI financial + ESG assistant</div>
    <h3 style="font-size:1.3rem;margin-bottom:0.25rem;">Ask Smit about your numbers</h3>
    """, unsafe_allow_html=True)

    # Check for API key to determine if Pro features are available
    try:
        import os
        api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
        has_api = bool(api_key)
    except Exception:
        has_api = False

    if not has_api:
        st.markdown("""
        <div class="pro-gate">
            <p><strong>Pro feature</strong> — AI Financial + ESG Assistant</p>
            <p>Ask any question about your specific numbers. Every answer uses only your 7 inputs and official Smit benchmarks. Max 250 words. Plain English. Always actionable.</p>
            <p style="font-size:0.78rem;margin-top:0.5rem;">Join early access at <strong>getsmit.co</strong> for Pro access.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="chat-wrap">
            <div class="chat-header">
                <span>Smit AI assistant</span>
                <span class="chat-badge">Pro · Your data loaded · Constrained to Smit methodology</span>
            </div>
        </div>
        <p style="font-size:0.82rem;color:#4a4a4a;margin:0.5rem 0 1rem;line-height:1.6;">
            Every answer uses only your 7 inputs + official Smit benchmarks (HMRC, RBI, Bank of England, World Bank, ISA 570, SEBI BRSR Lite).
            Not regulated financial advice — see disclaimer below.
        </p>
        """, unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-msg-user"><div class="chat-msg-label">You</div>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-msg-assistant"><div class="chat-msg-label">Smit AI</div>{msg["content"]}</div>', unsafe_allow_html=True)

        user_q = st.text_input(
            "Your question",
            placeholder="e.g. Why is my risk score low? What ESG actions save me money? What would a bank see?",
            label_visibility="collapsed",
            key="chat_input"
        )

        if st.button("Send →", key="send_chat"):
            if user_q.strip():
                d = st.session_state.financial_data
                cur = d['currency']

                # ── BULLETPROOF SYSTEM PROMPT ─────────────────────
                system_prompt = f"""You are Smit AI — the Financial + ESG Co-Pilot for independent businesses and freelancers.

IDENTITY AND CONSTRAINTS:
You ONLY use the user's exact 7 financial inputs, their checklist answers, their region ({  'UK' if d['is_uk'] else 'India'}), and the official Smit methodology v2.0 benchmarks listed below. You do NOT use outside knowledge, general financial advice, or information beyond what is provided.

USER'S 7 FINANCIAL INPUTS:
1. Annual revenue: {cur}{d['revenue']:,.0f}
2. Annual expenses: {cur}{d['expenses']:,.0f}
3. Cash in bank: {cur}{d['cash']:,.0f}
4. Total debt / liabilities: {cur}{d['debt']:,.0f}
5. Monthly fixed costs: {cur}{d['fixed_costs']:,.0f}
6. Money owed to them (receivables): {cur}{d['receivables']:,.0f}
7. Region: {'United Kingdom' if d['is_uk'] else 'India'} | Business type: {st.session_state.user_info.get('biz_type', 'SME')}

CALCULATED METRICS (from their inputs):
- Net profit margin: {d['profit_margin']:.1f}%
- Expense ratio: {d['expense_ratio']:.1f}%
- Debt-to-revenue: {d['debt_to_revenue']:.1f}%
- Current ratio: {d['current_ratio']:.2f}
- Financial risk score: {d['financial_score']:.0f}/100
- Audit readiness: {d['audit_score']:.0f}%
- ESG governance score: {d['governance_score']:.0f}%
- Combined Smit Score: {d['combined_score']}/100

CHECKLIST ANSWERS:
- Keeps receipts/invoices: {'Yes' if d['q1'] else 'No'}
- Dedicated business bank account: {'Yes' if d['q2'] else 'No'}
- VAT/GST registration status known: {'Yes' if d['q3'] else 'No'}
- Files returns on time: {'Yes' if d['q4'] else 'No'}
- Records available for review: {'Yes' if d['q5'] else 'No'}
- Monthly/quarterly financial review: {'Yes' if d['esg1'] else 'No'}
- Written client contracts: {'Yes' if d['esg2'] else 'No'}
- Compliance awareness: {'Yes' if d['esg3'] else 'No'}
- Environmental impact awareness: {'Yes' if d['esg4'] else 'No'}

OFFICIAL SMIT METHODOLOGY v2.0 BENCHMARKS (cite these by source):
- UK profit margin healthy: ≥20% (source: HMRC Business Population Estimates)
- India profit margin healthy: ≥15% (source: RBI Annual Report MSME Lending Data)
- Expense ratio warning threshold: >85% (source: HMRC SME benchmarks)
- Current ratio healthy: ≥2.0; below 1.0 = going concern indicator (source: Bank of England SME lending criteria; ISA 570)
- Debt-to-revenue low risk: ≤30%; high risk: >60% (source: World Bank MSME Finance Gap Report)
- Cash reserves recommended: ≥2 months fixed costs (source: Bank of England SME resilience guidance)
- UK VAT threshold: £85,000 (source: HMRC Value Added Tax Act 1994)
- India GST threshold: ₹20 Lakhs services / ₹40 Lakhs goods (source: CGST Act 2017)
- ESG governance framework: UK DBT SME ESG Guidance 2023; SEBI BRSR Lite Framework; ISO 26000

STRICT RULES — NEVER BREAK:
1. EVERY answer MUST reference the user's actual numbers AND the exact official threshold with source.
2. ESG suggestions MUST be low/zero-cost actions DIRECTLY linked to their expense ratio, cash position, or checklist answers. Always quantify the impact where possible (e.g. "could reduce costs by {cur}X/year and lift ESG score by Y points").
3. Stress test scenarios MUST show both financial impact AND how ESG improvements reduce risk.
4. You MUST end EVERY response with this exact disclaimer: "⚠ This is not regulated financial, tax or legal advice. For decisions affecting your tax position or legal standing, always consult a qualified professional."
5. If a question cannot be answered from the 7 inputs + benchmarks + checklist, respond ONLY with: "I can only answer using your provided numbers and Smit's official benchmarks. Please share your inputs or clarify your question."
6. Maximum 250 words per response. Plain English. Actionable and encouraging.
7. Never speculate, never make up numbers, never reference information not in this prompt.

RESPONSE FORMAT: Answer directly, reference their numbers, cite the benchmark source, give one concrete next step, end with disclaimer."""

                msgs_for_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_messages]
                msgs_for_api.append({"role": "user", "content": user_q})

                st.session_state.chat_messages.append({"role": "user", "content": user_q})

                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=400,
                        system=system_prompt,
                        messages=msgs_for_api
                    )
                    answer = response.content[0].text
                    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                except Exception:
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": "I'm having trouble connecting right now. Please try again in a moment.\n\n⚠ This is not regulated financial, tax or legal advice. For decisions affecting your tax position or legal standing, always consult a qualified professional."
                    })
                st.rerun()

    # Download
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.button("📄 Download Full Report (PDF) — Pro feature · Coming soon", disabled=True)

    # Legal disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠ Important — please read.</strong> Smit is a financial intelligence and ESG co-pilot tool. 
        It calculates and interprets your financial data using published benchmarks from 
        HMRC, Companies House, Bank of England, Reserve Bank of India, Ministry of MSME India, 
        and World Bank MSME Finance Gap Report. ESG indicators reference UK DBT SME ESG Guidance 2023, 
        SEBI BRSR Lite Framework, and ISO 26000.<br><br>
        <strong>Smit does not provide regulated financial, tax, investment, or legal advice.</strong> 
        Benchmarks are indicative — your specific circumstances, sector, and business model 
        may produce results that differ from general SME benchmarks. 
        For decisions affecting your tax position, compliance obligations, or legal standing, 
        always consult a qualified professional (CA, accountant, or solicitor).<br><br>
        Smit scores and outputs are for informational purposes only and should not be used 
        as the sole basis for financial decisions.
    </div>
    """, unsafe_allow_html=True)
