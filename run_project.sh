#!/bin/bash

# path to notebooks
NOTEBOOK_DIR="/Users/jack/ucsf_courses_resources/fall 2025/ds_217/ds217-11-final-jack-neary/run_project.sh"

# list of notebooks in order
NOTEBOOKS=(
  "q1_setup_exploration.ipynb"
  "q2_data_cleaning.ipynb"
  "q3_data_wrangling.ipynb"
  "q4_feature_engineering.ipynb"
  "q5_pattern_analysis.ipynb"
  "q6_modeling_preparation.ipynb"
  "q7_modeling.ipynb"
)

# loop through notebooks and execute each
for NB in "${NOTEBOOKS[@]}"; do
    echo "Running $NB ..."
    jupyter nbconvert --to notebook --execute --inplace "$NOTEBOOK_DIR/$NB"
    if [ $? -eq 0 ]; then
        echo "$NB completed successfully!"
    else
        echo "Error running $NB"
        exit 1
    fi
done

echo "All notebooks executed!"
