import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .config import (
    SELECTED_ROUTES,
    ROUTE_DISTANCE_KM,
    ROUTE_TYPE_MAP,
    SEAT_CAPACITY,
    RANDOM_SEED)

rng = np.random.default_rng(RANDOM_SEED)


# TODO: Integrate with booking simulator later

def _random_departure_date(n_flights: int, start_date: str = "2025-01-01",end_date:str="2025-03-01") -> pd.Series:
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    delta_days = (end - start).days

    days_offset = rng.integers(low=0, high=delta_days, size=n_flights)
    return [start + timedelta(days=int(d)) for d in days_offset]

def _assign_season(departure_dates: datetime) -> str:
    month = departure_dates.month
    if month in [3]:
        return "peak"
    elif month in [1,2]:
        return "normal"
    else:
        return "offpeak"
    
def generate_flights(num_flights: int) -> pd.DataFrame:
    """
    Generate a synthetic flights table.
    Each row = one flight instance.
    """
    routes = rng.choice(SELECTED_ROUTES, size=num_flights, replace=True)
    departure_dates = _random_departure_date(num_flights)

    records = []
    for i in range(num_flights):
        route = routes[i]
        departure_dt = departure_dates[i]

        origin , destination = route.split("-")
        distance_km = ROUTE_DISTANCE_KM(route,1500)
        season = _assign_season(departure_dt)
        route_type = ROUTE_TYPE_MAP.get(route,"business")

        record = {
            "flight_id": f"FL{i+1:05d}",
            "source_city": origin,
            "destination_city": destination,
            "route": route,
            "departure_datetime": departure_dt,
            "distance_km": distance_km,
            "season": season,
            "route_type": route_type,
            "seat_capacity": SEAT_CAPACITY,
            "airline": "SimAir"
        }

        records.append(record)
    flights_df = pd.DataFrame.from_records(records)
    return flights_df