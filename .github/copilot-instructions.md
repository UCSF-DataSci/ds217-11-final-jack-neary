# AI Coding Instructions for Chicago Beach Weather Sensors Analysis

This is a **data science course final exam project** implementing a complete 9-phase data analysis workflow on the Chicago Beach Weather Sensors dataset from the City of Chicago. The project focuses on predicting air or water temperature using sensor measurements.

## Project Architecture

The project follows a **sequential 9-phase workflow** where each phase builds on previous outputs:

```
Q1: Setup & Exploration → Q2: Data Cleaning → Q3: Data Wrangling → Q4: Feature Engineering
         ↓                      ↓                    ↓                     ↓
    EDA, stats            Imputation, outliers  Temporal index,       New features,
    visualizations        removal/capping       datetime parsing      transformations
         ↓                      ↓                    ↓                     ↓
Q5: Pattern Analysis → Q6: Modeling Prep → Q7: Modeling → Q8: Results → Q9: Writeup
     Correlations        Train/test split     Model training      Visualizations      Report
     Feature selection   Feature selection    Evaluation          Summary tables
```

**Key Data Characteristics:**
- **Time series data** with irregular sampling intervals from multiple beach sensors
- **Sensor dropouts** and missing data periods (not random MCAR, but systematic)
- **Chicago Beach Weather Dataset**: Air temp, water temp, wind speed, humidity, pressure, precipitation
- **~195K rows initially → ~150K after cleaning** (outlier removal impacts significantly)

## Critical Workflows & Patterns

### 1. Data Loading & Datetime Handling
- **Always parse `Measurement Timestamp` as datetime**: `pd.to_datetime(df['Measurement Timestamp'])`
- **Time series operations require datetime index**: Use `df.set_index('Measurement Timestamp')` for resampling
- **Forward-fill is appropriate for sensor data**: `df.ffill()` preserves temporal continuity (don't use simple mean imputation for time series)
- See `q1_setup_exploration.md` and `project_notes.md` for patterns

### 2. Outlier Handling Strategy
Used in actual implementation (`q2_written_out.py`):
- **Clipping by domain knowledge** (e.g., wind speed max 18-24 m/s based on historical records)
- **3-sigma filtering** for columns with many missing values
- **Column-specific bounds**: 
  - Rain columns: clip to physically realistic ranges (0-25mm for interval rain, 0-200mm for total)
  - Wind: 0-18 m/s (historical record 39 m/s in 1894, but sensor range typically lower)
  - Pressure: 800-1050 hPa
  - Solar radiation: 0-1100 W/m²
- **Skip percentage threshold**: Drop rows with missing values only if <5%; otherwise forward-fill

### 3. Feature Engineering Pipeline
From `project_notes.md`, the workflow is:
1. **Calculated features**: Dew point (from temp + humidity), gust factor (max wind / median wind)
2. **Log transformations**: Apply to right-skewed distributions (check results)
3. **Rolling statistics**: 7h, 12h, 24h rolling means for pressure, humidity (create lagged temporal features)
4. **Exclude non-predictive columns**: Station names, IDs, measurement labels, `Precipitation Type` (categorical)

**Multicollinearity concern**: Don't include both a raw variable AND its rolling mean in the same model (correlation > 0.99)

### 4. File I/O Conventions
Each question requires **exactly 3 artifacts** saved to `output/` directory with **specific formats**:

- **CSV files**: Always use `index=False` when saving
- **Text files**: Plain UTF-8, clean formatting (see `q8_results.md` for exact format examples)
- **PNG visualizations**: `dpi=150` or higher, clear axis labels, subplots with titles
- **Data passes validation**: Filenames are case-sensitive and exact

Example validation from `HINTS.md`:
```bash
ls -lh output/qX_filename.ext  # Verify exists
pd.read_csv('output/q1_exploration.csv').columns  # Check column names
wc -l output/q2_cleaning_report.txt  # Verify has content
```

### 5. Data Leakage Prevention (Critical for Q7)
From `q7_modeling.md` warnings:
- **Circular prediction logic**: Don't use `air_temp_rolling_7h` to predict `Air Temperature` (it IS the target)
- **Suspicious metrics**: Perfect R² (1.0) or RMSE < 0.01°C = likely leakage
- **Check correlations**: Any feature with correlation > 0.99 to target = probable leakage
- **Solution**: Use only independent features created from OTHER variables (not from the target itself)

### 6. Model Training & Comparison
Train 3 models in Q7 (see `q7_modeling.md`):
- **Linear Regression**: Baseline
- **Random Forest**: Tree-based, feature importance available
- **XGBoost**: Gradient boosting, best performance expected

Save outputs:
- `q7_predictions.csv` with actual vs all three model predictions
- `q7_model_metrics.txt` with R², RMSE, MAE for each model
- `q7_feature_importance.csv` with feature importance scores

### 7. Results Visualization (Q8)
Must create 3 artifacts:
- **PNG with 4 subplots minimum**: Model R² comparison bar chart, predictions vs actual scatter (with diagonal line), feature importance bar chart, residuals plot
- **CSV summary**: Metrics as rows, models as columns (see `q8_results.md` for exact format)
- **Text findings**: Best model reasoning, top features, temporal patterns, data quality notes

## Common Mistakes & Solutions

**Problem**: Dataset loading fails
- **Solution**: Run `chmod +x download_data.sh && ./download_data.sh` first

**Problem**: Datetime operations fail
- **Solution**: Verify with `df['Measurement Timestamp'].dtype` → should be `datetime64[ns]`; use `pd.to_datetime(..., errors='coerce')` for parsing issues

**Problem**: Memory error on large CSV
- **Solution**: Load columns selectively: `pd.read_csv(..., usecols=['col1', 'col2'])`; or chunks: `chunksize=10000`

**Problem**: Missing value handling removes too much data
- **Solution**: Use forward-fill for time series (`ffill()`), not drop rows unless <5% missing; median imputation acceptable for non-temporal

**Problem**: Perfect model performance (R²=1.0)
- **Solution**: Check for data leakage—review which features are independent of target

## Test & Validation

Run tests to validate artifacts:
```bash
pytest -q .github/test/test_assignment.py -v
```

Tests verify:
- All required output files exist with correct names
- CSV files have required columns
- Text files are properly formatted
- Numeric values are in expected ranges

## Key Files to Reference

- `q1_setup_exploration.md` - Data loading & EDA patterns
- `q2_data_cleaning.md` - Cleaning requirements  
- `q2_written_out.py` - **Actual implementation example** (reference for data cleaning strategy)
- `q7_modeling.md` - Model training & data leakage warnings
- `q8_results.md` - Visualization & summary table requirements
- `HINTS.md` - Troubleshooting datetime, CSV format, file validation issues
- `project_notes.md` - Development notes on actual approach taken

## Environment & Dependencies

- Python 3.8+
- Key libraries: `pandas>=2.0.0`, `numpy>=1.24.0`, `scikit-learn>=1.3.0`, `xgboost>=2.0.0`
- Jupyter notebooks converted from markdown via `jupytext --to notebook qX_*.md`
- Install: `pip install -r requirements.txt`
