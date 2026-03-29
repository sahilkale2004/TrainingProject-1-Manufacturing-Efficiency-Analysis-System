import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(
    page_title="Manufacturing Efficiency System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">

<style>
/* ── Base ── */
:root {
    --bg:        #0d0f12;
    --surface:   #141720;
    --card:      #1a1e28;
    --border:    #252b3a;
    --accent:    #f59e0b;
    --accent2:   #3b82f6;
    --success:   #10b981;
    --danger:    #ef4444;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --label:     #94a3b8;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ── Hero Header ── */
.hero {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 2.5rem 2.5rem 2rem;
    background: linear-gradient(135deg, #141720 0%, #1a1e28 60%, #1e2235 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-icon {
    font-size: 3rem;
    filter: drop-shadow(0 0 16px rgba(245,158,11,0.5));
}
.hero-text h1 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    margin: 0 0 0.25rem !important;
    letter-spacing: 0.04em;
}
.hero-text p {
    color: var(--muted);
    font-size: 0.9rem;
    margin: 0;
    font-weight: 300;
    letter-spacing: 0.03em;
}
.hero-badge {
    margin-left: auto;
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Section Cards ── */
.section-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.section-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.card-process::after  { background: var(--accent); }
.card-machine::after  { background: var(--accent2); }
.card-metrics::after  { background: var(--success); }

.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-title.amber { color: var(--accent); }
.section-title.blue  { color: var(--accent2); }
.section-title.green { color: var(--success); }
.section-title::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 6px currentColor;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(245,158,11,0.15) !important;
}

/* Labels */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    color: var(--label) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.2rem !important;
}

/* Selectbox dropdown arrow */
[data-testid="stSelectbox"] svg { color: var(--muted) !important; }

/* ── Submit Button ── */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%) !important;
    color: #0d0f12 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(245,158,11,0.3) !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(245,158,11,0.45) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── Result Panel ── */
.result-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    gap: 3rem;
    animation: slideUp 0.4s ease;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.score-ring {
    position: relative;
    width: 140px; height: 140px;
    flex-shrink: 0;
}
.score-ring svg { transform: rotate(-90deg); }
.score-label {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}
.score-label .val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    line-height: 1;
}
.score-label .sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 2px;
}

.result-info h2 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.5rem !important;
}
.result-info p {
    color: var(--muted);
    font-size: 0.85rem;
    margin: 0 0 1rem;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.06em;
}
.status-pill.high {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: var(--success);
}
.status-pill.low {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.3);
    color: var(--danger);
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ── Stat row ── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.stat-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    text-align: center;
}
.stat-item .s-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
}
.stat-item .s-key {
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-top: 1px;
}

/* Error / warning */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Column gaps */
[data-testid="stHorizontalBlock"] { gap: 1.5rem !important; }

/* Input step buttons */
[data-testid="stNumberInput"] button {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--muted) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon">⚙️</div>
    <div class="hero-text">
        <h1>Manufacturing Efficiency Analysis System</h1>
        <p>ML-powered efficiency scoring from machine, material, and process parameters</p>
    </div>
    <div class="hero-badge">v1.0 · Linear Regression</div>
