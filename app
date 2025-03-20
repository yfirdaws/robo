import streamlit as st
import pandas as pd
import pickle

# Load saved objects
with open("C:/Users/DELL/OneDrive/Documents/robo/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("C:/Users/DELL/OneDrive/Documents/robo/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("C:/Users/DELL/OneDrive/Documents/robo/label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

st.title("Robo-Advisor Risk Profiling")

# Input fields for a new user
age = st.number_input("Age", min_value=18, max_value=100, value=30)
income = st.number_input("Annual Income (₦)", min_value=0, value=1000000)
experience = st.number_input("Investment Experience (years)", min_value=0, value=2)
time_horizon = st.number_input("Time Horizon (years)", min_value=1, value=10)
risk_score = st.slider("Self-Reported Risk Score (1-10)", 1, 10, 5)
reaction = st.selectbox("Reaction to Losses", ["Panic", "Hold", "Buy More"])
goal = st.selectbox("Investment Goal", ["Preserve Capital", "Steady Growth", "Maximize Returns"])

# Create DataFrame for the new input
new_data = pd.DataFrame({
    "Age": [age],
    "Income": [income],
    "Investment Experience (years)": [experience],
    "Time Horizon (years)": [time_horizon],
    "Self-Reported Risk Score": [risk_score],
    "Reaction to Losses": [reaction],
    "Investment Goal": [goal]
})

# Convert categorical values using pre-fitted label encoders
for col in ['Reaction to Losses', 'Investment Goal']:
    new_data[col] = label_encoders[col].transform(new_data[col])

# Normalize numerical columns using the pre-fitted scaler
numerical_cols = ['Age', 'Income', 'Investment Experience (years)', 'Time Horizon (years)', 'Self-Reported Risk Score']
new_data[numerical_cols] = scaler.transform(new_data[numerical_cols])

# Make prediction
prediction = model.predict(new_data)[0]
risk_label = label_encoders['Risk Category'].inverse_transform([prediction])[0]

st.write(f"Predicted Risk Category: **{risk_label}**")
