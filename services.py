def calculate_fare(
    distance_km,
    duration_min,
    base_fare,
    per_km_rate,
    per_min_rate,
    min_fare
):
    fare = base_fare + (distance_km * per_km_rate) + (duration_min * per_min_rate)

    if fare < min_fare:
        fare = min_fare

    return round(fare, 2)