</div>
""", unsafe_allow_html=True)


# ── Section header helper ────────────────────────────────────────────────────
def section_header(label, color_class):
    st.markdown(f'<div class="section-title {color_class}">{label}</div>', unsafe_allow_html=True)


# ── Form ─────────────────────────────────────────────────────────────────────
with st.form("manufacturing_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-card card-process">', unsafe_allow_html=True)
        section_header("Process Parameters", "amber")
        inj_temp   = st.number_input("Injection Temperature (°C)", value=220.0, step=1.0)
        inj_press  = st.number_input("Injection Pressure (bar)",   value=120.0, step=1.0)
        cycle_time = st.number_input("Cycle Time (s)",             value=30.0,  step=0.5)
        cool_time  = st.number_input("Cooling Time (s)",           value=12.0,  step=0.5)
        viscosity  = st.number_input("Material Viscosity (cP)",    value=250.0, step=5.0)
        amb_temp   = st.number_input("Ambient Temperature (°C)",   value=25.0,  step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card card-machine">', unsafe_allow_html=True)
        section_header("Machine & Operator", "blue")
        machine_age   = st.number_input("Machine Age (years)",         value=5.0,  step=0.5)
        op_exp        = st.number_input("Operator Experience (years)", value=5.0,  step=0.5)
        maint_hours   = st.number_input("Maintenance Hours",           value=50.0, step=1.0)
        shift         = st.selectbox("Shift",         ["Day", "Evening", "Night"])
        machine_type  = st.selectbox("Machine Type",  ["Type_A", "Type_B", "Type_C"])
        material_grade = st.selectbox("Material Grade", ["Economy", "Standard", "Premium"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="section-card card-metrics">', unsafe_allow_html=True)
        section_header("Metrics & Time", "green")
        day           = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        temp_press    = st.number_input("Temp / Pressure Ratio",  value=1.8,  step=0.1)
        total_cycle   = st.number_input("Total Cycle Time (s)",   value=45.0, step=0.5)
        utilization   = st.number_input("Machine Utilization",    value=0.5,  step=0.01, min_value=0.0, max_value=1.0)
        pph           = st.number_input("Parts Per Hour",         value=30.0, step=1.0)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("⚡  Run Efficiency Analysis")


# ── Result ───────────────────────────────────────────────────────────────────
if submit:
    payload = {
        "Injection_Temperature":   inj_temp,
        "Injection_Pressure":      inj_press,
        "Cycle_Time":              cycle_time,
        "Cooling_Time":            cool_time,
        "Material_Viscosity":      viscosity,
        "Ambient_Temperature":     amb_temp,
        "Machine_Age":             machine_age,
        "Operator_Experience":     op_exp,
        "Maintenance_Hours":       maint_hours,
        "Shift":                   shift,
        "Machine_Type":            machine_type,
        "Material_Grade":          material_grade,
        "Day_of_Week":             day,
        "Temperature_Pressure_Ratio": temp_press,
        "Total_Cycle_Time":        total_cycle,
        "Machine_Utilization":     utilization,
        "Parts_Per_Hour":          pph,
    }

    with st.spinner(""):
        try:
            response = requests.post("https://trainingproject-1.onrender.com/predict", json=payload)

            if response.status_code == 200:
                score = response.json()["predicted_efficiency_score"]
                pct   = min(max(score, 0.0), 1.0) * 100
                high  = score > 0.5

                # SVG ring params
                radius = 54
                circ   = 2 * 3.14159 * radius
                dash   = (pct / 100) * circ
                color  = "#10b981" if high else "#ef4444"
                status_class = "high" if high else "low"
                status_label = "HIGH EFFICIENCY" if high else "LOW EFFICIENCY"
                status_icon  = "▲" if high else "▼"
                advice = (
                    "All parameters within optimal range. System operating efficiently."
                    if high else
                    "Review cycle time, machine utilization, and material viscosity for improvements."
                )

                st.markdown(f"""
                <div class="result-panel">
                    <div class="score-ring">
                        <svg width="140" height="140" viewBox="0 0 140 140">
                            <circle cx="70" cy="70" r="{radius}" fill="none"
                                    stroke="#252b3a" stroke-width="10"/>
                            <circle cx="70" cy="70" r="{radius}" fill="none"
                                    stroke="{color}" stroke-width="10"
                                    stroke-dasharray="{dash:.1f} {circ:.1f}"
                                    stroke-linecap="round"
                                    style="filter:drop-shadow(0 0 8px {color})"/>
                        </svg>
                        <div class="score-label">
                            <div class="val" style="color:{color}">{score:.3f}</div>
                            <div class="sub">Score</div>
                        </div>
                    </div>
                    <div class="result-info">
                        <h2 style="color:{color}">Analysis Complete</h2>
                        <p>{advice}</p>
                        <div class="status-pill {status_class}">
                            <div class="status-dot"></div>
                            {status_icon} {status_label}
                        </div>
                        <div class="stat-row">
                            <div class="stat-item">
                                <div class="s-val">{pct:.1f}%</div>
                                <div class="s-key">Efficiency %</div>
                            </div>
                            <div class="stat-item">
                                <div class="s-val">{pph:.0f}</div>
                                <div class="s-key">Parts / Hour</div>
                            </div>
                            <div class="stat-item">
                                <div class="s-val">{utilization:.0%}</div>
                                <div class="s-key">Utilization</div>
                            </div>
                            <div class="stat-item">
                                <div class="s-val">{shift}</div>
                                <div class="s-key">Shift</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"Backend error {response.status_code} — ensure the API is running.")

        except Exception as e:
            st.error(f"Connection failed: {e}")
