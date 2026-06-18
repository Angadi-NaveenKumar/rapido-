from fastapi import FastAPI
from pydantic import BaseModel

from database import engine, SessionLocal
from modules import Base, FareConfig


app = FastAPI(
    title="Ride Fare Estimation API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


class FareConfigRequest(BaseModel):
    vehicle_type: str
    base_fare: float
    per_km_rate: float
    per_min_rate: float
    min_fare: float
    surge_multiplier: float = 1.0
    night_charge_multiplier: float = 1.0
    is_active: bool = True


@app.get("/")
def home():
    return {"message": "Ride Fare Estimation API is running"}

@app.get("/health")
def health_check():
    return {"status": "success"}

@app.post("/api/v1/admin/fares")
def create_fare_config(fare: FareConfigRequest):

    db = SessionLocal()

    fare_config = FareConfig(
        vehicle_type=fare.vehicle_type,
        base_fare=fare.base_fare,
        per_km_rate=fare.per_km_rate,
        per_min_rate=fare.per_min_rate,
        min_fare=fare.min_fare,
        surge_multiplier=fare.surge_multiplier,
        night_charge_multiplier=fare.night_charge_multiplier,
        is_active=fare.is_active
    )

    db.add(fare_config)
    db.commit()
    db.refresh(fare_config)

    return {
        "message": "Fare Config Saved To Database"
    }

@app.get("/api/v1/admin/fares")
def get_fares():

    db = SessionLocal()

    fares = db.query(FareConfig).all()

    result = []

    for fare in fares:
        result.append({
            "id": fare.id,
            "vehicle_type": fare.vehicle_type,
            "base_fare": fare.base_fare,
            "per_km_rate": fare.per_km_rate,
            "per_min_rate": fare.per_min_rate,
            "min_fare": fare.min_fare
        })

    return result


class FareEstimateRequest(BaseModel):
    distance_km: float
    duration_min: float
    vehicle_type: str


@app.post("/api/v1/fare/estimate")
def estimate_fare(request: FareEstimateRequest):

    db = SessionLocal()

    fare_config = db.query(FareConfig).filter(
        FareConfig.vehicle_type == request.vehicle_type
    ).first()

    if not fare_config:
        return {"error": "Vehicle type not found"}

    fare = (
        fare_config.base_fare
        + request.distance_km * fare_config.per_km_rate
        + request.duration_min * fare_config.per_min_rate
    )

    if fare < fare_config.min_fare:
        fare = fare_config.min_fare

    return {
        "vehicle_type": request.vehicle_type,
        "estimated_fare": round(fare, 2)
    }
@app.put("/api/v1/admin/fares/{fare_id}")
def update_fare(fare_id: int, fare: FareConfigRequest):

    db = SessionLocal()

    fare_config = db.query(FareConfig).filter(
        FareConfig.id == fare_id
    ).first()

    if not fare_config:
        return {"message": "Fare Config Not Found"}

    fare_config.vehicle_type = fare.vehicle_type
    fare_config.base_fare = fare.base_fare
    fare_config.per_km_rate = fare.per_km_rate
    fare_config.per_min_rate = fare.per_min_rate
    fare_config.min_fare = fare.min_fare
    fare_config.surge_multiplier = fare.surge_multiplier
    fare_config.night_charge_multiplier = fare.night_charge_multiplier
    fare_config.is_active = fare.is_active

    db.commit()

    return {
        "message": "Fare Config Updated"
    }
@app.delete("/api/v1/admin/fares/{fare_id}")
def delete_fare(fare_id: int):
    db = SessionLocal()

    fare = db.query(FareConfig).filter(
        FareConfig.id == fare_id
    ).first()

    if not fare:
        return {"message": "Fare Config Not Found"}

    db.delete(fare)
    db.commit()

    return {"message": "Fare Config Deleted"}