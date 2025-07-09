
# Streamlit Application Requirements Specification: Forward Contract Valuation Simulator

## 1. Application Overview

### Purpose and Objectives
The "Forward Contract Valuation Simulator" Streamlit application aims to provide an interactive platform for users, particularly finance students and aspiring traders, to understand and simulate the pricing and mark-to-market (MTM) valuation of forward contracts. The application will demonstrate how initial forward prices are determined based on spot prices and risk-free rates, analyze the evolution of a forward contract's MTM value over its life, and differentiate between contracts with and without additional costs or benefits. A key objective is to visualize potential gains and losses for both long and short positions under varying market conditions, thereby demystifying core derivative concepts like the no-arbitrage principle and mark-to-market adjustments through hands-on engagement.

### Target Audience and Use Cases
*   **Target Audience:** Finance students, financial analysts, aspiring traders, and individuals interested in derivatives markets and quantitative finance.
*   **Use Cases:**
    *   **Educational Tool:** Students can manipulate parameters to gain a deeper understanding of forward contract mechanics and valuation.
    *   **Scenario Analysis:** Users can simulate different market scenarios (e.g., changes in spot price, interest rates) to observe their impact on contract value.
    *   **Risk and Profit Visualization:** Aid in understanding potential profit/loss profiles for different forward positions.

### Key Value Propositions
*   **Interactive Learning:** Provides a dynamic, hands-on experience for complex financial concepts.
*   **Clarity through Visualization:** Converts abstract financial formulas into intuitive, real-time charts.
*   **Practical Application:** Bridges theoretical knowledge with practical valuation scenarios.
*   **Accessibility:** Offers an easy-to-use interface without requiring advanced programming knowledge.

## 2. User Interface Requirements

### Layout and Navigation Structure
The application will feature a clear, intuitive single-page layout:
*   **Sidebar:** Will host all input parameters and controls, ensuring easy access and modification.
*   **Main Content Area:** Will display calculated values, explanations of formulas, and interactive visualizations.
*   **Section Headers:** Clear markdown headers will delineate distinct sections such as "Overview," "Input Parameters," "Calculated Values," "Valuation Formulas," and "Visualizations."

### Input Widgets and Controls
The application will provide the following interactive input widgets, primarily using Streamlit's `st.slider`, `st.number_input`, `st.radio`, and `st.checkbox` components:

*   **Contract Inception Parameters (for $F_0(T)$ calculation):**
    *   **Initial Spot Price ($S_0$):** `st.number_input` (e.g., 50 to 200, step 1, default 100).
    *   **Risk-Free Rate ($r$):** `st.number_input` (e.g., 0.01 to 0.10, step 0.001, representing 1% to 10%, default 0.05).
    *   **Time to Maturity ($T$):** `st.number_input` (e.g., 0.25 to 5.0 years, step 0.25, default 1.0).
    *   **Initial Present Value of Income ($PV_0(I)$):** `st.number_input` (e.g., 0 to 20, step 0.1, default 0.0). *Only enabled if "Include Costs/Benefits" is checked.*
    *   **Initial Present Value of Costs ($PV_0(C)$):** `st.number_input` (e.g., 0 to 20, step 0.1, default 0.0). *Only enabled if "Include Costs/Benefits" is checked.*

*   **Current Valuation Parameters (for $V_t(T)$ calculation and scenario analysis):**
    *   **Current Time ($t$):** `st.slider` (from 0.0 to $T$, step 0.01). This slider's maximum value will dynamically adjust based on `Time to Maturity ($T$)`.
    *   **Current Spot Price ($S_t$):** `st.number_input` (e.g., dynamic range based on $S_0$, step 1, default $S_0$).
    *   **Current Present Value of Income ($PV_t(I)$):** `st.number_input` (e.g., 0 to 20, step 0.1, default 0.0). *Only enabled if "Include Costs/Benefits" is checked.*
    *   **Current Present Value of Costs ($PV_t(C)$):** `st.number_input` (e.g., 0 to 20, step 0.1, default 0.0). *Only enabled if "Include Costs/Benefits" is checked.*
    *   **Position Type:** `st.radio` for "Long" or "Short" position.

*   **Feature Toggles:**
    *   **Include Costs/Benefits:** `st.checkbox` to toggle the visibility and inclusion of $PV_0(I)$, $PV_0(C)$, $PV_t(I)$, and $PV_t(C)$ in calculations.

