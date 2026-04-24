import pandas as pd

file_path = "2024_01 Underlying causes of death (Australia).xlsx"

# STEP 1 — Load data
df = pd.read_excel(file_path, sheet_name="Table 1.3", skiprows=5)

# STEP 2 — Rename columns
df.columns = [
    "Cause",
    "Male_Deaths", "Female_Deaths", "Total_Deaths",
    "Male_Rate", "Female_Rate", "Total_Rate"
]

# STEP 3 — Drop empty rows
df = df.dropna(how="all")

# STEP 4 — Identify AGE GROUP rows
age_groups = [
    "All persons", "Under 1 year", "1–14 years", "15–24 years",
    "25–34 years", "35–44 years", "45–54 years",
    "55–64 years", "65–74 years", "75–84 years",
    "85–94 years", "95 years and over"
]

# Create new column
df["Age_Group"] = None

current_age = None

for i in range(len(df)):
    value = str(df.loc[i, "Cause"]).strip()
    
    if value in age_groups:
        current_age = value
        df.loc[i, "Age_Group"] = current_age
    else:
        df.loc[i, "Age_Group"] = current_age

# STEP 5 — Remove age group rows themselves
df = df[~df["Cause"].isin(age_groups)]

# STEP 6 — Remove unwanted rows
df = df[~df["Cause"].str.contains("All causes", case=False, na=False)]

# STEP 7 — Clean weird values
df = df.replace({"np": None, "—": None})

# STEP 8 — Convert numeric columns
for col in df.columns[1:7]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# STEP 9 — Drop rows with missing key values
df = df.dropna(subset=["Total_Deaths"])

# STEP 10 — Final structure
df = df[[
    "Cause", "Age_Group",
    "Male_Deaths", "Female_Deaths", "Total_Deaths",
    "Male_Rate", "Female_Rate", "Total_Rate"
]]

# STEP 11 — Save
df.to_csv("table_1_3_cleaned.csv", index=False)

print("Table 1.3 cleaned successfully!")
print(df.head())