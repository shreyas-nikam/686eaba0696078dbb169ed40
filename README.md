
# FX Forward Mark-to-Market (MTM) Analyzer

This Streamlit application provides an interactive platform for simulating and analyzing the Mark-to-Market (MTM) value of Foreign Exchange (FX) forward contracts. It helps users understand how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

## Purpose and Objectives

*   **Educate Users**: Understand how FX forward prices are determined based on interest rate differentials.
*   **Analyze MTM Factors**: Analyze the various factors affecting the MTM value of an FX forward contract over its life.
*   **Illustrate Concepts**: Visually explain concepts such as forward premium, forward discount, and gain/loss scenarios from different counterparty perspectives.

## Getting Started

To run this application locally, follow these steps:

### Prerequisites

*   Python 3.9+
*   Docker (optional, for containerized deployment)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Run Streamlit**:
    ```bash
    streamlit run app.py
    ```
    The application will open in your default web browser.

### Running with Docker

1.  **Build the Docker image**:
    ```bash
    docker build -t fx-forward-mtm-analyzer .
    ```
2.  **Run the Docker container**:
    ```bash
    docker run -p 8501:8501 fx-forward-mtm-analyzer
    ```
    Access the application at `http://localhost:8501` in your web browser.

## Application Features

*   **Interactive Input Widgets**: Adjust initial contract parameters and current market parameters to see real-time updates.
*   **Currency Pair Selection**: Pre-fill common currency pair rates for quick scenario setup.
*   **Calculated Values Display**: View the initial FX Forward Price and current MTM values for long and short positions.
*   **Interactive Plots**:
    *   **Interest Rate Differential Impact Plot**: Visualize MTM changes based on interest rate differentials.
    *   **Spot Rate Change Impact Plot**: Visualize MTM changes based on current spot FX rates.
*   **Formula Display**: LaTeX-formatted financial formulas for clarity and educational purposes.

## Formulas Used

### FX Forward Price (continuous compounding)
$$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$

### Mark-to-Market value of an FX forward contract (long position)
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

---
© 2025 QuantUniversity. All Rights Reserved.
