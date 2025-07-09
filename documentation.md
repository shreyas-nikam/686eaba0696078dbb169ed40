id: 686eaba0696078dbb169ed40_documentation
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Developing an FX Forward Mark-to-Market Analyzer with Streamlit

## 1. Introduction: Understanding FX Forwards and MTM
Duration: 00:05:00

Foreign Exchange (FX) forward contracts are crucial financial instruments used by businesses and investors to hedge against currency risk or to speculate on future currency movements. An FX forward is an agreement to exchange a specified amount of one currency for another at a pre-determined rate (the forward rate) on a future date. Unlike spot transactions, the exchange does not happen immediately but at maturity.

As time passes and market conditions change (e.g., spot rates, interest rates), the value of an existing FX forward contract also changes. This change in value, representing the hypothetical profit or loss if the contract were to be closed out or revalued at current market conditions, is known as **Mark-to-Market (MTM)**. Understanding MTM is vital for risk management, accounting, and capital allocation for financial institutions and corporations engaged in international trade.

<aside class="positive">
<b>Why is MTM important for developers?</b> While finance professionals use these tools, developers build them. Understanding the underlying financial concepts allows you to create more robust, accurate, and user-friendly applications that meet the specific needs of financial analysis and trading desks. This codelab bridges that gap.
</aside>

This codelab will guide you through building and understanding a Streamlit application that analyzes the Mark-to-Market (MTM) value of a Foreign Exchange (FX) forward contract. You will learn:

*   The core concepts of FX forward pricing.
*   How MTM is calculated for an FX forward.
*   The key market parameters influencing MTM.
*   How to use Streamlit to create interactive web applications for financial analysis.
*   How to visualize the sensitivity of MTM to various market parameters.

**Key Concepts Explained:**

*   **Spot Rate ($S_{t,f/d}$):** The exchange rate for immediate delivery of a currency. $f/d$ denotes foreign currency per domestic currency. However, in our application, we consider $S_{f/d}$ as the number of units of domestic currency for one unit of foreign currency (e.g., USD/EUR means how many USD per 1 EUR).
*   **Forward Rate ($F_{0,f/d}(T)$):** The exchange rate agreed today for a currency exchange on a future date $T$.
*   **Risk-Free Rates ($r_f$, $r_d$):** The interest rates of the foreign ($r_f$) and domestic ($r_d$) currencies, typically derived from government bond yields or interbank lending rates, assumed to be risk-free.
*   **Time to Maturity ($T$):** The total time in years from the contract's inception to its expiration.
*   **Current Time ($t$):** The time elapsed in years since the contract's inception.
*   **Mark-to-Market (MTM):** The current value of an asset or liability based on current market prices. For an FX forward, it's the present value of the difference between the current spot rate and the discounted original forward rate.

## 2. Application Architecture and Flow
Duration: 00:07:00

The Streamlit application is designed as a single-page interactive tool. Its architecture is straightforward, following a typical data flow for analytical applications:

1.  **User Input:** The application gathers various parameters for the FX forward contract (initial spot rate, initial interest rates, contract maturity) and current market conditions (current time, current spot rate, current interest rates) via Streamlit's sidebar widgets.
2.  **Calculations:**
    *   First, it calculates the **initial FX Forward Price** based on the parameters at inception ($t=0$).
    *   Second, using the initial forward price and current market parameters, it calculates the **Mark-to-Market (MTM) value** of the contract.
3.  **Display Results:** The calculated initial forward price and the current MTM values (for both long and short positions) are displayed prominently in the main area of the application.
4.  **Interactive Visualizations:** Two interactive Plotly graphs are generated to illustrate the sensitivity of the MTM value to:
    *   Changes in the **interest rate differential** ($r_f - r_d$).
    *   Changes in the **current spot FX rate** ($S_{t,f/d}$).

**Conceptual Flow:**

```
++
|   User Input        |
| - Initial Spot (S0) |
| - Maturity (T)      |
| - Initial Rates     |
| - Current Time (t)  |
| - Current Spot (St) |
| - Current Rates     |
++--+
          |
          v
++
|   Core Calculations |
| - Calculate F0      |
| - Calculate MTM     |
++--+
          |
          v
++
|   Output Display    |
| - F0 Value          |
| - MTM Value (Long)  |
| - MTM Value (Short) |
++--+
          |
          v
++    ++
|   Visualization 1   |<+   Visualization 2   |
| (MTM vs. IR Diff)   |    | (MTM vs. Spot Rate) |
++    ++
```

