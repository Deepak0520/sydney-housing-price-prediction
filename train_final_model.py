"""
Trains the final deployed model (Linear Regression - the winner from analysis.ipynb
Part 3) on the FULL cleaned dataset (all 105 properties), and saves the fitted
pipeline for the Streamlit app to load.
"""
import warnings
warnings.filterwarnings("ignore")
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("sydney_housing_clean.csv", parse_dates=["sale_date"])

num_features = ["beds", "baths", "parking", "area_sqm_imputed", "area_known",
                 "distance_to_cbd_km", "total_rooms", "days_since_start"]
cat_features = ["suburb", "property_type_grouped", "sale_method"]

X = df[num_features + cat_features]
y = df["price"]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
])
pipe = Pipeline([("prep", preprocess), ("model", LinearRegression())])
pipe.fit(X, y)

joblib.dump(pipe, "house_price_model.joblib")
print("Saved house_price_model.joblib")
print("R2 on full training data:", pipe.score(X, y))

# save reference values the app needs: suburb -> distance_to_cbd_km, dataset min date,
# and the per-property-type median area used at training time to impute missing area
# (so the app's "I don't know the area" path uses the SAME fallback the model was
# trained on, instead of an arbitrary guess)
suburb_dist = df.groupby("suburb")["distance_to_cbd_km"].first().to_dict()
min_date = df["sale_date"].min()
area_median_by_grouped_type = df.groupby("property_type_grouped")["area_sqm_imputed"].median().to_dict()
import json
with open("app_reference.json", "w") as f:
    json.dump({
        "suburb_distance_km": suburb_dist,
        "min_sale_date": str(min_date.date()),
        "area_median_by_type": area_median_by_grouped_type,
    }, f, indent=2)
print("Saved app_reference.json")
print("Area medians by type:", area_median_by_grouped_type)
