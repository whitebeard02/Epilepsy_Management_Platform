# app/models/patient.py
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    clinician_id = Column(Integer, index=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())