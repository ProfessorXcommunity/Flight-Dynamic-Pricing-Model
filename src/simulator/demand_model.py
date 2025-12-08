import numpy as np
from .config import (
    BASE_DEMAND_BUSINESS,
    SEASON_PEAK_MULTIPLIER,
    SEASON_OFFPEAK_MULTIPLIER,
    SEASON_NORMAL_MULTIPLIER,
    TIME_BUCKETS,
    PRICE_ELASTICITY_BETA,
    WEEKEND_MULTIPLIER,
    RANDOM_SEED)

rng = np.random.default_rng(RANDOM_SEED)

def _season_factor(season: str) -> float:
    if season == "peak":
        return SEASON_PEAK_MULTIPLIER
    elif season == "offpeak":
        return SEASON_OFFPEAK_MULTIPLIER
    else:
        return SEASON_NORMAL_MULTIPLIER
    

def _route_factor(route_type: str) -> float:
    if route_type == "business":
        return 1.2
    else:
        return 1.0  
    
def _time_factor(days_to_departure: int) -> float:
    # TIME_BUCKETS = [(60, 0.3), (30, 0.6), (7, 1.0), (0, 1.4)]
    for threshold, factor in TIME_BUCKETS:
        if days_to_departure > threshold:
            return factor
        
    return TIME_BUCKETS[-1][1]

def _weekend_factor(is_weekend: bool) -> float:
    return WEEKEND_MULTIPLIER if is_weekend else 1.0

def price_factor(price: float,competitor_price: float) -> float:
    """
    Relative price effective:
    rel_price = price/ competitor_price
    demand proportional to exp(-beta * (rel_price - 1))
    """
    if competitor_price <= 0:
        return 1.0
    
    rel_price = price/competitor_price
    beta = PRICE_ELASTICITY_BETA

    factor = np.exp(-beta * (rel_price - 1.0))
    return float(np.clip(factor,0.1,2.5))


def expected_demand_lambda(
        route_type: str,
        season: str,
        days_to_departure: int,
        is_weekend: bool,
        price: float,
        competitor_price: float
) -> float:
    
    base = BASE_DEMAND_BUSINESS
    lam = (
        base
        * _route_factor(route_type)
        * _season_factor(season)
        * _time_factor(days_to_departure)
        * _weekend_factor(is_weekend)
        * price_factor(price, competitor_price)
    )
    return float(max(lam,0.0))  #recheck

def sample_bookings(lam: float,remaining_seats: int) -> int:
    if remaining_seats <= 0 or lam <= 0:
        return 0
    
    bookings = rng.poisson(lam)
    return int(min(bookings, remaining_seats))