"""
app.py — NSITN v2.0
National Social Impact & NGO Transparency Network
Modern Streamlit UI — light theme, card layout, animations.
"""

import streamlit as st
import time
from datetime import date, datetime

# ─── Must be first Streamlit call ───────────────────────────────────────────────
st.set_page_config(
    page_title="NSITN — NGO Transparency Network",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.data_manager import (
    init_storage, create_user, authenticate,
    register_ngo, get_approved_ngos, get_pending_ngos, get_all_ngos,
    get_ngo_by_id, admin_decision,
    get_donations_by_donor, get_donations_by_ngo,
    create_donation, create_receipt, get_receipt_by_donation,
    add_allocation, get_allocations_by_ngo,
    record_outcome, get_outcomes_by_ngo,
    get_ngo_impact_summary, get_platform_stats,
    UNIT_COST_DEFAULTS
)
from utils.ai_engine import run_ngo_analysis, predict_impact
from utils.chatbot import chat

init_storage()

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #F5F7FA;
    color: #1A202C;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Fade-in animation ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeInUp 0.55s ease both; }

/* ── Cards ── */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    margin-bottom: 18px;
    animation: fadeInUp 0.5s ease both;
    border: 1px solid #EDF2F7;
}
.card-accent {
    background: linear-gradient(135deg, #6C63FF 0%, #48BB78 100%);
    border-radius: 16px;
    padding: 28px;
    color: white;
    margin-bottom: 18px;
    animation: fadeInUp 0.5s ease both;
}
.card-warning {
    background: #FFFBEA;
    border: 1px solid #F6E05E;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.card-danger {
    background: #FFF5F5;
    border: 1px solid #FC8181;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.card-success {
    background: #F0FFF4;
    border: 1px solid #68D391;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
}

/* ── Stat chips ── */
.stat-chip {
    display: inline-block;
    background: #EBF4FF;
    color: #3182CE;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 600;
    margin: 3px;
}
.chip-green { background:#F0FFF4; color:#276749; }
.chip-red   { background:#FFF5F5; color:#C53030; }
.chip-yellow{ background:#FFFBEA; color:#975A16; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #6C63FF 0%, #4299E1 50%, #48BB78 100%);
    border-radius: 20px;
    padding: 52px 44px;
    text-align: center;
    color: white;
    margin-bottom: 32px;
    animation: fadeInUp 0.6s ease both;
}
.hero h1 { font-size: 2.6rem; font-weight: 700; margin-bottom: 8px; }
.hero p  { font-size: 1.1rem; opacity: 0.9; max-width: 600px; margin: 0 auto; }

/* ── Section headers ── */
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2D3748;
    margin: 24px 0 14px;
    padding-bottom: 8px;
    border-bottom: 3px solid #6C63FF;
    display: inline-block;
}

/* ── Buttons ── */
div.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(108,99,255,0.3) !important;
}

/* ── Progress bars ── */
.stProgress > div > div { border-radius: 999px; }

/* ── Inputs ── */
div.stTextInput > div > div > input,
div.stNumberInput > div > div > input,
div.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #E2E8F0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #EDF2F7;
}

/* ── Chatbot bubble ── */
.chat-bubble-user {
    background: #6C63FF;
    color: white;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0;
    max-width: 80%;
    margin-left: auto;
    font-size: 14px;
}
.chat-bubble-bot {
    background: #F7FAFC;
    color: #2D3748;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px 0;
    max-width: 85%;
    font-size: 14px;
    border: 1px solid #EDF2F7;
}

