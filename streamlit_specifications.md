# Streamlit Application Requirements Specification: Forward Contracts with Costs & Benefits Simulator

## 1. Application Overview

### Purpose and Objectives
This Streamlit application aims to provide an interactive platform for understanding the pricing and valuation of forward contracts on underlying assets that incur additional costs (e.g., storage) or provide benefits (e.g., dividends). It will demonstrate how these cash flows influence the forward price at inception ($F_0(T)$) and the mark-to-market (MTM) value ($V_t(T)$) throughout the contract's life. The primary objectives are to:
*   Illustrate the theoretical no-arbitrage conditions for forward contracts.
*   Enable users to analyze the impact of varying discrete costs and benefits on forward prices and MTM values.
*   Provide a visual representation of the evolution of MTM values over time and their sensitivity to input parameters.

### Target Audience and Use Cases
The application is designed for:
*   **Financial analysts and derivatives traders:** For quick scenario analysis and understanding valuation dynamics.
*   **Students of finance and derivatives:** To deepen their comprehension of complex forward contract valuation concepts beyond simplified cases, providing a hands-on learning experience.

### Key Value Propositions
*   **Interactive Learning:** Provides a dynamic environment to explore financial concepts, making abstract formulas tangible.
*   **Scenario Analysis:** Allows users to easily modify parameters and observe immediate impacts on pricing and valuation.
*   **Visual Insights:** Offers clear graphical representations of valuation trends and sensitivities, aiding in concept retention and analysis.
*   **Comprehensive Valuation:** Incorporates discrete costs and benefits, offering a more realistic and nuanced valuation model than basic forward contract pricing.

## 2. User Interface Requirements

The application will feature a clear, intuitive layout, designed for ease of use and immediate feedback.

### Layout and Navigation Structure
*   **Main Page Layout:** A single-page application structure will be utilized.
*   **Header:** Prominent title "Forward Contracts with Costs & Benefits Simulator" and an overview section.
*   **Input Section:** A dedicated section for all user-adjustable parameters, potentially organized using Streamlit's sidebar or `st.expander` for clarity.
*   **Calculated Outputs Section:** Displays key numerical results immediately below the inputs.
*   **Visualization Section:** Dedicated space for interactive charts, updating dynamically with input changes.
*   **Formulas Section:** Displays the core mathematical formulas used in the calculations, formatted in LaTeX.
*   **References Section:** Credits external resources as per requirements.

### Input Widgets and Controls
The application will provide interactive widgets for key financial parameters:
*   **Core Contract Parameters:**
    *   **Initial Spot Price ($S_0$):** `st.number_input` (e.g., default `100.0`, step `0.1`). Tooltip: "The current market price of the underlying asset at $t=0$."
    *   **Maturity ($T$):** `st.number_input` (e.g., default `1.0` year, step `0.1`). Tooltip: "Total time to maturity of the forward contract in years from $t=0$."
    *   **Risk-Free Rate ($r$):** `st.number_input` (e.g., default `0.05`, step `0.001`). Tooltip: "The annualized risk-free interest rate (e.g., enter 0.05 for 5%)."
*   **Current Valuation Parameters:**
    *   **Current Time ($t$):** `st.number_input` (e.g., default `0.5` year, step `0.01`). Tooltip: "The current point in time for MTM valuation ($0 \le t \le T$)."
    *   **Current Spot Price ($S_t$):** `st.number_input` (e.g., default `102.0`, step `0.1`). Tooltip: "The spot price of the underlying asset at the current time $t$."
*   **Cash Flow Specification:**
    *   **Dividends (Benefits):** `st.text_area` for JSON input (e.g., `'[{"amount": 2.0, "time_from_t0": 0.25}]'`). Tooltip: "Enter discrete dividends as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from $t=0$). Example: `[{\"amount\": 10.0, \"time_from_t0\": 0.5}]`."
    *   **Costs:** `st.text_area` for JSON input (e.g., `'[{"amount": 1.0, "time_from_t0": 0.5}]'`). Tooltip: "Enter discrete costs (e.g., storage) as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from $t=0$). Example: `[{\"amount\": 5.0, \"time_from_t0\": 0.75}]`."
*   **Position Type:** `st.radio` ('long', 'short'). Tooltip: "Select the position type for MTM valuation."

### Visualization Components and Display
*   **Calculated Outputs:**
    *   **Forward Price at Inception ($F_0(T)$):** Displayed using `st.metric` or `st.info`, showing values for "with Costs/Benefits" and "without Costs/Benefits".
    *   **MTM Value at Current Time ($V_t(T)$):** Displayed using `st.metric` or `st.info` for both "Long Position" and "Short Position".
