
import streamlit as st
import os

st.set_page_config(page_title="QuLab: Derivative Pricing and Valuation of Forward Contracts", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Derivative Pricing and Valuation of Forward Contracts")
st.divider()
st.markdown("""
### FX Forward Mark-to-Market (MTM) Analyzer

Welcome to the FX Forward Mark-to-Market (MTM) Analyzer! This interactive application is designed to help you understand and visualize the valuation dynamics of Foreign Exchange (FX) forward contracts. By adjusting various market parameters, you can explore how changes in spot rates and interest rate differentials impact the Mark-to-Market value of these derivatives.

#### What is an FX Forward Contract?
An FX forward contract is a customized agreement between two parties to exchange a specified amount of one currency for another currency on a future date at a pre-determined exchange rate. Unlike spot transactions, the exchange rate for a forward contract is fixed at the time the contract is initiated, regardless of future spot rate movements.

#### Mark-to-Market (MTM) Valuation
Mark-to-Market (MTM) is the process of valuing a financial instrument at its current market price. For an FX forward contract, the MTM value at any given time $t$ reflects the theoretical profit or loss if the contract were to be closed out (offset) at that moment. A positive MTM value for a long position indicates a gain, while a negative value indicates a loss. For a short position, the interpretation is reversed.

#### Key Concepts Explored in this Lab:
*   **Initial Forward Price**: How the forward price is determined at inception ($t=0$) based on the initial spot rate and the interest rate differential between the two currencies. This reflects the no-arbitrage principle.
*   **Interest Rate Parity**: The underlying economic principle that links spot and forward exchange rates with interest rates in different countries.
*   **Impact of Market Changes**: How the MTM value of an existing forward contract changes over time ($t > 0$) due to fluctuations in the current spot rate and current risk-free interest rates.
*   **Time Decay**: The influence of the remaining time to maturity on the MTM value.

#### Business Logic:
The application calculates two main values:
1.  **FX Forward Price (at inception)**: This is the price at which the FX forward contract was agreed upon at time $t=0$.
    The formula used for continuous compounding is:
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
    Where:
    *   $F_{0,f/d}(T)$ is the forward price at time 0 for a contract maturing at time $T$.
    *   $S_{0,f/d}$ is the initial spot exchange rate (foreign currency per domestic currency).
    *   $r_f$ is the foreign risk-free interest rate at inception.
    *   $r_d$ is the domestic risk-free interest rate at inception.
    *   $T$ is the original time to maturity of the forward contract in years.
    *   $e$ is the base of the natural logarithm.

2.  **Mark-to-Market Value (at current time $t$)**: This represents the current value of the contract. For a **long position** (agreement to buy foreign currency at maturity), the MTM value is calculated as:
    $$V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$$
    For a **short position** (agreement to sell foreign currency at maturity), the MTM value is:
    $$V_t^{short}(T) = -V_t^{long}(T)$$
    Where:
    *   $V_t(T)$ is the Mark-to-Market value at time $t$.
    *   $S_{t,f/d}$ is the current prevailing spot exchange rate at time $t$.
    *   $F_{0,f/d}(T)$ is the initial forward price calculated at $t=0$.
    *   $r_f$ is the current foreign risk-free interest rate.
    *   $r_d$ is the current domestic risk-free interest rate.
    *   $T$ is the original time to maturity.
    *   $t$ is the current time in years from the contract inception ($0 \le t \le T$).

By interacting with the sliders and inputs, you can observe how these parameters dynamically influence the forward price and the MTM value, providing insights into potential gains or losses for your forward positions.
""")

# Your code starts here
# Create the application_pages directory if it doesn't exist
if not os.path.exists("application_pages"):
    os.makedirs("application_pages")

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
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
