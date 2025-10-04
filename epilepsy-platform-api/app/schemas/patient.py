# app/schemas/patient.py

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional # <-- Import Optional

# Shared properties
class PatientBase(BaseModel):
    full_name: str
    date_of_birth: date
    clinician_id: int

# Properties to receive on item creation
class PatientCreate(PatientBase):
    pass

# New schema for updating a patient
class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    clinician_id: Optional[int] = None

# Properties to return to client
class Patient(PatientBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True