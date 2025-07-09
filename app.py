
import streamlit as st
import numpy as np

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
### Derivative Pricing and Valuation of Forward Contracts

In this lab, we explore the pricing and valuation of Foreign Exchange (FX) forward contracts. An FX forward contract is a customized agreement between two parties to exchange a specified amount of one currency for another at a predetermined exchange rate on a specific future date. Unlike spot transactions, which involve immediate delivery, forward contracts lock in an exchange rate for a future transaction, thereby mitigating foreign exchange risk.

#### **Purpose and Objectives**
The FX Forward Mark-to-Market (MTM) Analyzer Streamlit application aims to provide an interactive platform for simulating and analyzing the MTM value of Foreign Exchange (FX) forward contracts. Its primary objective is to enhance understanding of how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

Key objectives include:
*   **Educate Users**: Help users understand how FX forward prices are determined based on interest rate differentials.
*   **Analyze MTM Factors**: Allow users to analyze the various factors affecting the MTM value of an FX forward contract over its life.
*   **Illustrate Concepts**: Visually explain concepts such as forward premium, forward discount, and gain/loss scenarios from different counterparty perspectives.

#### **Key Value Propositions**
*   **Interactive Learning**: Provides a hands-on experience that deepens understanding beyond static explanations.
*   **Clarity of Concepts**: Simplifies complex financial formulas and their implications through dynamic visualizations.
*   **Accessibility**: A user-friendly interface that requires no prior programming knowledge to operate, making sophisticated financial analysis accessible.

#### **Core Formulas**

The following formulas are central to the calculations in this application:

*   **FX Forward Price (continuous compounding)**:
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
*   **Mark-to-Market value of an FX forward contract (long position)**:
    $$V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$$
    Where:
    *   $F_{0,f/d}(T)$ is the forward price at time 0 for a contract maturing at time $T$.
    *   $S_{0,f/d}$ is the spot exchange rate at time 0 (foreign currency per domestic currency).
    *   $S_{t,f/d}$ is the current spot exchange rate at time $t$.
    *   $r_f$ is the foreign risk-free interest rate.
    *   $r_d$ is the domestic risk-free interest rate.
    *   $T$ is the original time to maturity of the forward contract in years.
    *   $t$ is the current time in years from the contract inception ($0 \le t \le T$).
    *   $e$ is the base of the natural logarithm, approximated by `np.exp()`.

""")

# Your code starts here
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(label="Select a page", options=["FX Forward MTM Analyzer"])

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
