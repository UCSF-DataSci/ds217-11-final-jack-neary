# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime

# Load data from Q1 (or directly from source)
df = pd.read_csv('data/beach_sensors.csv')
# If you saved cleaned data from Q1, you can load it:
# df = pd.read_csv('output/q1_exploration.csv')  # This won't work - load original

# Q1
# check datatypes in dataset
original_df = df.copy()
df_dtypes = df.dtypes
print(f"These are the datatypes:\n{df_dtypes}")

# change Measurement Timestamp to datetime
df['Measurement Timestamp'] = pd.to_datetime(df['Measurement Timestamp'])
# change precipitation type to categorical
df['Precipitation Type'] = df['Precipitation Type'].astype('category')
print(df['Precipitation Type'].cat.categories)
print(df['Precipitation Type'].isna().sum())


# handle duplicates
dups = df.duplicated().sum() 
print(f"There are {dups} duplicates")

# check and handle missing values in dataset
missing = df.isna().sum()
print(f"These are all the missing values: {missing}")


# TODO:handle negative values
df['Rain Intensity'] = df['Rain Intensity'].clip(lower=0, upper=5)
df['Interval Rain'] = df['Interval Rain'].clip(lower=0,upper=25) # give reasoning for upper bound
df['Total Rain'] = df['Total Rain'].clip(lower=0, upper=200)
df['Solar Radiation'] = df['Solar Radiation'].clip(lower=0, upper=None) # give reasoning for upper bound
# TODO:handle extremely high values
df['Wind Speed'] = df['Wind Speed'].clip(lower=0, upper=18)# give reasoning for upper bound (highest value ever recorded was 39.. in 1894)
df['Maximum Wind Speed'] = df['Maximum Wind Speed'].clip(lower=0, upper=24) # give reasoning for upper bound (highest value ever recorded was 39, there were more 'high values than the 'Wind Speed' col, therefore higher max)
df['Barometric Pressure'] = df['Barometric Pressure'].clip(lower=800, upper=1050) # give reasoning for upper bound
df['Solar Radiation'] = df['Solar Radiation'].clip(lower=0, upper=1100) # give reasoning for upper bound

# TODO:look within columns to figure out which need further handling
# TODO:ffill / bfill, drop missing where <5%

cols_lots_missing = ['Wet Bulb Temperature', 'Total Rain', 'Heading']
"""
for col in df.columns:
    perc_missing = df[col].isna().mean()
    if perc_missing > 0.05:
        cols_lots_missing.append(col)
"""
df[cols_lots_missing] = df[cols_lots_missing].ffill()  #forward filled all with many missing columns
df = df.dropna(subset = ['Barometric Pressure', 'Air Temperature']) #dropping barometric pressure and air temperature missing values because < 5% missing
df_after_missing = df.copy()
df_after_missing[['Wind Speed', 'Maximum Wind Speed']] = df_after_missing[['Wind Speed', 'Maximum Wind Speed']].clip(lower=0, upper=60) # clip interval rain
print("Forward filled missing values in columns with many missing; dropped rows where Barometric Pressure and Air Temperature were missing")


# check for outliers and filter values beyond 3 standard deviations, for 'Wet Bulb Temperature', 'Total Rain', 'Heading'

df_clean = df_after_missing.copy()

for col in cols_lots_missing:
    mean, std = df_clean[col].mean(), df_clean[col].std()
    lower, upper = mean - 3*std, mean + 3*std
    df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]

print(f"Rows after removing outliers: {df_clean.shape[0]}")

# now handle for rain intensity and precipitation
# cap rain intensity at 85, then take mean or median for outlier handling?


df_clean.to_csv('output/q2_cleaned_data.csv', index = False)
print("Saved cleaned data to csv!")