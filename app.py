import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="CVEO Threat and Residual Risk Dashboard", layout="wide")

st.title("🛡️ CVEO Threat Risk Estimator Dashboard")
st.markdown("""
This dashboard estimates three risk levels related to CVEO (Criminal Violent Extremist Organization) threats:
1. **Raw Threat** – likelihood of success with no countermeasures
2. **Residual Threat** – risk with current mitigation
3. **Future Residual Threat** – projected risk with improved policies
""")

st.sidebar.header("📊 Model Inputs")
st.sidebar.subheader("Threat Intent & Capability")
P_A_given_T = st.sidebar.slider("P(Attack | Threat Intent)", 0.0, 1.0, 0.2, 0.01)

st.sidebar.subheader("Raw Threat Conditions (No Countermeasures)")
P_S_given_A_no_C = st.sidebar.slider("P(Success | Attempt, No Countermeasures)", 0.0, 1.0, 0.7, 0.01)

st.sidebar.subheader("Current Countermeasures")
P_C = st.sidebar.slider("P(Countermeasures Active)", 0.0, 1.0, 0.9, 0.01)
P_D_given_C = st.sidebar.slider("P(Detection | Countermeasures)", 0.0, 1.0, 0.85, 0.01)
P_S_given_D = st.sidebar.slider("P(Success | Detected)", 0.0, 1.0, 0.05, 0.01)
P_S_given_notD = st.sidebar.slider("P(Success | Not Detected)", 0.0, 1.0, 0.5, 0.01)

st.sidebar.subheader("Future Countermeasures")
P_D_future = st.sidebar.slider("Future P(Detection | Countermeasures)", 0.0, 1.0, 0.95, 0.01)
P_S_D_future = st.sidebar.slider("Future P(Success | Detected)", 0.0, 1.0, 0.03, 0.01)
P_S_notD_future = st.sidebar.slider("Future P(Success | Not Detected)", 0.0, 1.0, 0.4, 0.01)
P_A_future = st.sidebar.slider("Future P(Attack | Threat Intent)", 0.0, 1.0, 0.18, 0.01)

# Calculations
# Raw Threat
P_raw = P_A_given_T * P_S_given_A_no_C

# Current Residual Threat
P_D = P_C * P_D_given_C
P_notD = 1 - P_D
P_S_current = P_D * P_S_given_D + P_notD * P_S_given_notD
P_residual = P_A_given_T * P_S_current

# Future Residual Threat
P_notD_future = 1 - P_D_future
P_S_future = P_D_future * P_S_D_future + P_notD_future * P_S_notD_future
P_residual_future = P_A_future * P_S_future

# Risk Tier Mapping
def risk_tier(prob):
    if prob < 0.01:
        return "🟢 Low"
    elif prob < 0.05:
        return "🟡 Moderate"
    elif prob < 0.15:
        return "🟠 Significant"
    else:
        return "🔴 High"

col1, col2, col3 = st.columns(3)
col1.metric("Raw Threat", f"{P_raw:.2%}", help="Risk without any countermeasures")
col1.write(f"Risk Tier: {risk_tier(P_raw)}")

col2.metric("Current Residual Threat", f"{P_residual:.2%}", help="Risk with existing countermeasures")
col2.write(f"Risk Tier: {risk_tier(P_residual)}")

col3.metric("Future Residual Threat", f"{P_residual_future:.2%}", help="Projected risk after improvements")
col3.write(f"Risk Tier: {risk_tier(P_residual_future)}")

st.markdown("---")

# Plotting
labels = ["Raw", "Current Residual", "Future Residual"]
values = [P_raw, P_residual, P_residual_future]
colors = ['#d62728', '#ff7f0e', '#2ca02c']

fig, ax = plt.subplots()
ax.bar(labels, values, color=colors)
ax.set_ylim(0, max(0.01, max(values)) * 1.2)
ax.set_ylabel('Success Probability')
ax.set_title('CVEO Risk Profile')

for i, v in enumerate(values):
    ax.text(i, v + 0.005, f"{v:.2%}", ha='center')

st.pyplot(fig)

st.markdown("""
### 🧠 How This Works:
- **Raw Threat** is baseline likelihood with no mitigation.
- **Residual Threat** uses probabilistic calculus to simulate intervention effects.
- **Future Residual Threat** models enhanced detection and deterrence.
- **Risk Tiering** aligns with homeland security standards (Low, Moderate, Significant, High).
""")
