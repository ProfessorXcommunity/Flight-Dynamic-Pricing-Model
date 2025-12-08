from datetime import timedelta
import numpy as np
import pandas as pd

from .config import(
    BOOKING_HORIZON_DAYS,
    SEAT_CAPACITY,
    PRICE_GRID,
    MIN_PRICE,
    MAX_PRICE,
    RANDOM_SEED
)

from .demand_model import expected_demand_lambda, sample_bookings

rng = np.random.default_rng(RANDOM_SEED)

def simple_time_based_policy(context: dict) -> float:
    """
    basic pricing policy used only to generate initial data.
    """
    dtd = context['days_to_departure']
    if dtd > 60:
        return 3500
    elif dtd > 30:
        return 5500
    elif dtd > 7:
        return 7500
    else:
        return 9500

def simulate_single_flight(
        flight_row: pd.Series,
        pricing_policy=simple_time_based_policy,
        horizon_days: int = BOOKING_HORIZON_DAYS,
) -> pd.DataFrame:
    
    departure_dt = flight_row['departure_datetime']
    route = flight_row['route']
    route_type = flight_row['route_type']
    season = flight_row['season']
    seat_capacity = flight_row['seat_capacity']

    remaining_seats = seat_capacity

    records = []
    for t in range(horizon_days):
        days_to_departure = horizon_days - t
        booking_date = departure_dt - timedelta(days=days_to_departure)
        day_of_week = booking_date.weekday()
        is_weekend = day_of_week >=5

        #competitor base -> taking random around mid of PRICE_GRID

        competitor_base = np.median(PRICE_GRID)
        competitor_price = competitor_base * float(
            np.clip(rng.normal(loc=1.0,scale=0.15),0.7,1.3)
        )

        #final context result
        context = {
            "flight_id": flight_row["flight_id"],
            "route": route,
            "route_type": route_type,
            "season": season,
            "days_to_departure": days_to_departure,
            "remaining_seats": remaining_seats,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "competitor_price": competitor_price,
        }
        
        price = pricing_policy(context)
        price = float(np.clip(price,MIN_PRICE,MAX_PRICE))

        lam = expected_demand_lambda(
            route_type=route_type,
            season=season,
            days_to_departure=days_to_departure,
            is_weekend=is_weekend,
            price=price,
            competitor_price=competitor_price
        )

        bookings = sample_bookings(lam,remaining_seats)
        remaining_seats = max(remaining_seats - bookings, 0)

        revenue = price * bookings
        search_demand_idx = lam 

        records.append(
            {
                "flight_id": flight_row["flight_id"],
                "route": route,
                "origin": flight_row["source_city"],
                "destination": flight_row["destination_city"],
                "departure_datetime": departure_dt,
                "booking_date": booking_date,
                "t": t,
                "days_to_departure": days_to_departure,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "season": season,
                "route_type": route_type,
                "seat_capacity": seat_capacity,
                "remaining_seats": remaining_seats,
                "price": price,
                "competitor_price": competitor_price,
                "search_demand_idx": search_demand_idx,
                "bookings_made": bookings,
                "revenue": revenue,
            }
        )

        if remaining_seats <=0:
            break

    df = pd.DataFrame(records)
    if not df.empty:
        df['cumulative_bookings'] = df['bookings_made'].cumsum()
        df['sold_out_flag'] = df['remaining_seats'] <= 0

        return df 
    
def simulate_flights(
        flights_df: pd.DataFrame,
        pricing_policy: simple_time_based_policy,
        horizon_days: int = BOOKING_HORIZON_DAYS
) -> pd.DataFrame:
    

    all_records = []
    for _, row in flights_df.iterrows():
        df_single = simulate_single_flight(
            flight_row=row,
            pricing_policy=pricing_policy,
            horizon_days=horizon_days
        )
        all_records.append(df_single)

    if not all_records:
        return pd.DataFrame()
    
    bookings_df = pd.concat(all_records, ignore_index=True)
    return bookings_df