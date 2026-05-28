import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Subconscious Stability Predictor", layout="centered")
st.title("🧠 Subconscious Stability Predictor")
st.markdown("Adjust the sliders below to predict your subconscious stability category.")

# --- Input sliders ---
st.subheader("Input Variables")

col1, col2 = st.columns(2)

with col1:
    micro_expr = st.slider("Micro Expression Rate", 0.0, 30.0, 14.0)
    eye_move = st.slider("Eye Movement Variability", 5.0, 60.0, 30.0)
    hrv = st.slider("Heart Rate Variability", 10.0, 100.0, 60.0)
    breathing = st.slider("Breathing Rate", 5.0, 30.0, 16.0)
    reaction = st.slider("Reaction Time (ms)", 100.0, 900.0, 350.0)

with col2:
    error_rate = st.slider("Error Rate Per Task", 0.0, 15.0, 4.0)
    sleep = st.slider("Sleep Hours Last Night", 3.0, 12.0, 7.5)
    caffeine = st.slider("Caffeine Intake (mg)", 0.0, 400.0, 100.0)
    experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
    time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])

# --- Simple rule-based score calculation ---
# Each factor nudges the score up or down, normalized to 0-100

score = 50.0  # baseline

# HRV: higher = better
score += (hrv - 55) * 0.25

# Sleep: ideal ~7.5h
sleep_bonus = -(abs(sleep - 7.5)) * 3
score += sleep_bonus

# Reaction time: lower = better
score += (500 - reaction) * 0.04

# Error rate: lower = better
score -= error_rate * 1.5

# Breathing rate: ideal ~16
score -= abs(breathing - 16) * 0.5

# Micro expression: moderate is stable
score -= abs(micro_expr - 13) * 0.3

# Eye movement: lower variability = more stable
score -= (eye_move - 25) * 0.2

# Caffeine: moderate is ok, excess hurts
score -= max(0, caffeine - 200) * 0.05

# Experience boost
exp_map = {"Beginner": 0, "Intermediate": 3, "Expert": 6}
score += exp_map[experience]

# Time of day: morning slight boost
tod_map = {"Morning": 2, "Afternoon": 0, "Evening": -1}
score += tod_map[time_of_day]

# Clamp to 0-100
score = float(np.clip(score, 0, 100))

# --- Category thresholds ---
if score <= 30:
    category = "🔴 Low Stability"
    color = "#ff4d4d"
    description = "Your subconscious signals indicate high stress or instability. Consider rest and recovery."
elif score <= 70:
    category = "🟡 Normal Stability"
    color = "#f0c040"
    description = "Your subconscious state is balanced. Maintain healthy habits to stay in this range."
else:
    category = "🟢 High Stability"
    color = "#4caf50"
    description = "Excellent subconscious stability. You're operating at peak cognitive and emotional balance."

# --- Display result ---
st.divider()
st.subheader("Prediction Result")

st.markdown(
    f"""
    <div style="background-color:{color}22; border-left: 6px solid {color};
    padding: 20px; border-radius: 8px;">
        <h2 style="color:{color}; margin:0">{category}</h2>
        <h3 style="margin: 8px 0">Score: {score:.1f} / 100</h3>
        <p style="margin:0">{description}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Score bar ---
st.markdown("#### Stability Score")
st.progress(int(score))

# --- Category guide ---
with st.expander("📊 Category Reference"):
    st.markdown("""
    | Category | Score Range |
    |---|---|
    | 🔴 Low Stability | 0 – 30 |
    | 🟡 Normal Stability | 31 – 70 |
    | 🟢 High Stability | 71 – 100 |
    """)
    st.caption("Tip: Improve sleep quality, reduce error rate, and maintain moderate HRV for higher stability.")
