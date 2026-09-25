"""
Sydney Housing Price Prediction - Streamlit decision-support app.

Loads the trained Linear Regression pipeline (house_price_model.joblib, produced by
train_final_model.py) and lets a user enter property features to get a predicted
sale price, for Castle Hill, Parramatta, and Liverpool NSW.

Run with:  streamlit run app.py
"""
import json
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sydney Housing Price Predictor", page_icon="\U0001F3E1", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load("house_price_model.joblib")

@st.cache_data
def load_reference():
    with open("app_reference.json") as f:
        return json.load(f)

model = load_model()
ref = load_reference()
suburb_distance = ref["suburb_distance_km"]
min_sale_date = pd.to_datetime(ref["min_sale_date"])

st.title("Sydney Housing Price Predictor")
st.caption(
    "A decision-support prototype trained on 105 real sold properties (Aug-Sep 2026) "
    "from Castle Hill, Parramatta and Liverpool, NSW. Predictions come from a Linear "
    "Regression model - see the accompanying report for full methodology, evaluation "
    "and limitations."
)

with st.form("property_form"):
    st.subheader("Property details")
    col1, col2 = st.columns(2)
    with col1:
        suburb = st.selectbox("Suburb", options=list(suburb_distance.keys()))
        property_type = st.selectbox(
            "Property type", options=["House", "Apartment", "Townhouse", "Semi-detached"])
        beds = st.number_input("Bedrooms", min_value=0, max_value=10, value=3, step=1)
        baths = st.number_input("Bathrooms", min_value=0, max_value=10, value=2, step=1)
    with col2:
        parking = st.number_input("Parking spaces", min_value=0, max_value=10, value=1, step=1)
        area_known = st.checkbox("I know the floor/land area (m²)", value=False)
        area_sqm = st.number_input("Area (m²)", min_value=0, max_value=3000, value=150, step=10,
                                    disabled=not area_known)
        sale_method = st.selectbox(
            "Expected/likely sale method", options=["private treaty", "auction", "prior to auction"])

    submitted = st.form_submit_button("Predict sale price")

if submitted:
    row = pd.DataFrame([{
        "beds": beds,
        "baths": baths,
        "parking": parking,
        "area_sqm_imputed": area_sqm if area_known else None,
        "area_known": int(area_known),
        "distance_to_cbd_km": suburb_distance[suburb],
        "total_rooms": beds + baths,
        "days_since_start": (pd.Timestamp.today().normalize() - min_sale_date).days,
        "suburb": suburb,
        "property_type_grouped": property_type,
        "sale_method": sale_method,
    }])
    # if area unknown, fall back to EXACTLY the same per-property-type median the
    # model was trained on for missing areas (see train_final_model.py), so an
    # "unknown area" prediction is consistent with how the model learned to handle it
    if not area_known:
        row["area_sqm_imputed"] = ref["area_median_by_type"][property_type]

    pred = model.predict(row)[0]
    st.success(f"### Predicted sale price: ${pred:,.0f}")
    st.caption(
        "This is a point estimate from a model trained on only 105 properties - treat it as "
        "a starting reference, not a formal valuation, especially for houses, rare property "
        "types (Townhouse/Semi-detached), or any property with unusual condition or land "
        "features the model has no way to see. See Part 4 of the report for known failure cases."
    )

st.divider()
st.caption(
    "Data: manually collected from Domain.com.au sold listings, 7 Aug - 25 Sep 2026. "
    "Model: Linear Regression, 5-fold cross-validated, test R²=0.888. "
    "Built for SIT307/SIT720 Mini Project - Sydney Housing Price Prediction."
)
