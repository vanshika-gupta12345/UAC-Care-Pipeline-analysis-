# 🛡️ Care Transition Efficiency & Placement Outcome Analytics

## 📌 Project Overview
This project reframes the UAC dataset from a simple capacity-monitoring lens to a **process efficiency and outcome evaluation lens**. By analyzing how effectively children move from CBP custody to HHS care and eventually to vetted sponsors, this tool identifies systemic bottlenecks and provides actionable insights for policy reform.

## 🚀 Key Features
* **Dynamic Dashboard:** A high-end Streamlit web application for real-time monitoring.
* **Process Modeling:** Tracks the care pipeline as a flow system: `CBP Intake` → `HHS Care` → `Sponsor Placement`.
* **KPI Intelligence:** Calculation of Transfer Efficiency Ratios, Discharge Effectiveness, and Backlog Accumulation Rates.
* **Bottleneck Detection:** Automated visualization of stagnation periods and supply-demand imbalances.

## 📊 Calculated KPIs
* **Transfer Efficiency Ratio:** Measures the speed of movement from CBP to HHS.
* **Discharge Effectiveness Index:** Evaluates the success rate of sponsor placements.
* **Backlog Accumulation Rate:** Tracks the net daily volume change to predict system overflow.
* **Outcome Stability Score:** Measures the consistency of reunification success over time.

## 🛠️ Technology Stack
* **Language:** Python 3.9+
* **Analysis:** Pandas, NumPy, Scipy
* **Visualization:** Plotly (Interactive), Matplotlib/Seaborn (Static)
* **Dashboard:** Streamlit

## 📂 Project Structure
* `app.py`: The frontend code for the dynamic dashboard.
* `analysis.py`: The backend engine that processes the raw data and engineers features.
* `requirements.txt`: List of necessary Python libraries.
* `HHS_Unaccompanied_Alien_Children_Program.csv`: The source dataset.

## ⚙️ Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/uac-analytics.git](https://github.com/your-username/uac-analytics.git)
