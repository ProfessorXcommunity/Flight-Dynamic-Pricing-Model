import math
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

from .config import PRICE_GRID, BOOKING_HORIZON_DAYS, SEAT_CAPACITY
MODEL_PATH = "models/demand_model_gbr.pkl"
META_PATH = "models/demand_model_metadata.pkl"

def load_demand_model():
    model = joblib.load(MODEL_PATH)
    meta = joblib.load(META_PATH)
    return model, meta

# -- helper: creating features in the format as model expects --

def make_features_vector(meta:dict,context:dict, price:float,competitor_price:float):
    numeric_cols = meta.get("feature_cols_numeric", ["days_to_departure","remaining_seats_ratio","price","competitor_price","rel_price","day_of_week","is_weekend"])
    cat_cols = meta.get("feature_cols_categorical", ["route","season","route_type"])

    remaining_ratio = context['remaining_seats']/context.get('seat_capacity',SEAT_CAPACITY)

    numeric = {
        "days_to_departure": context["days_to_departure"],
        "remaining_seats_ratio": remaining_ratio,
        "price": price,
        "competitor_price": competitor_price,
        "rel_price": price / competitor_price if competitor_price>0 else 1.0,
        "day_of_week": context.get("day_of_week", 0),
        "is_weekend": 1 if context.get("is_weekend", False) else 0,
    }
# create a dataframe row with numeric + dummies :: missing dummies -> 0
    row = numeric.copy()
    for c in cat_cols:
        val = context.get(c,"")
        colname = f'{c}_{val}'
        row[colname] = 1

    X_columns = meta['X_columns']
    df = pd.DataFrame([{col : 0 for col in X_columns}])

    for k,v in numeric.items():
        if k in df.columns:
            df.at[0,k] = v 

    for k,v in row.items():
        if k in df.columns and k not in numeric:
            df.at[0,k] = v 

    return df 

def expected_bookings_from_model(model, meta, context: dict,price: float,competitor_price: float):

    X = make_features_vector(meta,context, price, competitor_price)

    pred = model.predict(X)[0]
    return max(float(pred),0.0)
