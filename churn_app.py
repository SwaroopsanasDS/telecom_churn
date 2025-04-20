import streamlit as st
import pandas as pd
from joblib import load
import requests
from streamlit_lottie import st_lottie

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="💡",
    layout="wide"
)

# ---- LOAD MODEL ----
model = load('random_forest_model.joblib')

# ---- LOTTIE HELPER FUNCTION ----
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# ---- LOTTIE ANIMATIONS ----
lottie_guns = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_j1adxtyb.json")
lottie_chatbot = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_4kx2q32n.json")
lottie_fireworks = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_V9t630.json")
lottie_customer_satisfaction = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_HJp9Uw.json")  # Fallback Lottie for testing

# ---- Fallback image if Lottie fails ----
fallback_image_url = "https://www.example.com/static_image.png"  # Example of fallback image URL

# ---- SNOWFALL ON ENTRY ----
st.snow()

# ---- HEADER SECTION ----
st.markdown(f"""
    <div style="
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in-out;
        color: #111111;
    ">
        <h1 style='color:#111111;'> Customer Churn Prediction App</h1>
        <p style='font-size: 18px; font-weight: 500; color: #111111; margin-top: 0.5rem;'>
            Use this smart tool to identify and retain your valuable customers!
        </p>
    </div>
""", unsafe_allow_html=True)

# ---- GUNFIRE STICKER (LEFT-HAND SIDE), CUSTOMER SATISFACTION (CENTER) AND CHATBOT STICKER (RIGHT-HAND SIDE) ----
col1, col2, col3 = st.columns([1, 8, 1])  # Corrected to have three columns (for left, middle, right)

with col1:
    if lottie_guns:
        st_lottie(lottie_guns, height=110, key="gunfire")
with col2:
    if lottie_customer_satisfaction:
        st_lottie(lottie_customer_satisfaction, height=110, key="customer_satisfaction")  # Placed in the center
    else:
        st.image(fallback_image_url, width=110)  # Fallback to static image if Lottie doesn't load
with col3:
    if lottie_chatbot:
        st_lottie(lottie_chatbot, height=110, key="chatbot")

# ---- MAIN FORM ----
st.markdown("<div class='container'>", unsafe_allow_html=True)

with st.form(key="form_churn"):
    st.markdown("### 📥 Enter Customer Information")

    col1, col2 = st.columns(2)
    with col1:
        tenure = st.number_input("📆 Tenure (months)", min_value=0, max_value=100, value=12)
        internet_service = st.selectbox("🌐 Internet Service", ['DSL', 'Fiber optic', 'No'])
    with col2:
        contract = st.selectbox("📄 Contract Type", ['Month-to-month', 'One year', 'Two year'])
        monthly_charges = st.number_input("💰 Monthly Charges", min_value=0, max_value=200, value=70)
        total_charges = st.number_input("🧮 Total Charges", min_value=0, max_value=10000, value=1500)

    submit_btn = st.form_submit_button("🔍 Predict")

# ---- ENCODING ----
label_mapping = {
    'DSL': 0,
    'Fiber optic': 1,
    'No': 2,
    'Month-to-month': 0,
    'One year': 1,
    'Two year': 2,
}

# ---- PREDICTION ----
if submit_btn:
    internet_service_val = label_mapping[internet_service]
    contract_val = label_mapping[contract]

    prediction = model.predict([[tenure, internet_service_val, contract_val, monthly_charges, total_charges]])

    st.markdown("---")
    st.subheader("🧠 Prediction Result")

    if prediction[0] == 0:
        st.success("✅ The customer is likely to **stay**. Great job keeping them happy!")
        st.snow()
        if lottie_fireworks:
            st_lottie(lottie_fireworks, height=200, key="fireworks")
    else:
        st.error("⚠️ The customer is likely to **churn**. Time to act!")
        st.markdown("💡 Tip: Engage this customer with offers or personalized support.")

st.markdown("</div>", unsafe_allow_html=True)
