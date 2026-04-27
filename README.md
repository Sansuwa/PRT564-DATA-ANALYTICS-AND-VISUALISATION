
# Mortality Patterns in Australia (2015–2024)

## Project Overview
This project performs an in-depth data analysis and predictive modeling of mortality patterns in Australia between 2015 and 2024. By integrating multiple heterogeneous datasets, our team developed a data pipeline to preprocess, analyze, and model death counts across various causes, genders, and age groups.

## Key Objectives
* **Data Pipeline Construction:** Build a robust pipeline to clean and integrate raw data from multiple sources.
* **Exploratory Data Analysis (EDA):** Identify trends in mortality over time and correlation between demographic groups.
* **Predictive Modeling:** Implement and evaluate multiple regression models (Linear, Ridge, Random Forest, Poisson) to predict mortality counts.
* **Classification:** Differentiate between cancer-related and non-cancer-related causes of death using Decision Tree classifiers.

## Data Analysis Pipeline


## Technologies Used
* **Python:** Primary language for analysis.
* **Pandas & NumPy:** Data manipulation and cleaning.
* **Scikit-Learn:** Model development (Linear Regression, Ridge, Random Forest, Decision Tree).
* **Statsmodels:** Poisson regression implementation.
* **Matplotlib & Seaborn:** Data visualization.

## Results Summary
Our analysis demonstrates that mortality data is highly non-linear, with **Random Forest Regression** providing the best predictive accuracy ($R^2 \approx 0.99$). Key drivers of mortality trends identified include COVID-19, malignant neoplasms, and general symptomatic conditions.

| Model | RMSE | $R^2$ |
| :--- | :--- | :--- |
| Linear (Full) | 2499.68 | 0.0047 |
| Random Forest | 210.10 | 0.9929 |

## Project Structure
* `/`: Jupyter notebooks containing the analysis code.
* `/Datasets`: Contains raw and processed data (Table 1.3 & 1.5).
* `/Results`: Generated figures and CSV result files.

## How to Run
1. Clone the repository.
2. Ensure you have the required libraries installed:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn statsmodels openpyxl
   ```
3. Run the cleaning scripts first, then execute the main analysis notebook.

## Authors
* [Sansuwa Shrestha]
* [Name 2]
* [Name 3]
