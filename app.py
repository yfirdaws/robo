import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from portfolio_optimizer import get_stock_data, mean_variance_optimization  # Import portfolio functions

# ✅ **Load Model & Preprocessors**
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# ✅ **Initialize Session State**
if "risk_tolerance" not in st.session_state:
    st.session_state["risk_tolerance"] = None

# ✅ **Navigation Sidebar**
st.title("Investor Profiling & Portfolio Optimization by Firdaws Yahaya")
#st.sidebar.title("Navigation")
#page = st.sidebar.radio("Go to", ["Home (Risk Form)", "Portfolio Recommendation"])

# ✅ **Page 1: Risk Profiling (Home)**
# ---------------------------------------------------------
#if page == "Home (Risk Form)":
    #st.subheader("📋 Investor Risk Profile Form")

    # **Input Fields**
age = st.number_input("Age", min_value=18, max_value=100, value=30)
income = st.number_input("Annual Income (₦)", min_value=0, value=1000000)
experience = st.number_input("Investment Experience (years)", min_value=0, value=2)
time_horizon = st.number_input("Time Horizon (years)", min_value=1, value=10)
risk_score = st.slider("Self-Reported Risk Score (1-10)", 1, 10, 5)
reaction = st.selectbox("Reaction to Losses", ["Panic", "Hold", "Buy More"])
goal = st.selectbox("Investment Goal", ["Preserve Capital", "Steady Growth", "Maximize Returns"])

    # **Prepare Input Data**
new_data = pd.DataFrame({
    "Age": [age],
    "Income": [income],
    "Investment Experience (years)": [experience],
    "Time Horizon (years)": [time_horizon],
    "Self-Reported Risk Score": [risk_score],
    "Reaction to Losses": [reaction],
    "Investment Goal": [goal]
})

# **Encode Categorical Features**
for col in ['Reaction to Losses', 'Investment Goal']:
    if col in label_encoders:
        new_data[col] = label_encoders[col].transform(new_data[col])
    else:
        st.error(f"❌ Error: '{col}' is missing from label_encoders.")

# **Normalize Numerical Data**
numerical_cols = ['Age', 'Income', 'Investment Experience (years)', 'Time Horizon (years)', 'Self-Reported Risk Score']
new_data[numerical_cols] = scaler.transform(new_data[numerical_cols])

# ✅ **Make Prediction**
if st.button("Submit"):
    prediction = model.predict(new_data)[0]

    if "Risk Category" in label_encoders:
        risk_label = label_encoders["Risk Category"].inverse_transform([prediction])[0]
    else:
        st.error("❌ Error: 'Risk Category' is missing from label_encoders.")
        risk_label = "Unknown"

    st.session_state["risk_tolerance"] = risk_label  # Store risk tolerance
    st.success(f"Predicted Risk Category: **{risk_label}**")
    st.write("Go to **Portfolio Recommendation** to see your suggested allocation.")

# ---------------------------------------------------------
# ✅ **Page 2: Portfolio Recommendation**
# ---------------------------------------------------------
#elif page == "Portfolio Recommendation":
    #st.switch_page("pages/portfolio_recommendation")  # Automatically switches to the second page