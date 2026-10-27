"""Polished Streamlit client for the diabetes prediction FastAPI service."""

import os

import requests
import streamlit as st


st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        :root {
            --navy: #102a43;
            --blue: #176b87;
            --teal: #22a699;
            --mint: #e9f8f5;
            --slate: #526777;
            --border: #dce8ec;
        }

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 4%, rgba(34, 166, 153, 0.12), transparent 28rem),
                radial-gradient(circle at 92% 12%, rgba(23, 107, 135, 0.10), transparent 25rem),
                #f8fbfc;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 2.4rem 2.6rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.28);
            border-radius: 24px;
            background: linear-gradient(125deg, #102a43 0%, #176b87 62%, #22a699 100%);
            color: white;
            box-shadow: 0 20px 50px rgba(16, 42, 67, 0.16);
        }

        .hero::after {
            content: '';
            position: absolute;
            width: 250px;
            height: 250px;
            right: -65px;
            top: -80px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.09);
        }

        .hero-badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            margin-bottom: 0.8rem;
            border: 1px solid rgba(255, 255, 255, 0.32);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.12);
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .hero h1 {
            max-width: 700px;
            margin: 0 0 0.65rem;
            color: white;
            font-size: clamp(2rem, 5vw, 3.2rem);
            line-height: 1.08;
            letter-spacing: -0.04em;
        }

        .hero p {
            max-width: 680px;
            margin: 0;
            color: rgba(255, 255, 255, 0.82);
            font-size: 1.02rem;
            line-height: 1.65;
        }

        .section-heading {
            margin: 0 0 0.2rem;
            color: var(--navy);
            font-size: 1.35rem;
            font-weight: 700;
        }

        .section-copy {
            margin: 0 0 1rem;
            color: var(--slate);
            font-size: 0.93rem;
        }

        [data-testid="stForm"] {
            padding: 1.5rem 1.6rem 1.2rem;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 12px 35px rgba(16, 42, 67, 0.07);
        }

        [data-testid="stNumberInput"] label p {
            color: var(--navy);
            font-weight: 600;
        }

        [data-testid="stNumberInput"] input {
            border-radius: 10px;
        }

        .stButton > button, [data-testid="stFormSubmitButton"] > button {
            min-height: 3rem;
            border: 0;
            border-radius: 12px;
            background: linear-gradient(100deg, var(--blue), var(--teal));
            color: white;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(23, 107, 135, 0.18);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
            border: 0;
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 12px 24px rgba(23, 107, 135, 0.24);
        }

        .info-card {
            height: 100%;
            padding: 1.15rem 1.2rem;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.78);
        }

        .info-card strong {
            display: block;
            margin-bottom: 0.35rem;
            color: var(--navy);
        }

        .info-card span {
            color: var(--slate);
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .result-card {
            padding: 1.4rem 1.5rem;
            margin-top: 1.2rem;
            border-radius: 18px;
        }

        .result-card h3 {
            margin: 0 0 0.35rem;
        }

        .result-card p {
            margin: 0;
            line-height: 1.55;
        }

        .result-low {
            border: 1px solid #a9dfd3;
            background: #ecfaf6;
            color: #155e54;
        }

        .result-high {
            border: 1px solid #f2c2bd;
            background: #fff3f1;
            color: #943c33;
        }

        .disclaimer {
            padding: 1rem 1.2rem;
            margin-top: 1.5rem;
            border-left: 4px solid var(--teal);
            border-radius: 0 12px 12px 0;
            background: var(--mint);
            color: #31515c;
            font-size: 0.86rem;
            line-height: 1.55;
        }

        @media (max-width: 700px) {
            .block-container { padding: 1rem 0.8rem 2rem; }
            .hero { padding: 1.8rem 1.4rem; border-radius: 18px; }
            [data-testid="stForm"] { padding: 1.1rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="hero-badge">AI-assisted health screening</div>
        <h1>Understand diabetes risk in seconds.</h1>
        <p>
            Enter eight common health measurements to receive an educational
            prediction from a K-Nearest Neighbours model.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h2 class="section-heading">Patient health profile</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">Complete every field, then submit the form for an estimate.</p>',
    unsafe_allow_html=True,
)

with st.form("risk_assessment_form"):
    left, right = st.columns(2, gap="large")

    with left:
        pregnancies = st.number_input(
            "Pregnancies",
            min_value=0,
            max_value=17,
            value=2,
            step=1,
            help="Number of previous pregnancies.",
        )
        glucose = st.number_input(
            "Glucose (mg/dL)",
            min_value=0,
            max_value=200,
            value=120,
            step=1,
            help="Plasma glucose concentration from the dataset measurement.",
        )
        blood_pressure = st.number_input(
            "Diastolic blood pressure (mm Hg)",
            min_value=0,
            max_value=130,
            value=70,
            step=1,
            help="Diastolic blood pressure in millimetres of mercury.",
        )
        skin_thickness = st.number_input(
            "Skin thickness (mm)",
            min_value=0,
            max_value=100,
            value=20,
            step=1,
            help="Triceps skin-fold thickness in millimetres.",
        )

    with right:
        insulin = st.number_input(
            "2-hour serum insulin (μU/mL)",
            min_value=0,
            max_value=850,
            value=79,
            step=1,
            help="Two-hour serum insulin measurement.",
        )
        bmi = st.number_input(
            "Body mass index (BMI)",
            min_value=0.0,
            max_value=70.0,
            value=25.0,
            step=0.1,
            format="%.1f",
            help="Weight in kilograms divided by height in metres squared.",
        )
        diabetes_pedigree = st.number_input(
            "Diabetes pedigree function",
            min_value=0.0,
            max_value=2.5,
            value=0.5,
            step=0.001,
            format="%.3f",
            help="Dataset score representing family history of diabetes.",
        )
        age = st.number_input(
            "Age (years)",
            min_value=18,
            max_value=90,
            value=30,
            step=1,
            help="Patient age in completed years.",
        )

    submitted = st.form_submit_button(
        "Assess diabetes risk",
        type="primary",
        use_container_width=True,
    )

if submitted:
    payload = {
        "Pregnancies": int(pregnancies),
        "Glucose": float(glucose),
        "BloodPressure": float(blood_pressure),
        "SkinThickness": float(skin_thickness),
        "Insulin": float(insulin),
        "BMI": float(bmi),
        "DiabetesPedigreeFunction": float(diabetes_pedigree),
        "Age": int(age),
    }

    try:
        with st.spinner("Analyzing the health profile..."):
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            label = result["result_label"]
            confidence = float(result["confidence"])

        if label not in {"Diabetic", "Not Diabetic"}:
            raise ValueError("Unexpected prediction label")

        result_class = "result-high" if label == "Diabetic" else "result-low"
        result_title = (
            "Higher model-indicated risk"
            if label == "Diabetic"
            else "Lower model-indicated risk"
        )
        result_copy = (
            "The model classified this profile as diabetic. Please discuss any health concerns "
            "with a qualified healthcare professional."
            if label == "Diabetic"
            else "The model classified this profile as not diabetic. Continue routine screening "
            "and consult a healthcare professional for medical advice."
        )

        st.markdown(
            f"""
            <div class="result-card {result_class}">
                <h3>{result_title}</h3>
                <p>{result_copy}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(confidence, text=f"Model vote confidence: {confidence:.1%}")

    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        st.warning(
            "The prediction service is unavailable. Start FastAPI with "
            "`python -m uvicorn main:app --reload`, or verify the deployed `API_URL`."
        )

st.markdown("### How the assessment works")
info_one, info_two, info_three = st.columns(3, gap="medium")

with info_one:
    st.markdown(
        """
        <div class="info-card">
            <strong>1. Enter measurements</strong>
            <span>Provide the eight values expected by the trained model.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_two:
    st.markdown(
        """
        <div class="info-card">
            <strong>2. Secure API request</strong>
            <span>The interface sends the values to the FastAPI prediction endpoint.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_three:
    st.markdown(
        """
        <div class="info-card">
            <strong>3. Review the estimate</strong>
            <span>The result shows the predicted class and neighbour-vote confidence.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="disclaimer">
        <strong>Important:</strong> This application is an educational demonstration, not a
        medical diagnosis or validated clinical risk score. Its confidence value represents
        the KNN model's nearest-neighbour vote, not a calibrated probability of diabetes.
    </div>
    """,
    unsafe_allow_html=True,
)
