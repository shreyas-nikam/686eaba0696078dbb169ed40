
# FX Forward MTM Analyzer

## 1. Application Overview

### Purpose and Objectives
The FX Forward Mark-to-Market (MTM) Analyzer Streamlit application provides an interactive platform for simulating and analyzing the MTM value of Foreign Exchange (FX) forward contracts. Its primary objective is to enhance understanding of how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

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

## 2. How to Run the Application

To run this Streamlit application, follow these steps:

### Using Docker (Recommended)
1.  **Build the Docker image:**
    ```bash
    docker build -t fx-forward-mtm-analyzer .
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 fx-forward-mtm-analyzer
    ```
3.  Open your web browser and navigate to `http://localhost:8501`.

### Without Docker (Directly with Python)
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
5.  Open your web browser and navigate to the address provided by Streamlit (usually `http://localhost:8501`).

## 3. Application Features

*   Interactive input widgets for initial and current contract parameters.
*   Pre-fill functionality for currency pairs to set default rates.
*   Real-time display of calculated FX Forward Price and MTM values.
*   Interactive plots showing the impact of interest rate differentials and spot rate changes on MTM value using Plotly.
*   Formulas displayed using LaTeX for clarity.
*   Clear explanations and interpretation text for business implications.

## 4. Formulas Used

*   **FX Forward Price (continuous compounding)**:
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
*   **Mark-to-Market value of an FX forward contract (long position)**:
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

## 5. References
[16] - (Add your specific reference here for FX Forward Price formula)
[17] - (Add your specific reference here for MTM value formula)

## 6. License
(Specify your licensing information here if applicable)

## 7. Contact
For any inquiries, please contact [Your Name/Organization].
