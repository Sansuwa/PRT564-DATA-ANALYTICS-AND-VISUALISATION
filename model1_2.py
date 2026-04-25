# ==============================
# FULL DATA ANALYSIS (FINAL VERSION)
# ==============================

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import ttest_rel
import os

sns.set(style="whitegrid")


# ==============================
# 2. Load Data
# ==============================
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "table_1_5_cleaned.csv")

df = pd.read_csv(file_path)

print("Data Loaded Successfully")
print(df.head())


# ==============================
# 3. Data Preparation
# ==============================

# Standardise column names
df.rename(columns={"Sex": "Gender"}, inplace=True)

# Remove 'Persons' (optional for cleaner gender comparison)
df = df[df["Gender"] != "Persons"]

# Remove zero values (optional)
df = df[df["Deaths"] > 0]

# Ensure correct data types
df["Year"] = df["Year"].astype(int)
df["Deaths"] = df["Deaths"].astype(float)

print("\nCleaned Data:")
print(df.head())


# ==============================
# 4. Time Series Analysis
# ==============================
trend = df.groupby("Year")["Deaths"].sum()

plt.figure()
trend.plot(marker='o')
plt.title("Total Deaths Over Time")
plt.xlabel("Year")
plt.ylabel("Deaths")
plt.show()


# ==============================
# 5. Gender Analysis
# ==============================
gender = df.groupby("Gender")["Deaths"].sum()

plt.figure()
gender.plot(kind='bar')
plt.title("Deaths by Gender")
plt.ylabel("Deaths")
plt.show()


# ==============================
# 6. Top Diseases Analysis
# ==============================
top_diseases = df.groupby("Cause")["Deaths"].sum().sort_values(ascending=False).head(10)

plt.figure()
top_diseases.plot(kind='barh')
plt.title("Top 10 Diseases by Deaths")
plt.xlabel("Deaths")
plt.show()


# ==============================
# 7. Correlation Analysis
# ==============================
pivot = df.pivot_table(values="Deaths", index="Year", columns="Gender")

plt.figure()
sns.heatmap(pivot.corr(), annot=True)
plt.title("Correlation Heatmap")
plt.show()


# ==============================
# 8. Regression Dataset
# ==============================
reg_data = df.groupby("Year")["Deaths"].sum().reset_index()

X = reg_data[["Year"]]
y = reg_data["Deaths"]


# ==============================
# 9. Train Regression Models
# ==============================
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Random Forest": RandomForestRegressor(random_state=42)
}

results = {}

for name, model in models.items():
    model.fit(X, y)
    preds = model.predict(X)
    
    mse = mean_squared_error(y, preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, preds)
    
    results[name] = {"MSE": mse, "RMSE": rmse, "R2": r2}
    
    # Plot Actual vs Predicted
    plt.figure()
    plt.scatter(X, y)
    plt.plot(X, preds)
    plt.title(f"{name}: Actual vs Predicted")
    plt.xlabel("Year")
    plt.ylabel("Deaths")
    plt.show()


# ==============================
# 10. Model Performance
# ==============================
results_df = pd.DataFrame(results).T
print("\nModel Performance:")
print(results_df)


# ==============================
# 11. Best Model Visualization
# ==============================
best_model = RandomForestRegressor(random_state=42)
best_model.fit(X, y)
preds = best_model.predict(X)

plt.figure()
plt.plot(X, y, label="Actual")
plt.plot(X, preds, label="Predicted")
plt.legend()
plt.title("Actual vs Predicted Deaths (Best Model)")
plt.xlabel("Year")
plt.ylabel("Deaths")
plt.show()


# ==============================
# 12. Statistical Testing (Paired T-Test)
# ==============================
lin_preds = LinearRegression().fit(X, y).predict(X)
rf_preds = RandomForestRegressor(random_state=42).fit(X, y).predict(X)

t_stat, p_value = ttest_rel(lin_preds, rf_preds)

print("\nT-Test Results:")
print("T-statistic:", t_stat)
print("P-value:", p_value)

if p_value < 0.05:
    print("Result: Significant difference between models")
else:
    print("Result: No significant difference between models")


# ==============================
# 13. Extra Insight: Disease Trend Example
# ==============================
# Show trend for one major disease
example_disease = df["Cause"].value_counts().index[0]
disease_trend = df[df["Cause"] == example_disease].groupby("Year")["Deaths"].sum()

plt.figure()
disease_trend.plot(marker='o')
plt.title(f"Trend for {example_disease}")
plt.xlabel("Year")
plt.ylabel("Deaths")
plt.show()


# ==============================
# END
# ==============================