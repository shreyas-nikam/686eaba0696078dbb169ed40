
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Helper Functions
def parse_cash_flows(json_str):
    try:
        if not json_str.strip():
            return []
        data = json.loads(json_str)
        if not isinstance(data, list):
            st.error("Cash flow input must be a JSON list of objects.")
            return []
        for item in data:
            if not isinstance(item, dict) or "amount" not in item or "time_from_t0" not in item:
                st.error("Each cash flow object must have 'amount' and 'time_from_t0' keys.")
                return []
            if not isinstance(item["amount"], (int, float)) or not isinstance(item["time_from_t0"], (int, float)):
                st.error("Cash flow 'amount' and 'time_from_t0' must be numbers.")
                return []
            if item["time_from_t0"] < 0:
                st.error("Cash flow 'time_from_t0' cannot be negative.")
                return []
        return data
    except json.JSONDecodeError:
        st.error("Invalid JSON format for cash flows. Please check your syntax.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred parsing cash flows: {e}")
        return []

def calculate_present_value(cash_flows, rate, current_time, maturity):
    pv = 0.0
    for cf in cash_flows:
        amount = cf["amount"]
        time_from_t0 = cf["time_from_t0"]
        if time_from_t0 >= current_time and time_from_t0 <= maturity:
            discount_period = time_from_t0 - current_time
            if discount_period < 0: # Should not happen with t_j_CF >= t check, but good for robustness
                continue
            pv += amount / (1 + rate)**discount_period
    return pv

def calculate_forward_price_at_inception(S0, T, r, dividends, costs):
    pv_dividends_at_0 = calculate_present_value(dividends, r, 0, T)
    pv_costs_at_0 = calculate_present_value(costs, r, 0, T)
    F0_T = (S0 - pv_dividends_at_0 + pv_costs_at_0) * (1 + r)**T
    return F0_T

def calculate_mtm_value(St, T, t_current, r, F0_T, dividends, costs):
    pv_remaining_dividends = calculate_present_value(dividends, r, t_current, T)
    pv_remaining_costs = calculate_present_value(costs, r, t_current, T)
    
    # Ensure remaining_time_to_maturity is non-negative
    remaining_time_to_maturity = max(0, T - t_current)
    
    Vt_T_long = (St - pv_remaining_dividends + pv_remaining_costs) - F0_T * (1 + r)**(-remaining_time_to_maturity)
    return Vt_T_long

