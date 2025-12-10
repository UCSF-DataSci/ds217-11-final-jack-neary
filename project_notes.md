# Q1 setup and exploration
- loaded data
- got data shape, col names, data types, date range, missing values and percentages for each column
- got all numeric columns and descriptive statistics
- 3 plots look pretty good, two histograms and one time series (air temp over time)

# Q2 data cleaning
- printed all datatypes; converted measurement timestamp to datetime and made this the index; precipitation type changed to string
- found all missing values, columns with many missing values were forward filled, which is acceptable with timeseries data because it uses the most recent value to impute the missing value(s) preserving temporal sequence
- missing values for barometric pressure column were dropped because it was such a low percentage (<5%) therefore can drop and won't harm any modeling down the line
- cleaned data from 196,138 rows to 149,408 after handling for outliers

# Q3 Data Wrangling
- *for Q3_datetime_info might have to use another method for datetime parsing.. maybe*
*dateutil.relativedelta because I can't get the all the, correct, info with my current method*
- successfully wrangled data, set to datetime, set as index (then unset) and saved to .csv

# Q4 Feature engineering
- calculated dew_point using Air Temperature and Humidity
- calculated gust_factor using Maximum Wind Speed / Wind Speed(median)
- log transformed all columns to try to improve right skewness and worked for some columns
- calculated rolling barometric pressure (7hr and 12hr)
- calculated rolling humidity (12hr and 24hr)

# Q5 Pattern analysis
- plotted a heatmap of the correlation coefficients for *most* variables
- looking at the heatmap made decisions of what variables can be predictors (making sure to choose ones that weren't used to calculate each other)
- good to know so not to include highly correlated variables b/c of multicolinearity when we bulid out our model
- 



# Important: look over