/* ── DNA badge ── */
.dna-badge {
    background: linear-gradient(90deg, #6C63FF, #48BB78);
    color: white;
    font-family: monospace;
    font-size: 1rem;
    padding: 6px 18px;
    border-radius: 8px;
    display: inline-block;
    font-weight: 700;
    letter-spacing: 2px;
}

/* ── Receipt ── */
.receipt-box {
    font-family: monospace;
    background: #FAFAFA;
    border: 1.5px dashed #CBD5E0;
    border-radius: 12px;
    padding: 20px 24px;
    font-size: 13px;
    line-height: 1.8;
}

/* ── Tables ── */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.custom-table th {
    background: #EBF4FF;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    color: #2B6CB0;
}
.custom-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #EDF2F7;
}
.custom-table tr:hover td { background: #F7FAFC; }

/* ── Score ring (text) ── */
.score-big {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════════════════════
def ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

ss("user", None)
ss("page", "home")
ss("chat_history", [])
ss("payment_stage", None)
ss("payment_data", None)
ss("show_chatbot", False)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def nav(page):
    st.session_state.page = page
    st.rerun()

def score_color(score):
    score = float(score)
    if score >= 70: return "chip-green"
    if score >= 45: return "chip-yellow"
    return "chip-red"

def risk_color(risk):
    risk = float(risk)
    if risk < 30: return "chip-green"
    if risk < 50: return "chip-yellow"
    return "chip-red"

def score_emoji(score):
    score = float(score)
    if score >= 70: return "🟢"
    if score >= 45: return "🟡"
    return "🔴"

def render_score_bar(label, value, max_val=100, color="#6C63FF"):
    pct = min(float(value) / max_val * 100, 100)
    st.markdown(f"**{label}** — `{value}`")
    st.progress(pct / 100)

def card(content_fn, *args, **kwargs):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    content_fn(*args, **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🌐 NSITN")
        st.markdown("*Transparency Network*")
        st.markdown("---")

        if st.session_state.user:
            u = st.session_state.user
            st.markdown(f"👤 **{u['name']}**")
            st.markdown(f"<span class='stat-chip'>{u['role'].upper()}</span>", unsafe_allow_html=True)
            st.markdown("---")

            role = u["role"]
            if role == "donor":
                if st.button("🏠 Home",            use_container_width=True): nav("home")
                if st.button("🔍 Browse NGOs",     use_container_width=True): nav("browse_ngos")
                if st.button("💰 My Donations",    use_container_width=True): nav("my_donations")
                if st.button("💬 AI Chatbot",      use_container_width=True): nav("chatbot")

            elif role == "ngo":
                if st.button("🏠 Dashboard",       use_container_width=True): nav("ngo_dashboard")
                if st.button("📁 Add Allocation",  use_container_width=True): nav("add_allocation")
                if st.button("📊 Record Outcome",  use_container_width=True): nav("record_outcome")
                if st.button("📈 My Analytics",    use_container_width=True): nav("ngo_analytics")

            elif role == "admin":
                if st.button("🛡️ Admin Panel",     use_container_width=True): nav("admin_panel")
                if st.button("📊 Platform Stats",  use_container_width=True): nav("platform_stats")
                if st.button("🏢 All NGOs",        use_container_width=True): nav("all_ngos")

            st.markdown("---")
            if st.button("🚪 Logout",              use_container_width=True):
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("🏠 Home",    use_container_width=True): nav("home")
            if st.button("🔐 Login",   use_container_width=True): nav("login")
            if st.button("📝 Sign Up", use_container_width=True): nav("signup")
            if st.button("💬 Chatbot", use_container_width=True): nav("chatbot")

        st.markdown("---")
        st.markdown("<small>NSITN v2.0 · Hackathon Edition</small>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="hero fade-in">
        <h1>🌐 NSITN</h1>
        <p>National Social Impact & NGO Transparency Network<br>
        Every donation, traced. Every outcome, verified. Every rupee, accountable.</p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_platform_stats()
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "✅ NGOs Verified", stats["total_ngos"]),
        (c2, "💰 Total Raised", f"₹{stats['total_raised']:,.0f}"),
        (c3, "🎯 Donations",     stats["total_donations"]),
        (c4, "🙏 Beneficiaries", stats["total_beneficiaries"]),
    ]
    for col, label, val in metrics:
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:20px">
                <div style="font-size:1.8rem;font-weight:800;color:#6C63FF">{val}</div>
                <div style="font-size:0.85rem;color:#718096;margin-top:4px">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("1️⃣", "NGO Registers", "NGO submits details & gets AI-scored"),
        ("2️⃣", "Admin Verifies", "Admin reviews Trust DNA, Risk & approves"),
        ("3️⃣", "Donor Gives",    "Donor sees full transparency before donating"),
        ("4️⃣", "Outcome Traced", "Every rupee traced to real-world outcomes"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;min-height:140px">
                <div style="font-size:2rem">{icon}</div>
                <div style="font-weight:700;margin:8px 0 4px">{title}</div>
                <div style="font-size:0.82rem;color:#718096">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if not st.session_state.user:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("🚀 Get Started — Login / Sign Up", use_container_width=True):
                nav("signup")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SIGN UP
# ═══════════════════════════════════════════════════════════════════════════════
def page_signup():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="card fade-in">
            <h2 style="text-align:center;color:#6C63FF">📝 Create Account</h2>
        </div>""", unsafe_allow_html=True)

        with st.container():
            name  = st.text_input("Full Name", placeholder="Your name")
            email = st.text_input("Email", placeholder="you@example.com")
            pwd   = st.text_input("Password", type="password")
            role  = st.selectbox("I am a...", ["donor", "ngo", "admin"],
                                 format_func=lambda x: {"donor":"💙 Donor","ngo":"🏢 NGO","admin":"🛡️ Admin"}[x])

            ngo_fields = {}
            if role == "ngo":
                st.markdown("**NGO Details:**")
                ngo_fields["cause"]    = st.selectbox("Cause Area", [
                    "education","health","environment","food","water",
                    "women","children","disability","livelihood","other"])
                ngo_fields["location"] = st.text_input("City / State")
                ngo_fields["founded"]  = st.text_input("Founded Year", "2015")
                ngo_fields["reg"]      = st.text_input("Registration Number")
                ngo_fields["desc"]     = st.text_area("Brief Description", height=80)

            if st.button("✅ Create Account", use_container_width=True):
                if not all([name, email, pwd]):
                    st.error("Please fill all fields.")
                else:
                    user, msg = create_user(name, email, pwd, role)
                    if user:
                        if role == "ngo":
                            ngo, nmsg = register_ngo(
                                name, email, ngo_fields.get("cause","other"),
                                ngo_fields.get("location",""), ngo_fields.get("founded",""),
                                ngo_fields.get("reg",""), ngo_fields.get("desc","")
                            )
                            if ngo:
                                run_ngo_analysis(ngo["ngo_id"])
                                st.success("✅ NGO registered! Pending admin approval.")
                            else:
                                st.warning(f"User created but NGO registration issue: {nmsg}")
                        else:
                            st.success("✅ Account created! Please login.")
                        time.sleep(1)
                        nav("login")
                    else:
                        st.error(msg)

            st.markdown("<div style='text-align:center;margin-top:12px'>Already have an account? </div>",
                        unsafe_allow_html=True)
            if st.button("🔐 Login", use_container_width=True):
                nav("login")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
def page_login():
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("""
        <div class="card fade-in">
            <h2 style="text-align:center;color:#6C63FF">🔐 Login</h2>
        </div>""", unsafe_allow_html=True)

        email = st.text_input("Email")
        pwd   = st.text_input("Password", type="password")

        if st.button("Login →", use_container_width=True):
            user = authenticate(email, pwd)
            if user:
                st.session_state.user = user
                st.success(f"Welcome back, {user['name']}!")
                time.sleep(0.5)
                dest = {"donor":"home","ngo":"ngo_dashboard","admin":"admin_panel"}.get(user["role"],"home")
                nav(dest)
            else:
                st.error("Invalid email or password.")

        if st.button("📝 Create Account", use_container_width=True):
            nav("signup")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BROWSE NGOs (Donor)
# ═══════════════════════════════════════════════════════════════════════════════
def page_browse_ngos():
    st.markdown('<div class="section-title">🔍 Browse Verified NGOs</div>', unsafe_allow_html=True)
    ngos = get_approved_ngos()

    if not ngos:
        st.info("No approved NGOs yet. Check back soon!")
        return

    # Filter bar
    c1, c2 = st.columns([2, 1])
    with c1:
        search = st.text_input("🔎 Search by name or cause", placeholder="e.g. education, health...")
    with c2:
        sort_by = st.selectbox("Sort by", ["Transparency Score ↓", "Risk % ↑", "Name A-Z"])

    if search:
        ngos = [n for n in ngos if search.lower() in n["name"].lower()
                or search.lower() in n["cause"].lower()]

    if sort_by == "Transparency Score ↓":
        ngos = sorted(ngos, key=lambda x: float(x["transparency_score"]), reverse=True)
    elif sort_by == "Risk % ↑":
        ngos = sorted(ngos, key=lambda x: float(x["risk_percent"]))
    else:
        ngos = sorted(ngos, key=lambda x: x["name"])

    for n in ngos:
        ts   = float(n["transparency_score"])
        risk = float(n["risk_percent"])
        sc   = score_color(ts)
        rc   = risk_color(risk)

        st.markdown(f"""
        <div class="card fade-in">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px">
                <div>
                    <div style="font-size:1.15rem;font-weight:700;color:#2D3748">{n['name']}</div>
                    <div style="color:#718096;font-size:0.88rem;margin-top:2px">
                        📍 {n['location']} &nbsp;|&nbsp; 🎯 {n['cause'].title()} &nbsp;|&nbsp; Est. {n['founded_year']}
                    </div>
                </div>
                <div style="text-align:right">
                    <span class="dna-badge">{n['trust_dna']}</span>
                </div>
            </div>
            <div style="margin:12px 0 6px">
                <span class="stat-chip {sc}">Transparency: {ts:.1f}%</span>
                <span class="stat-chip {rc}">Risk: {risk:.1f}%</span>
                <span class="stat-chip">Accuracy: {n['outcome_accuracy']}%</span>
            </div>
            <div style="font-size:0.88rem;color:#4A5568;margin-top:6px">{n['description'][:160]}{'...' if len(n.get('description',''))>160 else ''}</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([2, 1, 1])
        with c2:
            if st.button(f"📊 Details", key=f"det_{n['ngo_id']}", use_container_width=True):
                st.session_state.selected_ngo = n["ngo_id"]
                nav("ngo_detail")
        with c3:
            if st.session_state.user and st.session_state.user["role"] == "donor":
                if st.button(f"💙 Donate", key=f"don_{n['ngo_id']}", use_container_width=True):
                    st.session_state.donate_to = n["ngo_id"]
                    nav("donate")
            elif not st.session_state.user:
                if st.button(f"🔐 Login to Donate", key=f"ld_{n['ngo_id']}", use_container_width=True):
                    nav("login")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NGO DETAIL (Transparency for Donor)
# ═══════════════════════════════════════════════════════════════════════════════
def page_ngo_detail():
    ngo_id = st.session_state.get("selected_ngo")
    if not ngo_id:
        nav("browse_ngos")
        return
    n = get_ngo_by_id(ngo_id)
    if not n:
        st.error("NGO not found.")
        return

    ts   = float(n["transparency_score"])
    risk = float(n["risk_percent"])

    st.markdown(f"""
    <div class="card-accent fade-in">
        <h2 style="margin:0 0 6px">{n['name']}</h2>
        <div style="opacity:0.85">{n['cause'].title()} · {n['location']} · Since {n['founded_year']}</div>
        <div style="margin-top:14px"><span class="dna-badge">{n['trust_dna']}</span></div>
    </div>""", unsafe_allow_html=True)

    # Safety check widget
    safety = "✅ SAFE TO DONATE" if ts >= 60 and risk < 40 else (
             "⚠️ DONATE WITH CAUTION" if ts >= 40 else "🚨 HIGH RISK — CAUTION")
    color  = "#276749" if ts >= 60 and risk < 40 else ("#975A16" if ts >= 40 else "#C53030")
    bg     = "#F0FFF4"  if ts >= 60 and risk < 40 else ("#FFFBEA" if ts >= 40 else "#FFF5F5")
    st.markdown(f"""
    <div style="background:{bg};border-radius:12px;padding:18px;text-align:center;margin-bottom:16px">
        <div style="font-size:1.3rem;font-weight:800;color:{color}">{safety}</div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**📊 Transparency Breakdown**")
        render_score_bar("Transparency Score",     ts)
        render_score_bar("Allocation Efficiency",  float(n["allocation_efficiency"]))
        render_score_bar("Outcome Accuracy",       float(n["outcome_accuracy"]))
        render_score_bar("Timeliness",             float(n["timeliness_score"]))
        render_score_bar("Donation Consistency",   float(n["donation_consistency"]))
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**📈 Impact Summary**")
        impact = get_ngo_impact_summary(ngo_id)
        st.metric("Total Raised",       f"₹{impact['total_raised']:,.0f}")
        st.metric("Total Allocated",    f"₹{impact['total_allocated']:,.0f}")
        st.metric("Beneficiaries",      impact["total_beneficiaries"])
        st.metric("Avg Outcome Accuracy", f"{impact['avg_outcome_accuracy']}%")
        st.metric("Activities Run",     impact["num_activities"])
        st.markdown("</div>", unsafe_allow_html=True)

    # Impact Prediction
    st.markdown('<div class="section-title">🔮 Impact Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    pred_amt = st.number_input("Enter donation amount to predict impact (₹)", min_value=100, value=1000, step=100)
    pred = predict_impact(ngo_id, pred_amt)
    st.markdown(f"""
    <div style="background:#EBF4FF;border-radius:10px;padding:16px;margin-top:8px">
        <span style="font-size:1.1rem">💡 <b>₹{pred_amt:,.0f}</b> could support 
        <b style="color:#6C63FF">{pred['predicted_beneficiaries']} beneficiaries</b> 
        via <b>{pred['top_activity']}</b></span>
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Past outcomes
    outcomes = get_outcomes_by_ngo(ngo_id)
    if outcomes:
        st.markdown('<div class="section-title">📋 Past Outcomes</div>', unsafe_allow_html=True)
        rows = "".join([
            f"<tr><td>{o['activity_type'].title()}</td><td>{o['planned_units']}</td>"
            f"<td>{o['actual_units']}</td><td>{o['outcome_accuracy']}%</td>"
            f"<td>{o['beneficiaries_reached']}</td></tr>"
            for o in outcomes[-8:]
        ])
        st.markdown(f"""
        <table class="custom-table">
            <tr><th>Activity</th><th>Planned</th><th>Delivered</th><th>Accuracy</th><th>Beneficiaries</th></tr>
            {rows}
        </table>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.user and st.session_state.user["role"] == "donor":
        if st.button("💙 Donate to this NGO", use_container_width=True):
            st.session_state.donate_to = ngo_id
            nav("donate")
    if st.button("← Back to NGOs"):
        nav("browse_ngos")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DONATE (Payment simulation)
# ═══════════════════════════════════════════════════════════════════════════════
def page_donate():
    user = st.session_state.user
    if not user or user["role"] != "donor":
        nav("login"); return

    ngo_id = st.session_state.get("donate_to")
    if not ngo_id:
        nav("browse_ngos"); return
    ngo = get_ngo_by_id(ngo_id)
    if not ngo:
        st.error("NGO not found."); return

    stage = st.session_state.payment_stage

    # ── STAGE 0: Form ────────────────────────────────────────────────────────
    if stage is None:
        st.markdown(f"""
        <div class="card fade-in">
            <h2 style="color:#6C63FF">💙 Donate to {ngo['name']}</h2>
            <div style="color:#718096;margin-bottom:6px">{ngo['cause'].title()} · {ngo['location']}</div>
            <span class="dna-badge">{ngo['trust_dna']}</span>
        </div>""", unsafe_allow_html=True)

        # Show quick safety summary
        ts = float(ngo["transparency_score"])
        risk = float(ngo["risk_percent"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Transparency", f"{ts:.1f}%")
        c2.metric("Risk", f"{risk:.1f}%")
        c3.metric("Outcome Accuracy", f"{ngo['outcome_accuracy']}%")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        amount = st.number_input("💵 Donation Amount (₹)", min_value=10, value=500, step=50)
        upi    = st.text_input("📱 UPI ID", placeholder="yourname@upi")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("💳 PAY NOW", use_container_width=True):
            if not upi or "@" not in upi:
                st.error("Please enter a valid UPI ID (e.g. name@upi)")
            else:
                st.session_state.payment_data  = {"amount": amount, "upi": upi}
                st.session_state.payment_stage = "processing"
                st.rerun()

    # ── STAGE 1: Processing spinner ──────────────────────────────────────────
    elif stage == "processing":
        st.markdown("""
        <div style="text-align:center;padding:60px 20px" class="fade-in">
            <div style="font-size:3rem">⚡</div>
            <h2>Processing Payment...</h2>
            <div style="color:#718096">Connecting to payment gateway</div>
        </div>""", unsafe_allow_html=True)
        prog = st.progress(0)
        for i in range(101):
            prog.progress(i)
            time.sleep(0.018)
        st.session_state.payment_stage = "success"
        st.rerun()

    # ── STAGE 2: Success ─────────────────────────────────────────────────────
    elif stage == "success":
        pd = st.session_state.payment_data
        # Save to DB
        donation = create_donation(user["user_id"], ngo_id, pd["amount"], pd["upi"])
        receipt  = create_receipt(donation, user["name"], user["email"], ngo["name"])
        # Run analysis to update scores
        run_ngo_analysis(ngo_id)

        st.markdown("""
        <div style="text-align:center;padding:30px" class="fade-in">
            <div style="font-size:4rem">🎉</div>
            <h1 style="color:#276749">Payment Successful!</h1>
        </div>""", unsafe_allow_html=True)

        # Thank you card
        st.markdown(f"""
        <div class="card-success fade-in" style="text-align:center">
            <h3>Thank you, {user['name']}! ❤️</h3>
            <p>Your donation of <b>₹{pd['amount']:,.0f}</b> to <b>{ngo['name']}</b> has been recorded.<br>
            Every rupee is traced through our DOTE engine — you'll see the impact!</p>
        </div>""", unsafe_allow_html=True)

        # Receipt
        st.markdown('<div class="section-title">🧾 Donation Receipt</div>', unsafe_allow_html=True)
        receipt_text = f"""
╔══════════════════════════════════════════════╗
             NSITN — OFFICIAL RECEIPT           
══════════════════════════════════════════════
  Receipt ID   : {receipt['receipt_id']}
  Donation ID  : {receipt['donation_id']}
══════════════════════════════════════════════
  Donor Name   : {receipt['donor_name']}
  Donor Email  : {receipt['donor_email']}
  UPI ID       : {receipt['upi_id']}
══════════════════════════════════════════════
  NGO Name     : {receipt['ngo_name']}
  Amount       : ₹{float(receipt['amount']):,.2f}
  Date/Time    : {receipt['donated_at']}
══════════════════════════════════════════════
  Trust DNA    : {ngo['trust_dna']}
  Transparency : {ngo['transparency_score']}%
  Risk         : {ngo['risk_percent']}%
══════════════════════════════════════════════
  Generated    : {receipt['generated_at']}
  NSITN v2.0   — Powered by DOTE Engine
╚══════════════════════════════════════════════╝
""".strip()
        st.markdown(f'<div class="receipt-box">{receipt_text}</div>', unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download Receipt (.txt)",
            data=receipt_text,
            file_name=f"NSITN_Receipt_{receipt['receipt_id']}.txt",
            mime="text/plain",
            use_container_width=True
        )

        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.payment_stage = None
            st.session_state.payment_data  = None
            nav("home")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: MY DONATIONS (Donor)
# ═══════════════════════════════════════════════════════════════════════════════
def page_my_donations():
    user = st.session_state.user
    if not user:
        nav("login"); return

    st.markdown('<div class="section-title">💰 My Donations</div>', unsafe_allow_html=True)
    donations = get_donations_by_donor(user["user_id"])

    if not donations:
        st.info("You haven't made any donations yet.")
        if st.button("🔍 Browse NGOs"): nav("browse_ngos")
        return

    total = sum(float(d["amount"]) for d in donations)
    st.markdown(f"""
    <div class="card-accent fade-in" style="padding:20px">
        <span style="font-size:1.4rem;font-weight:700">₹{total:,.0f}</span>
        <span style="opacity:0.85"> total donated across {len(donations)} donations</span>
    </div>""", unsafe_allow_html=True)

    for d in reversed(donations):
        ngo = get_ngo_by_id(d["ngo_id"])
        ngo_name = ngo["name"] if ngo else "Unknown NGO"
        receipt = get_receipt_by_donation(d["donation_id"])

        st.markdown(f"""
        <div class="card fade-in">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                <div>
                    <div style="font-weight:700;font-size:1rem">{ngo_name}</div>
                    <div style="color:#718096;font-size:0.85rem">{d['donated_at']} · UPI: {d['upi_id']}</div>
                    <div style="font-size:0.8rem;color:#A0AEC0">ID: {d['donation_id']} · Receipt: {d['receipt_id']}</div>
                </div>
                <div style="font-size:1.5rem;font-weight:800;color:#6C63FF">₹{float(d['amount']):,.0f}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        if receipt:
            receipt_text = f"""
NSITN Receipt — {receipt['receipt_id']}
NGO: {receipt['ngo_name']} | Amount: ₹{float(receipt['amount']):,.2f}
Donor: {receipt['donor_name']} | UPI: {receipt['upi_id']}
Date: {receipt['donated_at']}
Generated: {receipt['generated_at']}
""".strip()
            st.download_button(
                f"⬇️ Receipt {d['receipt_id']}",
                data=receipt_text,
                file_name=f"NSITN_{d['receipt_id']}.txt",
                key=f"dl_{d['donation_id']}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NGO DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_ngo_dashboard():
    user = st.session_state.user
    if not user or user["role"] != "ngo":
        nav("login"); return

    # Find NGO record by email
    ngos = get_all_ngos()
    ngo  = next((n for n in ngos if n["email"] == user["email"]), None)
    if not ngo:
        st.warning("NGO profile not found. Please register your NGO.")
        return

    # Run fresh analysis
    analysis = run_ngo_analysis(ngo["ngo_id"])
    ngo = get_ngo_by_id(ngo["ngo_id"])   # refresh

    status_color = {"approved":"#276749","pending":"#975A16","rejected":"#C53030"}
    sc = status_color.get(ngo["status"], "#718096")

    st.markdown(f"""
    <div class="card-accent fade-in">
        <h2 style="margin:0 0 4px">{ngo['name']}</h2>
        <div style="opacity:0.85">{ngo['cause'].title()} · {ngo['location']}</div>
        <div style="margin-top:10px">
            <span class="dna-badge">{ngo['trust_dna']}</span>
            <span style="background:rgba(255,255,255,0.25);padding:4px 14px;border-radius:999px;font-size:13px;margin-left:8px;font-weight:600;color:white">
                Status: {ngo['status'].upper()}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

    if ngo["status"] == "pending":
        st.markdown('<div class="card-warning">⏳ Your NGO is pending admin approval. Scores are being computed.</div>',
                    unsafe_allow_html=True)
    elif ngo["status"] == "rejected":
        st.markdown(f'<div class="card-danger">❌ Rejected. Admin note: {ngo["admin_note"]}</div>',
                    unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transparency", f"{analysis['transparency']:.1f}%")
    c2.metric("Risk",         f"{analysis['risk']:.1f}%")
    c3.metric("Outcome Acc.", f"{analysis['breakdown']['outcome_accuracy']:.1f}%")
    c4.metric("Alloc Eff.",   f"{analysis['breakdown']['allocation_efficiency']:.1f}%")

    if analysis["anomalies"]:
        st.markdown('<div class="section-title">⚠️ Anomalies Detected</div>', unsafe_allow_html=True)
        for a in analysis["anomalies"]:
            st.markdown(f'<div class="card-warning">{a.get("flag","⚠️ Anomaly")} | Activity: {a.get("activity","")} | Accuracy: {a.get("accuracy","")}%</div>',
                        unsafe_allow_html=True)

    # Score breakdown
    st.markdown('<div class="section-title">📊 Score Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    bd = analysis["breakdown"]
    render_score_bar("Allocation Efficiency", bd["allocation_efficiency"])
    render_score_bar("Outcome Accuracy",      bd["outcome_accuracy"])
    render_score_bar("Timeliness",            bd["timeliness_score"])
    render_score_bar("Donation Consistency",  bd["donation_consistency"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Explanations
    with st.expander("🔬 See Score Explanations"):
        for k, v in bd["explanations"].items():
            st.markdown(f"**{k.replace('_',' ').title()}:** {v}")

    # Quick actions
    st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📁 Add Allocation", use_container_width=True): nav("add_allocation")
    with c2:
        if st.button("📊 Record Outcome", use_container_width=True): nav("record_outcome")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ADD ALLOCATION (DOTE)
# ═══════════════════════════════════════════════════════════════════════════════
def page_add_allocation():
    user = st.session_state.user
    if not user or user["role"] != "ngo":
        nav("login"); return

    ngos = get_all_ngos()
    ngo  = next((n for n in ngos if n["email"] == user["email"]), None)
    if not ngo:
        st.error("NGO profile not found."); return

    st.markdown('<div class="section-title">📁 Add Donation Allocation (DOTE)</div>',
                unsafe_allow_html=True)

    # Show donations available to allocate
    donations = get_donations_by_ngo(ngo["ngo_id"])
    if not donations:
        st.info("No donations received yet. Wait for donors to contribute.")
        return

    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    don_options = {d["donation_id"]: f"₹{d['amount']} on {d['donated_at'][:10]}" for d in donations}
    sel_don_id  = st.selectbox("Link to Donation", list(don_options.keys()),
                               format_func=lambda x: don_options[x])

    activity = st.selectbox("Activity Type", list(UNIT_COST_DEFAULTS.keys()),
                            format_func=str.title)
    default_cost = UNIT_COST_DEFAULTS.get(activity, 100)

    c1, c2 = st.columns(2)
    with c1:
        unit_cost     = st.number_input("Unit Cost (₹)", min_value=1, value=default_cost)
    with c2:
        units_planned = st.number_input("Units Planned", min_value=1, value=100)

    total_cost = unit_cost * units_planned
    st.markdown(f"""
    <div class="card-success" style="margin-top:10px">
        <b>Auto-calculated:</b><br>
        💰 Total Cost = ₹{total_cost:,.0f} &nbsp;|&nbsp;
        👥 Est. Beneficiaries = ~{max(1, units_planned//3)}
    </div>""", unsafe_allow_html=True)

    alloc_date   = st.date_input("Allocation Start Date", value=date.today())
    outcome_date = st.date_input("Expected Outcome Date")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✅ Save Allocation", use_container_width=True):
        alloc = add_allocation(
            ngo["ngo_id"], sel_don_id, activity,
            unit_cost, units_planned,
            alloc_date.strftime("%Y-%m-%d"), outcome_date.strftime("%Y-%m-%d")
        )
        run_ngo_analysis(ngo["ngo_id"])
        st.success(f"✅ Allocation saved! ID: {alloc['alloc_id']}")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RECORD OUTCOME
# ═══════════════════════════════════════════════════════════════════════════════
def page_record_outcome():
    user = st.session_state.user
    if not user or user["role"] != "ngo":
        nav("login"); return

    ngos = get_all_ngos()
    ngo  = next((n for n in ngos if n["email"] == user["email"]), None)
    if not ngo:
        st.error("NGO profile not found."); return

    st.markdown('<div class="section-title">📊 Record Activity Outcome</div>', unsafe_allow_html=True)

    allocations = get_allocations_by_ngo(ngo["ngo_id"])
    if not allocations:
        st.info("No allocations found. Add allocations first.")
        return

    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    alloc_options = {
        a["alloc_id"]: f"{a['activity_type'].title()} — {a['units_planned']} units (₹{a['total_cost']})"
        for a in allocations
    }
    sel_alloc_id = st.selectbox("Select Allocation", list(alloc_options.keys()),
                                format_func=lambda x: alloc_options[x])

    alloc = next(a for a in allocations if a["alloc_id"] == sel_alloc_id)
    st.markdown(f"""
    <div class="card-warning">
        📋 Planned: <b>{alloc['units_planned']} {alloc['activity_type']}s</b>
        &nbsp;|&nbsp; Unit cost: ₹{alloc['unit_cost']}
        &nbsp;|&nbsp; Total budget: ₹{alloc['total_cost']}
    </div>""", unsafe_allow_html=True)

    actual_units = st.number_input("Actual Units Delivered", min_value=0,
                                   max_value=int(float(alloc["units_planned"])) * 2,
                                   value=int(float(alloc["units_planned"])))
    beneficiaries = st.number_input("Beneficiaries Reached", min_value=0, value=max(1, actual_units // 3))

    planned = float(alloc["units_planned"])
    accuracy = min((actual_units / planned * 100) if planned > 0 else 0, 100)
    acc_color = "#276749" if accuracy >= 70 else ("#975A16" if accuracy >= 50 else "#C53030")
    st.markdown(f"""
    <div style="background:#EBF4FF;border-radius:10px;padding:14px;margin-top:8px">
        Outcome Accuracy = <b style="color:{acc_color}">{accuracy:.1f}%</b>
        &nbsp;{'✅' if accuracy>=70 else ('⚠️' if accuracy>=50 else '🚨')}
        &nbsp;{'Good' if accuracy>=70 else ('Moderate' if accuracy>=50 else 'Below threshold — will raise risk score')}
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✅ Submit Outcome", use_container_width=True):
        outcome, msg = record_outcome(ngo["ngo_id"], sel_alloc_id, actual_units, beneficiaries)
        if outcome:
            run_ngo_analysis(ngo["ngo_id"])
            st.success(f"✅ Outcome recorded! Accuracy: {outcome['outcome_accuracy']}%")
        else:
            st.error(msg)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NGO ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
def page_ngo_analytics():
    user = st.session_state.user
    if not user or user["role"] != "ngo":
        nav("login"); return

    ngos = get_all_ngos()
    ngo  = next((n for n in ngos if n["email"] == user["email"]), None)
    if not ngo:
        st.error("NGO profile not found."); return

    st.markdown('<div class="section-title">📈 NGO Analytics</div>', unsafe_allow_html=True)
    impact = get_ngo_impact_summary(ngo["ngo_id"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Raised",    f"₹{impact['total_raised']:,.0f}")
    c2.metric("Total Allocated", f"₹{impact['total_allocated']:,.0f}")
    c3.metric("Beneficiaries",   impact["total_beneficiaries"])
    c4.metric("Avg Accuracy",    f"{impact['avg_outcome_accuracy']}%")

    # Allocations table
    allocations = get_allocations_by_ngo(ngo["ngo_id"])
    if allocations:
        st.markdown('<div class="section-title">📁 Allocations (DOTE)</div>', unsafe_allow_html=True)
        rows = "".join([
            f"<tr><td>{a['alloc_id']}</td><td>{a['activity_type'].title()}</td>"
            f"<td>₹{a['unit_cost']}</td><td>{a['units_planned']}</td>"
            f"<td>{a['units_delivered']}</td><td>₹{a['total_cost']}</td>"
            f"<td>{a['outcome_date']}</td></tr>"
            for a in allocations
        ])
        st.markdown(f"""
        <table class="custom-table">
            <tr><th>ID</th><th>Activity</th><th>Unit Cost</th><th>Planned</th>
            <th>Delivered</th><th>Total Cost</th><th>Due Date</th></tr>
            {rows}
        </table>""", unsafe_allow_html=True)

    # Outcomes
    outcomes = get_outcomes_by_ngo(ngo["ngo_id"])
    if outcomes:
        st.markdown('<div class="section-title">📊 Outcomes</div>', unsafe_allow_html=True)
        rows = "".join([
            f"<tr><td>{o['activity_type'].title()}</td><td>{o['planned_units']}</td>"
            f"<td>{o['actual_units']}</td><td>{o['outcome_accuracy']}%</td>"
            f"<td>{o['beneficiaries_reached']}</td><td>{o['recorded_at'][:10]}</td></tr>"
            for o in outcomes
        ])
        st.markdown(f"""
        <table class="custom-table">
            <tr><th>Activity</th><th>Planned</th><th>Actual</th><th>Accuracy</th>
            <th>Beneficiaries</th><th>Date</th></tr>
            {rows}
        </table>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN PANEL
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin_panel():
    user = st.session_state.user
    if not user or user["role"] != "admin":
        nav("login"); return

    st.markdown("""
    <div class="card-accent fade-in">
        <h2>🛡️ Admin Verification Panel</h2>
        <div style="opacity:0.85">Review NGOs before they go public to donors</div>
    </div>""", unsafe_allow_html=True)

    pending = get_pending_ngos()
    if not pending:
        st.success("✅ No pending NGOs. All caught up!")
    else:
        st.markdown(f'<div class="section-title">⏳ Pending NGOs ({len(pending)})</div>',
                    unsafe_allow_html=True)
        for n in pending:
            analysis = run_ngo_analysis(n["ngo_id"])
            n = get_ngo_by_id(n["ngo_id"])   # refresh scores

            ts   = float(n["transparency_score"])
            risk = float(n["risk_percent"])

            st.markdown(f"""
            <div class="card fade-in">
                <div style="font-size:1.1rem;font-weight:700">{n['name']}</div>
                <div style="color:#718096;font-size:0.85rem;margin-bottom:10px">
                    {n['cause'].title()} · {n['location']} · Reg: {n['registration_number']}
                </div>
                <span class="stat-chip {score_color(ts)}">Transparency: {ts:.1f}%</span>
                <span class="stat-chip {risk_color(risk)}">Risk: {risk:.1f}%</span>
                <span class="dna-badge" style="font-size:0.8rem;padding:4px 12px">{n['trust_dna']}</span>
                <span class="stat-chip">Outcome Acc: {n['outcome_accuracy']}%</span>
                <div style="margin-top:10px;font-size:0.88rem;color:#4A5568">{n['description'][:200]}</div>
            </div>""", unsafe_allow_html=True)

            if analysis["anomalies"]:
                for a in analysis["anomalies"]:
                    st.markdown(f'<div class="card-warning">{a.get("flag","⚠️ Anomaly")}</div>',
                                unsafe_allow_html=True)

            note = st.text_input(f"Admin note (optional)", key=f"note_{n['ngo_id']}")
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button(f"✅ Approve", key=f"app_{n['ngo_id']}", use_container_width=True):
                    admin_decision(n["ngo_id"], "approved", note)
                    st.success(f"✅ {n['name']} approved!")
                    st.rerun()
            with c2:
                if st.button(f"❌ Reject", key=f"rej_{n['ngo_id']}", use_container_width=True):
                    admin_decision(n["ngo_id"], "rejected", note or "Did not meet transparency standards.")
                    st.warning(f"❌ {n['name']} rejected.")
                    st.rerun()
            st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL NGOs (Admin)
# ═══════════════════════════════════════════════════════════════════════════════
def page_all_ngos():
    user = st.session_state.user
    if not user or user["role"] != "admin":
        nav("login"); return

    st.markdown('<div class="section-title">🏢 All NGOs</div>', unsafe_allow_html=True)
    ngos = get_all_ngos()
    for n in ngos:
        status_bg = {"approved":"#F0FFF4","pending":"#FFFBEA","rejected":"#FFF5F5"}.get(n["status"],"#F7FAFC")
        st.markdown(f"""
        <div class="card fade-in" style="background:{status_bg}">
            <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
                <div>
                    <b>{n['name']}</b> · {n['cause'].title()} · {n['location']}<br>
                    <span class="stat-chip {score_color(n['transparency_score'])}">T: {n['transparency_score']}%</span>
                    <span class="stat-chip {risk_color(n['risk_percent'])}">R: {n['risk_percent']}%</span>
                    <span class="dna-badge" style="font-size:0.75rem;padding:3px 10px">{n['trust_dna']}</span>
                </div>
                <div>
                    <span style="font-weight:700;color:{'#276749' if n['status']=='approved' else '#C53030' if n['status']=='rejected' else '#975A16'}">
                        {n['status'].upper()}
                    </span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PLATFORM STATS (Admin)
# ═══════════════════════════════════════════════════════════════════════════════
def page_platform_stats():
    user = st.session_state.user
    if not user or user["role"] != "admin":
        nav("login"); return

    st.markdown('<div class="section-title">📊 Platform Statistics</div>', unsafe_allow_html=True)
    s = get_platform_stats()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Approved NGOs",    s["total_ngos"])
    c2.metric("Total Donations",  s["total_donations"])
    c3.metric("Total Raised",     f"₹{s['total_raised']:,.0f}")
    c4.metric("Beneficiaries",    s["total_beneficiaries"])

    all_ngos = get_all_ngos()
    approved = sum(1 for n in all_ngos if n["status"] == "approved")
    pending  = sum(1 for n in all_ngos if n["status"] == "pending")
    rejected = sum(1 for n in all_ngos if n["status"] == "rejected")

    st.markdown('<div class="section-title">NGO Status Breakdown</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("✅ Approved", approved)
    c2.metric("⏳ Pending",  pending)
    c3.metric("❌ Rejected", rejected)

    if approved > 0:
        st.markdown('<div class="section-title">Top NGOs by Transparency</div>', unsafe_allow_html=True)
        top = sorted(
            [n for n in all_ngos if n["status"] == "approved"],
            key=lambda x: float(x["transparency_score"]), reverse=True
        )[:5]
        rows = "".join([
            f"<tr><td>{n['name']}</td><td>{n['transparency_score']}%</td>"
            f"<td>{n['risk_percent']}%</td><td>{n['trust_dna']}</td></tr>"
            for n in top
        ])
        st.markdown(f"""
        <table class="custom-table">
            <tr><th>NGO</th><th>Transparency</th><th>Risk</th><th>Trust DNA</th></tr>
            {rows}
        </table>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AI CHATBOT
# ═══════════════════════════════════════════════════════════════════════════════
def page_chatbot():
    st.markdown("""
    <div class="card-accent fade-in" style="padding:24px">
        <h2 style="margin:0 0 4px">💬 NSITN AI Assistant</h2>
        <div style="opacity:0.85">Ask me anything about NGOs, transparency, donations & more</div>
    </div>""", unsafe_allow_html=True)

    # Quick prompts
    st.markdown("**Quick questions:**")
    quick = [
        "What is Trust DNA?", "How is risk calculated?",
        "Platform stats", "Explain transparency score",
        "How do donations work?", "Predict impact of ₹2000"
    ]
    cols = st.columns(3)
    for i, q in enumerate(quick):
        with cols[i % 3]:
            if st.button(q, key=f"qp_{i}", use_container_width=True):
                st.session_state.chat_history.append((q, chat(q)))
                st.rerun()

    # Chat display
    st.markdown("---")
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f'<div class="chat-bubble-user">🧑 {user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble-bot">🤖 {bot_msg}</div>', unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_input = st.text_input("Message", placeholder="Ask me anything...", label_visibility="collapsed")
        with c2:
            submit = st.form_submit_button("Send →", use_container_width=True)

    if submit and user_input.strip():
        response = chat(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append((user_input, response))
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    render_sidebar()
    page = st.session_state.page

    routes = {
        "home":           page_home,
        "login":          page_login,
        "signup":         page_signup,
        "browse_ngos":    page_browse_ngos,
        "ngo_detail":     page_ngo_detail,
        "donate":         page_donate,
        "my_donations":   page_my_donations,
        "ngo_dashboard":  page_ngo_dashboard,
        "add_allocation": page_add_allocation,
        "record_outcome": page_record_outcome,
        "ngo_analytics":  page_ngo_analytics,
        "admin_panel":    page_admin_panel,
        "all_ngos":       page_all_ngos,
        "platform_stats": page_platform_stats,
        "chatbot":        page_chatbot,
    }

    fn = routes.get(page, page_home)
    fn()


if __name__ == "__main__":
    main()