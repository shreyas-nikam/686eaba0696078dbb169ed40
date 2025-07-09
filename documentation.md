id: 686eaba0696078dbb169ed40_documentation
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Building an FX Forward Mark-to-Market (MTM) Analyzer with Streamlit

## 1. Introduction to FX Forward MTM Analyzer
Duration: 00:05:00

Welcome to this codelab, where we will explore the **QuLab: Derivative Pricing and Valuation of Forward Contracts** application, specifically focusing on its **FX Forward Mark-to-Market (MTM) Analyzer** module. This interactive Streamlit application provides a hands-on approach to understanding the valuation dynamics of Foreign Exchange (FX) forward contracts.

<aside class="positive">
This codelab is designed to provide developers with a comprehensive understanding of the application's functionalities, underlying financial concepts, and its implementation using Streamlit and Python. By the end, you'll be able to run, understand, and potentially extend this powerful financial tool.
</aside>

### What is an FX Forward Contract?
An FX forward contract is a bilateral agreement to exchange a specified amount of one currency for another currency at a pre-determined exchange rate on a future date. The key characteristic is that the exchange rate is fixed at the contract's inception, irrespective of future market movements. These contracts are crucial for hedging currency risk in international trade and investment.

### Mark-to-Market (MTM) Valuation
Mark-to-Market (MTM) is the process of valuing an asset or liability based on its current market price. For an FX forward contract, the MTM value at any given time $t$ represents the theoretical profit or loss if the contract were to be closed out (offset by an opposing trade) at that exact moment. A positive MTM for a long position indicates a gain, while a negative value indicates a loss. The reverse applies to a short position. Understanding MTM is vital for risk management and financial reporting.

### Key Concepts Explored

This application helps visualize several fundamental concepts in financial derivatives:

*   **Initial Forward Price ($F_{0,f/d}(T)$):** This is the rate at which the contract is initially agreed upon. It's derived from the spot rate and the interest rate differential between the two currencies, adhering to the no-arbitrage principle.
*   **Interest Rate Parity:** This economic principle links spot and forward exchange rates with interest rates in different countries. The application implicitly demonstrates this by showing how interest rate differentials influence the forward price and subsequent MTM values.
*   **Impact of Market Changes:** Observe how MTM values of an existing contract fluctuate in response to changes in the current spot rate and current risk-free interest rates.
*   **Time Decay:** The remaining time to maturity ($T-t$) is a critical factor influencing the MTM value, particularly through the discounting component.

### Application Architecture

The application is structured into two main Python files:

1.  **`app.py`**: This is the main entry point for the Streamlit application. It sets up the page configuration, displays the main title, and handles navigation to different modules (currently only the FX Forward MTM Analyzer).
2.  **`application_pages/fx_forward_mtm_analyzer.py`**: This file contains the core logic and Streamlit UI components specifically for the FX Forward MTM Analyzer. It defines functions for calculating forward prices and MTM values and generates the interactive plots.

This modular design promotes readability and maintainability, making it easier to add more financial tools in the future.

### Business Logic and Formulas

The application calculates two primary values based on continuous compounding:

1.  **FX Forward Price (at inception, $t=0$):**
    This formula determines the rate at which the contract is set:
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
    Where:
    *   $F_{0,f/d}(T)$ is the forward price at time 0 for a contract maturing at time $T$.
    *   $S_{0,f/d}$ is the initial spot exchange rate (foreign currency per domestic currency).
    *   $r_f$ is the foreign risk-free interest rate at inception.
    *   $r_d$ is the domestic risk-free interest rate at inception.
    *   $T$ is the original time to maturity of the forward contract in years.
    *   $e$ is the base of the natural logarithm.

2.  **Mark-to-Market Value (at current time $t$):**
    This represents the current value of the contract.
    For a **long position** (agreement to buy foreign currency at maturity):
    $$V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$$
    For a **short position** (agreement to sell foreign currency at maturity):
    $$V_t^{short}(T) = -V_t^{long}(T)$$
    Where:
    *   $V_t(T)$ is the Mark-to-Market value at time $t$.
    *   $S_{t,f/d}$ is the current prevailing spot exchange rate at time $t$.
    *   $F_{0,f/d}(T)$ is the initial forward price calculated at $t=0$.
    *   $r_f$ is the current foreign risk-free interest rate.
    *   $r_d$ is the current domestic risk-free interest rate.
    *   $T$ is the original time to maturity.
    *   $t$ is the current time in years from the contract inception ($0 \le t \le T$).

