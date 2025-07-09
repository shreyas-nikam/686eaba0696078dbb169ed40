
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="QuLab: Forward Contracts Valuation", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Forward Contracts with Costs & Benefits Simulator")
st.divider()
st.markdown(r\"\"\"
In this lab, we explore the intricate world of **Forward Contracts**, focusing specifically on how **discrete costs (like storage) and benefits (like dividends)** impact their pricing and valuation. A forward contract is a customized contract between two parties to buy or sell an asset at a specified price on a future date. Unlike futures, forward contracts are over-the-counter (OTC) instruments, meaning they are not traded on exchanges and are subject to counterparty risk.

### Core Concepts:

1.  **No-Arbitrage Principle:** The fundamental concept guiding the pricing of derivatives. It states that in an efficient market, it's impossible to make risk-free profit by simultaneously buying and selling different assets. This principle dictates that the forward price must reflect the cost of holding the underlying asset until maturity, including any costs incurred or benefits received.

2.  **Forward Price at Inception ($F_0(T)$):** This is the price agreed upon today for a transaction that will occur at a future date $T$. When the underlying asset generates benefits (e.g., dividends, convenience yield) or incurs costs (e.g., storage, insurance) during the contract's life, these cash flows must be accounted for.
    The formula for the forward price at inception, considering discrete costs and benefits, is:
    $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1 + r)^T$$
    Where:
    *   $S_0$: Initial spot price of the underlying asset at time $t=0$.
    *   $PV_0(I)$: Present Value of all discrete benefits (Income/Dividends) received from time $t=0$ to maturity $T$.
        $$PV_0(I) = \sum_{j} I_j (1 + r)^{-t_j^I}$$
        Here, $I_j$ is the amount of the $j$-th benefit, and $t_j^I$ is the time (in years from $t=0$) when the $j$-th benefit is received.
    *   $PV_0(C)$: Present Value of all discrete costs incurred from time $t=0$ to maturity $T$.
        $$PV_0(C) = \sum_{k} C_k (1 + r)^{-t_k^C}$$
        Here, $C_k$ is the amount of the $k$-th cost, and $t_k^C$ is the time (in years from $t=0$) when the $k$-th cost is incurred.
    *   $r$: Annualized risk-free interest rate.
    *   $T$: Total time to maturity of the forward contract in years from $t=0$.

3.  **Mark-to-Market (MTM) Value ($V_t(T)$):** This is the value of the forward contract at any point in time $t$ before maturity. It represents the profit or loss that would be realized if the contract were to be closed out (marked to market) at the current time $t$. The MTM value changes as the spot price of the underlying asset, interest rates, and time to maturity change.

    For a **long position** (agreement to buy), the MTM value at time $t$ is:
    $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$
    Where:
    *   $S_t$: Spot price of the underlying asset at the current time $t$.
    *   $PV_t(I)$: Present Value of *remaining* discrete benefits from time $t$ to maturity $T$.
    *   $PV_t(C)$: Present Value of *remaining* discrete costs from time $t$ to maturity $T$.
    *   $F_0(T)$: The original forward price agreed upon at $t=0$.
    *   $(1 + r)^{-(T-t)}$: Discount factor for the remaining life of the contract $(T-t)$.

    The present value of *remaining* cash flows from time $t$ to maturity $T$ is calculated as:
    $$PV_t(CF) = \sum_{j | t_j^{CF} \ge t} CF_j (1 + r)^{-(t_j^{CF} - t)}$$
    Here, $CF_j$ is the amount of the $j$-th cash flow (either $I_j$ or $C_k$), and $t_j^{CF}$ is its original time from $t=0$. Only cash flows occurring at or after the current time $t$ are considered.

    For a **short position** (agreement to sell), the MTM value is simply the negative of the long position's MTM value:
    $$V_t(T)_{short} = -V_t(T)_{long}$$

This application allows you to interactively adjust all these parameters and visualize their impact on the forward price and MTM value in real-time.
\"\"\")

st.divider()

# Placeholder for navigation, though we have only one page
page = st.sidebar.selectbox(label="Navigation", options=["Forward Contracts Simulator"])

if page == "Forward Contracts Simulator":
    from application_pages.forward_contracts_simulator import run_page
    run_page()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