*   **Informative Text:** Markdown sections explaining the formulas and their components, including:
    *   Forward price at inception with costs/benefits:
        $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1 + r)^T$$
        Where $PV_0(I) = \sum_{j} I_j (1 + r)^{-t_j^I}$ and $PV_0(C) = \sum_{k} C_k (1 + r)^{-t_k^C}$.
    *   MTM value during the life of the contract (long position):
        $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$
        Where $PV_t(I)$ and $PV_t(C)$ are the present values of *remaining* costs and benefits from time $t$ to maturity $T$.
    *   MTM value for a short position:
        $$V_t(T)_{short} = -V_t(T)_{long}$$
    *   Present value of cash flows:
        $$PV_t(CF) = \sum_{j | t_j^{CF} \ge t} CF_j (1 + r)^{-(t_j^{CF} - t)}$$
*   **Input Validation and Feedback:**
    *   Display error messages using `st.error` if inputs are invalid (e.g., `current_time_t > maturity_time_T`, negative prices, malformed JSON).
    *   Provide `st.warning` messages for non-critical issues (e.g., empty cash flow lists).

## 3. Visualization Requirements

The application will leverage interactive plotting libraries to effectively communicate insights. Plotly is preferred for its interactivity in Streamlit, with Matplotlib as a fallback.

### Chart Types and Visualization Libraries
*   **Trend Plot:**
    *   **Type:** Line chart showing `MTM Value Evolution Over Time`.
    *   **Content:**
        *   One line for MTM value (long position) with specified costs/benefits.
        *   One line for MTM value (long position) without costs/benefits (for comparison).
        *   A vertical line marking the `current_time_t`.
        *   A horizontal line at $Y=0$ to clearly show gains/losses.
    *   **Libraries:** Plotly Express (`px.line`) or Matplotlib (`plt.plot`).
    *   **Axes:** X-axis: 'Time (Years)', Y-axis: 'MTM Value'.
    *   **Title:** 'MTM Value Evolution Over Time (Long Position)'.
*   **Relationship Plot:**
    *   **Type:** Line or Scatter plot illustrating the sensitivity of the forward price at inception.
    *   **Content:**
        *   Plot $F_0(T)$ against a range of multipliers applied to the original `cost_cash_flows`.
        *   Plot $F_0(T)$ against a range of multipliers applied to the original `dividend_cash_flows`.
    *   **Libraries:** Plotly Express (`px.line` or `px.scatter`) or Matplotlib.
    *   **Axes:** X-axis: 'Multiplier of Original Costs/Benefits', Y-axis: 'Forward Price ($F_0(T)$)'.
    *   **Title:** 'Sensitivity of Forward Price to Costs/Benefits Magnitude'.
*   **Aggregated Comparison Plot:**
    *   **Type:** Bar chart.
    *   **Content:** Compare the MTM outcomes (at `current_time_t`) for predefined scenarios:
        *   'Base Case (with C/B)'
        *   'No Costs/Benefits'
        *   'Double Dividends'
        *   'Double Costs'
    *   **Libraries:** Plotly Express (`px.bar`) or Matplotlib.
    *   **Axes:** X-axis: 'Scenario', Y-axis: 'MTM Value'.
    *   **Title:** 'MTM Value Comparison Across Scenarios (Long Position)'.

### Interactive Visualization Features
*   **Dynamic Updates:** All charts will update in real-time as users adjust input parameters.
*   **Tooltips (Plotly):** On-hover tooltips displaying precise data values (e.g., time and MTM value for the trend plot, multiplier and forward price for the sensitivity plot).
*   **Zoom and Pan (Plotly):** Users should be able to zoom into specific areas of the charts and pan across the data.
*   **Legend Toggling (Plotly):** Ability to show/hide individual series by clicking on legend items.

### Real-time Updates and Responsiveness
*   The application must be responsive, with calculations and plot generations completing quickly upon user input changes, ideally within typical Streamlit re-run times.
*   The performance should align with the "execute end-to-end on a mid-spec laptop (8 GB RAM) in fewer than 5 minutes" constraint.

### Annotation and Tooltip Specifications
*   **Clear Titles:** Each plot will have a concise and descriptive title.
*   **Labeled Axes:** Both X and Y axes will be clearly labeled with units where appropriate.
*   **Legends:** Essential for distinguishing between different data series in multi-line/bar charts.
*   **Color-Blind Friendly Palette:** A color scheme that is accessible to users with color vision deficiencies will be adopted.
*   **Font Size:** Font sizes in visualizations will be $\ge 12$ pt for readability.
*   **Gridlines:** Appropriate gridlines will be used to aid in reading values.

### Additional Requirements
*   **Open-Source Libraries:** Only open-source Python libraries from PyPI will be used.
*   **Code Comments and Narrative:** Although this is a specification, the underlying code implementation will adhere to the lab's requirement for clear code comments and narrative.
*   **Data Handling:** The application will incorporate robust input parsing and validation for cash flow data, as demonstrated in the Jupyter notebook's `parse_cash_flows` function.