By manipulating the input parameters in the application, you can observe these formulas in action and gain practical insights into derivative valuation.

## 2. Setting Up Your Development Environment
Duration: 00:03:00

To run this Streamlit application, you'll need Python installed on your system. We recommend Python 3.8 or newer.

### Prerequisites

*   Python (3.8+)
*   `pip` (Python package installer)

### Installation Steps

1.  **Install Streamlit and other dependencies**:
    Open your terminal or command prompt and run the following command:

    ```bash
    pip install streamlit numpy plotly
    ```
    *   `streamlit`: The framework for building interactive web applications.
    *   `numpy`: Essential for numerical operations, especially for generating ranges for plots.
    *   `plotly`: Used for creating interactive and high-quality plots within the Streamlit app.

2.  **Create the project directory structure**:
    Create a main directory for your project (e.g., `QuLab_FX_Analyzer`). Inside this, create another directory named `application_pages`.

    ```bash
    mkdir QuLab_FX_Analyzer
    cd QuLab_FX_Analyzer
    mkdir application_pages
    ```

3.  **Create the `app.py` file**:
    Inside the `QuLab_FX_Analyzer` directory, create a file named `app.py` and paste the provided code into it.

4.  **Create the `fx_forward_mtm_analyzer.py` file**:
    Inside the `application_pages` directory, create a file named `fx_forward_mtm_analyzer.py` and paste the provided code into it.

    Your directory structure should look like this:

    ```
    QuLab_FX_Analyzer/
    ├── app.py
    └── application_pages/
        └── fx_forward_mtm_analyzer.py
    ```

<aside class="positive">
Ensure your file names and directory structure exactly match the instructions, as Python's import system is case-sensitive and relies on correct paths.
</aside>

## 3. Understanding `app.py` - The Main Entry Point
Duration: 00:03:00

The `app.py` file serves as the main orchestrator for our Streamlit application. It's responsible for the overall page configuration, displaying the main title, and managing the navigation between different application modules.

Let's break down its components:

```python
import streamlit as st
import os

# Set basic page configuration: title and wide layout
st.set_page_config(page_title="QuLab: Derivative Pricing and Valuation of Forward Contracts", layout="wide")

# Display a logo in the sidebar
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()

# Main title of the application
st.title("QuLab: Derivative Pricing and Valuation of Forward Contracts")
st.divider()

# Introduction and conceptual explanation
st.markdown("""
### FX Forward Mark-to-Market (MTM) Analyzer
... (Detailed explanation of FX Forwards, MTM, Key Concepts, and Business Logic with formulas) ...
""")

# Ensure the 'application_pages' directory exists
if not os.path.exists("application_pages"):
    os.makedirs("application_pages")

# Sidebar navigation using a selectbox
page = st.sidebar.selectbox(label="Navigation", options=["FX Forward MTM Analyzer"])

# Conditional loading and running of the selected page
if page == "FX Forward MTM Analyzer":
    # Dynamic import of the specific analyzer module
    from application_pages.fx_forward_mtm_analyzer import run_fx_forward_mtm_analyzer
    # Execute the main function of the analyzer
    run_fx_forward_mtm_analyzer()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
```

### Key Elements of `app.py`:

*   **`st.set_page_config()`**: Configures the browser tab title and sets the page layout to `wide`, utilizing more screen space.
*   **`st.sidebar.image()` and `st.sidebar.divider()`**: Adds visual branding and separation in the sidebar.
*   **`st.title()` and `st.markdown()`**: Displays the main application title and extensive introductory text, including detailed explanations of financial concepts and formulas. This provides crucial context to the user before they interact with the analysis tools.
*   **`os.makedirs("application_pages")`**: A safeguard to ensure the `application_pages` directory exists before attempting to import modules from it.
*   **`st.sidebar.selectbox()`**: Creates a navigation dropdown in the sidebar. Currently, it only has one option, "FX Forward MTM Analyzer", but this structure allows for easy expansion with more modules.
*   **`from application_pages.fx_forward_mtm_analyzer import run_fx_forward_mtm_analyzer`**: This is a dynamic import statement. When "FX Forward MTM Analyzer" is selected, the `run_fx_forward_mtm_analyzer` function from the corresponding file is imported.
*   **`run_fx_forward_mtm_analyzer()`**: Calls the main function of the selected module, which then renders its specific UI and performs calculations.
*   **Footer**: Includes copyright information and a disclaimer, which is important for financial applications.

