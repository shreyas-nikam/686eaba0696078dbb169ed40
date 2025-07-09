
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import exp

def calculate_forward_price(S0, rf, rd, T):
    """Calculates the FX Forward Price at inception (t=0)."""
    return S0 * exp((rf - rd) * T)

def calculate_mtm_long(St, F0T, rf_current, rd_current, T, t):
    """Calculates the Mark-to-Market value for a long FX forward position at time t."""
    # Ensure T-t is not negative for the exponent, though Streamlit slider should prevent it.
    time_to_maturity_remaining = max(0.0, T - t)
    return St - F0T * exp(-(rf_current - rd_current) * time_to_maturity_remaining)

def run_fx_forward_mtm_analyzer():
    st.header("FX Forward MTM Analyzer")

    st.markdown("""
    Use the controls in the sidebar to define your FX Forward contract and analyze its Mark-to-Market (MTM) value under various market conditions.
    """)

    st.sidebar.header("1. Initial Contract Parameters (t=0)")

    # Currency Pair Selection to pre-fill rates
    currency_pairs = {
        "Custom": {}, # Empty for manual input
        "USD/EUR (Domestic=USD, Foreign=EUR)": {
            "S0_f_d": 1.08, "rf_initial": 0.035, "rd_initial": 0.05,
            "rf_current": 0.03, "rd_current": 0.045
        },
        "ZAR/EUR (Domestic=ZAR, Foreign=EUR)": {
            "S0_f_d": 19.50, "rf_initial": 0.035, "rd_initial": 0.08,
            "rf_current": 0.03, "rd_current": 0.075
        },
        "EUR/USD (Domestic=EUR, Foreign=USD)": {
            "S0_f_d": 0.92, "rf_initial": 0.05, "rd_initial": 0.035,
            "rf_current": 0.045, "rd_current": 0.03
        }
    }

    selected_pair_label = st.sidebar.selectbox(
        label="Select Currency Pair (Pre-fill Rates)",
        options=list(currency_pairs.keys()),
        help="Choose a synthetic currency pair to pre-populate typical spot rates and interest rate differentials. You can then adjust rates manually."
    )

    # Use session state to manage inputs and pre-fill logic
    if "s0_value" not in st.session_state:
        st.session_state.s0_value = 1.08 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 1.0
    if "T_value" not in st.session_state:
        st.session_state.T_value = 1.0
    if "rf_initial_value" not in st.session_state:
        st.session_state.rf_initial_value = 0.035 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0
    if "rd_initial_value" not in st.session_state:
        st.session_state.rd_initial_value = 0.05 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0
    if "t_value" not in st.session_state:
        st.session_state.t_value = 0.0
    if "st_value" not in st.session_state:
        st.session_state.st_value = 1.08 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 1.0
    if "rf_current_value" not in st.session_state:
        st.session_state.rf_current_value = 0.03 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0
    if "rd_current_value" not in st.session_state:
        st.session_state.rd_current_value = 0.045 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0

    # Pre-fill values if a specific currency pair is selected and it's not "Custom"
    # This logic only applies on selection change, not on every re-render unless explicitly triggered.
    if selected_pair_label != "Custom" and selected_pair_label in currency_pairs:
        prefill_data = currency_pairs[selected_pair_label]
        st.session_state.s0_value = prefill_data.get("S0_f_d", st.session_state.s0_value)
        st.session_state.rf_initial_value = prefill_data.get("rf_initial", st.session_state.rf_initial_value)
        st.session_state.rd_initial_value = prefill_data.get("rd_initial", st.session_state.rd_initial_value)
        st.session_state.st_value = prefill_data.get("St_f_d", prefill_data["S0_f_d"]) # Use initial spot as default current spot
        st.session_state.rf_current_value = prefill_data.get("rf_current", st.session_state.rf_current_value)
        st.session_state.rd_current_value = prefill_data.get("rd_current", st.session_state.rd_current_value)


    S0_f_d = st.sidebar.number_input(
        label="Initial Spot FX Rate ($S_{0,f/d}$)",
        min_value=0.1, max_value=100.0, value=st.session_state.s0_value, step=0.01, format="%.4f",
        help="The spot exchange rate at the inception of the contract. Example: How many units of domestic currency for one unit of foreign currency."
    )
    T_maturity = st.sidebar.slider(
        label="Original Contract Maturity ($T$)",
        min_value=0.1, max_value=5.0, value=st.session_state.T_value, step=0.1,
        help="The total time to maturity of the FX forward contract in years from inception."
    )
    rf_initial = st.sidebar.number_input(
        label="Foreign Risk-Free Rate at Inception ($r_{f,initial}$)",
        min_value=-0.05, max_value=0.20, value=st.session_state.rf_initial_value, step=0.001, format="%.4f",
        help="The risk-free interest rate of the foreign currency at contract inception."
    )
    rd_initial = st.sidebar.number_input(
        label="Domestic Risk-Free Rate at Inception ($r_{d,initial}$)",
        min_value=-0.05, max_value=0.20, value=st.session_state.rd_initial_value, step=0.001, format="%.4f",
        help="The risk-free interest rate of the domestic currency at contract inception."
    )

    st.sidebar.header("2. Current Market Parameters (at time t)")

    t_current = st.sidebar.slider(
        label="Current Time ($t$)",
        min_value=0.0, max_value=T_maturity, value=st.session_state.t_value, step=0.01,
        help=f"The current time in years from contract inception ($0 \le t \le T = {T_maturity:.1f}$). For $t=0$, MTM is usually zero (ignoring transaction costs)."
    )

    # Adjust default for current spot to be around initial spot for better UX on first load
    # This also helps with the +/- 10% range.
    spot_range_min = S0_f_d * 0.9
    spot_range_max = S0_f_d * 1.1

    St_f_d = st.sidebar.number_input(
        label="Current Spot FX Rate ($S_{t,f/d}$)",
        min_value=spot_range_min, max_value=spot_range_max, value=st.session_state.st_value, step=0.01, format="%.4f",
        help=f"The prevailing spot exchange rate in the market at the current time $t$. (Range: {spot_range_min:.2f} to {spot_range_max:.2f})"
    )
    rf_current = st.sidebar.number_input(
        label="Current Foreign Risk-Free Rate ($r_{f,current}$)",
        min_value=-0.05, max_value=0.20, value=st.session_state.rf_current_value, step=0.001, format="%.4f",
        help="The current risk-free interest rate of the foreign currency at time $t$. This can differ from $r_{f,initial}$."
    )
    rd_current = st.sidebar.number_input(
        label="Current Domestic Risk-Free Rate ($r_{d,current}$)",
        min_value=-0.05, max_value=0.20, value=st.session_state.rd_current_value, step=0.001, format="%.4f",
        help="The current risk-free interest rate of the domestic currency at time $t$. This can differ from $r_{d,initial}$."
    )

    # Input Validation
    if t_current > T_maturity:
        st.error("Error: Current Time (t) cannot be greater than Original Contract Maturity (T). Please adjust the slider.")
        st.stop() # Stop execution if validation fails

    # --- Calculations ---
    F0T = calculate_forward_price(S0_f_d, rf_initial, rd_initial, T_maturity)
    Vt_long = calculate_mtm_long(St_f_d, F0T, rf_current, rd_current, T_maturity, t_current)
    Vt_short = -Vt_long

    st.subheader("Calculated Values")
    st.markdown(f"**Initial FX Forward Price ($F_{{0,f/d}}(T)$):** `{F0T:.4f}`")
    st.markdown(f"**Current MTM Value (Long Position, $V_t^{{long}}(T)$):** `{Vt_long:.4f}`")
    st.markdown(f"**Current MTM Value (Short Position, $V_t^{{short}}(T)$):** `{Vt_short:.4f}`")

    st.markdown("""
    ### Interpretation of MTM Values
    *   A **positive MTM** for a **long position** means the contract has gained value since inception, indicating a theoretical profit if closed out today.
    *   A **negative MTM** for a **long position** means the contract has lost value, indicating a theoretical loss.
    *   For a **short position**, the interpretation is reversed: a positive MTM means a loss, and a negative MTM means a gain.
    """)

    st.subheader("Interactive Plots")

    # --- Plot 1: Interest Rate Differential Impact ---
    st.markdown("#### MTM Value vs. Interest Rate Differential ($r_f - r_d$)")
    st.markdown("""
    This plot shows how the MTM value changes as the **Foreign Risk-Free Rate** ($r_f$) varies,
    while keeping the **Domestic Risk-Free Rate** ($r_d$) constant. This effectively changes the interest rate differential.
    Observe how MTM sensitivity relates to changes in interest rates.
    """)

    rf_values = np.linspace(-0.05, 0.20, 100) # Range for rf to plot
    mtm_long_rf_impact = [calculate_mtm_long(St_f_d, F0T, rf_val, rd_current, T_maturity, t_current) for rf_val in rf_values]
    mtm_short_rf_impact = [-val for val in mtm_long_rf_impact]

    fig_rates = go.Figure()
    fig_rates.add_trace(go.Scatter(x=rf_values - rd_current, y=mtm_long_rf_impact, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_rates.add_trace(go.Scatter(x=rf_values - rd_current, y=mtm_short_rf_impact, mode='lines', name='Short Position MTM', line=dict(color='red')))

    fig_rates.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Zero MTM")
    fig_rates.update_layout(
        title='MTM Value vs. Interest Rate Differential (varying $r_f$)',
        xaxis_title='Interest Rate Differential ($r_f - r_d$)',
        yaxis_title='MTM Value',
        hovermode="x unified",
        font=dict(size=12)
    )
    st.plotly_chart(fig_rates, use_container_width=True)


    # --- Plot 2: Spot Rate Change Impact ---
    st.markdown("#### MTM Value vs. Current Spot FX Rate ($S_{t,f/d}$)")
    st.markdown("""
    This plot illustrates how the MTM value reacts to changes in the **Current Spot FX Rate** ($S_{t,f/d}$).
    The vertical dashed line indicates the **Initial FX Forward Price** ($F_{0,f/d}(T)$), which is the rate
    at which the contract was originally agreed upon.
    """)

    spot_values = np.linspace(S0_f_d * 0.8, S0_f_d * 1.2, 100) # Range around initial spot for plotting
    mtm_long_spot_impact = [calculate_mtm_long(s_val, F0T, rf_current, rd_current, T_maturity, t_current) for s_val in spot_values]
    mtm_short_spot_impact = [-val for val in mtm_long_spot_impact]

    fig_spot = go.Figure()
    fig_spot.add_trace(go.Scatter(x=spot_values, y=mtm_long_spot_impact, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_spot.add_trace(go.Scatter(x=spot_values, y=mtm_short_spot_impact, mode='lines', name='Short Position MTM', line=dict(color='red')))

    fig_spot.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Zero MTM")
    fig_spot.add_vline(x=F0T, line_dash="dash", line_color="green", annotation_text=f"Initial Forward Price: {F0T:.4f}",
                        annotation_position="top right")
    fig_spot.update_layout(
        title='MTM Value vs. Current Spot FX Rate ($S_t$)',
        xaxis_title='Current Spot Rate ($S_t$)',
        yaxis_title='MTM Value',
        hovermode="x unified",
        font=dict(size=12)
    )
    st.plotly_chart(fig_spot, use_container_width=True)

    st.subheader("Formulas Used")
    st.markdown("The core calculations in this application are based on the following financial formulas:")

    st.markdown("### FX Forward Price (continuous compounding)")
    st.latex(r"F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}")
    st.markdown("""
    Where:
    *   $F_{0,f/d}(T)$ is the forward price at time 0 for a contract maturing at time $T$.
    *   $S_{0,f/d}$ is the spot exchange rate at time 0 (foreign currency per domestic currency).
    *   $r_f$ is the foreign risk-free interest rate.
    *   $r_d$ is the domestic risk-free interest rate.
    *   $T$ is the original time to maturity of the forward contract in years.
    *   $e$ is the base of the natural logarithm.
    """)

    st.markdown("### Mark-to-Market value of an FX forward contract (long position)")
    st.latex(r"V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}")
    st.markdown("""
    Where:
    *   $V_t^{long}(T)$ is the Mark-to-Market value for a long position at time $t$.
    *   $S_{t,f/d}$ is the current spot exchange rate at time $t$.
    *   $F_{0,f/d}(T)$ is the initial forward price calculated at $t=0$.
    *   $r_f$ is the current foreign risk-free interest rate.
    *   $r_d$ is the current domestic risk-free interest rate.
    *   $T$ is the original time to maturity.
    *   $t$ is the current time in years from the contract inception ($0 \le t \le T$).
    *   $e$ is the base of the natural logarithm.
    """)
    st.markdown(r"For a **short position**, $V_t^{short}(T) = -V_t^{long}(T)$.")


    st.subheader("References")
    st.markdown("""
    The formulas used in this application are standard in financial mathematics for derivative pricing.
    [16] John C. Hull, *Options, Futures, and Other Derivatives*, 11th Edition. Pearson.
    [17] CFA Institute, *Derivatives* (CFA Program Curriculum Level II).
    """)
