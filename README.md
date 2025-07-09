A comprehensive `README.md` for your Streamlit application lab project:

---

# QuLab: FX Forward Mark-to-Market (MTM) Analyzer

[![Made with Streamlit](https://streamlit.io/images/brand/streamlit-mark-color.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Project Description

The "FX Forward Mark-to-Market (MTM) Analyzer" is an interactive Streamlit application designed as a practical lab project for understanding and visualizing the valuation dynamics of Foreign Exchange (FX) forward contracts. It allows users to manipulate various market parameters, such as spot rates and interest rate differentials, to observe their impact on the Mark-to-Market value of these derivatives.

This application serves as an educational tool to explore key concepts in derivative valuation, including:
*   **Initial Forward Price**: How the forward price is determined at inception ($t=0$) based on the initial spot rate and interest rate differentials (reflecting the no-arbitrage principle).
*   **Interest Rate Parity**: The underlying economic principle linking spot and forward exchange rates with interest rates.
*   **Impact of Market Changes**: How the MTM value of an existing forward contract changes over time ($t > 0$) due to fluctuations in current spot rates and current risk-free interest rates.
*   **Time Decay**: The influence of the remaining time to maturity on the MTM value.

By simulating different market scenarios, users can gain insights into potential gains or losses for various FX forward positions (long or short).

## ✨ Features

*   **Interactive Input Controls**: Easily adjust initial contract parameters (spot rate, maturity, initial interest rates) and current market parameters (current time, current spot rate, current interest rates) using sliders and number inputs.
*   **Currency Pair Presets**: Quickly pre-fill common (synthetic) currency pair data (e.g., USD/EUR, EUR/USD, ZAR/EUR) to facilitate quick exploration.
*   **Dynamic Calculations**:
    *   Calculates the **Initial FX Forward Price** ($F_{0,f/d}(T)$) based on interest rate parity.
    *   Computes the **Current Mark-to-Market (MTM) Value** for both long ($V_t^{long}(T)$) and short ($V_t^{short}(T)$) FX forward positions.
*   **Real-time Visualization**:
    *   **MTM vs. Interest Rate Differential Plot**: Illustrates how the MTM value changes as the foreign risk-free rate varies (keeping the domestic rate constant).
    *   **MTM vs. Current Spot FX Rate Plot**: Shows the sensitivity of MTM value to changes in the prevailing spot exchange rate.
*   **Clear Formula Display**: Detailed display of the financial formulas used for forward price calculation and MTM valuation, aiding understanding.
*   **Input Validation**: Basic validation to ensure logical consistency (e.g., current time `t` cannot exceed original maturity `T`).

## 🚀 Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   `git` (for cloning the repository)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/quolab-fx-forward-mtm-analyzer.git
    cd quolab-fx-forward-mtm-analyzer
    ```
    *(Replace `your-username/quolab-fx-forward-mtm-analyzer` with the actual repository URL)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    Create a `requirements.txt` file in the root directory of your project with the following content:

    ```
    streamlit>=1.30.0
    numpy>=1.20.0
    plotly>=5.0.0
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♀️ Usage

1.  **Run the Streamlit application:**
    Ensure your virtual environment is active, then run:
    ```bash
    streamlit run app.py
    ```

2.  **Access the Application:**
    Your web browser should automatically open to `http://localhost:8501` (or a similar address) where the application is running.

3.  **Interact with the Analyzer:**
    *   **Sidebar Controls:** Use the sliders and number inputs in the left sidebar to set the `Initial Contract Parameters` (at time t=0) and `Current Market Parameters` (at time t).
    *   **Currency Pair Selection:** Use the "Select Currency Pair" dropdown to pre-populate typical values for various synthetic currency pairs.
    *   **Observe Results:** The calculated `Initial FX Forward Price` and `Current MTM Value` will update dynamically in the main area, along with the interactive plots demonstrating sensitivity to key market variables.
    *   **Interpret MTM:** Understand that a positive MTM for a long position indicates a theoretical gain, while a negative MTM indicates a theoretical loss (and vice-versa for a short position).

## 📁 Project Structure

```
quolab-fx-forward-mtm-analyzer/
├── app.py                            # Main Streamlit entry point, handles navigation and initial page setup.
├── requirements.txt                  # Lists Python dependencies for the project.
├── application_pages/                # Directory for modularizing application pages/features.
│   └── fx_forward_mtm_analyzer.py    # Contains the core logic and UI for the FX Forward MTM Analyzer.
└── README.md                         # This comprehensive README file.
```

## 🛠️ Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: The open-source app framework used to build the interactive web application.
*   **NumPy**: Used for numerical operations, particularly for generating value ranges for plots.
*   **Plotly**: Utilized for creating interactive and informative data visualizations (line charts).

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to good coding practices and includes relevant tests if applicable.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details (you might need to create this file in your repository if it doesn't exist).

**Acknowledgement:**
This lab was generated using the QuCreate platform developed by QuantUniversity. The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.

## ✉️ Contact

For questions or further information, please feel free to reach out:

*   **Project Maintainer**: [Your Name/GitHub Profile Link] (e.g., `https://github.com/your-username`)
*   **QuantUniversity**: [https://www.quantuniversity.com/](https://www.quantuniversity.com/)

---

## License

QuantUniversity License
