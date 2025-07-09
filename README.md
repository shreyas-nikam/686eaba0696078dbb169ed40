
# Forward Contract Valuation Simulator

## Overview
This Streamlit application provides an interactive platform for users to understand and simulate the pricing and mark-to-market (MTM) valuation of forward contracts. It demonstrates how initial forward prices are determined, analyzes the evolution of a forward contract's MTM value over its life, and differentiates between contracts with and without additional costs or benefits. The application visualizes potential gains and losses for both long and short positions under varying market conditions.

## Features
*   **Interactive Learning:** Dynamic, hands-on experience for complex financial concepts.
*   **Clarity through Visualization:** Converts abstract financial formulas into intuitive, real-time charts using Plotly.
*   **Practical Application:** Bridges theoretical knowledge with practical valuation scenarios.
*   **User-Friendly Interface:** Easy-to-use interface without requiring advanced programming knowledge.

## How to Run

### Local Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

### Docker
1.  **Build the Docker image:**
    ```bash
    docker build -t forward-contract-simulator .
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 forward-contract-simulator
    ```
    Open your web browser and navigate to `http://localhost:8501`.

## Application Structure
*   `app.py`: The main Streamlit application file.
*   `application_pages/`: Directory containing individual page modules.
    *   `application_pages/page1.py`: Contains the core logic and UI for the Forward Contract Valuation Simulator.
*   `requirements.txt`: Lists Python dependencies.
*   `Dockerfile`: Docker configuration for containerization.

## Contact
For any questions or feedback, please contact QuantUniversity.

© 2025 QuantUniversity. All Rights Reserved.
