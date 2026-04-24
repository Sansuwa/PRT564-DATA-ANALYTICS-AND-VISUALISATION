import pandas as pd

file_path = "2024_01 Underlying causes of death (Australia).xlsx"

# STEP 1 — Load data
df = pd.read_excel(file_path, sheet_name="Table 1.4", skiprows=5)

# STEP 2 — Drop the "no." column (usually 2nd column)
df = df.drop(df.columns[1], axis=1)

# STEP 3 — Rename first column
df = df.rename(columns={df.columns[0]: "Cause"})

# STEP 4 — Fix year column names
years = list(range(2015, 2025))
df.columns = ["Cause"] + years[:len(df.columns)-1]

# STEP 5 — Drop empty rows
df = df.dropna(how="all")

# STEP 6 — Identify AGE GROUPS
age_groups = [
    "All persons", "Under 1 year", "1–14 years", "15–24 years",
    "25–34 years", "35–44 years", "45–54 years",
    "55–64 years", "65–74 years", "75–84 years",
    "85–94 years", "95 years and over"
]

df["Age_Group"] = None
current_age = None

for i in range(len(df)):
    value = str(df.loc[i, "Cause"]).strip()
    
    if value in age_groups:
        current_age = value
    df.loc[i, "Age_Group"] = current_age

# STEP 7 — Remove age group header rows
df = df[~df["Cause"].isin(age_groups)]

# STEP 8 — Remove unwanted rows
df = df[~df["Cause"].str.contains("All causes", case=False, na=False)]

# STEP 9 — Convert numeric values
for col in years:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# STEP 10 — Convert to LONG FORMAT (IMPORTANT)
df_long = df.melt(
    id_vars=["Cause", "Age_Group"],
    var_name="Year",
    value_name="Deaths"
)

# STEP 11 — Drop missing values
df_long = df_long.dropna()

# STEP 12 — Save
df_long.to_csv("table_1_4_cleaned.csv", index=False)

print("Table 1.4 cleaned successfully!")
print(df_long.head())