## 3. Core Financial Formulas
Duration: 00:10:00

The application's core lies in two fundamental financial formulas: one for calculating the FX Forward Price and another for determining its Mark-to-Market (MTM) value.

### FX Forward Price at Inception ($t=0$)

The no-arbitrage FX forward price is determined by the spot rate and the risk-free interest rates of the two currencies involved. It reflects the interest rate parity theorem.

The formula used is:
$$F_{0,f/d}(T) = S_{0,f/d}e^{(r_{f,initial} - r_{d,initial})T}$$

Where:
*   $F_{0,f/d}(T)$: The FX forward price at time $t=0$ for maturity $T$.
*   $S_{0,f/d}$: The spot FX rate at time $t=0$ (units of domestic currency per one unit of foreign currency).
*   $e$: The base of the natural logarithm (approximately 2.71828).
*   $r_{f,initial}$: The risk-free interest rate of the foreign currency at time $t=0$.
*   $r_{d,initial}$: The risk-free interest rate of the domestic currency at time $t=0$.
*   $T$: The total time to maturity of the contract in years.

In Python, this is implemented by the `calculate_fx_forward_price` function:

```python
def calculate_fx_forward_price(S0_f_d, rf_initial, rd_initial, T):
    """Calculates the FX Forward Price at inception (t=0)."""
    return S0_f_d * exp((rf_initial - rd_initial) * T)
```

### Mark-to-Market (MTM) Value for a Long FX Forward Position

The MTM value ($V_t(T)$) at any time $t$ before maturity $T$ reflects the difference between the current spot rate and the *present value* of the original forward rate, discounted at the *current* market rates for the *remaining* maturity.

The formula used for a long position (buying foreign currency) is:
$$V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_{f,current} - r_{d,current})(T - t)}$$

Where:
*   $V_t^{long}(T)$: The Mark-to-Market value for a long position at current time $t$.
*   $S_{t,f/d}$: The current spot FX rate at time $t$.
*   $F_{0,f/d}(T)$: The original FX forward price agreed at $t=0$.
*   $e$: The base of the natural logarithm.
*   $r_{f,current}$: The current risk-free interest rate of the foreign currency at time $t$.
*   $r_{d,current}$: The current risk-free interest rate of the domestic currency at time $t$.
*   $T$: The total time to maturity from inception.
*   $t$: The current time elapsed from inception.
*   $(T-t)$: The remaining time to maturity.

<aside class="negative">
It is crucial to note that the discount factor in the MTM formula uses *current* interest rates ($r_{f,current}$, $r_{d,current}$) and the *remaining* time to maturity ($T-t$), as these are the relevant rates and time period for valuing the future cash flow at time $t$.
</aside>

In Python, this is implemented by the `calculate_mtm` function:

```python
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
```

## 4. Setting Up Your Environment
Duration: 00:03:00

Before running the Streamlit application, you need to set up your Python environment.

### Step 4.1: Install Dependencies

Open your terminal or command prompt and install the necessary Python libraries:

```console
pip install streamlit numpy plotly
```

### Step 4.2: Save the Application Code

Create a new Python file named `main_page.py` and paste the entire code provided in the problem description into this file.

<button>
  [Download main_page.py](link_to_gist_or_repo_if_available_otherwise_ignore_this_button_and_tell_user_to_copy_paste)
</button>

```python
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

    #  Currency Pair Selection for Pre-filling 
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

    #  Input Widgets in Sidebar 
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

    #  Calculations 
    F0_f_d = calculate_fx_forward_price(S0_f_d, rf_initial, rd_initial, T)
    Vt_long = calculate_mtm(St_f_d, F0_f_d, rf_current, rd_current, T, t)
    Vt_short = -Vt_long

    st.subheader("2. Calculated Values")
    st.markdown(f"**FX Forward Price at Inception ($F_{{0,f/d}}(T)$):**\n"
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

    #  Plot 1: Interest Rate Differential Impact 
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

    #  Plot 2: Spot Rate Change Impact 
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

```

### Step 4.3: Run the Application

Navigate to the directory where you saved `main_page.py` in your terminal and run the Streamlit command:

```console
streamlit run main_page.py
```

