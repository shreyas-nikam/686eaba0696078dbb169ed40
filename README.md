
# Forward Rate Agreement (FRA) Settlement Simulator

This Streamlit application provides an interactive educational tool for understanding the mechanics, pricing, and settlement of Forward Rate Agreements (FRAs). It allows users to simulate various FRA scenarios, visualize settlement calculations, and understand the impact of market conditions.

## Features

- **FRA Settlement Simulation**: Configure FRA terms and observe real-time calculations for fixed interest, floating interest, net payment, and cash settlement.
- **Market Rate Sensitivity Analysis**: Visualize how changes in the Market Reference Rate (MRR) affect the FRA cash settlement.
- **APR Conversion Utility**: Convert Annual Percentage Rates (APR) between different compounding frequencies to ensure rate consistency in financial calculations.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Using Docker (Recommended):**
    Ensure you have Docker installed.
    ```bash
    docker build -t fra-simulator .
    docker run -p 8501:8501 fra-simulator
    ```
    Open your web browser and navigate to `http://localhost:8501`.

3.  **Using Python (Local):**
    Ensure you have Python 3.9+ installed.
    ```bash
    pip install -r requirements.txt
    streamlit run app.py
    ```
    Open your web browser and navigate to the address provided by Streamlit (usually `http://localhost:8501`).

## Application Structure

-   `app.py`: The main Streamlit application file.
-   `application_pages/`: Directory containing individual application pages (e.g., `fra_settlement.py`, `apr_conversion.py`).
-   `requirements.txt`: Lists all Python dependencies.
-   `Dockerfile`: Defines the Docker image for the application.

## Learning Outcomes

-   Understand the components and calculations involved in FRA settlement.
-   Analyze the impact of market rate movements on FRA values.
-   Master the conversion of APRs across different compounding frequencies.

---
© 2025 QuantUniversity. All Rights Reserved.