This file acts as a simple router, directing control to the appropriate module based on user selection, making the application modular and scalable.

## 4. Deep Dive into `fx_forward_mtm_analyzer.py` - Core Logic
Duration: 00:15:00

This file contains the heart of the FX Forward MTM Analyzer, encompassing the financial calculations, user interface elements, and data visualization.

```python
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import exp

# Function to calculate initial forward price
def calculate_forward_price(S0, rf, rd, T):
    """Calculates the FX Forward Price at inception (t=0)."""
    return S0 * exp((rf - rd) * T)

# Function to calculate MTM for a long position
def calculate_mtm_long(St, F0T, rf_current, rd_current, T, t):
    """Calculates the Mark-to-Market value for a long FX forward position at time t."""
    time_to_maturity_remaining = max(0.0, T - t)
    return St - F0T * exp(-(rf_current - rd_current) * time_to_maturity_remaining)

# Main function for the analyzer module
def run_fx_forward_mtm_analyzer():
    st.header("FX Forward MTM Analyzer")

    st.markdown("""
    Use the controls in the sidebar to define your FX Forward contract and analyze its Mark-to-Market (MTM) value under various market conditions.
    """)

    st.sidebar.header("1. Initial Contract Parameters (t=0)")

    # Dictionary to pre-fill rates for common currency pairs
    currency_pairs = {
        "Custom": {},
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

    # Sidebar selectbox for currency pair selection
    selected_pair_label = st.sidebar.selectbox(
        label="Select Currency Pair (Pre-fill Rates)",
        options=list(currency_pairs.keys()),
        help="Choose a synthetic currency pair to pre-populate typical spot rates and interest rate differentials. You can then adjust rates manually."
    )

    # Session state to manage and persist input values across re-runs
    if "s0_value" not in st.session_state: st.session_state.s0_value = 1.08 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 1.0
    if "T_value" not in st.session_state: st.session_state.T_value = 1.0
    if "rf_initial_value" not in st.session_state: st.session_state.rf_initial_value = 0.035 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0
    if "rd_initial_value" not in st.session_state: st.session_state.rd_initial_value = 0.05 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0
    if "t_value" not in st.session_state: st.session_state.t_value = 0.0
    if "st_value" not in st.session_state: st.session_state.st_value = 1.08 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 1.0
    if "rf_current_value" not in st.session_state: st.session_state.rf_current_value = 0.03 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0
    if "rd_current_value" not in st.session_state: st.session_state.rd_current_value = 0.045 if selected_pair_label == "USD/EUR (Domestic=USD, Foreign=EUR)" else 0.0

    # Logic to pre-fill values based on selected currency pair
    if selected_pair_label != "Custom" and selected_pair_label in currency_pairs:
        prefill_data = currency_pairs[selected_pair_label]
        st.session_state.s0_value = prefill_data.get("S0_f_d", st.session_state.s0_value)
        st.session_state.rf_initial_value = prefill_data.get("rf_initial", st.session_state.rf_initial_value)
        st.session_state.rd_initial_value = prefill_data.get("rd_initial", st.session_state.rd_initial_value)
        st.session_state.st_value = prefill_data.get("St_f_d", prefill_data["S0_f_d"])
        st.session_state.rf_current_value = prefill_data.get("rf_current", st.session_state.rf_current_value)
        st.session_state.rd_current_value = prefill_data.get("rd_current", st.session_state.rd_current_value)

    # Input widgets for initial contract parameters (in sidebar)
    S0_f_d = st.sidebar.number_input(label="Initial Spot FX Rate ($S_{0,f/d}$)", min_value=0.1, max_value=100.0, value=st.session_state.s0_value, step=0.01, format="%.4f", help="...")
    T_maturity = st.sidebar.slider(label="Original Contract Maturity ($T$)", min_value=0.1, max_value=5.0, value=st.session_state.T_value, step=0.1, help="...")
    rf_initial = st.sidebar.number_input(label="Foreign Risk-Free Rate at Inception ($r_{f,initial}$)", min_value=-0.05, max_value=0.20, value=st.session_state.rf_initial_value, step=0.001, format="%.4f", help="...")
    rd_initial = st.sidebar.number_input(label="Domestic Risk-Free Rate at Inception ($r_{d,initial}$)", min_value=-0.05, max_value=0.20, value=st.session_state.rd_initial_value, step=0.001, format="%.4f", help="...")

    st.sidebar.header("2. Current Market Parameters (at time t)")

    # Input widgets for current market parameters (in sidebar)
    t_current = st.sidebar.slider(label="Current Time ($t$)", min_value=0.0, max_value=T_maturity, value=st.session_state.t_value, step=0.01, help=f"...")
    spot_range_min = S0_f_d * 0.9
    spot_range_max = S0_f_d * 1.1
    St_f_d = st.sidebar.number_input(label="Current Spot FX Rate ($S_{t,f/d}$)", min_value=spot_range_min, max_value=spot_range_max, value=st.session_state.st_value, step=0.01, format="%.4f", help=f"...")
    rf_current = st.sidebar.number_input(label="Current Foreign Risk-Free Rate ($r_{f,current}$)", min_value=-0.05, max_value=0.20, value=st.session_state.rf_current_value, step=0.001, format="%.4f", help="...")
    rd_current = st.sidebar.number_input(label="Current Domestic Risk-Free Rate ($r_{d,current}$)", min_value=-0.05, max_value=0.20, value=st.session_state.rd_current_value, step=0.001, format="%.4f", help="...")

    # Input Validation
    if t_current > T_maturity:
        st.error("Error: Current Time (t) cannot be greater than Original Contract Maturity (T). Please adjust the slider.")
        st.stop()

    # Calculations based on user inputs
    F0T = calculate_forward_price(S0_f_d, rf_initial, rd_initial, T_maturity)
    Vt_long = calculate_mtm_long(St_f_d, F0T, rf_current, rd_current, T_maturity, t_current)
    Vt_short = -Vt_long

    # Display calculated values
    st.subheader("Calculated Values")
    st.markdown(f"**Initial FX Forward Price ($F_{{0,f/d}}(T)$):** `{F0T:.4f}`")
    st.markdown(f"**Current MTM Value (Long Position, $V_t^{{long}}(T)$):** `{Vt_long:.4f}`")
    st.markdown(f"**Current MTM Value (Short Position, $V_t^{{short}}(T)$):** `{Vt_short:.4f}`")

    # Interpretation of MTM values
    st.markdown("""
    ### Interpretation of MTM Values
    *   A **positive MTM** for a **long position** means the contract has gained value since inception, indicating a theoretical profit if closed out today.
    *   A **negative MTM** for a **long position** means the contract has lost value, indicating a theoretical loss.
    *   For a **short position**, the interpretation is reversed: a positive MTM means a loss, and a negative MTM means a gain.
    """)

    st.subheader("Interactive Plots")

    # Plot 1: MTM vs. Interest Rate Differential
    st.markdown("#### MTM Value vs. Interest Rate Differential ($r_f - r_d$)")
    st.markdown("""
    This plot shows how the MTM value changes as the **Foreign Risk-Free Rate** ($r_f$) varies,
    while keeping the **Domestic Risk-Free Rate** ($r_d$) constant. This effectively changes the interest rate differential.
    Observe how MTM sensitivity relates to changes in interest rates.
    """)
    rf_values = np.linspace(-0.05, 0.20, 100)
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

    # Plot 2: MTM vs. Current Spot FX Rate
    st.markdown("#### MTM Value vs. Current Spot FX Rate ($S_{t,f/d}$)")
    st.markdown("""
    This plot illustrates how the MTM value reacts to changes in the **Current Spot FX Rate** ($S_{t,f/d}$).
    The vertical dashed line indicates the **Initial FX Forward Price** ($F_{0,f/d}(T)$), which is the rate
    at which the contract was originally agreed upon.
    """)
    spot_values = np.linspace(S0_f_d * 0.8, S0_f_d * 1.2, 100)
    mtm_long_spot_impact = [calculate_mtm_long(s_val, F0T, rf_current, rd_current, T_maturity, t_current) for s_val in spot_values]
    mtm_short_spot_impact = [-val for val in mtm_long_spot_impact]
    fig_spot = go.Figure()
    fig_spot.add_trace(go.Scatter(x=spot_values, y=mtm_long_spot_impact, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_spot.add_trace(go.Scatter(x=spot_values, y=mtm_short_spot_impact, mode='lines', name='Short Position MTM', line=dict(color='red')))
    fig_spot.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Zero MTM")
    fig_spot.add_vline(x=F0T, line_dash="dash", line_color="green", annotation_text=f"Initial Forward Price: {F0T:.4f}", annotation_position="top right")
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
    st.markdown("""...""") # Description of variables
    st.markdown("### Mark-to-Market value of an FX forward contract (long position)")
    st.latex(r"V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}")
    st.markdown("""...""") # Description of variables
    st.markdown(r"For a **short position**, $V_t^{short}(T) = -V_t^{long}(T)$.")

    st.subheader("References")
    st.markdown("""...""") # References to financial literature
```