This command will open a new tab in your web browser displaying the Streamlit application.

## 5. Exploring the Application: Contract Setup and Parameters
Duration: 00:08:00

Once the application is running, you'll see a main display area and a sidebar on the left. The sidebar is where you input all the contract and market parameters.

### Step 5.1: Select Currency Pair Defaults

At the top of the sidebar, you'll find a dropdown labeled **"Select Currency Pair (Pre-fill Rates)"**.

*   **Custom**: Allows you to set all parameters manually.
*   **USD/EUR (Example)**: Pre-fills values typical for a EUR/USD pair (where EUR is foreign, USD is domestic). For example, a value of 1.08 means 1 EUR = 1.08 USD. Note: $r_d$ will be the USD rate, $r_f$ the EUR rate.
*   **ZAR/EUR (Example)**: Pre-fills values for a EUR/ZAR pair. For example, 19.0 means 1 EUR = 19.0 ZAR. Note: $r_d$ will be the ZAR rate, $r_f$ the EUR rate.

<aside class="positive">
Experiment with these pre-set options to quickly grasp the impact of different interest rate differentials and spot rates without manual input.
</aside>

### Step 5.2: Set Initial Contract Parameters ($t=0$)

This section defines the terms of the FX forward contract at the moment it was initiated.

*   **Initial Spot FX Rate ($S_{0,f/d}$)**: This is the prevailing spot rate when the contract was entered. Adjust this to see how the initial forward price is affected.
*   **Original Contract Maturity ($T$)**: The total duration of the forward contract in years. This influences both the initial forward price and the remaining time for MTM calculations.
*   **Foreign Risk-Free Rate at Inception ($r_{f,initial}$)**: The risk-free interest rate for the foreign currency at contract inception.
*   **Domestic Risk-Free Rate at Inception ($r_{d,initial}$)**: The risk-free interest rate for the domestic currency at contract inception.

### Step 5.3: Set Current Market Parameters ($t$)

This section reflects the current market conditions at which the contract is being revalued.

*   **Current Time ($t$)**: This slider represents how much time has passed since the contract's inception. As you increase $t$, the remaining maturity ($T-t$) decreases, bringing the contract closer to expiration.
*   **Current Spot FX Rate ($S_{t,f/d}$)**: The current prevailing spot rate in the market. This is often the most significant driver of MTM changes.
*   **Current Foreign Risk-Free Rate ($r_{f,current}$)**: The current risk-free interest rate for the foreign currency. This might have changed since inception.
*   **Current Domestic Risk-Free Rate ($r_{d,current}$)**: The current risk-free interest rate for the domestic currency. This also might have changed since inception.

<aside class="positive">
Observe how the `Max` value for "Current Time ($t$)" dynamically adjusts to match the "Original Contract Maturity ($T$)". This ensures you don't set a current time beyond the contract's maturity.
</aside>

## 6. Exploring the Application: Calculated Values and Visualizations
Duration: 00:10:00

As you adjust the parameters in the sidebar, the main section of the application updates in real-time, displaying the calculated values and interactive plots.

### Step 6.1: Analyze Calculated Values

The "Calculated Values" section provides the key numerical outputs:

*   **FX Forward Price at Inception ($F_{0,f/d}(T)$)**: This is the rate agreed upon when the contract was initiated. It's calculated once at the beginning based on initial parameters.
    *   **Try This:** Increase $r_{f,initial}$ relative to $r_{d,initial}$ (or vice versa) and observe how $F_{0,f/d}(T)$ changes. A higher foreign rate (relative to domestic) typically leads to a higher forward price if $S_{0,f/d}$ is domestic/foreign.
*   **Current Mark-to-Market (MTM) Value**: This is broken down into:
    *   **Long Position MTM ($V_t^{long}(T)$)**: What a buyer of the foreign currency would gain or lose.
    *   **Short Position MTM ($V_t^{short}(T)$)**: What a seller of the foreign currency would gain or lose (which is simply the negative of the long position MTM).
    *   **Try This:** Set $t=0$. The MTM should ideally be close to zero (ignoring transaction costs), as no time has passed for market conditions to change relative to the initial contract.

### Step 6.2: Interpret Interactive Visualizations

The "Interactive Visualizations" section presents two Plotly graphs that help you understand the sensitivity of the MTM value to changes in key market drivers.

