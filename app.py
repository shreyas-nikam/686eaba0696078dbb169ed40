
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="QuLab", layout="wide")

# Check if logo exists
logo_path = Path("qu_logo.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path))
else:
    st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")

st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
### FX Forward Mark-to-Market (MTM) Analyzer

This application provides an interactive platform for simulating and analyzing the Mark-to-Market (MTM) value of Foreign Exchange (FX) forward contracts. It aims to enhance understanding of how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

#### Purpose and Objectives:
*   **Educate Users**: Help users understand how FX forward prices are determined based on interest rate differentials.
*   **Analyze MTM Factors**: Allow users to analyze the various factors affecting the MTM value of an FX forward contract over its life.
*   **Illustrate Concepts**: Visually explain concepts such as forward premium, forward discount, and gain/loss scenarios from different counterparty perspectives.

#### Target Audience and Use Cases:
**Target Audience**: Students, financial professionals, and anyone interested in derivatives, foreign exchange markets, and financial risk management.

**Use Cases**:
*   **Educational Tool**: For learners to interactively explore theoretical concepts of FX forward pricing and valuation.
*   **Scenario Analysis**: Practitioners can test hypothetical market movements and their impact on contract values.
*   **Risk Understanding**: Visualize how changes in underlying parameters contribute to MTM gains or losses, aiding in risk assessment.

#### Key Value Propositions:
*   **Interactive Learning**: Provides a hands-on experience that deepens understanding beyond static explanations.
*   **Clarity of Concepts**: Simplifies complex financial formulas and their implications through dynamic visualizations.
*   **Accessibility**: A user-friendly interface that requires no prior programming knowledge to operate, making sophisticated financial analysis accessible.

---
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["FX Forward MTM Analyzer"])
if page == "FX Forward MTM Analyzer":
    from application_pages.fx_forward_mtm_analyzer import run_fx_forward_mtm_analyzer
    run_fx_forward_mtm_analyzer()

# Your code ends
st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors")


# License
st.markdown('''
---
**License:** QuantUniversity License
''')
