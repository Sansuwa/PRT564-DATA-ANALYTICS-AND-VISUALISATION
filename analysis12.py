import pandas as pd

file_path = "2024_01 Underlying causes of death (Australia).xlsx"

# STEP 1 — Read raw data (no skipping yet)
df_raw = pd.read_excel(file_path, sheet_name="Table 1.2", header=None)

# STEP 2 — Find where real header starts
for i in range(15):
    print(i, df_raw.iloc[i, 0])

# 👉 After checking output, set correct row (usually around 4–6)
header_row = 4

# STEP 3 — Reload with proper header
df = pd.read_excel(file_path, sheet_name="Table 1.2", header=header_row)

# STEP 4 — Drop first useless column ("no.")
df = df.drop(df.columns[1], axis=1)

# STEP 5 — Rename first column
df = df.rename(columns={df.columns[0]: "Cause"})

# STEP 6 — Remove unwanted rows
df = df.dropna(subset=["Cause"])
df = df[~df["Cause"].astype(str).str.contains("Total deaths|Causes of death|CHAPTER", case=False, na=False)]

# STEP 7 — Clean column names (flatten multi-level)
new_cols = []

years = list(range(2015, 2025))
genders = ["Males", "Females", "Persons"]

for year in years:
    for gender in genders:
        new_cols.append(f"{year}_{gender}")

# Apply names (skip first column)
df.columns = ["Cause"] + new_cols[:len(df.columns)-1]

# STEP 8 — Convert to numeric
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# STEP 9 — Drop rows with too many missing values
df = df.dropna(thresh=5)

# STEP 10 — SAVE WIDE FORMAT
df.to_csv("table_1_2_wide.csv", index=False)

print("✅ Wide format saved")

# ---------------------------------------------------
# 🔥 STEP 11 — CONVERT TO LONG FORMAT (IMPORTANT)
# ---------------------------------------------------

df_long = df.melt(
    id_vars=["Cause"],
    var_name="Year_Gender",
    value_name="Deaths"
)

# Split Year and Gender
df_long[["Year", "Gender"]] = df_long["Year_Gender"].str.split("_", expand=True)

df_long = df_long.drop(columns=["Year_Gender"])

# Convert year to int
df_long["Year"] = df_long["Year"].astype(int)

# Drop missing
df_long = df_long.dropna()

# SAVE LONG FORMAT
df_long.to_csv("table_1_2_long.csv", index=False)

print("✅ Long format saved")