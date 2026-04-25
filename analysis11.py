import pandas as pd

file_path = "/Users/manishagautam/Desktop/Git - Data/PRT564-DATA-ANALYTICS-AND-VISUALISATION/2024_01 Underlying causes of death (Australia).xlsx"

# STEP 1 — Load the CORRECT sheet
df = pd.read_excel(file_path, sheet_name="Table 1.1", skiprows=7)

# STEP 2 — Check data
print("Initial shape:", df.shape)
print(df.head(10))
print("Columns:", df.columns)
print("Number of columns:", len(df.columns))


# STEP 3 — Drop empty columns and rows
df = df.dropna(axis=1, how='all')
df = df.dropna(how='all')
df = df.reset_index(drop=True)


# STEP 4 — Keep only first 13 columns (actual data)
df = df.iloc[:, :13]


# STEP 5 — Rename columns
df.columns = [
    "Cause",
    "Male_Deaths", "Female_Deaths", "Total_Deaths",
    "Male_CrudeRate", "Female_CrudeRate", "Total_CrudeRate",
    "Male_StdRate", "Female_StdRate", "Total_StdRate",
    "Male_YPLL", "Female_YPLL", "Total_YPLL"
]


# STEP 6 — Clean rows
df = df.dropna(subset=["Cause"])
df = df[~df["Cause"].astype(str).str.contains("Total|All", case=False, na=False)]


# STEP 7 — Convert numbers
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()


# STEP 8 — Final check
print("\nCleaned Data:")
print(df.head())
print("\nFinal shape:", df.shape)


# STEP 9 — Save cleaned data
df.to_csv("table_1_1_cleaned.csv", index=False)

print("\n✅ DONE — cleaned_data.csv saved!")
