from datetime import datetime


SELECTED_ROUTES = [
    "Delhi-Mumbai",
    "Delhi-Bangalore",
    "Delhi-Kolkata",
    "Delhi-Chennai",
    "Mumbai-Delhi",
    "Mumbai-Bangalore",
    "Mumbai-Kolkata",
    "Bangalore-Delhi",
    "Bangalore-Mumbai",
    "Kolkata-Mumbai",
]

# Price grid for ticket pricing simulation
PRICE_GRID = [2500, 3500, 4500, 5500, 6500, 7500, 8500, 10000, 12000]

MIN_PRICE = min(PRICE_GRID)
MAX_PRICE = max(PRICE_GRID)

BOOKING_HORIZON_DAYS = 90

SEAT_CAPACITY = 180

ROUTE_TYPE_MAP = {
    route:"business" for route in SELECTED_ROUTES
}

ROUTE_DISTANCE_KM = {
    "Delhi-Mumbai": 1150,
    "Delhi-Bangalore": 1750,
    "Delhi-Kolkata": 1300,
    "Delhi-Chennai": 1750,
    "Mumbai-Delhi": 1150,
    "Mumbai-Bangalore": 840,
    "Mumbai-Kolkata": 1650,
    "Bangalore-Delhi": 1750,
    "Bangalore-Mumbai": 840,
    "Kolkata-Mumbai": 1650,
}

BASE_DEMAND_BUSINESS = 6.0
SEASON_PEAK_MULTIPLIER = 1.5
SEASON_OFFPEAK_MULTIPLIER = 0.7
SEASON_NORMAL_MULTIPLIER = 1.0

TIME_BUCKETS = [
(60, 0.3),   # >60 days out: low demand
    (30, 0.6),   # 60–31
    (7, 1.0),    # 30–8
    (0, 1.4), 
]

PRICE_ELASTICITY_BETA = 2.0

WEEKEND_MULTIPLIER = 1.2

RANDOM_SEED = 42