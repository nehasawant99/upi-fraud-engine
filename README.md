🛡️ UPI Fraud Detection & Risk Scoring Engine  

A full‑stack fraud intelligence platform that simulates cyber‑attacks, scores transaction risks, and visualizes suspicious activity in real time. Built with **Flask**, **Pandas**, **Plotly/Dash**, and **NetworkX**, this project transforms raw UPI transaction data into actionable fraud insights.  

---

🚀 Features  
- **Risk Scoring Engine**  
  Calculates transaction risk based on amount anomalies, device history, and behavioral patterns.  
- **User Risk Profiles**  
  Summarizes each user’s average risk score, number of high‑risk transactions, and most common fraud reasons.  
- **Interactive Dashboards**  
  Clickable, filterable charts built with Plotly/Dash for fraud trend exploration.  
- **Network Diagrams**  
  Graphs linking users, devices, and transactions, with edge colors showing severity (red = High, orange = Medium, green = Low).  
- **Executive Reporting**  
  CSV exports and visual summaries for compliance and audit teams.  

---

📂 Project Structure  
```
├── data/
│   └── transactions.csv        # Input dataset
├── output/
│   └── fraud_report.csv        # Generated fraud report
├── src/
│   └── risk_engine.py          # Core risk scoring logic
├── main.py                     # Dashboard + analysis pipeline
└── README.md                   # Project documentation
```

---

🛠️ Tech Stack  
- Backend: Flask, Pandas  
- Visualization: Matplotlib, Seaborn, Plotly, Dash  
- Graph Analysis: NetworkX  
- Data: Synthetic UPI transaction dataset  

---

📊 Sample Visuals  
- Risk level distribution bar chart  
- Risk score trend line chart  
- Top fraud reasons bar chart  
- User–Device–Transaction network diagram  

---

⚡ Getting Started  
1. Clone the repo:  
   ```bash
   git clone https://github.com/nehasawant99/upi-fraud-engine.git
   ```
2. Install dependencies:  
   ```bash
   pip install pandas matplotlib seaborn plotly dash networkx
   ```
3. Run the dashboard:  
   ```bash
   python main.py
   ```
4. Open in browser: `http://127.0.0.1:8050`  

---

🔍 Future Enhancements  
- Real‑time streaming with Kafka  
- Geo‑location anomaly detection  
- Machine learning models for predictive fraud scoring  
- Role‑based dashboards (executive vs developer view)  

---

🏆 Why It’s Unique  
Unlike static fraud reports, this engine combines **risk scoring, interactive dashboards, and network analysis** into one cohesive platform — making fraud detection **visual, explainable, and actionable**.  

