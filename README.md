
# FX Forward Mark-to-Market (MTM) Analyzer

## Overview
The FX Forward Mark-to-Market (MTM) Analyzer Streamlit application is an interactive platform designed for simulating and analyzing the MTM value of Foreign Exchange (FX) forward contracts. It helps users understand how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

## Purpose and Objectives
*   **Educate Users**: Helps users understand how FX forward prices are determined based on interest rate differentials.
*   **Analyze MTM Factors**: Allows users to analyze the various factors affecting the MTM value of an FX forward contract over its life.
*   **Illustrate Concepts**: Visually explains concepts such as forward premium, forward discount, and gain/loss scenarios from different counterparty perspectives.

## Key Value Propositions
*   **Interactive Learning**: Provides a hands-on experience that deepens understanding beyond static explanations.
*   **Clarity of Concepts**: Simplifies complex financial formulas and their implications through dynamic visualizations.
*   **Accessibility**: A user-friendly interface that requires no prior programming knowledge to operate, making sophisticated financial analysis accessible.

## How to Run the Application

### Using Docker
1.  **Build the Docker image**:
    ```bash
    docker build -t fx-forward-mtm-analyzer .
    ```
2.  **Run the Docker container**:
    ```bash
    docker run -p 8501:8501 fx-forward-mtm-analyzer
    ```
3.  Open your web browser and navigate to `http://localhost:8501`.

### Locally (using Python)
1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
5.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Application Structure
*   `app.py`: The main Streamlit application file.
*   `application_pages/`: Directory containing individual application pages.
    *   `application_pages/forward_mtm_analyzer.py`: Contains the core logic and UI for the FX Forward MTM analysis.
*   `requirements.txt`: Lists all Python dependencies.
*   `Dockerfile`: Defines the Docker image for the application.

## Formulas Used
The application implements the following core financial formulas:

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
