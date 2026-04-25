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


