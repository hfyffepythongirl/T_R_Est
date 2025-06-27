import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Terrorist Attack Risk Dashboard", layout="wide")

st.title("🛡️ Terrorist Attack Success Risk Estimator Dashboard")
st.markdown("""
This interactive dashboard estimates the probability that a terrorist attack will succeed **if attempted**, using a Bayesian model. Adjust the parameters to simulate different defense and threat scenarios.
""")

# Sidebar for user inputs
st.sidebar.header("📊 Simulation Parameters")
P_C = st.sidebar.slider("Countermeasures Active (P_C)", 0.0, 1.0, 0.95, 0.01)
P_D_given_C = st.sidebar.slider("Detection Rate if Countermeasures Active (P_D|C)", 0.0, 1.0, 0.9, 0.01)
P_O_low = st.sidebar.slider("Probability of Low Complexity Attack (P_O_low)", 0.0, 1.0, 0.7, 0.01)
P_S_given_D = st.sidebar.slider("Success if Detected (P_S|D)", 0.0, 1.0, 0.05, 0.01)
P_S_given_notD_Olow = st.sidebar.slider("Success if Undetected & Low Complexity (P_S|~D,O_low)", 0.0, 1.0, 0.7, 0.01)
P_S_given_notD_Ohigh = st.sidebar.slider("Success if Undetected & High Complexity (P_S|~D,O_high)", 0.0, 1.0, 0.4, 0.01)

# Derived values
P_O_high = 1 - P_O_low
P_D = P_C * P_D_given_C
P_notD = 1 - P_D

# Calculate final risk estimate
P_success = (
    P_D * P_S_given_D + 
    P_notD * (
        P_O_low * P_S_given_notD_Olow + 
        P_O_high * P_S_given_notD_Ohigh
    )
)

# Layout: Two columns
col1, col2 = st.columns(2)

with col1:
    st.metric(label="🧮 Estimated Probability of Success (If Attempted)", value=f"{P_success:.2%}")

    st.markdown("""
    ### 🔍 Assumptions Summary
    - **P(Countermeasures Active)**: {0:.2f}
    - **P(Detection | Countermeasures)**: {1:.2f}
    - **P(Low Complexity Attack)**: {2:.2f}
    - **P(Success | Detected)**: {3:.2f}
    - **P(Success | Undetected & Low Complexity)**: {4:.2f}
    - **P(Success | Undetected & High Complexity)**: {5:.2f}
    """.format(P_C, P_D_given_C, P_O_low, P_S_given_D, P_S_given_notD_Olow, P_S_given_notD_Ohigh))

with col2:
    # Create bar chart
    labels = ['Detected Path', 'Undetected + Low Complexity', 'Undetected + High Complexity']
    values = [
        P_D * P_S_given_D,
        P_notD * P_O_low * P_S_given_notD_Olow,
        P_notD * P_O_high * P_S_given_notD_Ohigh
    ]

    fig, ax = plt.subplots()
    ax.barh(labels, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax.set_xlim(0, max(0.01, max(values)) * 1.2)
    ax.set_xlabel('Contribution to Success Probability')
    ax.set_title('Risk Breakdown by Path')
    st.pyplot(fig)
  
