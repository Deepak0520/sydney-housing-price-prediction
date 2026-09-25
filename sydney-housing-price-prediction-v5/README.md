# Sydney Housing Price Prediction and Decision Support System

SIT307/SIT720 Mini Project. Predicts Sydney residential property sale prices for three suburbs
(Castle Hill, Parramatta, Liverpool NSW) from 105 real sold-property listings manually collected
from Domain.com.au, and serves the trained model through a Streamlit decision-support app.

See `Mini_Project_Sydney_Housing_Report.pdf` for the full write-up (problem definition, EDA,
modelling, failure analysis, ML/LLM/human comparison, and app deployment/reflection).

## Contents

- `sydney_housing_raw.csv` - the 105 manually collected sold properties (raw).
- `sydney_housing_clean.csv` - cleaned + feature-engineered version used for modelling.
- `build_dataset.py` - builds the raw dataset from the manually transcribed listing records.
- `Task8.1D.ipynb` - full analysis notebook (Parts 1-5): EDA, feature engineering, 3-model
  comparison with 5-fold CV, failure analysis, ML vs LLM vs human comparison.
- `train_final_model.py` - retrains the winning model (Linear Regression) on the full dataset and
  saves `house_price_model.joblib` + `app_reference.json` for the app.
- `app.py` - the Streamlit decision-support app.
- `Mini_Project_Sydney_Housing_Report.pdf` / `build_report.py` - the final PDF report and its
  generator script.
- `requirements.txt` - Python dependencies.

## Running it yourself

```bash
pip install -r requirements.txt

# 1. Rebuild the dataset (optional, already included as CSV)
python3 build_dataset.py

# 2. Re-run the analysis notebook (Jupyter: Kernel -> Restart & Run All)
#    or from the command line:
jupyter nbconvert --to notebook --execute --inplace Task8.1D.ipynb

# 3. Train and save the deployed model
python3 train_final_model.py

# 4. Launch the app
streamlit run app.py
```

Then open the local URL Streamlit prints (typically http://localhost:8501), fill in a property's
suburb, type, beds, baths, parking and (optionally) area, and click **Predict sale price**.

## Data source and disclosure

All 105 properties were manually read from Domain.com.au's public "Sold" search results pages
for each suburb (7 Aug - 25 Sep 2026), keeping only listings with a disclosed sale price. See the
report's Part 1 for data quality notes and limitations (price-disclosure bias, missing area
values, confounding between suburb and property type, short collection window).


