# app/schemas/patient.py

from pydantic import BaseModel, ConfigDict # <-- Import ConfigDict
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    full_name: str
    date_of_birth: date
    clinician_id: int

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    clinician_id: Optional[int] = None

class Patient(PatientBase):
    id: int
    created_at: datetime

    # --- Use model_config instead of class Config ---
    model_config = ConfigDict(from_attributes=True)