#impot Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from scipy.stats import ttest_rel

#Load Dataset
df = pd.read_csv("table_1_5_cleaned.csv")
print(df.head())
print(df.info())

# Processing for modeling
# Convert Year and Deaths to numeric
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce")

# Remove missing values
df = df.dropna()

# Encode Sex column
df["Sex_Code"] = df["Sex"].astype("category").cat.codes
print(df.head())

# MODEL 1: Simple Linear Regression
# Predict deaths using Year only
X1 = df[["Year"]]
y = df["Deaths"]
X_train1, X_test1, y_train, y_test = train_test_split(
    X1, y, test_size=0.2, random_state=42
)
linear_model = LinearRegression()
linear_model.fit(X_train1, y_train)
linear_pred = linear_model.predict(X_test1)
linear_rmse = np.sqrt(mean_squared_error(y_test, linear_pred))
linear_r2 = r2_score(y_test, linear_pred)
print("\nMODEL 1: Linear Regression")
print("Coefficient:", linear_model.coef_)
print("Intercept:", linear_model.intercept_)
print("RMSE:", linear_rmse)
print("R2:", linear_r2)

# MODEL 2: Multiple Linear Regression
# Predict deaths using Year + Sex
X2 = df[["Year", "Sex_Code"]]
X_train2, X_test2, y_train, y_test = train_test_split(
    X2, y, test_size=0.2, random_state=42
)
multi_model = LinearRegression()
multi_model.fit(X_train2, y_train)
multi_pred = multi_model.predict(X_test2)
multi_rmse = np.sqrt(mean_squared_error(y_test, multi_pred))
multi_r2 = r2_score(y_test, multi_pred)
print("\nMODEL 2: Multiple Linear Regression")
print("Coefficients:", multi_model.coef_)
print("Intercept:", multi_model.intercept_)
print("RMSE:", multi_rmse)
print("R2:", multi_r2)

# MODEL 3: Poisson Regression
# Suitable because deaths are count data
X3 = df[["Year", "Sex_Code"]]
X3 = sm.add_constant(X3)
y3 = df["Deaths"]
poisson_model = sm.GLM(
    y3,
    X3,
    family=sm.families.Poisson())
poisson_results = poisson_model.fit()
print("\nMODEL 3: Poisson Regression")
print(poisson_results.summary())
print("Poisson AIC:", poisson_results.aic)

# Statistical Test
# Compare Linear Regression vs Multiple Linear Regression
t_stat, p_value = ttest_rel(linear_pred, multi_pred)
print("\nStatistical Test")
print("T-statistic:", t_stat)
print("P-value:", p_value)
if p_value < 0.05:
    print("Result: Significant difference between models")
else:
    print("Result: No significant difference between models")

# Model Comparison Table
comparison = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Multiple Linear Regression",
        "Poisson Regression"
    ],
    "RMSE": [
        linear_rmse,
        multi_rmse,
        "N/A"
    ],
    "R2": [
        linear_r2,
        multi_r2,
        "N/A"
    ],
    "AIC": [
        "N/A",
        "N/A",
        poisson_results.aic
    ]
})
print("\nModel Comparison")
print(comparison)

# Save results
comparison.to_csv("model_comparison_results.csv", index=False)

print("\nDone! Model comparison saved.")







