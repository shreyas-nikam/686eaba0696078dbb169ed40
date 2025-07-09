# Streamlit Application Requirements Specification: FX Forward MTM Analyzer

## 1. Application Overview

### Purpose and Objectives
The FX Forward Mark-to-Market (MTM) Analyzer Streamlit application aims to provide an interactive platform for simulating and analyzing the MTM value of Foreign Exchange (FX) forward contracts. Its primary objective is to enhance understanding of how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

Key objectives include:
*   **Educate Users**: Help users understand how FX forward prices are determined based on interest rate differentials.
*   **Analyze MTM Factors**: Allow users to analyze the various factors affecting the MTM value of an FX forward contract over its life.
*   **Illustrate Concepts**: Visually explain concepts such as forward premium, forward discount, and gain/loss scenarios from different counterparty perspectives.

### Target Audience and Use Cases
**Target Audience**: Students, financial professionals, and anyone interested in derivatives, foreign exchange markets, and financial risk management.

**Use Cases**:
*   **Educational Tool**: For learners to interactively explore theoretical concepts of FX forward pricing and valuation.
*   **Scenario Analysis**: Practitioners can test hypothetical market movements and their impact on contract values.
*   **Risk Understanding**: Visualize how changes in underlying parameters contribute to MTM gains or losses, aiding in risk assessment.

### Key Value Propositions
*   **Interactive Learning**: Provides a hands-on experience that deepens understanding beyond static explanations.
*   **Clarity of Concepts**: Simplifies complex financial formulas and their implications through dynamic visualizations.
*   **Accessibility**: A user-friendly interface that requires no prior programming knowledge to operate, making sophisticated financial analysis accessible.

## 2. User Interface Requirements

### Layout and Navigation Structure
The application will feature a clean, intuitive, two-column layout:
*   **Sidebar (Left Column)**: Will host all user input widgets and controls for parameters and scenarios. This ensures that users can easily modify inputs and observe immediate changes.
*   **Main Display Area (Right Column)**: Will present the calculated results (FX Forward Price, MTM values) and all interactive visualization plots.

### Input Widgets and Controls
All interactive inputs will be placed in the sidebar and include inline help text or tooltips as specified in user requirements.

#### 2.1. Initial Contract Parameters (at time $t=0$)
These parameters define the contract at its inception.
*   **Initial Spot FX Rate** ($S_{0,f/d}$): Numeric input (e.g., `st.number_input` or `st.slider`).
    *   **Label**: "Initial Spot FX Rate ($S_{0,f/d}$)"
    *   **Range**: Appropriate range (e.g., 0.5 to 2.0 or 50 to 200, depending on currency pair context).
    *   **Help Text**: "The spot exchange rate at the inception of the contract. Example: How many units of domestic currency for one unit of foreign currency."
*   **Original Contract Maturity** ($T$): Numeric input (e.g., `st.number_input` or `st.slider`).
    *   **Label**: "Original Contract Maturity ($T$)"
    *   **Range**: (e.g., 0.0 to 5.0 years, in steps of 0.1).
    *   **Help Text**: "The total time to maturity of the FX forward contract in years from inception."
*   **Foreign Risk-Free Rate at Inception** ($r_{f,initial}$): Numeric input.
    *   **Label**: "Foreign Risk-Free Rate at Inception ($r_{f,initial}$)"
    *   **Range**: (e.g., -0.02 to 0.10, representing -2% to 10%).
    *   **Help Text**: "The risk-free interest rate of the foreign currency at contract inception."
*   **Domestic Risk-Free Rate at Inception** ($r_{d,initial}$): Numeric input.
    *   **Label**: "Domestic Risk-Free Rate at Inception ($r_{d,initial}$)"
    *   **Range**: (e.g., -0.02 to 0.10, representing -2% to 10%).
    *   **Help Text**: "The risk-free interest rate of the domestic currency at contract inception."

#### 2.2. Current Market Parameters (at time $t$)
These parameters define the current market conditions used for MTM calculation.
*   **Current Time** ($t$): Numeric input (e.g., `st.slider`).
    *   **Label**: "Current Time ($t$)"
    *   **Range**: 0.0 to $T$ (dynamically adjust max based on `Original Contract Maturity`).
    *   **Help Text**: "The current time in years from contract inception ($0 \le t \le T$). For $t=0$, MTM is usually zero (ignoring transaction costs)."
*   **Current Spot FX Rate** ($S_{t,f/d}$): Numeric input.
    *   **Label**: "Current Spot FX Rate ($S_{t,f/d}$)"
    *   **Range**: (e.g., +/- 10% around `Initial Spot FX Rate`).
    *   **Help Text**: "The prevailing spot exchange rate in the market at the current time $t$."
*   **Current Foreign Risk-Free Rate** ($r_{f,current}$): Numeric input.
    *   **Label**: "Current Foreign Risk-Free Rate ($r_{f,current}$)"
    *   **Range**: (e.g., -0.02 to 0.10).
    *   **Help Text**: "The current risk-free interest rate of the foreign currency at time $t$. This can differ from $r_{f,initial}$."
*   **Current Domestic Risk-Free Rate** ($r_{d,current}$): Numeric input.
    *   **Label**: "Current Domestic Risk-Free Rate ($r_{d,current}$)"
    *   **Range**: (e.g., -0.02 to 0.10).
    *   **Help Text**: "The current risk-free interest rate of the domestic currency at time $t$. This can differ from $r_{d,initial}$."

