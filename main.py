import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.risk_engine import calculate_risk

df = pd.read_csv("data/transactions.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

results = []

for user in df["user_id"].unique():
    user_data = df[df["user_id"] == user]
    avg_amount = user_data["amount"].mean()
    known_devices = []

    for _, row in user_data.iterrows():
        score, reasons = calculate_risk(row, avg_amount, known_devices)
        known_devices.append(row["device_id"])

        if score >= 60:
            level = "High"
        elif score >= 30:
            level = "Medium"
        else:
            level = "Low"

        results.append({
         "transaction_id": row["transaction_id"],
         "user_id": row["user_id"],
         "device_id": row["device_id"],   # ✅ include device_id here
         "risk_score": score,
         "risk_level": level,
         "reasons": ", ".join(reasons)
})


report = pd.DataFrame(results)
report.to_csv("output/fraud_report.csv", index=False)
print(report)


import plotly.express as px
import dash
from dash import dcc, html, dash_table
import networkx as nx
import io
import base64

# Load fraud report
report = pd.read_csv("output/fraud_report.csv")

# --- User Risk Profiles ---
user_profiles = report.groupby("user_id").agg(
    avg_risk_score=("risk_score", "mean"),
    high_risk_count=("risk_level", lambda x: (x == "High").sum()),
    common_reasons=("reasons", lambda x: (
        pd.Series(", ".join(x.dropna().astype(str)))
        .str.split(", ")
        .explode()
        .value_counts()
        .idxmax() if len(x.dropna()) > 0 else "None"
    ))
).reset_index()


# --- Interactive Charts ---
fig_dist = px.histogram(report, x="risk_level", color="risk_level", title="Risk Level Distribution")
fig_trend = px.line(report, x="transaction_id", y="risk_score", color="risk_level", title="Risk Score Trend")
reason_counts = report["reasons"].str.split(", ").explode().value_counts()
fig_reasons = px.bar(x=reason_counts.values, y=reason_counts.index, orientation="h", title="Top Risk Reasons")

# --- Network Diagram ---
G = nx.Graph()
for _, row in report.iterrows():
    user = f"User {row['user_id']}"
    device = f"Device {row['device_id']}"
    G.add_node(user, color="blue")
    G.add_node(device, color="red")
    G.add_edge(user, device, risk=row["risk_level"])

plt.figure(figsize=(8,6))
colors = ["blue" if G.nodes[n]["color"]=="blue" else "red" for n in G.nodes]

# Build edge colors based on risk level
edge_colors = []
for u, v, d in G.edges(data=True):
    if d["risk"] == "High":
        edge_colors.append("red")
    elif d["risk"] == "Medium":
        edge_colors.append("orange")
    else:
        edge_colors.append("green")

nx.draw(G, with_labels=True, node_color=colors, edge_color=edge_colors, font_size=8)
plt.title("User–Device–Transaction Network")


buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)
network_img = base64.b64encode(buf.read()).decode("utf-8")
plt.close()

# --- Dash App Layout ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Fraud Intelligence Dashboard"),

    html.H2("User Risk Profiles"),
    dash_table.DataTable(
        data=user_profiles.to_dict("records"),
        columns=[{"name": i, "id": i} for i in user_profiles.columns],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"}
    ),

    html.H2("Interactive Charts"),
    dcc.Graph(figure=fig_dist),
    dcc.Graph(figure=fig_trend),
    dcc.Graph(figure=fig_reasons),

    html.H2("Network Diagram"),
    html.Img(src="data:image/png;base64,{}".format(network_img), style={"width":"80%"})
])

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)

# --- Visualization Section ---
# Risk level distribution
plt.figure(figsize=(6,4))
sns.countplot(data=report, x="risk_level", palette="coolwarm")
plt.title("Distribution of Risk Levels")
plt.xlabel("Risk Level")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.show()

# Risk score trend over time
plt.figure(figsize=(10,5))
sns.lineplot(data=report, x="transaction_id", y="risk_score", hue="risk_level", marker="o")
plt.title("Risk Score Trend by Transaction")
plt.xlabel("Transaction ID")
plt.ylabel("Risk Score")
plt.legend(title="Risk Level")
plt.tight_layout()
plt.show()

# Top reasons contributing to risk
reason_counts = report["reasons"].str.split(", ").explode().value_counts()
plt.figure(figsize=(8,5))
sns.barplot(x=reason_counts.values, y=reason_counts.index, palette="viridis")
plt.title("Top Risk Reasons")
plt.xlabel("Count")
plt.ylabel("Reason")
plt.tight_layout()
plt.show()
