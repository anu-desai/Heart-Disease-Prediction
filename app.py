
import pandas as pd
import streamlit as st
import joblib

# Page setup
st.set_page_config(page_icon='❤️', page_title='Heart Disease Detector', layout='wide')

# Modern CSS for industry-standard look
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            background-color: #f4f6fb;
        }
        .stApp {
            background: linear-gradient(120deg, #f4f6fb 60%, #e0e7ff 100%);
        }
        .stButton>button {
            background: linear-gradient(90deg, #e84118 0%, #fbc531 100%);
            color: #fff;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            padding: 0.6em 2.5em;
            box-shadow: 0 2px 8px rgba(232,65,24,0.08);
            border: none;
            transition: background 0.2s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #c23616 0%, #e1b12c 100%);
            color: #fff;
        }
        .stSidebar {
            background-color: #fff;
        }
        .risk-low {
            color: #44bd32;
            font-weight: bold;
            font-size: 1.5em;
        }
        .risk-high {
            color: #e84118;
            font-weight: bold;
            font-size: 1.5em;
        }
        .hero {
            background: linear-gradient(90deg, #e84118 0%, #fbc531 100%);
            border-radius: 18px;
            padding: 2.5em 2em 2em 2em;
            margin-bottom: 2em;
            box-shadow: 0 4px 24px rgba(232,65,24,0.10);
            color: #fff;
            text-align: center;
        }
        .card {
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(44,62,80,0.07);
            padding: 2em 2em 1.5em 2em;
            margin-bottom: 2em;
        }
        .stNumberInput>div>input {
            border-radius: 6px;
            border: 1px solid #e1e1e1;
        }
        .stSelectbox>div>div {
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4490/4490641.png", width=120)
    st.title("Heart Disease Prediction")
    st.markdown("<span style='color:#e84118;font-weight:bold;'>Powered by Machine Learning</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style='font-size:1.1em;'>
        <b>Instructions:</b><br>
        Enter patient details on the right and click <b>Predict Risk</b>.<br>
        The model will estimate the risk of heart disease.
        </div>
    """, unsafe_allow_html=True)


# Load dataset and model
df = pd.read_csv('cleaned_data.csv')
model = joblib.load('log_model.joblib')

# Hero section
st.markdown("""
    <div class='hero'>
        <img src='https://cdn-icons-png.flaticon.com/512/4490/4490641.png' width='90' style='margin-bottom:1em;'>
        <h1 style='margin-bottom:0.2em;'>Heart Disease Detector</h1>
        <div style='font-size:1.2em;'>Industry-grade ML-powered risk prediction for heart disease.<br>Enter patient details below to get started.</div>
    </div>
""", unsafe_allow_html=True)

# User input card
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Enter Patient Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input('Age', min_value=1, max_value=100, step=1, help="Enter age in years")
        gender = st.radio('Gender', options=['Male', 'Female'], horizontal=True)
        gender = 1 if gender == 'Male' else 0

        chest_pain_type = st.selectbox(
            'Chest Pain Type',
            options=['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptotic'],
            help="Type of chest pain experienced"
        )
        chest_pain_type = {'Typical angina': 0, 'Atypical angina': 1, 'Non-anginal pain': 2, 'Asymptotic': 3}[chest_pain_type]

        resting_bp = st.number_input('Resting Blood Pressure (mm Hg)', min_value=50, max_value=250, step=1)
        cholestrol = st.number_input('Cholesterol (mg/dl)', min_value=50, max_value=600, step=1)
        fasting_blood_sugar = st.radio('Fasting Blood Sugar > 120 mg/dl?', options=['Yes', 'No'], horizontal=True)
        fasting_blood_sugar = 1 if fasting_blood_sugar == 'Yes' else 0

    with col2:
        resting_ecg = st.selectbox(
            'Resting ECG Results',
            options=['normal', 'having ST wave abnormality', 'left ventricular hypertrophy'],
            help="Resting electrocardiographic results"
        )
        resting_ecg = {'normal': 0, 'having ST wave abnormality': 1, 'left ventricular hypertrophy': 2}[resting_ecg]

        max_heart = st.number_input('Maximum Heart Rate Achieved', min_value=50, max_value=250, step=1)
        exang = st.radio('Exercise Induced Angina?', options=['Yes', 'No'], horizontal=True)
        exang = 1 if exang == 'Yes' else 0

        oldpeak = st.number_input('ST Depression Induced by Exercise', min_value=0.0, max_value=10.0, step=0.1)
        slope = st.selectbox(
            'Slope of Peak Exercise ST Segment',
            options=['upslopping', 'flat', 'downslopping'],
            help="Slope of the peak exercise ST segment"
        )
        slope = {'upslopping': 0, 'flat': 1, 'downslopping': 2}[slope]

        ca = st.selectbox('Number of Major Vessels (0-4) Colored by Fluoroscopy', options=[0, 1, 2, 3, 4])
        defect = st.selectbox(
            'Thalassemia (defect)',
            options=['normal', 'fixed defect', 'reversible defect'],
            help="Type of thalassemia"
        )
        defect = {'normal': 1, 'fixed defect': 2, 'reversible defect': 3}[defect]

    st.markdown("---")
    if st.button('Predict Risk', use_container_width=True):
        data = [[age, gender, chest_pain_type, resting_bp, cholestrol, fasting_blood_sugar,
                 resting_ecg, max_heart, exang, oldpeak, slope, ca, defect]]
        prediction = model.predict(data)[0]

        if prediction == 0:
            st.markdown('<div class="risk-low"><span style="font-size:2em;">✔️</span> LOW RISK OF HEART DISEASE</div>', unsafe_allow_html=True)
            st.image('https://t4.ftcdn.net/jpg/10/31/02/31/360_F_1031023150_2anqMJmLC6fTSUMfOv9914z8hNNcS3A4.jpg', width=150)
            st.success("The patient is at low risk. Encourage healthy lifestyle!")
        else:
            st.markdown('<div class="risk-high"><span style="font-size:2em;">⚠️</span> HIGH RISK OF HEART DISEASE</div>', unsafe_allow_html=True)
            st.image('https://static.vecteezy.com/system/resources/previews/047/743/949/non_2x/heart-risk-icon-vector.jpg', width=150)
            st.error("The patient is at high risk. Recommend further medical evaluation.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <center>
        <small>© 2026 Heart Disease Detector | Built with ❤️ using Streamlit</small>
    </center>
""", unsafe_allow_html=True)