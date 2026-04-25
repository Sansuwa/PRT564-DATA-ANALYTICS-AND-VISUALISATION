import pandas as pd

file_path = "2024_01 Underlying causes of death (Australia).xlsx"

# STEP 1 — Load the sheet
df = pd.read_excel(file_path, sheet_name="Table 1.5", skiprows=6)

print("Initial shape:", df.shape)

# STEP 2 — Drop the "no." column
df = df.drop(df.columns[1], axis=1)

# STEP 3 — Rename first column
df = df.rename(columns={df.columns[0]: "Cause"})

# STEP 4 — Create proper column names
years = list(range(2015, 2025))
new_cols = ["Cause"]

for year in years:
    new_cols.extend([f"{year}_Male", f"{year}_Female", f"{year}_Total"])

# Adjust in case of mismatch
df.columns = new_cols[:len(df.columns)]

# STEP 5 — Remove empty rows
df = df.dropna(how="all")

# STEP 6 — Remove unwanted rows
df = df[~df["Cause"].str.contains("Total deaths", case=False, na=False)]
df = df[~df["Cause"].str.contains("CHAPTER", case=False, na=False)]

# STEP 7 — Convert values to numeric
for col in df.columns[1:]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "")
        .str.replace("np", "")
        .str.replace("—", "")
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# STEP 8 — Convert to LONG FORMAT
df_long = df.melt(id_vars="Cause", var_name="Year_Sex", value_name="Deaths")

# STEP 9 — Split Year and Sex
df_long[["Year", "Sex"]] = df_long["Year_Sex"].str.split("_", expand=True)

# STEP 10 — Clean final dataset
df_long = df_long.drop(columns=["Year_Sex"])
df_long = df_long.dropna()

# STEP 11 — Save
df_long.to_csv("table_1_5_cleaned.csv", index=False)

print("Table 1.5 cleaned successfully!")
print(df_long.head())
