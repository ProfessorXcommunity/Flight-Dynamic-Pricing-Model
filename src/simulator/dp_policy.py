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
    metadata = joblib.load(META_PATH)
    return model, metadata

