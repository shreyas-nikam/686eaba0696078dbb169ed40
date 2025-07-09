# FX Forward MTM Analyzer Streamlit Application

This Streamlit application provides an interactive platform for simulating and analyzing the Mark-to-Market (MTM) value of Foreign Exchange (FX) forward contracts. It helps users understand how interest rate differentials and spot rate changes influence the valuation dynamics and risk exposure of these contracts.

## Features

*   **Interactive Learning**: Hands-on experience to deepen understanding of FX forward pricing and valuation.
*   **Scenario Analysis**: Test hypothetical market movements and their impact on contract values.
*   **Risk Understanding**: Visualize how changes in underlying parameters contribute to MTM gains or losses.
*   **Dynamic Visualizations**: Real-time updates of calculations and plots as inputs are adjusted.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

    The application will open in your web browser, typically at `http://localhost:8501`.

## Docker

You can also run this application using Docker:

1.  **Build the Docker image:**
    ```bash
    docker build -t fx-forward-mtm .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 fx-forward-mtm
    ```

    Access the application in your browser at `http://localhost:8501`.

## Application Structure

*   `app.py`: The main Streamlit application file.
*   `application_pages/`: Directory containing individual pages of the application.
    *   `page1.py`: Contains the logic for the FX Forward MTM analysis page.
*   `requirements.txt`: Lists all Python dependencies.
*   `Dockerfile`: Defines the Docker image for the application.

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
The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
