
import streamlit as st
import math

st.set_page_config(page_title="FX Forward MTM Analyzer", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: FX Forward MTM Analyzer")
st.divider()
st.markdown("""
Welcome to the **FX Forward Mark-to-Market (MTM) Analyzer**!

This interactive application provides a platform for simulating and analyzing the Mark-to-Market (MTM) value of Foreign Exchange (FX) forward contracts. It aims to deepen your understanding of how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

### What is an FX Forward Contract?
An FX forward contract is a customized agreement between two parties to exchange a specified amount of one currency for another at a pre-agreed exchange rate (the forward rate) on a specified future date. Unlike spot transactions, the exchange does not happen immediately but at maturity.

### Purpose and Objectives
*   **Educate Users**: Understand how FX forward prices are determined based on interest rate differentials.
*   **Analyze MTM Factors**: Analyze various factors affecting the MTM value of an FX forward contract over its life.
*   **Illustrate Concepts**: Visually explain concepts such as forward premium, forward discount, and gain/loss scenarios from different counterparty perspectives.

### Key Value Propositions
*   **Interactive Learning**: Provides a hands-on experience that deepens understanding beyond static explanations.
*   **Clarity of Concepts**: Simplifies complex financial formulas and their implications through dynamic visualizations.
*   **Accessibility**: A user-friendly interface that requires no prior programming knowledge to operate.

### Core Formulas
The application uses the following fundamental formulas:

1.  **FX Forward Price (continuous compounding)**:
    The forward price $F_{0,f/d}(T)$ at time 0 for a contract maturing at time $T$ is calculated as:
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
    Where:
    *   $S_{0,f/d}$ is the spot exchange rate at time 0 (foreign currency per domestic currency).
    *   $r_f$ is the foreign risk-free interest rate.
    *   $r_d$ is the domestic risk-free interest rate.
    *   $T$ is the original time to maturity of the forward contract in years.
    *   $e$ is the base of the natural logarithm.

2.  **Mark-to-Market (MTM) Value of an FX Forward Contract (Long Position)**:
    Let $F_{t,f/d}(T)$ be the current forward rate for the remaining maturity $(T-t)$:
    $$F_{t,f/d}(T) = S_{t,f/d}e^{(r_{f,current} - r_{d,current})(T - t)}$$
    Then, the MTM value for a long position at time $t$ is:
    $$V_t^{long}(T) = (F_{t,f/d}(T) - F_{0,f/d}(T)) \cdot e^{-r_{d,current}(T-t)}$$
    And for a short position:
    $$V_t^{short}(T) = -(F_{t,f/d}(T) - F_{0,f/d}(T)) \cdot e^{-r_{d,current}(T-t)}$$
    Where:
    *   $F_{0,f/d}(T)$ is the initial forward price calculated at $t=0$.
    *   $S_{t,f/d}$ is the current spot exchange rate at time $t$.
    *   $r_{f,current}$ is the current foreign risk-free interest rate at time $t$.
    *   $r_{d,current}$ is the current domestic risk-free interest rate at time $t$.
    *   $T$ is the original time to maturity in years.
    *   $t$ is the current time in years from inception ($0 \le t \le T$).
    *   $e$ is the base of the natural logarithm.

    This application uses these formulas to dynamically calculate and visualize the MTM based on user-defined parameters.

### How to use this application:
1.  **Adjust Initial Contract Parameters**: Define the characteristics of the FX forward contract at its inception.
2.  **Adjust Current Market Parameters**: Input the current market conditions to see how the MTM value changes.
3.  **Select Currency Pair**: Use the dropdown to pre-fill realistic rates for common currency pairs, or input them manually.
4.  **Observe Results**: The calculated FX Forward Price and MTM values will update in real-time, along with interactive plots illustrating the impact of interest rate differentials and spot rate changes.

""")

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["FX Forward MTM Analyzer"])
if page == "FX Forward MTM Analyzer":
    from application_pages.page1 import run_page1
    run_page1()
# Your code ends

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors")