*   **Interactive Elements and Feedback Mechanisms:**
    *   All calculations and visualizations will update in real-time as input parameters are adjusted.
    *   Display of `Initial Forward Price ($F_0(T)$)` and `Current MTM Value ($V_t(T)$)` prominently as numeric outputs.
    *   Inline help text or tooltips will be provided for each control to describe its purpose and impact.
    *   Validation: The application will include checks for valid input ranges (e.g., $t$ must be $\le T$).

### Valuation Formulas Display
The application will explicitly display the relevant financial formulas using LaTeX formatting for clarity:

*   **Initial Forward Price ($F_0(T)$):**
    *   Without costs/benefits:
        `$$F_0(T) = S_0 (1+r)^T$$`
    *   With costs/benefits:
        `$$F_0(T) = (S_0 - PV_0(I) + PV_0(C)) (1+r)^T$$`

*   **Mark-to-Market (MTM) Value ($V_t(T)$) for a Long Position:**
    *   Without costs/benefits:
        `$$V_t(T) = S_t - F_0(T)(1+r)^{-(T-t)}$$`
    *   With costs/benefits:
        `$$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1+r)^{-(T-t)}$$`

*   **Mark-to-Market (MTM) Value ($V_t(T)$) for a Short Position:**
    *   The MTM value for a short position is the negative of the long position's MTM. The application will compute the long MTM value first and then negate it for the short position display.

## 3. Visualization Requirements

### Chart Types and Visualization Libraries
The application will utilize Plotly for interactive visualizations, ensuring a rich user experience. Three core visualizations will be provided:

1.  **Trend Plot (Line Plot):**
    *   **Purpose:** Shows the evolution of the MTM value ($V_t(T)$) of the forward contract from inception ($t=0$) to maturity ($t=T$).
    *   **Data:** MTM values for both long and short positions plotted against time.
    *   **X-axis:** Time ($t$) from 0 to $T$.
    *   **Y-axis:** MTM Value ($V_t(T)$).
    *   **Scenarios:** Allow for various spot price paths (e.g., linear increase/decrease, constant, or user-defined simple path simulation).

2.  **Relationship Plot (Scatter Plot):**
    *   **Purpose:** Illustrates the sensitivity of $V_t(T)$ to changes in $S_t$ at a fixed point in time.
    *   **Data:** MTM values plotted against a range of possible $S_t$ values around the current $S_t$.
    *   **X-axis:** Spot Price ($S_t$).
    *   **Y-axis:** MTM Value ($V_t(T)$).
    *   **Highlight:** Current $S_t$ and corresponding $V_t(T)$ will be highlighted.

3.  **Aggregated Comparison (Bar Chart):**
    *   **Purpose:** Visualizes profit/loss outcomes at maturity ($T$) for different settlement spot prices ($S_T$) relative to $F_0(T)$.
    *   **Data:** Profit/Loss (P&L) at maturity for several discrete $S_T$ values (e.g., $S_T < F_0(T)$, $S_T = F_0(T)$, $S_T > F_0(T)$).
    *   **X-axis:** Settlement Spot Price ($S_T$) scenarios.
    *   **Y-axis:** Profit/Loss at Maturity ($P\&L_T$).
    *   **Coloring:** Differentiate positive (profit) and negative (loss) outcomes, and long/short positions.

### Interactive Visualization Features
*   **Zoom and Pan:** Users should be able to zoom into specific areas of the plots and pan across the data.
*   **Tooltips:** On hover, tooltips will display precise numerical values for data points (e.g., for the Trend Plot, hover will show time, spot price, and MTM value).
*   **Legends:** Clearly indicate long vs. short positions and any other distinguishing features on the plots.

### Real-Time Updates and Responsiveness
*   All visualizations will update instantaneously as any input parameter is changed, providing immediate feedback on how market variables affect forward contract valuation.
*   The application will be designed to be responsive, ensuring optimal viewing and interaction across various device screen sizes.

### Annotation and Tooltip Specifications
*   **Titles:** Each chart will have a clear, descriptive title (e.g., "MTM Value Over Time for Long/Short Forward Position").
*   **Axis Labels:** All axes will be clearly labeled with appropriate units (e.g., "Time (Years)", "Spot Price", "MTM Value ($)").
*   **Color Palette:** A color-blind-friendly palette will be used for all visualizations to ensure accessibility.
*   **Font Size:** Minimum font size of 12pt will be maintained for readability.
*   **Data Points:** Specific annotations or markers will be used to highlight key data points, such as initial price, current MTM, or breakeven points.
