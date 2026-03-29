import streamlit as st
import requests
import json

st.set_page_config(
    page_title="CardioScan — Heart Disease Predictor",
    page_icon="🫀",
    layout="centered"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0f14 !important;
    color: #e8e6e1;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0d0f14 !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
footer { display: none !important; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-icon {
    font-size: 3.2rem;
    display: block;
    margin-bottom: 0.6rem;
    animation: pulse 2.2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    color: #ffffff;
    margin: 0 0 0.4rem;
    letter-spacing: -0.02em;
    line-height: 1.15;
}
.hero h1 span { color: #e8443a; }
.hero p {
    color: #7a7f8e;
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ── Section Labels ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #e8443a;
    margin: 2rem 0 0.9rem;
    padding-left: 1px;
}

/* ── Card / Form Container ── */
.form-card {
    background: #13161d;
    border: 1px solid #1e2230;
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 1.2rem;
}

/* ── Streamlit Widget Overrides ── */
label[data-baseweb="label"] > div,
.stSelectbox label,
.stNumberInput label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #9aa0b0 !important;
    letter-spacing: 0.01em;
    margin-bottom: 4px !important;
}

/* Inputs */
input[type="number"],
div[data-baseweb="select"] > div {
    background: #0d0f14 !important;
    border: 1px solid #2a2f3d !important;
    border-radius: 8px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s;
}
input[type="number"]:focus,
div[data-baseweb="select"]:focus-within > div {
    border-color: #e8443a !important;
    box-shadow: 0 0 0 3px rgba(232,68,58,0.12) !important;
}

/* Dropdown menu */
ul[data-baseweb="menu"] {
    background: #1a1e28 !important;
    border: 1px solid #2a2f3d !important;
    border-radius: 8px !important;
}
li[role="option"]:hover {
    background: #e8443a22 !important;
}

/* ── Submit Button ── */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #e8443a 0%, #c0302a 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    margin-top: 1.2rem !important;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.15s;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px);
}
div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0);
}

/* ── Result Cards ── */
.result-box {
    border-radius: 14px;
    padding: 1.6rem 2rem;
    margin-top: 1.6rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    animation: fadeUp 0.4s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-box.danger {
    background: rgba(232,68,58,0.1);
    border: 1px solid rgba(232,68,58,0.35);
}
.result-box.safe {
    background: rgba(52,199,89,0.08);
    border: 1px solid rgba(52,199,89,0.3);
}
.result-icon { font-size: 2.4rem; flex-shrink: 0; }
.result-content h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    font-weight: 400;
    margin: 0 0 0.25rem;
}
.result-box.danger .result-content h3 { color: #e8443a; }
.result-box.safe .result-content h3 { color: #34c759; }
.result-content p {
    font-size: 0.88rem;
    color: #7a7f8e;
    margin: 0;
}
.prob-badge {
    margin-left: auto;
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
}
.result-box.danger .prob-badge { color: #e8443a; }
.result-box.safe .prob-badge { color: #34c759; }

/* ── Divider ── */
hr { border-color: #1e2230 !important; margin: 1.5rem 0 !important; }

/* ── Warning / Error toast ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Column gap ── */
[data-testid="column"] { gap: 0.4rem; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-icon">🫀</span>
    <h1>Cardio<span>Scan</span></h1>
    <p>Clinical heart disease risk assessment · Powered by machine learning</p>
</div>
""", unsafe_allow_html=True)

# ─── Form ─────────────────────────────────────────────────────────────────────
with st.form("prediction_form"):

    st.markdown('<div class="section-label">Patient Demographics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
        sex = st.selectbox("Biological Sex", options=[0, 1],
                           format_func=lambda x: "♀  Female" if x == 0 else "♂  Male")
    with col2:
        chest_pain_type = st.selectbox("Chest Pain Type",
            options=[0, 1, 2, 3],
            format_func=lambda x: ["Typical Angina", "Atypical Angina",
                                   "Non-anginal Pain", "Asymptomatic"][x])
        fasting_blood_sugar = st.selectbox("Fasting Blood Sugar > 120 mg/dL",
            options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

    st.markdown('<div class="section-label">Cardiovascular Metrics</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        resting_blood_pressure = st.number_input("Resting BP (mm Hg)", min_value=50, max_value=250, value=120)
        cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=600, value=200)
        max_heart_rate = st.number_input("Max Heart Rate (bpm)", min_value=50, max_value=250, value=150)
    with col4:
        resting_ecg = st.selectbox("Resting ECG Results",
            options=[0, 1, 2],
            format_func=lambda x: ["Normal", "ST-T Wave Abnormality", "LV Hypertrophy"][x])
        exercise_induced_angina = st.selectbox("Exercise-Induced Angina",
            options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        st_depression = st.number_input("ST Depression (induced by exercise)",
                                        min_value=0.0, max_value=10.0, value=0.0, step=0.1)

    st.markdown('<div class="section-label">Additional Diagnostics</div>', unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    with col5:
        st_slope = st.selectbox("ST Slope",
            options=[0, 1, 2],
            format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])
    with col6:
        num_major_vessels = st.selectbox("Major Vessels (fluoroscopy)",
            options=[0, 1, 2, 3, 4])
    with col7:
        thalassemia = st.selectbox("Thalassemia",
            options=[0, 1, 2, 3],
            format_func=lambda x: ["Normal", "Fixed Defect", "Reversible Defect", "Unknown"][x])

    submit_button = st.form_submit_button(label="Run Cardiac Risk Assessment →")

# ─── Result ───────────────────────────────────────────────────────────────────
if submit_button:
    payload = {
        "age": float(age), "sex": float(sex),
        "chest_pain_type": float(chest_pain_type),
        "resting_blood_pressure": float(resting_blood_pressure),
        "cholesterol": float(cholesterol),
        "fasting_blood_sugar": float(fasting_blood_sugar),
        "resting_ecg": float(resting_ecg),
        "max_heart_rate": float(max_heart_rate),
        "exercise_induced_angina": float(exercise_induced_angina),
        "st_depression": float(st_depression),
        "st_slope": float(st_slope),
        "num_major_vessels": float(num_major_vessels),
        "thalassemia": float(thalassemia)
    }

    with st.spinner("Analysing patient data…"):
        try:
            backend_url = "https://trainingproject-2-heart-disease.onrender.com/predict"
            response = requests.post(backend_url, json=payload, timeout=15)

            if response.status_code == 200:
                result = response.json()
                prob = result["heart_disease_probability"]
                pred = result["prediction"]

                if pred == 1:
                    st.markdown(f"""
                    <div class="result-box danger">
                        <span class="result-icon">⚠️</span>
                        <div class="result-content">
                            <h3>Heart Disease Detected</h3>
                            <p>Elevated risk indicators found. Consult a cardiologist.</p>
                        </div>
                        <span class="prob-badge">{prob:.0%}</span>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-box safe">
                        <span class="result-icon">✅</span>
                        <div class="result-content">
                            <h3>No Heart Disease Detected</h3>
                            <p>Low risk profile based on provided parameters.</p>
                        </div>
                        <span class="prob-badge">{prob:.0%}</span>
                    </div>""", unsafe_allow_html=True)

            else:
                st.warning(f"Backend unreachable — HTTP {response.status_code}. Ensure the Render service is live.")

        except Exception as e:
            st.error(f"Connection error: {e}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<p style="text-align:center; font-size:0.75rem; color:#3a3f50; margin:0; padding-bottom:1.5rem;">
    CardioScan · For educational & research use only · Not a substitute for professional medical advice
</p>
""", unsafe_allow_html=True)
