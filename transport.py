import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# 1. Generate synthetic data
# ----------------------------
np.random.seed(42)
routes = ["CBD-Rongai", "CBD-Thika", "CBD-Kikuyu", "CBD-Eastlands", "CBD-Kasarani"]

# Demand: number of passengers per hour per route
demand = np.random.randint(200, 800, size=len(routes))

# Supply: number of matatus assigned per route (capacity = 14 each)
supply_matatus = np.random.randint(10, 40, size=len(routes))
capacity_per_matatu = 14
supply_capacity = supply_matatus * capacity_per_matatu

# Create DataFrame
data = pd.DataFrame({
    "Route": routes,
    "Passenger_Demand": demand,
    "Matatus_Assigned": supply_matatus,
    "Total_Capacity": supply_capacity
})

# ----------------------------
# 2. Calculate shortages/excess
# ----------------------------
data["Gap"] = data["Passenger_Demand"] - data["Total_Capacity"]

suggestions = []
for i, row in data.iterrows():
    if row["Gap"] > 0:
        needed = int(np.ceil(row["Gap"] / capacity_per_matatu))
        suggestions.append(f"Add {needed} matatus to {row['Route']} (shortage of {row['Gap']} seats)")
    elif row["Gap"] < 0:
        excess = int(abs(row["Gap"]) / capacity_per_matatu)
        suggestions.append(f"Reallocate {excess} matatus from {row['Route']} (excess capacity)")
    else:
        suggestions.append(f"{row['Route']} is balanced")
data["Suggestion"] = suggestions

# ----------------------------
# 3. Streamlit Web Interface
# ----------------------------
st.title("🚐 Matatu Demand vs Supply Analysis")
st.write("This app simulates matatu passenger demand and capacity across routes, and suggests reallocation.")

# Show table
st.dataframe(data)

# Bar chart: Demand vs Capacity
st.subheader("📊 Passenger Demand vs Capacity")
fig, ax = plt.subplots()
bar_width = 0.35
x = np.arange(len(routes))
ax.bar(x, data["Passenger_Demand"], bar_width, label="Passenger Demand")
ax.bar(x + bar_width, data["Total_Capacity"], bar_width, label="Total Capacity")
ax.set_xticks(x + bar_width / 2)
ax.set_xticklabels(routes, rotation=30)
ax.set_ylabel("Number of Passengers / Seats")
ax.legend()
st.pyplot(fig)

# Download results
st.subheader("⬇️ Download Analysis")
csv = data.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "matatu_analysis.csv", "text/csv")