def run_page():
    st.header("Forward Contracts with Costs & Benefits Simulator")

    # Layout using columns for input widgets
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Core Contract Parameters")
        S0 = st.number_input(
            "Initial Spot Price ($S_0$):",
            min_value=0.01, value=100.0, step=0.1,
            help="The current market price of the underlying asset at t=0."
        )
        T = st.number_input(
            "Maturity ($T$):",
            min_value=0.1, value=1.0, step=0.1,
            help="Total time to maturity of the forward contract in years from t=0."
        )
        r = st.number_input(
            "Risk-Free Rate ($r$):",
            min_value=0.001, value=0.05, step=0.001, format="%.3f",
            help="The annualized risk-free interest rate (e.g., enter 0.05 for 5%)."
        )

    with col2:
        st.subheader("Current Valuation Parameters")
        t_current = st.number_input(
            "Current Time ($t$):",
            min_value=0.0, value=0.5, step=0.01,
            help="The current point in time for MTM valuation ($0 \\le t \\le T$).",
            key="current_time_t"
        )
        St = st.number_input(
            "Current Spot Price ($S_t$):",
            min_value=0.01, value=102.0, step=0.1,
            help="The spot price of the underlying asset at the current time t."
        )

    st.subheader("Cash Flow Specification")
    col_cf1, col_cf2 = st.columns(2)
    with col_cf1:
        dividends_json = st.text_area(
            "Dividends (Benefits) [JSON]:",
            value='[{"amount": 2.0, "time_from_t0": 0.25}, {"amount": 2.5, "time_from_t0": 0.75}]',
            height=100,
            help="Enter discrete dividends as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from t=0). Example: `[{\"amount\": 10.0, \"time_from_t0\": 0.5}]`."
        )
    with col_cf2:
        costs_json = st.text_area(
            "Costs [JSON]:",
            value='[{"amount": 1.0, "time_from_t0": 0.5}]',
            height=100,
            help="Enter discrete costs (e.g., storage) as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from t=0). Example: `[{\"amount\": 5.0, \"time_from_t0\": 0.75}]`."
        )

    position_type = st.radio(
        "Position Type for MTM Valuation:",
        ('long', 'short'),
        help="Select the position type for MTM valuation."
    )

    st.divider()

    # Input Validation
    if t_current > T:
        st.error("Error: Current Time (t) cannot be greater than Maturity (T). Please adjust the inputs.")
        st.stop()
    if S0 <= 0 or St <= 0:
        st.error("Error: Spot prices ($S_0$, $S_t$) must be positive.")
        st.stop()
    if r < 0:
        st.error("Error: Risk-Free Rate ($r$) cannot be negative.")
        st.stop()


    # Parse cash flows
    dividends = parse_cash_flows(dividends_json)
    costs = parse_cash_flows(costs_json)

    if not dividends and dividends_json.strip():
        st.warning("Could not parse dividends JSON. Using empty list.")
    if not costs and costs_json.strip():
        st.warning("Could not parse costs JSON. Using empty list.")

    # Calculations
    F0_T_with_cb = calculate_forward_price_at_inception(S0, T, r, dividends, costs)
    F0_T_without_cb = calculate_forward_price_at_inception(S0, T, r, [], []) # For comparison

    Vt_T_long = calculate_mtm_value(St, T, t_current, r, F0_T_with_cb, dividends, costs)
    Vt_T_short = -Vt_T_long if position_type == 'short' else Vt_T_long # MTM for short position

    st.subheader("Calculated Outputs")
    col_metrics1, col_metrics2 = st.columns(2)
    with col_metrics1:
        st.metric(label="Forward Price at Inception ($F_0(T)$) (with C/B)", value=f"{F0_T_with_cb:,.2f}")
    with col_metrics2:
        st.metric(label="Forward Price at Inception ($F_0(T)$) (without C/B)", value=f"{F0_T_without_cb:,.2f}")

    mtm_label = f"MTM Value at Current Time ($V_t(T)$) ({position_type.capitalize()} Position)"
    st.metric(label=mtm_label, value=f"{Vt_T_short:,.2f}") # Use Vt_T_short which is already adjusted for position_type

    st.divider()

    st.subheader("Visualizations")

    # --- 1. MTM Value Evolution Over Time (Long Position) ---
    st.markdown("#### MTM Value Evolution Over Time (Long Position)")
    num_points = 100
    time_points = np.linspace(0, T, num_points)
    mtm_values_with_cb = []
    mtm_values_without_cb = []

    # Original F0_T (needed for comparison)
    original_F0_T_with_cb = calculate_forward_price_at_inception(S0, T, r, dividends, costs)
    original_F0_T_without_cb = calculate_forward_price_at_inception(S0, T, r, [], [])

    # Simulate spot price evolution for visualization - simple linear path for demonstration
    # This is a simplification; in reality, spot price follows a stochastic process.
    # For a more realistic simulation, one might use a Geometric Brownian Motion.
    # For this lab, we'll assume a linear path from S0 to St, then a constant or similar
    # or just use the current spot price as a reference point for the plot.
    # For simplicity, let's assume a linear path from S0 to an estimated ST at maturity if no new info.
    # Or, perhaps more directly, assume St remains constant or linearly moves to some target.
    # For robust MTM evolution, let's make St scale from S0 to a hypothetical S_T that implies
    # a reasonable (e.g., no arbitrage) forward path without new information.
    # A simplified approach for visualization: linearly interpolate spot price from S0 to S_T_expected at T
    # where S_T_expected = F0_T_with_cb for consistency.

    # Option 1: Simple linear interpolation from S0 to a point that makes MTM 0 at T if no new information
    # This might not be intuitive.
    # Option 2: Assume S_t_simulated remains constant at S0 or some other base.
    # Option 3: For the purpose of *evolution*, we need a dynamic S_t. Let's make S_t follow a simple trend.
    # For a true MTM plot over time, we need a time-series of S_t.
    # Let's simplify: for the plot, we assume S_t linearly moves from S0 at t=0 to some value at T.
    # A simple assumption: S_t evolves such that if it tracks the forward curve without new info, MTM stays 0.
    # However, the task requests MTM value evolution over time where S_t is an input.
    # Let's generate a hypothetical S_t path for the plot.
    # A reasonable hypothetical path for S_t could be S_t = S0 * (1 + r)^t (ignoring dividends/costs for this sim path)
    # or just a straight line from S0 to some value that makes sense at T, e.g. F0_T_with_cb.
    
    # For a clear MTM evolution, we usually plot MTM(t) assuming S_t is the *actual* spot price at time t.
    # To make a smooth curve, we'll interpolate St from S0 at t=0 to a value at T (e.g., F0_T_with_cb)
    # This is still a simplification, but allows for a plot.
    
    # Let's assume S_t increases linearly from S0 to a value of (S0 + F0_T_with_cb)/2 * (T_sim_end/T) for the plot.
    # This is not ideal but provides a changing S_t for the plot.
    # A better way for MTM EVOLUTION plot: Plot MTM(t) for varying 't' assuming S_t follows *some* path.
    # The simplest path that demonstrates MTM is where S_t tracks F_t.
    
    # Let's try: S_t = S0 * (1 + r)^t (simplified no-arbitrage spot path without CFs) for the plot
    # Or simply: S_t remains constant for plot purpose
    # To show MTM evolution, we need S_t to change.
    # A good illustrative S_t path could be (S_current_at_t_input - S0) / t_current * time_point + S0 for t < t_current
    # and then linearly to a final value. This is getting complex.
    
    # Let's simplify the MTM evolution plot for now:
    # MTM is calculated at each time_point (x-axis).
    # What should be S_t for the plot?
    # Option 1: Assume S_t grows at risk-free rate from S0 (S_t_plot = S0 * (1+r)**time_point)
    # Option 2: Assume S_t is constant for the plot (S_t_plot = St)
    # Option 3: Use the provided St as the anchor for t_current and interpolate S_t for other points.
    
    # For a *simulated* evolution, Option 1 is common.
    # Let's go with a simulated S_t that starts at S0 and reaches St at t_current, then continues linearly to T
    # Or, simpler: let's assume S_t increases linearly from S0 to S_T_expected (F0_T_with_cb) for the plot.

    # Simulating spot price for MTM evolution plot
    # Let's use a very simple linear interpolation for S_t_plot from S0 to some arbitrary ending price, e.g., S0*1.1 at T.
    # This will just illustrate the curve, not represent actual market movements.
    
    S_T_plot_end_value = F0_T_with_cb # A reasonable end point for S_t if no new info
    S_t_for_plot = np.linspace(S0, S_T_plot_end_value, num_points)

    for i, t_val in enumerate(time_points):
        # Using the interpolated S_t_for_plot
        current_S_t_for_plot = S_t_for_plot[i]
        
        # Recalculate F0_T_with_cb for current S0 (if S0 was changing along with t_val)
        # But F0_T is fixed at inception. So use the already calculated F0_T_with_cb.
        
        mtm_val_with = calculate_mtm_value(current_S_t_for_plot, T, t_val, r, F0_T_with_cb, dividends, costs)
        mtm_values_with_cb.append(mtm_val_with)
        
        mtm_val_without = calculate_mtm_value(current_S_t_for_plot, T, t_val, r, F0_T_without_cb, [], [])
        mtm_values_without_cb.append(mtm_val_without)

    df_mtm_evolution = pd.DataFrame({
        'Time (Years)': time_points,
        'MTM Value (with C/B)': mtm_values_with_cb,
        'MTM Value (without C/B)': mtm_values_without_cb
    })

    fig_mtm_evolution = go.Figure()
    fig_mtm_evolution.add_trace(go.Scatter(x=df_mtm_evolution['Time (Years)'], y=df_mtm_evolution['MTM Value (with C/B)'],
                                           mode='lines', name='MTM Value (with C/B)'))
    fig_mtm_evolution.add_trace(go.Scatter(x=df_mtm_evolution['Time (Years)'], y=df_mtm_evolution['MTM Value (without C/B)'],
                                           mode='lines', name='MTM Value (without C/B)'))

    # Add vertical line for current time
    fig_mtm_evolution.add_vline(x=t_current, line_dash="dash", line_color="grey", annotation_text=f"Current Time (t={t_current:.2f})")
    # Add horizontal line for Y=0
    fig_mtm_evolution.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even (Y=0)")

    fig_mtm_evolution.update_layout(
        title='MTM Value Evolution Over Time (Long Position)',
        xaxis_title='Time (Years)',
        yaxis_title='MTM Value',
        hovermode="x unified",
        legend_title_text='Scenario'
    )
    st.plotly_chart(fig_mtm_evolution, use_container_width=True)

    # --- 2. Sensitivity of Forward Price to Costs/Benefits Magnitude ---
    st.markdown("#### Sensitivity of Forward Price to Costs/Benefits Magnitude")
    multipliers = np.linspace(0, 2, 21) # From 0x to 2x original amount

    f0_sensitivity_costs = []
    f0_sensitivity_dividends = []

    # Original PV of costs/benefits
    original_pv_costs = calculate_present_value(costs, r, 0, T)
    original_pv_dividends = calculate_present_value(dividends, r, 0, T)

    for mult in multipliers:
        # Sensitivity to Costs
        temp_costs_for_sensitivity = [{"amount": cf["amount"] * mult, "time_from_t0": cf["time_from_t0"]} for cf in costs]
        f0_costs = calculate_forward_price_at_inception(S0, T, r, dividends, temp_costs_for_sensitivity)
        f0_sensitivity_costs.append(f0_costs)

        # Sensitivity to Dividends
        temp_dividends_for_sensitivity = [{"amount": cf["amount"] * mult, "time_from_t0": cf["time_from_t0"]} for cf in dividends]
        f0_dividends = calculate_forward_price_at_inception(S0, T, r, temp_dividends_for_sensitivity, costs)
        f0_sensitivity_dividends.append(f0_dividends)

    df_sensitivity = pd.DataFrame({
        'Multiplier': multipliers,
        'Forward Price (Costs Multiplied)': f0_sensitivity_costs,
        'Forward Price (Dividends Multiplied)': f0_sensitivity_dividends
    })

    fig_sensitivity = go.Figure()
    fig_sensitivity.add_trace(go.Scatter(x=df_sensitivity['Multiplier'], y=df_sensitivity['Forward Price (Costs Multiplied)'],
                                        mode='lines', name='F0(T) vs. Costs Multiplier'))
    fig_sensitivity.add_trace(go.Scatter(x=df_sensitivity['Multiplier'], y=df_sensitivity['Forward Price (Dividends Multiplied)'],
                                        mode='lines', name='F0(T) vs. Dividends Multiplier'))

    fig_sensitivity.update_layout(
        title='Sensitivity of Forward Price to Costs/Benefits Magnitude',
        xaxis_title='Multiplier of Original Costs/Benefits',
        yaxis_title='Forward Price ($F_0(T)$)',
        hovermode="x unified",
        legend_title_text='Factor'
    )
    st.plotly_chart(fig_sensitivity, use_container_width=True)

    # --- 3. Aggregated Comparison Plot (MTM Value Across Scenarios) ---
    st.markdown("#### MTM Value Comparison Across Scenarios (Long Position)")

    # Define scenarios
    scenarios = {
        'Base Case (with C/B)': {
            'dividends': dividends,
            'costs': costs
        },
        'No Costs/Benefits': {
            'dividends': [],
            'costs': []
        },
        'Double Dividends': {
            'dividends': [{"amount": cf["amount"] * 2, "time_from_t0": cf["time_from_t0"]} for cf in dividends],
            'costs': costs
        },
        'Double Costs': {
            'dividends': dividends,
            'costs': [{"amount": cf["amount"] * 2, "time_from_t0": cf["time_from_t0"]} for cf in costs]
        }
    }

    scenario_mtm_values = []
    scenario_names = []

    for name, params in scenarios.items():
        # Need to recalculate F0_T for each scenario based on *its* cash flows
        # Then calculate MTM using that F0_T.
        
        scenario_F0_T = calculate_forward_price_at_inception(S0, T, r, params['dividends'], params['costs'])
        mtm_val = calculate_mtm_value(St, T, t_current, r, scenario_F0_T, params['dividends'], params['costs'])
        
        # If the displayed MTM is for the selected position_type, apply it here
        if position_type == 'short':
            mtm_val = -mtm_val
            
        scenario_mtm_values.append(mtm_val)
        scenario_names.append(name)

    df_scenario_comparison = pd.DataFrame({
        'Scenario': scenario_names,
        'MTM Value': scenario_mtm_values
    })

    fig_scenario_comparison = px.bar(
        df_scenario_comparison,
        x='Scenario',
        y='MTM Value',
        title=f'MTM Value Comparison Across Scenarios ({position_type.capitalize()} Position)',
        labels={'MTM Value': 'MTM Value ($)'},
        text='MTM Value'
    )
    fig_scenario_comparison.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    fig_scenario_comparison.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_scenario_comparison, use_container_width=True)
