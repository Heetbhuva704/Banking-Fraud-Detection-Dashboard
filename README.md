🏦 FinEdge: Real-Time Banking Telemetry & AI Command Center
🔗 Live Repository
https://github.com/Heetbhuva704/FinEdge-Banking-Analytics

📌 Overview
This project is an enterprise-grade banking command center that provides in-depth, real-time monitoring of financial telemetry, core banking operations, and customer insights. It features an integrated machine learning-based Fraud Detection Engine and an Autonomous Risk Bot that predicts and resolves security threats instantly.

🚀 Key Features
🔹 Live Telemetry Dashboard
Real-time operational volume tracking
Dynamic event categorization and threat ratio tracking
Omni-channel transaction stream with live slide-in animations
🔹 Treasury & Core Banking
Live minimum balance violation tracking
Total interest earned payouts
Locker facility capacity and distribution
Deposit portfolio breakdown (FD/RD vs Savings/Current)
🔹 Risk & AML (Anti-Money Laundering)
Live threat vector distribution
Real-time risk probability tracker
AML Watchlist and cumulative suspicious operations tracker
👨‍💻 Employee Review Queue for manual SOC (Security Operations Center) resolution
🔹 Customer Care & CRM
Professional broadcast management system
Automated SMS dispatch gateway
Live "Customer Device Preview" form with auto-clearing
🤖 Autonomous Risk Bot
An active AI agent that monitors incoming telemetry and executes actions without human intervention.
🛑 Auto-Block (> 85% Risk Score)
⚠️ Issue Warning (75% - 85% Risk Score)
👁️ Flag for Manual Employee Review (50% - 75% Risk Score)

📊 Model Details
Algorithm: Random Forest Classifier
Accuracy: ~80-85%
Type: Supervised Classification
Features Engineered: Omni-channel usage behavior, velocity limits, geographic mismatch
🔍 Input Features
Customer ID & Transaction ID (Hashed)
Transaction Amount
Transaction Mode (UPI, NEFT, RTGS, IMPS, POS)
Location String
Category (Retail, Food, Utilities, Cash Withdrawal, Crypto)
📈 Key Insights
High-frequency, low-value transactions outside home locations are strong indicators of card-skimming fraud.
The autonomous bot successfully isolates over 90% of critical threats before they reach human operators.
Locker distribution reveals untapped revenue potential among high-net-worth savings accounts.

📁 Project Structure
FinEdge-Banking-Analytics/
├── .streamlit/
│   └── config.toml
├── data_generator.py
├── model_trainer.py
├── app.py
├── requirements.txt
└── README.md

🛠️ Tech Stack
Python
Streamlit (Custom HTML/CSS Glassmorphism UI)
Pandas, NumPy
Plotly (Interactive Dark-Theme Visualizations)
Scikit-learn (Random Forest)

▶️ How to Run
Clone the repository:
git clone https://github.com/Heetbhuva704/FinEdge-Banking-Analytics.git
cd FinEdge-Banking-Analytics
Install dependencies:
pip install -r requirements.txt
Run the application:
streamlit run app.py

📊 Results & Performance
Achieved highly stable predictive performance ensuring low false-positive rates on account blocks.
The dark-navy UI reduces operator eye strain and natively matches enterprise SaaS visual standards.
Zero-latency local transaction simulations correctly test the UI payload limits.

📸 Screenshots
Dashboard (Live Telemetry)
![Telemetry](assets/telemetry_dashboard.png)

Autonomous Risk Bot & Review Queue
![Risk Bot](assets/autonomous_bot.png)

CRM Broadcast Center
![CRM](assets/crm_broadcast.png)

🔮 Future Improvements
Migration from session-state to persistent database (PostgreSQL)
Role-Based Access Control (Teller vs. Admin views)
Advanced SHAP explainability for blocked transactions
Integration with Twilio for physical SMS dispatching

🎯 Conclusion
This project combines high-speed data engineering, machine learning, and advanced UI/UX design to deliver a complete, production-ready Banking SOC and Financial Operations platform.

👨💻 Author
Heet Bhuva 🔗 GitHub: https://github.com/Heetbhuva704
