# Sydney Housing Price Prediction and Decision Support System

SIT307/SIT720 Mini Project. Predicts Sydney residential property sale prices for three suburbs
(Castle Hill, Parramatta, Liverpool NSW) from 105 real sold-property listings manually collected
from Domain.com.au, and serves the trained model through a Streamlit decision-support app.

See `Task8.1D.ipynb` (or `Task8.1D.pdf` for a non-interactive copy) for the full write-up:
problem definition, EDA, feature engineering, 3-model comparison with 5-fold CV, failure
analysis, ML vs LLM vs human comparison, and the app deployment/reflection (Part 6).

## Contents

- `Task8.1D.ipynb` - the full analysis notebook (Parts 1-6): problem definition and data
  collection, EDA and feature engineering, model development and evaluation, failure analysis,
  ML vs LLM vs human comparison, and final app deployment/reflection.
- `Task8.1D.pdf` - the same notebook exported to PDF (submitted copy).
- `sydney_housing_raw.csv` - the 105 manually collected sold properties (raw).
- `sydney_housing_clean.csv` - cleaned + feature-engineered version used for modelling.
- `build_dataset.py` - builds the raw dataset from the manually transcribed listing records.
- `train_final_model.py` - retrains the winning model (Linear Regression) on the full dataset and
  saves `house_price_model.joblib` + `app_reference.json` for the app.
- `app.py` - the Streamlit decision-support app.
- `figs/` - saved plots and app screenshots used in the notebook.
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
for each suburb (7 Aug - 25 Sep 2026), keeping only listings with a disclosed sale price. See
Part 1 of the notebook for data quality notes and limitations (price-disclosure bias, missing
area values, confounding between suburb and property type, short collection window).

## GenAI use

Generative AI (Claude, Anthropic) supported roughly 20-30% of this submission - code structuring,
research, and quality checking - and was also directly used as the "LLM" arm of the Part 5
comparison, as permitted by the assignment brief. All data collection, analysis, interpretation
and write-up were completed independently, per the GenAI acknowledgement in the notebook.
