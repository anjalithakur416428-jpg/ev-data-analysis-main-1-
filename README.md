# 🏎️ EV Trends Analysis & Forecasting System

A professional, high-performance analytical dashboard designed to track, analyze, and forecast Electric Vehicle (EV) population trends, range evolution, and geographic adoption patterns.

## 🚀 Key Features

### 📊 Performance & Forecasting
*   **2030 Range Projection**: Linear regression models forecasting average EV range growth through the next decade.
*   **Tech Maturity Profile**: Advanced violin plots analyzing range distribution across top manufacturers (Tesla, Chevrolet, Nissan, etc.).
*   **Innovation Index**: Benchmarking brands by model variety and technological diversity.

### 🌍 Advanced Geo Analysis
*   **Multi-Mode Mapping**: Switch between **Density Heatmaps**, **Vehicle Point Explorers**, and **Regional Bubble Maps**.
*   **Urban Insights**: Identification of the Top 10 EV Cities and market share analysis by Legislative District.

### 📈 Growth Trends
*   **Adoption S-Curves**: Cumulative growth tracking for market leaders.
*   **Market Velocity (YoY)**: Year-over-year percentage growth analysis to identify adoption acceleration.
*   **Fleet Maturity**: Segmentation of the fleet into Legacy, Mass Market, and Modern eras.

### 📄 Pro Explorer
*   **Data Integrity Suite**: Automatic scanning for missing values and data quality issues.
*   **Dynamic Data Grid**: Interactive exploration of raw vehicle records.
*   **CSV Export**: One-click download of filtered datasets for external reporting.

## 🛠️ Technical Stack
*   **Language**: Python 3.10+
*   **Dashboard**: Streamlit
*   **Visualizations**: Plotly (Interactive Charts & Mapbox)
*   **Data Processing**: Pandas & NumPy
*   **Coordinate Extraction**: Custom Regex-based parser for "Vehicle Location" strings.

## 📦 Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install streamlit pandas plotly numpy
   ```

2. **Run the Dashboard**:
   ```bash
   streamlit run analysis_dashboard.py
   ```

## 📂 Project Structure
*   `analysis_dashboard.py`: Main application code with multi-tab layout and analytical logic.
*   `Electric_Vehicle_Population_Data.csv`: Primary dataset (ensure this is in the root directory).
*   `README.md`: Documentation and project overview.

---
**Developed for Advanced EV Market Research & Forecasting.**
