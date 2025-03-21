import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 AI-Driven Portfolio Recommendation")
st.write("✅ The page is running!")

# ✅ Check if risk tolerance is set, otherwise show a warning
if "risk_tolerance" not in st.session_state:
    st.warning("⚠️ Please go to the **Risk Profiling** page and select your risk category.")
    st.stop()  # Stop execution if risk profile is missing

# Get risk tolerance from session state
risk_label = st.session_state["risk_tolerance"]
st.write(f"### Your Risk Category: **{risk_label}**")

# Map risk category to suggested assets
risk_mapping = {
    "Conservative": ["BND", "TLT", "GLD"],
    "Moderate": ["SPY", "QQQ", "VNQ"],
    "Aggressive": ["TSLA", "NVDA", "BTC-USD"]
}

suggested_assets = risk_mapping.get(risk_label, ["SPY"])
st.write(f"### Suggested Investment Classes: {', '.join(suggested_assets)}")

# Example: Generate random asset allocation
np.random.seed(42)
weights = np.random.rand(len(suggested_assets))
weights /= weights.sum()  # Normalize to sum to 1

# Display allocations
st.write("### Portfolio Allocation")
for asset, weight in zip(suggested_assets, weights):
    st.write(f"✅ {asset}: **{weight*100:.2f}%**")

# Show Pie Chart
fig, ax = plt.subplots()
ax.pie(weights, labels=suggested_assets, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

st.success("📢 Portfolio generated dynamically based on your risk profile.")
