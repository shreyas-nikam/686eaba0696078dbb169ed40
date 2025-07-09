# FX Forward Mark-to-Market (MTM) Analyzer

## Project Title
**FX Forward Mark-to-Market (MTM) Analyzer: An Interactive Streamlit Application**

## 1. Project Description
This Streamlit application serves as an interactive laboratory tool designed to help users understand and analyze the Mark-to-Market (MTM) valuation of Foreign Exchange (FX) forward contracts. By providing a user-friendly interface, it allows finance students, practitioners, and enthusiasts to experiment with various market parameters (spot rates, interest rates, time to maturity) and observe their real-time impact on the FX forward price at inception and its subsequent MTM value.

The application calculates the initial forward price using the covered interest rate parity formula and then determines the MTM value of a long (or short) FX forward position based on changes in current market conditions. It features dynamic visualizations to illustrate the sensitivity of MTM to changes in current spot rates and interest rate differentials.

## 2. Features

*   **Initial FX Forward Price Calculation:** Computes the forward price at contract inception ($t=0$) based on initial spot rate and risk-free interest rates (foreign and domestic) and contract maturity.
*   **Mark-to-Market (MTM) Valuation:** Calculates the MTM value for both long and short FX forward positions at any given time ($t$) before maturity, reflecting changes in current spot rates and interest rates.
*   **Interactive Input Parameters:**
    *   Adjust initial spot rate ($S_{0,f/d}$), original contract maturity ($T$), and initial risk-free rates ($r_{f,initial}$, $r_{d,initial}$).
    *   Modify current time ($t$), current spot rate ($S_{t,f/d}$), and current risk-free rates ($r_{f,current}$, $r_{d,current}$).
*   **Currency Pair Presets:** Conveniently pre-fills input fields with example values for common currency pairs (USD/EUR, ZAR/EUR) to facilitate quick experimentation.
*   **Dynamic Input Ranges:** Adjusts the input range for the current spot rate based on the initial spot rate for a more intuitive user experience.
*   **Formula Display:** Shows the underlying mathematical formulas (LaTeX) for FX Forward Price and MTM calculations for clarity and educational purposes.
*   **Visualizations (Plotly):**
    *   **MTM vs. Interest Rate Differential:** A line plot showing how MTM changes as the current foreign risk-free rate varies.
    *   **MTM vs. Current Spot FX Rate:** A line plot demonstrating the sensitivity of MTM to changes in the prevailing spot exchange rate.
*   **Clear Metrics:** Displays calculated values prominently using Streamlit's `st.metric` for easy readability.
*   **Comprehensive Explanations:** Provides markdown text to explain the concepts, interpretations of results, and references.

## 3. Getting Started

### Prerequisites

Before you can run this application, ensure you have the following installed:

*   **Python 3.8+**
*   **pip** (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/fx-forward-mtm-analyzer.git
    cd fx-forward-mtm-analyzer
    ```
    (Replace `your_username/fx-forward-mtm-analyzer` with the actual repository path if different).

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    Create a `requirements.txt` file in the root directory of your project with the following content:
    ```
    streamlit
    numpy
    plotly
    ```
    Then install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

## 4. Usage

To run the Streamlit application:

1.  Ensure you are in the root directory of the cloned repository and your virtual environment is activated (if used).
2.  Execute the Streamlit command, specifying the path to the main application file:
    ```bash
    streamlit run application_pages/main_page.py
    ```
3.  Your web browser should automatically open a new tab displaying the application. If not, copy the URL provided in your terminal (e.g., `http://localhost:8501`).

### How to Use the Application:

*   **Sidebar Controls:** All input parameters for contract setup and current market conditions are located in the sidebar.
    *   Use the **"Select Currency Pair"** dropdown to pre-fill example values for spot rates and interest rates. You can then fine-tune these values.
    *   Adjust the **"Initial Contract Parameters ($t=0$)"** to define your FX forward contract's inception terms.
    *   Modify the **"Current Market Parameters ($t$)"** sliders and number inputs to simulate market movements and analyze MTM at different points in time or under varying conditions.
*   **Main Display Area:**
    *   Observe the calculated **FX Forward Price at Inception** and the **Current Mark-to-Market (MTM) Value** for both long and short positions.
    *   Explore the interactive **Plotly charts** to visualize the sensitivity of the MTM value to changes in interest rate differentials and current spot FX rates. Hover over the plots for detailed values.

## 5. Project Structure

The project follows a simple, clean structure:

```
fx-forward-mtm-analyzer/
├── application_pages/
│   └── main_page.py       # Main Streamlit application script
├── requirements.txt       # List of Python dependencies
└── README.md              # This README file
```

## 6. Technology Stack

*   **Python 3.x**: The core programming language.
*   **Streamlit**: The open-source app framework used to build the interactive web interface.
*   **NumPy**: Essential library for numerical operations, particularly for generating data points for plots.
*   **Plotly**: Used for creating interactive and dynamic visualizations (charts and graphs) within the Streamlit application.

## 7. Contributing

This project is primarily a lab exercise, but contributions are welcome! If you have suggestions for improvements, feature requests, or bug reports, please feel free to:

1.  **Fork** the repository.
2.  **Create a new branch** (`git checkout -b feature/your-feature-name`).
3.  **Make your changes**.
4.  **Commit your changes** (`git commit -m 'Add new feature'`).
5.  **Push to the branch** (`git push origin feature/your-feature-name`).
6.  **Open a Pull Request**.

## 8. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: A `LICENSE` file should be created in the root directory if you're formally releasing this project.)*

## 9. Contact

For any questions or inquiries, please feel free to reach out:

*   **Your Name/Institution:** [Your Name or Institution's Name Here]
*   **Email:** [your.email@example.com]
*   **GitHub:** [https://github.com/your_username](https://github.com/your_username) (Optional)

---

**Disclaimer:** This application is for educational and illustrative purposes only. It should not be used for actual financial trading or investment decisions. The formulas and assumptions are simplified and may not reflect all complexities of real-world financial markets.


## License

QuantUniversity License