### Breakdown of `fx_forward_mtm_analyzer.py`:

1.  **Imports**: Necessary libraries like `streamlit` for UI, `numpy` for numerical operations (especially for plotting ranges), `plotly.graph_objects` for interactive plots, and `math.exp` for the exponential function in financial formulas.

2.  **Financial Calculation Functions**:
    *   `calculate_forward_price(S0, rf, rd, T)`: Implements the no-arbitrage formula for the forward price at contract inception.
    *   `calculate_mtm_long(St, F0T, rf_current, rd_current, T, t)`: Computes the Mark-to-Market value for a long forward position at time `t`, considering the current spot rate and current interest rates. The `max(0.0, T - t)` ensures that remaining time to maturity is not negative.

3.  **`run_fx_forward_mtm_analyzer()` Function**: This is the main function called by `app.py`. It orchestrates the entire analyzer interface and logic:

    *   **Header and Introduction**: Sets a sub-header and a brief instructional markdown.
    *   **Sidebar Inputs**:
        *   **Currency Pair Selection (`st.sidebar.selectbox`)**: Provides predefined currency pairs (e.g., USD/EUR) to pre-populate input fields with typical rates. This enhances user experience by providing a starting point.
        *   **Session State (`st.session_state`)**: Crucially used to maintain the state of input widgets (`number_input`, `slider`) across Streamlit re-runs. This ensures that user-entered values are not lost when the app reloads due to interactions. The logic pre-fills these state variables based on the `selected_pair_label`.
        *   **Initial Contract Parameters (`st.sidebar.number_input`, `st.sidebar.slider`)**: Collects inputs like initial spot rate ($S_{0,f/d}$), original maturity ($T$), initial foreign risk-free rate ($r_{f,initial}$), and initial domestic risk-free rate ($r_{d,initial}$).
        *   **Current Market Parameters**: Collects inputs for the current time ($t$), current spot rate ($S_{t,f/d}$), current foreign risk-free rate ($r_{f,current}$), and current domestic risk-free rate ($r_{d,current}$). Note that `St_f_d`'s default and range are dynamically set based on `S0_f_d` for better realism.
    *   **Input Validation**: A simple check ensures that `t_current` does not exceed `T_maturity`, providing immediate feedback to the user and preventing erroneous calculations.
    *   **Calculations**: Calls the `calculate_forward_price` and `calculate_mtm_long` functions with the current input parameters to derive `F0T`, `Vt_long`, and `Vt_short`.
    *   **Display Calculated Values**: Presents the `F0T`, `Vt_long`, and `Vt_short` values clearly formatted.
    *   **Interpretation of MTM Values**: Provides a concise guide on how to interpret positive and negative MTM values for both long and short positions.
    *   **Interactive Plots (`plotly.graph_objects`)**:
        *   **MTM vs. Interest Rate Differential**: Shows how MTM changes as the foreign risk-free rate varies. This helps visualize the sensitivity of the forward contract to interest rate changes.
        *   **MTM vs. Current Spot FX Rate**: Illustrates the direct impact of current spot rate fluctuations on the MTM value, clearly marking the initial forward price as a reference point. Both plots include lines for long and short positions and a zero MTM line for easy reference.
    *   **Formulas Used**: Re-iterates the mathematical formulas used in the calculations, along with descriptions of each variable, for educational purposes. This reinforces the theoretical underpinnings of the application.
    *   **References**: Provides academic references for the financial formulas.