#### 2.3. Currency Pair Selection
*   **Dropdown**: `st.selectbox` for synthetic currency pairs.
    *   **Label**: "Select Currency Pair (Pre-fill Rates)"
    *   **Options**: e.g., "USD/EUR" ($r_d$=USD, $r_f$=EUR), "ZAR/EUR" ($r_d$=ZAR, $r_f$=EUR).
    *   **Functionality**: Selecting a pair will pre-fill realistic default values for `Initial Spot FX Rate`, `r_{f,initial}`, `r_{d,initial}`, `r_{f,current}`, and `r_{d,current}`. Users should still be able to override these pre-filled values using the individual numeric inputs.
    *   **Help Text**: "Choose a synthetic currency pair to pre-populate typical spot rates and interest rate differentials. You can then adjust rates manually."

### Visualization Components (Charts, Graphs, Tables)
The main display area will feature:
*   **Calculated Values Display**:
    *   **FX Forward Price** ($F_{0,f/d}(T)$): Clearly display the calculated initial forward price based on `Initial Contract Parameters`.
    *   **Current MTM Value**: Display the calculated MTM value for both long and short positions.
        *   **Long Position MTM**: $V_t^{long}(T)$
        *   **Short Position MTM**: $V_t^{short}(T)$ (which is $-V_t^{long}(T)$)
*   **Interactive Plots**:
    *   **Interest Rate Differential Impact Plot**: A line plot showing MTM value against varying interest rate differentials (by varying one rate, holding the other constant).
    *   **Spot Rate Change Impact Plot**: A line plot showing MTM value against varying current spot FX rates.

### Interactive Elements and Feedback Mechanisms
*   **Real-time Updates**: All calculations and visualizations will update automatically and instantaneously as user inputs are changed.
*   **Input Validation**: Implement basic validation (e.g., $t \le T$, rates within reasonable bounds) with informative error messages.
*   **Interpretation Text**: Brief narrative cells will accompany the plots and MTM value display, explaining the business implications and concepts illustrated (e.g., "A positive MTM for a long position indicates a gain...").
*   **References Section**: A dedicated section at the bottom for all references used, including the original source of the formulas.
*   **Formula Display**: The core formulas will be displayed within the application using LaTeX formatting for clarity.

## 3. Visualization Requirements

### Chart Types and Visualization Libraries
*   **Core Visuals**:
    *   **Line Plots**: Used for "Interest Rate Differential Impact" and "Spot Rate Change Impact" to show continuous relationships and trends.
*   **Visualization Library**: `matplotlib.pyplot` will be the primary library for plotting as per the Jupyter Notebook content, leveraging `st.pyplot` for display.
*   **Interactive Visualization Features**:
    *   While `matplotlib` plots in Streamlit are static, interactivity will be achieved through the dynamic nature of Streamlit inputs. Users modifying sliders will trigger re-renders of the plots with new data ranges and calculations.
    *   Consideration for future enhancement: Integration with `Plotly` or `Altair` could enable true interactive features like zooming, panning, and dynamic tooltips on the plots themselves, if resource constraints allow for non-static fallback.

### Real-time Updates and Responsiveness
*   All charts and calculated values will dynamically update in real-time as users adjust input parameters via sliders, text inputs, or dropdowns. This ensures immediate feedback and an immersive analytical experience.
*   The application will be optimized for performance to ensure updates occur quickly, ideally within milliseconds, to meet the sub-5-minute execution constraint on a mid-spec laptop.

### Annotation and Tooltip Specifications
*   **Clear Titles and Labels**: Each plot will have a descriptive title, clearly labeled X and Y axes, and a legend distinguishing between long and short positions.
    *   **X-axis for Interest Rate Differential Plot**: "Interest Rate Differential ($r_f - r_d$)"
    *   **X-axis for Spot Rate Change Plot**: "Current Spot Rate ($S_t$)"
    *   **Y-axis for all plots**: "MTM Value"
*   **Horizontal Line for Zero MTM**: A horizontal line at $Y=0$ will be prominently displayed on both plots to visually indicate the break-even point for MTM.
*   **Vertical Line for Original Forward Price**: On the "Spot Rate Change Impact Plot", a vertical line at $X = F_{0,f/d}(T)$ will indicate the original forward price, highlighting its relation to the current spot rate for MTM calculation.
*   **Color Palette**: Adopt a color-blind-friendly palette to ensure accessibility for all users.
*   **Font Size**: Ensure text (titles, labels, legends, numbers) has a minimum font size of 12pt for readability.

### Formula Display (as per general requirements)
The following formulas will be displayed within the application, likely in an "About" or "Formulas" section, using LaTeX formatting:

*   **FX Forward Price (continuous compounding)** [16]:
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
*   **Mark-to-Market value of an FX forward contract (long position)** [17]:
    $$V_t(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$$
    Where:
    *   $F_{0,f/d}(T)$ is the forward price at time 0 for a contract maturing at time $T$.
    *   $S_{0,f/d}$ is the spot exchange rate at time 0 (foreign currency per domestic currency).
    *   $S_{t,f/d}$ is the current spot exchange rate at time $t$.
    *   $r_f$ is the foreign risk-free interest rate.
    *   $r_d$ is the domestic risk-free interest rate.
    *   $T$ is the original time to maturity of the forward contract in years.
    *   $t$ is the current time in years from the contract inception ($0 \le t \le T$).
    *   $e$ is the base of the natural logarithm.

This specification provides a detailed blueprint for the development of the Streamlit FX Forward MTM Analyzer application, ensuring all core functionalities, user experience, and visualization requirements are met.