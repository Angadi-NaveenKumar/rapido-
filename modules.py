from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class FareConfig(Base):
    __tablename__ = "fare_configs"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_type = Column(String, unique=True, nullable=False)

    base_fare = Column(Float, nullable=False)

    per_km_rate = Column(Float, nullable=False)

    per_min_rate = Column(Float, nullable=False)

    min_fare = Column(Float, nullable=False)

    surge_multiplier = Column(Float, default=1.0)

    night_charge_multiplier = Column(Float, default=1.0)

    is_active = Column(Boolean, default=True)