#### MTM Value vs. Interest Rate Differential ($r_f - r_d$)

This plot shows how the MTM changes if the current foreign risk-free rate ($r_{f,current}$) varies, keeping all other parameters (including $r_{d,current}$) constant.

*   **Understanding the Plot:**
    *   The X-axis represents the interest rate differential ($r_f - r_d$).
    *   The Y-axis represents the MTM value for both long and short positions.
    *   A red star marker indicates the current MTM value based on your sidebar inputs.
    *   A dashed grey line at Y=0 represents zero MTM.
*   **Try This:**
    1.  Keep the "Current Spot FX Rate ($S_{t,f/d}$)" slider fixed.
    2.  Adjust the "Current Foreign Risk-Free Rate ($r_{f,current}$)" in the sidebar. Observe how the red marker moves along the curve, showing the MTM's sensitivity to this rate.
    3.  Consider the slope: A steep slope indicates high sensitivity, meaning small changes in interest rates can lead to large MTM fluctuations.

#### MTM Value vs. Current Spot FX Rate ($S_t$)

This plot illustrates the sensitivity of the MTM value to changes in the current spot FX rate ($S_{t,f/d}$), holding all other parameters constant. This is typically the most significant driver of MTM.

*   **Understanding the Plot:**
    *   The X-axis represents the current spot rate ($S_t$).
    *   The Y-axis represents the MTM value for both long and short positions.
    *   A dashed purple vertical line marks the initial FX forward price ($F_{0,f/d}(T)$).
    *   A solid red vertical line indicates the current spot rate ($S_{t,f/d}$) from your sidebar input.
    *   A dashed grey line at Y=0 represents zero MTM.
*   **Try This:**
    1.  Adjust the "Current Spot FX Rate ($S_{t,f/d}$)" slider in the sidebar.
    2.  Observe how the solid red line (current spot) moves. The MTM changes linearly with the current spot rate.
    3.  Notice that for a long position, MTM is positive when $S_t$ is higher than the discounted original forward rate (the rate where the MTM crosses zero for the long position). It's negative when $S_t$ is lower. The opposite holds for a short position.

<aside class="positive">
<b>Key Insight:</b> For an FX forward, a long position benefits when the spot rate at time $t$ has moved *above* the effective forward rate, while a short position benefits when it moves *below* it. This is why spot rate changes are often the primary driver of MTM.
</aside>

## 7. Understanding the Application's Source Code
Duration: 00:12:00

Let's break down the `main_page.py` code to understand how Streamlit is used to create this interactive application and connect it with the financial calculations.

The code is structured into several logical sections:

### Section 7.1: Imports and Core Calculation Functions

```python
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
    return St_f_d - F0_f_d * exp(-(rf_current - rd_current) * remaining_maturity)
```
*   **`streamlit as st`**: The fundamental library for building the web application.
*   **`numpy as np`**: Used for numerical operations, especially `np.linspace` for generating ranges for plots.
*   **`plotly.graph_objects as go`**: For creating interactive and publication-quality plots.
*   **`from math import exp`**: Used for the exponential function $e^x$.
*   The `calculate_fx_forward_price` and `calculate_mtm` functions encapsulate the core financial logic, making the main Streamlit code cleaner and easier to read.

### Section 7.2: Streamlit Application Entry Point (`run_main_page`)

```python
def run_main_page():
    st.header("FX Forward Mark-to-Market (MTM) Analyzer")
    st.markdown("""...""") # Introduction text
    st.subheader("1. Contract Setup and Market Parameters")
```
*   The entire application logic resides within the `run_main_page()` function. Streamlit executes this function from top to bottom every time a user interacts with a widget.
*   `st.header`, `st.markdown`, `st.subheader` are used to structure the layout and add textual content.

### Section 7.3: Sidebar Input Widgets

