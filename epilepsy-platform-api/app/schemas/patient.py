# app/schemas/patient.py
from pydantic import BaseModel
from datetime import date, datetime

class PatientBase(BaseModel):
    full_name: str
    date_of_birth: date
    clinician_id: int

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True