# app/schemas/clinician.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema for creating a new clinician
class ClinicianCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for returning clinician data (without the password)
class Clinician(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True