```python
    st.sidebar.subheader("Currency Pair & Defaults")
    currency_pair = st.sidebar.selectbox(
        label="Select Currency Pair (Pre-fill Rates)", ...
    )
    defaults = { ... } # Dictionary defining default values
    selected_defaults = defaults[currency_pair]

    st.sidebar.subheader("Initial Contract Parameters ($t=0$)")
    S0_f_d = st.sidebar.number_input(...)
    T = st.sidebar.slider(...)
    rf_initial = st.sidebar.number_input(...)
    rd_initial = st.sidebar.number_input(...)

    st.sidebar.subheader("Current Market Parameters ($t$)")
    t = st.sidebar.slider(...)
    St_f_d = st.sidebar.number_input(...)
    rf_current = st.sidebar.number_input(...)
    rd_current = st.sidebar.number_input(...)
```
*   All input widgets (sliders, number inputs, select boxes) are prefixed with `st.sidebar.` to place them in the left sidebar.
*   Each widget takes a `label`, `min_value`, `max_value`, `value` (default), `step`, `format`, and `help` text.
*   The `currency_pair` select box dynamically updates the `selected_defaults` dictionary, which in turn sets the initial `value` for other input widgets. This provides a user-friendly way to pre-populate parameters.
*   Notice how `t`'s `max_value` is dynamically set to `T`, ensuring logical constraints. Similarly, `St_f_d`'s min/max values are dynamically adjusted around `S0_f_d`.

### Section 7.4: Performing Calculations

```python
    #  Calculations 
    F0_f_d = calculate_fx_forward_price(S0_f_d, rf_initial, rd_initial, T)
    Vt_long = calculate_mtm(St_f_d, F0_f_d, rf_current, rd_current, T, t)
    Vt_short = -Vt_long
```
*   After all inputs are collected, the two core functions (`calculate_fx_forward_price` and `calculate_mtm`) are called with the current input values.
*   `Vt_short` is simply derived as the negative of `Vt_long`.

### Section 7.5: Displaying Calculated Values

```python
    st.subheader("2. Calculated Values")
    st.markdown(f"**FX Forward Price at Inception ($F_{{0,f/d}}(T)$):**\n"
                f"The initial forward price... **{F0_f_d:.4f}**.")
    st.latex(r"F_{0,f/d}(T) = S_{0,f/d}e^{(r_{f,initial} - r_{d,initial})T}")

    st.markdown(f"**Current Mark-to-Market (MTM) Value:**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Long Position MTM ($V_t^{long}(T)$)", value=f"{Vt_long:.4f}")
    with col2:
        st.metric(label="Short Position MTM ($V_t^{short}(T)$)", value=f"{Vt_short:.4f}")
    st.latex(r"V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_{f,current} - r_{d,current})(T - t)}")
```
*   `st.subheader`, `st.markdown`, and `st.latex` are used to present the calculated values along with their corresponding formulas for clarity.
*   `st.columns(2)` creates two columns, allowing the long and short MTM metrics to be displayed side-by-side using `st.metric`.

### Section 7.6: Interactive Visualizations (Plotly)

```python
    st.subheader("3. Interactive Visualizations")
    # ... Plot 1: MTM vs. Interest Rate Differential ...
    rf_current_range = np.linspace(...)
    mtm_long_rates = [calculate_mtm(...) for r_f in rf_current_range]
    fig_rates = go.Figure()
    fig_rates.add_trace(go.Scatter(x=ir_differential, y=mtm_long_rates, mode='lines', name='Long Position'))
    # ... add other traces, layout, etc. ...
    st.plotly_chart(fig_rates, use_container_width=True)

    # ... Plot 2: MTM vs. Current Spot FX Rate ...
    spot_range = np.linspace(...)
    mtm_long_spot = [calculate_mtm(...) for s in spot_range]
    fig_spot = go.Figure()
    fig_spot.add_trace(go.Scatter(x=spot_range, y=mtm_long_spot, mode='lines', name='Long Position'))
    # ... add other traces, layout, etc. ...
    st.plotly_chart(fig_spot, use_container_width=True)
```
*   For each plot, a range of values (e.g., `rf_current_range`, `spot_range`) is generated using `np.linspace`.
*   The `calculate_mtm` function is called repeatedly for each value in the generated range to create the data points for the plot.
*   `go.Figure()` creates a new Plotly figure object.
*   `fig.add_trace(go.Scatter(...))` adds a line or scatter plot to the figure.
*   `fig.add_vline` and `fig.add_hline` add useful reference lines to the plots.
*   `fig.update_layout` customizes titles, axis labels, and other visual properties.
*   `st.plotly_chart(fig, use_container_width=True)` renders the Plotly figure in the Streamlit application, making it interactive (zoom, pan, hover).

### Section 7.7: References

```python
    st.subheader("4. References")
    st.markdown("""...""")
