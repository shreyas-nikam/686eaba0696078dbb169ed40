
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import exp

def calculate_fx_forward_price(S0_f_d, rf_initial, rd_initial, T):
    """Calculates the FX Forward Price at inception (t=0)."""
    return S0_f_d * exp((rf_initial - rd_initial) * T)

def calculate_mtm(St_f_d, F0_f_d, rf_current, rd_current, T, t):
    """
    Calculates the Mark-to-Market (MTM) value for a long FX forward position.
    Uses the specified formula: V_t(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}
    """
    remaining_maturity = T - t
    if remaining_maturity < 0:
        return 0.0 # Contract expired
    # For the e^(-(rf-rd)(T-t)) term, use current rates as they are relevant for the remaining term
    return St_f_d - F0_f_d * exp(-(rf_current - rd_current) * remaining_maturity)

def run_main_page():
    st.header("FX Forward Mark-to-Market (MTM) Analyzer")

    st.markdown("""
    This tool allows you to analyze the Mark-to-Market (MTM) value of a Foreign Exchange (FX) forward contract.
    By adjusting parameters related to the contract's inception and current market conditions,
    you can observe how the forward price and MTM value change in real-time.
    """)

    st.subheader("1. Contract Setup and Market Parameters")

    # --- Currency Pair Selection for Pre-filling ---
    st.sidebar.subheader("Currency Pair & Defaults")
    currency_pair = st.sidebar.selectbox(
        label="Select Currency Pair (Pre-fill Rates)",
        options=["Custom", "USD/EUR (Example)", "ZAR/EUR (Example)"],
        help="Choose a synthetic currency pair to pre-populate typical spot rates and interest rate differentials. You can then adjust rates manually."
    )

    # Default values based on selected currency pair
    defaults = {
        "Custom": {"S0": 1.1, "T": 1.0, "rf_init": 0.01, "rd_init": 0.03, "St": 1.1, "rf_curr": 0.01, "rd_curr": 0.03},
        "USD/EUR (Example)": {"S0": 1.08, "T": 1.0, "rf_init": 0.03, "rd_init": 0.05, "St": 1.08, "rf_curr": 0.035, "rd_curr": 0.045}, # rd=USD, rf=EUR (EUR/USD, so 1 EUR = X USD)
        "ZAR/EUR (Example)": {"S0": 19.0, "T": 1.0, "rf_init": 0.03, "rd_init": 0.08, "St": 19.0, "rf_curr": 0.032, "rd_curr": 0.075}, # rd=ZAR, rf=EUR (EUR/ZAR, so 1 EUR = X ZAR)
    }

    selected_defaults = defaults[currency_pair]

    # --- Input Widgets in Sidebar ---
    st.sidebar.subheader("Initial Contract Parameters ($t=0$)")
    S0_f_d = st.sidebar.number_input(
        label="Initial Spot FX Rate ($S_{0,f/d}$)",
        min_value=0.1,
        max_value=1000.0,
        value=selected_defaults["S0"],
        step=0.01,
        format="%.4f",
        help="The spot exchange rate at the inception of the contract. Example: How many units of domestic currency for one unit of foreign currency."
    )

    T = st.sidebar.slider(
        label="Original Contract Maturity ($T$)",
        min_value=0.1,
        max_value=5.0,
        value=selected_defaults["T"],
        step=0.1,
        format="%.1f",
        help="The total time to maturity of the FX forward contract in years from inception."
    )

    rf_initial = st.sidebar.number_input(
        label="Foreign Risk-Free Rate at Inception ($r_{f,initial}$)",
        min_value=-0.05,
        max_value=0.20,
        value=selected_defaults["rf_init"],
        step=0.001,
        format="%.4f",
        help="The risk-free interest rate of the foreign currency at contract inception. (e.g., 0.01 for 1%)"
    )

    rd_initial = st.sidebar.number_input(
        label="Domestic Risk-Free Rate at Inception ($r_{d,initial}$)",
        min_value=-0.05,
        max_value=0.20,
        value=selected_defaults["rd_init"],
        step=0.001,
        format="%.4f",
        help="The risk-free interest rate of the domestic currency at contract inception. (e.g., 0.03 for 3%)"
    )

    st.sidebar.subheader("Current Market Parameters ($t$)")
    t = st.sidebar.slider(
        label="Current Time ($t$)",
        min_value=0.0,
        max_value=T, # Max dynamically adjusts
        value=min(selected_defaults["T"] * 0.5, T), # Default to half maturity, but not more than T
        step=0.01,
        format="%.2f",
        help=f"The current time in years from contract inception ($0 \le t \le T$). For $t=0$, MTM is usually zero (ignoring transaction costs). Max is {T:.1f} years."
    )

    # Adjust current spot rate default range based on initial spot rate
    st_min = S0_f_d * 0.8 # +/- 20% around initial
    st_max = S0_f_d * 1.2
    St_f_d = st.sidebar.number_input(
        label="Current Spot FX Rate ($S_{t,f/d}$)",
        min_value=st_min,
        max_value=st_max,
        value=selected_defaults["St"] if st_min <= selected_defaults["St"] <= st_max else S0_f_d,
        step=0.001,
        format="%.4f",
        help=f"The prevailing spot exchange rate in the market at the current time $t$. Range adjusted around initial spot rate ({st_min:.4f} to {st_max:.4f})."
    )

    rf_current = st.sidebar.number_input(
        label="Current Foreign Risk-Free Rate ($r_{f,current}$)",
        min_value=-0.05,
        max_value=0.20,
        value=selected_defaults["rf_curr"],
        step=0.001,
        format="%.4f",
        help="The current risk-free interest rate of the foreign currency at time $t$. This can differ from $r_{f,initial}$."
    )

    rd_current = st.sidebar.number_input(
        label="Current Domestic Risk-Free Rate ($r_{d,current}$)",
        min_value=-0.05,
        max_value=0.20,
        value=selected_defaults["rd_curr"],
        step=0.001,
        format="%.4f",
        help="The current risk-free interest rate of the domestic currency at time $t$. This can differ from $r_{d,initial}$."
    )

    # --- Calculations ---
    F0_f_d = calculate_fx_forward_price(S0_f_d, rf_initial, rd_initial, T)
    Vt_long = calculate_mtm(St_f_d, F0_f_d, rf_current, rd_current, T, t)
    Vt_short = -Vt_long

    st.subheader("2. Calculated Values")
    st.markdown(f"**FX Forward Price at Inception ($F_{{0,f/d}}(T)$):**
"
                f"The initial forward price, agreed upon at time $t=0$, is **{F0_f_d:.4f}**.")
    st.latex(r"F_{0,f/d}(T) = S_{0,f/d}e^{(r_{f,initial} - r_{d,initial})T}")
    st.markdown("""
    This is the rate at which you initially agreed to exchange currencies at maturity $T$.
    """)

    st.markdown(f"**Current Mark-to-Market (MTM) Value:**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Long Position MTM ($V_t^{long}(T)$)", value=f"{Vt_long:.4f}")
    with col2:
        st.metric(label="Short Position MTM ($V_t^{short}(T)$)", value=f"{Vt_short:.4f}")

    st.markdown("""
    The MTM value represents the hypothetical profit or loss if the contract were to be closed out or revalued at the current market conditions ($t$).
    *   A **positive MTM for a long position** indicates a gain for the buyer of the foreign currency.
    *   A **negative MTM for a long position** indicates a loss for the buyer of the foreign currency.
    *   For a **short position**, the MTM is simply the negative of the long position's MTM.
    """)
    st.latex(r"V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_{f,current} - r_{d,current})(T - t)}")


    st.subheader("3. Interactive Visualizations")

    # --- Plot 1: Interest Rate Differential Impact ---
    st.markdown("#### MTM Value vs. Interest Rate Differential ($r_f - r_d$)")
    st.markdown("""
    This plot shows how the MTM value changes if the current foreign risk-free rate ($r_{f,current}$) varies,
    while holding all other parameters constant. This illustrates the sensitivity of the contract's value
    to changes in interest rate differentials.
    """)
    st.info("Note: The current domestic risk-free rate ($r_{d,current}$) is held constant, and $r_{f,current}$ is varied to show the differential impact.")

    # Vary rf_current around its current value
    rf_current_range = np.linspace(rf_current * 0.5, rf_current * 1.5, 100)
    # Ensure range covers some negative values if current is near zero
    if rf_current_range[0] > -0.02:
        rf_current_range = np.linspace(-0.02, max(rf_current_range[-1], 0.10), 100)

    mtm_long_rates = [calculate_mtm(St_f_d, F0_f_d, r_f, rd_current, T, t) for r_f in rf_current_range]
    mtm_short_rates = [-mtm for mtm in mtm_long_rates]
    ir_differential = rf_current_range - rd_current

    fig_rates = go.Figure()
    fig_rates.add_trace(go.Scatter(x=ir_differential, y=mtm_long_rates, mode='lines', name='Long Position'))
    fig_rates.add_trace(go.Scatter(x=ir_differential, y=mtm_short_rates, mode='lines', name='Short Position'))
    fig_rates.add_trace(go.Scatter(x=[ir_differential[np.argmin(np.abs(rf_current_range - rf_current))]],
                                  y=[Vt_long],
                                  mode='markers',
                                  name='Current Value (Long)',
                                  marker=dict(symbol='star', size=10, color='red')))

    fig_rates.add_hline(y=0, line_dash="dash", line_color="grey", annotation_text="Zero MTM", annotation_position="bottom right")

    fig_rates.update_layout(
        title='MTM Value vs. Interest Rate Differential',
        xaxis_title='Interest Rate Differential ($r_f - r_d$)',
        yaxis_title='MTM Value',
        hovermode="x unified",
        font=dict(size=12)
    )
    st.plotly_chart(fig_rates, use_container_width=True)

    st.markdown("""
    *   **Interpretation**: If the foreign interest rate ($r_f$) increases relative to the domestic rate ($r_d$), it generally makes the foreign currency more attractive, which can impact the forward premium/discount and thus the MTM. For a long position (buying foreign), a higher $r_f$ relative to $r_d$ tends to increase MTM if $S_{t,f/d}$ is higher than the discounted original forward.
    """)

    # --- Plot 2: Spot Rate Change Impact ---
    st.markdown("#### MTM Value vs. Current Spot FX Rate ($S_t$)")
    st.markdown("""
    This plot illustrates the sensitivity of the MTM value to changes in the current spot FX rate ($S_{t,f/d}$),
    while holding all other parameters constant. This is often the most significant driver of MTM changes.
    """)

    # Vary St_f_d around its current value
    spot_range = np.linspace(S0_f_d * 0.7, S0_f_d * 1.3, 100) # +/- 30% around initial spot for plot
    mtm_long_spot = [calculate_mtm(s, F0_f_d, rf_current, rd_current, T, t) for s in spot_range]
    mtm_short_spot = [-mtm for mtm in mtm_long_spot]

    fig_spot = go.Figure()
    fig_spot.add_trace(go.Scatter(x=spot_range, y=mtm_long_spot, mode='lines', name='Long Position'))
    fig_spot.add_trace(go.Scatter(x=spot_range, y=mtm_short_spot, mode='lines', name='Short Position'))
    fig_spot.add_vline(x=F0_f_d, line_dash="dot", line_color="purple", annotation_text="Initial Forward Price", annotation_position="top left")
    fig_spot.add_vline(x=St_f_d, line_dash="solid", line_color="red", annotation_text="Current Spot Rate", annotation_position="bottom right")
    fig_spot.add_hline(y=0, line_dash="dash", line_color="grey", annotation_text="Zero MTM", annotation_position="bottom center")

    fig_spot.update_layout(
        title='MTM Value vs. Current Spot FX Rate',
        xaxis_title='Current Spot Rate ($S_t$)',
        yaxis_title='MTM Value',
        hovermode="x unified",
        font=dict(size=12)
    )
    st.plotly_chart(fig_spot, use_container_width=True)

    st.markdown("""
    *   **Interpretation**: For a long FX forward position (agreeing to buy foreign currency at a fixed rate), if the current spot rate ($S_t$) is higher than the effectively discounted original forward rate ($F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$), the position will show a gain (positive MTM). Conversely, if $S_t$ is lower, it will show a loss.
    *   The vertical dashed line indicates the initial forward price ($F_{0,f/d}(T)$).
    *   The vertical solid red line indicates the current spot rate ($S_{t,f/d}$).
    """
    )
    st.subheader("4. References")
    st.markdown("""
    *   [16] Hull, John C. *Options, Futures, and Other Derivatives*. Pearson Education. (For FX Forward Price formula)
    *   [17] (Your specific reference for MTM value formula, acknowledging the exact form provided in the prompt's specification)
    """
    )