<aside class="positive">
The use of `st.session_state` is a best practice in Streamlit for managing widget values. Without it, inputs would reset on every rerun (e.g., when a slider is adjusted), leading to a frustrating user experience.
</aside>

<aside class="negative">
The current input validation only checks `t_current > T_maturity`. For a production application, more robust validation for rates (e.g., preventing extremely negative rates or ensuring rates are reasonable) might be required, though for an educational tool, the current ranges are usually sufficient.
</aside>

## 5. Running the Application
Duration: 00:02:00

Now that you have the files set up, let's run the Streamlit application and interact with it.

1.  **Open your terminal or command prompt.**
2.  **Navigate to your project's root directory** (where `app.py` is located):

    ```bash
    cd QuLab_FX_Analyzer
    ```

3.  **Run the Streamlit application**:

    ```bash
    streamlit run app.py
    ```

    This command will:
    *   Start a local web server.
    *   Open your default web browser to the application's URL (usually `http://localhost:8501`).

### Interacting with the Application

Once the application opens in your browser:

*   **Initial View**: You will see the main title, the introductory markdown, and the "FX Forward MTM Analyzer" selected in the sidebar.
*   **Adjust Parameters**:
    *   Use the **"Select Currency Pair"** dropdown in the sidebar to load predefined sets of initial and current market parameters. This is a great way to quickly see different scenarios.
    *   Manually adjust the sliders and number inputs for:
        *   **Initial Contract Parameters**: `Initial Spot FX Rate`, `Original Contract Maturity`, `Foreign/Domestic Risk-Free Rates at Inception`.
        *   **Current Market Parameters**: `Current Time (t)`, `Current Spot FX Rate`, `Current Foreign/Domestic Risk-Free Rates`.
