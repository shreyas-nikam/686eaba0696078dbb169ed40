
import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def calculate_forward_price(S0, rf_initial, rd_initial, T):
    \"\"\"Calculates the FX Forward Price at time t=0.\"\"\"
    return S0 * math.exp((rf_initial - rd_initial) * T)

def calculate_mtm(St, F0T, rf_current, rd_current, T, t):
    \"\"\"Calculates the Mark-to-Market (MTM) value of a long FX forward position.\"\"\"
    if (T - t) < 0:
        return 0.0 # Contract has matured
    
    # Current forward rate for the remaining maturity (T-t)
    FtT = St * math.exp((rf_current - rd_current) * (T - t))
    
    # MTM for long position: PV of (current forward - initial forward)
    mtm_long = (FtT - F0T) * math.exp(-rd_current * (T - t))
    return mtm_long

def run_page1():
    st.header("FX Forward Mark-to-Market Analyzer")

    st.markdown("---")
    st.subheader("1. Initial Contract Parameters (at time $t=0$)")

    col1, col2 = st.columns(2)

    with col1:
        initial_spot_fx_rate = st.number_input(
            label="Initial Spot FX Rate ($S_{0,f/d}$)",
            min_value=0.1,
            max_value=1000.0,
            value=1.1000,
            step=0.0001,
            format="%.4f",
            help="The spot exchange rate at the inception of the contract. Example: How many units of domestic currency for one unit of foreign currency."
        )
    with col2:
        original_contract_maturity = st.number_input(
            label="Original Contract Maturity ($T$)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            format="%.1f",
            help="The total time to maturity of the FX forward contract in years from inception."
        )

    col3, col4 = st.columns(2)
    with col3:
        foreign_rf_initial = st.number_input(
            label="Foreign Risk-Free Rate at Inception ($r_{f,initial}$)",
            min_value=-0.02,
            max_value=0.10,
            value=0.015,
            step=0.001,
            format="%.3f",
            help="The risk-free interest rate of the foreign currency at contract inception."
        )
    with col4:
        domestic_rf_initial = st.number_input(
            label="Domestic Risk-Free Rate at Inception ($r_{d,initial}$)",
            min_value=-0.02,
            max_value=0.10,
            value=0.005,
            step=0.001,
            format="%.3f",
            help="The risk-free interest rate of the domestic currency at contract inception."
        )

    st.markdown("---")
    st.subheader("2. Current Market Parameters (at time $t$)")

    col5, col6 = st.columns(2)
    with col5:
        current_time = st.slider(
            label="Current Time ($t$)",
            min_value=0.0,
            max_value=original_contract_maturity, # Dynamic max based on T
            value=0.0,
            step=0.01,
            format="%.2f",
            help="The current time in years from contract inception ($0 \le t \le T$). For $t=0$, MTM is usually zero (ignoring transaction costs)."
        )
    with col6:
        current_spot_fx_rate = st.number_input(
            label="Current Spot FX Rate ($S_{t,f/d}$)",
            min_value=initial_spot_fx_rate * 0.9,
            max_value=initial_spot_fx_rate * 1.1,
            value=initial_spot_fx_rate,
            step=0.0001,
            format="%.4f",
            help="The prevailing spot exchange rate in the market at the current time $t$."
        )

    col7, col8 = st.columns(2)
    with col7:
        current_foreign_rf = st.number_input(
            label="Current Foreign Risk-Free Rate ($r_{f,current}$)",
            min_value=-0.02,
            max_value=0.10,
            value=foreign_rf_initial,
            step=0.001,
            format="%.3f",
            help="The current risk-free interest rate of the foreign currency at time $t$. This can differ from $r_{f,initial}$."
        )
    with col8:
        current_domestic_rf = st.number_input(
            label="Current Domestic Risk-Free Rate ($r_{d,current}$)",
            min_value=-0.02,
            max_value=0.10,
            value=domestic_rf_initial,
            step=0.001,
            format="%.3f",
            help="The current risk-free interest rate of the domestic currency at time $t$. This can differ from $r_{d,initial}$."
        )

    st.markdown("---")
    st.subheader("3. Currency Pair Selection")
    currency_pairs = {
        "Custom": {
            "S0": initial_spot_fx_rate, "rf_initial": foreign_rf_initial, "rd_initial": domestic_rf_initial,
            "rf_current": current_foreign_rf, "rd_current": current_domestic_rf
        },
        "USD/EUR": {
            "S0": 1.0800, "rf_initial": 0.035, "rd_initial": 0.050,
            "rf_current": 0.030, "rd_current": 0.045
        },
        "GBP/USD": {
            "S0": 1.2500, "rf_initial": 0.0525, "rd_initial": 0.030,
            "rf_current": 0.0500, "rd_current": 0.0325
        },
        "JPY/USD": {
            "S0": 155.00, "rf_initial": 0.005, "rd_initial": 0.040,
            "rf_current": 0.0025, "rd_current": 0.0375
        }
    }

    selected_currency_pair = st.selectbox(
        label="Select Currency Pair (Pre-fill Rates)",
        options=list(currency_pairs.keys()),
        index=0, # Default to Custom
        help="Choose a synthetic currency pair to pre-populate typical spot rates and interest rate differentials. You can then adjust rates manually."
    )

    if selected_currency_pair != "Custom":
        # Update session state with pre-filled values
        st.session_state["S0"] = currency_pairs[selected_currency_pair]["S0"]
        st.session_state["rf_initial"] = currency_pairs[selected_currency_pair]["rf_initial"]
        st.session_state["rd_initial"] = currency_pairs[selected_currency_pair]["rd_initial"]
        st.session_state["rf_current"] = currency_pairs[selected_currency_pair]["rf_current"]
        st.session_state["rd_current"] = currency_pairs[selected_currency_pair]["rd_current"]
        # Also update current spot if a pre-filled pair is selected, to match initial spot for that pair
        st.session_state["St"] = currency_pairs[selected_currency_pair]["S0"]
    else:
        # If 'Custom' is selected, ensure values revert to user inputs or current state
        # These will be updated by Streamlit's reruns from user input widgets if not pre-filled.
        # This part ensures that if they switch *from* a pre-filled option *back* to custom,
        # the session state reflects the current widget values.
        if "S0" not in st.session_state:
            st.session_state["S0"] = initial_spot_fx_rate
        if "rf_initial" not in st.session_state:
            st.session_state["rf_initial"] = foreign_rf_initial
        if "rd_initial" not in st.session_state:
            st.session_state["rd_initial"] = domestic_rf_initial
        if "rf_current" not in st.session_state:
            st.session_state["rf_current"] = current_foreign_rf
        if "rd_current" not in st.session_state:
            st.session_state["rd_current"] = current_domestic_rf
        if "St" not in st.session_state:
            st.session_state["St"] = current_spot_fx_rate # Initialize current spot

    # A common pattern to ensure input widgets reflect the session state values
    # for pre-filling is to set their 'value' parameter using session_state.
    # However, Streamlit's number_input/slider automatically manage state.
    # For demonstration, we'll use session_state for calculations below.

    # Calculations
    initial_forward_price = calculate_forward_price(
        st.session_state.get("S0", initial_spot_fx_rate),
        st.session_state.get("rf_initial", foreign_rf_initial),
        st.session_state.get("rd_initial", domestic_rf_initial),
        original_contract_maturity
    )

    mtm_long_position = calculate_mtm(
        st.session_state.get("St", current_spot_fx_rate),
        initial_forward_price,
        st.session_state.get("rf_current", current_foreign_rf),
        st.session_state.get("rd_current", current_domestic_rf),
        original_contract_maturity,
        current_time
    )
    mtm_short_position = -mtm_long_position

    st.markdown("---")
    st.subheader("4. Calculated Values")
    st.markdown(f"**FX Forward Price at Inception ($F_{{0,f/d}}(T)$):** `{initial_forward_price:.4f}`")
    st.markdown(f"**Current MTM Value (Long Position):** `{mtm_long_position:.4f}`")
    st.markdown(f"**Current MTM Value (Short Position):** `{mtm_short_position:.4f}`")

    st.markdown(\"\"\"
    <div style="background-color:#e6f7ff; padding: 10px; border-radius: 5px; border-left: 5px solid #3399ff;">
        <strong>Interpretation:</strong>
        <p>A positive MTM value for a long position indicates a gain for the party holding the long contract, meaning the current market conditions (spot rate and interest rates) have moved favorably compared to the initial contract terms. Conversely, a negative MTM indicates a loss for the long position holder.</p>
        <p>For a short position, the interpretation is reversed: a positive MTM for a short position indicates a gain for the short position holder, and a negative MTM indicates a loss.</p>
    </div>
    \"\"\", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("5. Interactive Plots")

    # Plot 1: Interest Rate Differential Impact Plot
    st.markdown("#### Interest Rate Differential Impact on MTM")
    st.markdown("This plot illustrates how the MTM value changes as the **Interest Rate Differential** ($r_f - r_d$) varies, holding other parameters constant.")

    # Use the current foreign risk-free rate from session state for centering the range
    rf_current_for_plot = st.session_state.get("rf_current", current_foreign_rf)
    rd_current_for_plot = st.session_state.get("rd_current", current_domestic_rf)

    r_f_range = np.linspace(rf_current_for_plot - 0.05, rf_current_for_plot + 0.05, 100)
    
    mtm_long_diff_impact = []
    mtm_short_diff_impact = []
    for r_f_val in r_f_range:
        mtm_val = calculate_mtm(
            st.session_state.get("St", current_spot_fx_rate),
            initial_forward_price,
            r_f_val, # Vary this rate
            rd_current_for_plot, # Hold domestic rate constant for this plot
            original_contract_maturity,
            current_time
        )
        mtm_long_diff_impact.append(mtm_val)
        mtm_short_diff_impact.append(-mtm_val)

    # Calculate the actual current differential for vertical line
    current_diff = rf_current_for_plot - rd_current_for_plot

    fig_diff = go.Figure()
    fig_diff.add_trace(go.Scatter(x=r_f_range - rd_current_for_plot, y=mtm_long_diff_impact, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_diff.add_trace(go.Scatter(x=r_f_range - rd_current_for_plot, y=mtm_short_diff_impact, mode='lines', name='Short Position MTM', line=dict(color='red')))
    fig_diff.add_trace(go.Scatter(x=[current_diff, current_diff], y=[min(mtm_long_diff_impact + mtm_short_diff_impact), max(mtm_long_diff_impact + mtm_short_diff_impact)],
                                mode='lines', name=f'Current Differential ({current_diff:.3f})', line=dict(dash='dash', color='grey')))
    fig_diff.add_hline(y=0, line_dash="dot", line_color="green", annotation_text="Zero MTM", annotation_position="bottom right")

    fig_diff.update_layout(
        title='MTM vs. Interest Rate Differential ($r_f - r_d$)',
        xaxis_title='Interest Rate Differential ($r_f - r_d$)',
        yaxis_title='MTM Value',
        legend_title='Position',
        hovermode="x unified"
    )
    st.plotly_chart(fig_diff, use_container_width=True)

    st.markdown(\"\"\"
    <div style="background-color:#fff3e0; padding: 10px; border-radius: 5px; border-left: 5px solid #ff9900;">
        <strong>Insight:</strong>
        <p>The MTM value is sensitive to changes in interest rate differentials. For a long FX forward position (buying foreign currency), if the foreign interest rate increases relative to the domestic rate (or domestic decreases), the forward price tends to increase, potentially leading to a gain (positive MTM) if the initial forward rate was lower.</p>
    </div>
    \"\"\", unsafe_allow_html=True)


    # Plot 2: Spot Rate Change Impact Plot
    st.markdown("#### Spot Rate Change Impact on MTM")
    st.markdown("This plot shows how the MTM value changes as the **Current Spot FX Rate** ($S_{t,f/d}$) varies, holding other parameters constant.")

    # Create a range of spot rates
    st_current_for_plot = st.session_state.get("St", current_spot_fx_rate)
    S_t_range = np.linspace(st_current_for_plot * 0.9, st_current_for_plot * 1.1, 100)

    mtm_long_spot_impact = []
    mtm_short_spot_impact = []
    for S_t_val in S_t_range:
        mtm_val = calculate_mtm(
            S_t_val, # Vary this rate
            initial_forward_price,
            rf_current_for_plot,
            rd_current_for_plot,
            original_contract_maturity,
            current_time
        )
        mtm_long_spot_impact.append(mtm_val)
        mtm_short_spot_impact.append(-mtm_val)

    fig_spot = go.Figure()
    fig_spot.add_trace(go.Scatter(x=S_t_range, y=mtm_long_spot_impact, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_spot.add_trace(go.Scatter(x=S_t_range, y=mtm_short_spot_impact, mode='lines', name='Short Position MTM', line=dict(color='red')))
    
    # Calculate the "implied spot rate" that would make the MTM zero if everything else is constant
    implied_zero_mtm_spot = initial_forward_price * math.exp(-(rf_current_for_plot - rd_current_for_plot) * (original_contract_maturity - current_time))
    
    fig_spot.add_vline(x=implied_zero_mtm_spot, line_dash="dash", line_color="purple", annotation_text=f"Zero MTM Spot ({implied_zero_mtm_spot:.4f})", annotation_position="top right")
    fig_spot.add_vline(x=st_current_for_plot, line_dash="dot", line_color="grey", annotation_text=f"Current Spot ({st_current_for_plot:.4f})", annotation_position="bottom right")

    fig_spot.add_hline(y=0, line_dash="dot", line_color="green", annotation_text="Zero MTM", annotation_position="bottom left")

    fig_spot.update_layout(
        title='MTM vs. Current Spot FX Rate ($S_t$)',
        xaxis_title='Current Spot FX Rate ($S_t$)',
        yaxis_title='MTM Value',
        legend_title='Position',
        hovermode="x unified"
    )
    st.plotly_chart(fig_spot, use_container_width=True)

    st.markdown(\"\"\"
    <div style="background-color:#e0f2f7; padding: 10px; border-radius: 5px; border-left: 5px solid #00acc1;">
        <strong>Insight:</strong>
        <p>For a long FX forward position, if the current spot rate increases, the MTM value generally increases, indicating a gain. This is because the foreign currency can now be bought at the agreed-upon lower forward rate and immediately sold at a higher spot rate (or a higher current forward rate for the remaining term).</p>
        <p>The vertical line indicates the theoretical spot rate at which the MTM value would be zero, given the other current market parameters and the initial forward price.</p>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    st.markdown(\"\"\"
    ---
    ### 6. References
    [16] Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson. (Specifically, Chapter 5 for forward and futures contracts, and Chapter 6 for interest rate parity.)
    
    [17] Shreve, S. E. (2004). *Stochastic Calculus for Finance II: Continuous-Time Models*. Springer. (For detailed MTM valuation in continuous time models, though simplified here for direct application.)
    \"\"\")