*   **Observe Changes**: As you adjust the parameters, the `Initial FX Forward Price`, `Current MTM Value (Long Position)`, and `Current MTM Value (Short Position)` will update in real-time.
*   **Explore Plots**: The interactive plots will also dynamically change, showing you the sensitivity of the MTM value to variations in interest rate differentials and current spot rates. Hover over the lines on the plots to see specific values.
*   **Read Explanations**: Pay attention to the "Interpretation of MTM Values" and "Formulas Used" sections on the main page to deepen your understanding.

Experiment with various combinations of inputs to build an intuitive grasp of how these financial parameters influence the valuation of FX forward contracts.

## 6. Extending and Customizing
Duration: 00:07:00

This application provides a solid foundation for understanding FX forward contract valuation. Here are some ideas for how you can extend and customize it:

### 1. Adding More Currency Pairs

You can expand the `currency_pairs` dictionary in `fx_forward_mtm_analyzer.py` to include more real-world or synthetic currency scenarios. Research current interest rates and typical spot rates for different pairs to make them realistic.

### 2. Implementing Different Compounding Frequencies

The current formulas use continuous compounding. Financial contracts can also use discrete compounding (e.g., annual, semi-annual, quarterly).

*   **Discrete Compounding Formula for Forward Price:**
    $$F_{0,f/d}(T) = S_{0,f/d} \frac{(1 + r_d \cdot \text{days}_d/360)^{\text{count}_d}}{(1 + r_f \cdot \text{days}_f/360)^{\text{count}_f}}$$
    Or, for simple annual compounding:
    $$F_{0,f/d}(T) = S_{0,f/d} \frac{(1 + r_d T)}{(1 + r_f T)}$$
*   **Challenge**: Add a `selectbox` in the sidebar to allow users to choose between "Continuous" and "Annual Discrete" compounding, then adjust `calculate_forward_price` and `calculate_mtm_long` accordingly.

### 3. Incorporating Bid-Ask Spreads

Real-world markets have bid-ask spreads for spot rates and interest rates.
*   **Challenge**: Add input fields for bid-ask spreads for $S_0$, $S_t$, $r_f$, and $r_d$. Modify the calculation functions to compute MTM from the perspective of a bank (buying at bid, selling at ask) or a client, reflecting these spreads.

### 4. Scenario Analysis and Stress Testing

*   **Challenge**: Add a feature to run pre-defined market scenarios (e.g., "interest rate hike", "currency depreciation") and show the MTM impact. This could involve setting up predefined changes to $S_t$, $r_{f,current}$, and $r_{d,current}$.

### 5. Historical Data Integration

*   **Challenge**: Connect the application to a financial data API (e.g., Alpha Vantage, Yahoo Finance API if available for historical FX) to fetch real historical spot rates and potentially interest rates, allowing users to analyze past contract performance. This would require handling API keys and data parsing.

### 6. Adding More Derivative Types

*   **Challenge**: As a larger project, you could extend QuLab to analyze other simple derivatives like currency swaps, interest rate swaps, or even basic options (though options pricing is significantly more complex). Each would likely require its own `application_pages` module.

### Tips for Customization:

*   **Modularization**: Keep your code organized. If you add new features, consider creating new functions or even new files within `application_pages` if the complexity warrants it.
*   **Streamlit Components**: Explore other Streamlit widgets (`st.checkbox`, `st.button`, `st.expander`) to enhance the user interface.
*   **Error Handling**: Implement more robust error handling and input validation beyond the basic checks.
*   **Documentation**: Add comments to your code and update the `st.markdown` explanations as you add new features.

This application serves as an excellent starting point for building more complex financial tools. Happy coding!
